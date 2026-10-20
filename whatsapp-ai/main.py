import os
import json
import uuid
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel
from fastapi import FastAPI, Form, Depends, HTTPException, Request, status, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from groq import Groq
from twilio.rest import Client
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from database import get_db
from models import User, Product, Invoice, RestockRequest, Supplier, SalesLog

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
twilio_client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))

# --- REAL-TIME SYNC BUS ---
# Every channel (counter POS tab, WhatsApp webhook, AI copilot widget) pushes a
# broadcast through here after any change that affects stock, sales, or debt.
# All connected dashboard tabs receive it instantly instead of waiting for the
# 3-second poll, so "sold via WhatsApp" shows up on the counter screen live.
class SyncBus:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, event: str, payload: dict):
        dead = []
        message = json.dumps({"event": event, "payload": payload})
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                dead.append(connection)
        for d in dead:
            self.disconnect(d)

sync_bus = SyncBus()

@app.websocket("/ws/sync")
async def sync_socket(websocket: WebSocket):
    """Dashboard, WhatsApp channel, and AI widget all share this single
    real-time channel. Connect once from the frontend and listen for events:
    'sale_completed', 'stock_adjusted', 'product_created', 'invoice_updated'."""
    await sync_bus.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # keep-alive; we don't expect client messages
    except WebSocketDisconnect:
        sync_bus.disconnect(websocket)

# --- INPUT MODEL SCHEMAS ---
class CartItem(BaseModel):
    name: str
    qty: int

class MasterCheckoutPayload(BaseModel):
    items: List[CartItem]
    is_debt: bool
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    payment_method: str
    bank_name: Optional[str] = None
    use_etr: bool
    operator: str

class ProductCreationPayload(BaseModel):
    name: str
    part_number: Optional[str] = None
    barcode: Optional[str] = None
    buying_price: float
    selling_price: float
    stock_count: int
    role: str

class StockAdjustmentPayload(BaseModel):
    product_id: int
    qty_delta: int
    role: str
    operator: str

class InvoicePaymentPayload(BaseModel):
    invoice_id: int
    amount_paid: float

# --- ACCOUNTABILITY WHATSAPP SYSTEM GATEWAY ---
@app.post("/webhook")
async def inbound_whatsapp_webhook(Body: str = Form(...), From: str = Form(...), db: Session = Depends(get_db)):
    sender_phone = From.replace("whatsapp:", "").strip()
    msg_clean = Body.lower().strip()
    
    # Track exactly who is making the change
    user = db.query(User).filter(User.phone_number == sender_phone).first()
    operator_tag = f"WhatsApp ({user.name if user else 'Unknown'} - {sender_phone})"
    user_role = user.role if user else "customer"

    if user_role in ["employee", "admin"]:
        if "sold" in msg_clean:
            # Parse text with Llama engine
            completion = client.chat.completions.create(
                messages=[{"role": "system", "content": "Extract data. Output strictly as PRODUCT_NAME:QTY"},
                          {"role": "user", "content": Body}],
                model="llama-3.3-70b-versatile"
            )
            try:
                p_name, qty = completion.choices[0].message.content.strip().split(":")
                qty = int(qty)
                product = db.query(Product).filter(Product.name.ilike(f"%{p_name.strip()}%")).first()
                
                if product and product.stock_count >= qty:
                    unit_price = float(product.selling_price if product.selling_price else product.price)
                    unit_buying_price = float(product.buying_price or 0)
                    product.stock_count -= qty
                    sale_ref = uuid.uuid4().hex[:12]
                    db.add(SalesLog(
                        sale_ref=sale_ref,
                        product_name=product.name, quantity_sold=qty,
                        total_price=unit_price * qty,
                        unit_selling_price=unit_price, unit_buying_price=unit_buying_price,
                        sold_by=operator_tag, payment_method="Cash"
                    ))
                    db.commit()
                    twilio_client.messages.create(from_='whatsapp:+14155238886', body=f"✅ Recorded. Logged by {operator_tag}.", to=From)
                    # Push to the dashboard/AI widget immediately — this is the
                    # "field sale shows up on the counter screen live" requirement.
                    await sync_bus.broadcast("sale_completed", {
                        "sale_ref": sale_ref, "product_name": product.name,
                        "qty": qty, "source": "whatsapp", "operator": operator_tag
                    })
                    return {"status": "ok"}
            except Exception:
                pass
    return {"status": "ok"}

# --- SALES CHECKOUT CORE ENGINE (WITH REAL TIME STOCK VERIFICATION) ---
@app.post("/api/sales/checkout")
async def process_sales_checkout(payload: MasterCheckoutPayload, db: Session = Depends(get_db)):
    if not payload.items:
        raise HTTPException(status_code=400, detail="The active register cart layout is empty.")

    total_sale_amount = 0.0
    items_summary_log = []
    sale_ref = uuid.uuid4().hex[:12]  # ties every line item + the receipt together for reprinting

    # 1. Real-time stock validation loop
    for item in payload.items:
        product = db.query(Product).filter(Product.name == item.name).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Item variant '{item.name}' not found.")
        if product.stock_count < item.qty:
            raise HTTPException(status_code=400, detail=f"Stock out constraint error! Only {product.stock_count} units left for {product.name}.")
        
        # Calculate dynamic prices
        unit_price = float(product.selling_price if product.selling_price else product.price)
        unit_buying_price = float(product.buying_price or 0)
        item_total = unit_price * item.qty
        total_sale_amount += item_total
        
        # Deduct items immediately
        product.stock_count -= item.qty
        items_summary_log.append({
            "name": product.name, "qty": item.qty,
            "unit_price": unit_price, "unit_buying_price": unit_buying_price
        })

    # 2. Factor in 16% ETR Kenyan Tax option if selected
    if payload.use_etr:
        total_sale_amount = total_sale_amount * 1.16

    # 3. Handle Debt vs Instant Payment Routing
    if payload.is_debt:
        if not payload.customer_name or not payload.customer_phone:
            raise HTTPException(status_code=400, detail="Customer credentials are mandatory for credit logging.")
        
        existing_invoice = db.query(Invoice).filter(Invoice.customer_phone == payload.customer_phone.strip()).first()
        if existing_invoice:
            existing_invoice.amount_due = float(existing_invoice.amount_due) + total_sale_amount
            current_history = json.loads(existing_invoice.debtor_items_json or '[]')
            current_history.extend(items_summary_log)
            existing_invoice.debtor_items_json = json.dumps(current_history)
        else:
            new_invoice = Invoice(
                customer_name=payload.customer_name.strip(),
                customer_phone=payload.customer_phone.strip(),
                amount_due=total_sale_amount,
                due_date=(datetime.utcnow() + timedelta(days=30)).date(),
                is_paid=False,
                debtor_items_json=json.dumps(items_summary_log)
            )
            db.add(new_invoice)
    else:
        # Record into central logs for non-debt cash/mpesa transactions
        for entry in items_summary_log:
            db.add(SalesLog(
                sale_ref=sale_ref,
                product_name=entry["name"], quantity_sold=entry["qty"],
                total_price=entry["unit_price"] * entry["qty"] * (1.16 if payload.use_etr else 1.0),
                unit_selling_price=entry["unit_price"], unit_buying_price=entry["unit_buying_price"],
                sold_by=payload.operator, payment_method=payload.payment_method,
                bank_name=payload.bank_name
            ))
            
    db.commit()

    receipt = {
        "sale_ref": sale_ref,
        "items": items_summary_log,
        "total": total_sale_amount,
        "use_etr": payload.use_etr,
        "operator": payload.operator,
        "is_debt": payload.is_debt,
        "timestamp": datetime.utcnow().isoformat()
    }

    # Push to every connected dashboard/WhatsApp/AI channel instantly
    await sync_bus.broadcast("sale_completed", receipt)

    return {"status": "success", "receipt_data": items_summary_log, "total": total_sale_amount, "sale_ref": sale_ref}


# --- RECEIPT REPRINT (58mm thermal layout data source) ---
@app.get("/api/sales/receipt/{sale_ref}")
async def fetch_receipt_for_reprint(sale_ref: str, db: Session = Depends(get_db)):
    lines = db.query(SalesLog).filter(SalesLog.sale_ref == sale_ref).all()
    if not lines:
        raise HTTPException(status_code=404, detail="No receipt found for that sale reference.")
    return {
        "sale_ref": sale_ref,
        "timestamp": lines[0].created_at,
        "operator": lines[0].sold_by,
        "payment_method": lines[0].payment_method,
        "items": [{"name": l.product_name, "qty": l.quantity_sold, "unit_price": float(l.unit_selling_price)} for l in lines],
        "total": sum(float(l.total_price) for l in lines)
    }

# --- PRODUCT DUPLICATION ARCHITECTURE PROTECTION ---
@app.post("/api/products/secure-create")
async def create_new_product(payload: ProductCreationPayload, db: Session = Depends(get_db)):
    # Block duplicate entries
    duplicate_check = db.query(Product).filter(
        or_(Product.name.ilike(payload.name.strip()), 
            Product.part_number == payload.part_number)
    ).first()
    
    if duplicate_check:
        raise HTTPException(status_code=400, detail=f"A product record with the descriptor identifier '{payload.name}' already exists in your table.")

    new_product = Product(
        name=payload.name.strip(), part_number=payload.part_number, barcode=payload.barcode,
        buying_price=payload.buying_price, selling_price=payload.selling_price,
        stock_count=payload.stock_count, price=payload.selling_price
    )
    db.add(new_product)
    db.commit()
    await sync_bus.broadcast("product_created", {"name": new_product.name, "stock_count": new_product.stock_count})
    return {"status": "success"}

# --- SECURITY STOCK MODIFICATION ROUTE ---
@app.post("/api/products/modify-inventory")
async def adjust_stock_metrics(payload: StockAdjustmentPayload, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product entity not found.")

    # Enforce access permissions
    if payload.qty_delta < 0 and payload.role != "admin":
        raise HTTPException(status_code=403, detail="Security policy block: Employees cannot reduce stock counts manually.")

    product.stock_count += payload.qty_delta
    db.commit()
    await sync_bus.broadcast("stock_adjusted", {
        "product_id": product.id, "name": product.name,
        "new_stock_count": product.stock_count, "adjusted_by": payload.operator
    })
    return {"status": "success"}

# --- INVOICE DRILL DOWN AND PAYMENTS AGGREGATION ---
@app.get("/api/invoices/drilldown/{invoice_id}")
async def fetch_invoice_breakdown(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice record missing.")
    return {
        "id": invoice.id,
        "customer": invoice.customer_name,
        "phone": invoice.customer_phone,
        "balance": float(invoice.amount_due),
        "due_date": invoice.due_date,
        "items": json.loads(invoice.debtor_items_json or '[]')
    }

@app.post("/api/invoices/collect-payment")
async def clear_debt_balance(payload: InvoicePaymentPayload, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.id == payload.invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice record missing.")
        
    invoice.amount_due = float(invoice.amount_due) - payload.amount_paid
    if invoice.amount_due <= 0:
        invoice.amount_due = 0.0
        invoice.is_paid = True
    db.commit()
    await sync_bus.broadcast("invoice_updated", {
        "invoice_id": invoice.id, "customer": invoice.customer_name,
        "remaining_balance": float(invoice.amount_due), "is_paid": invoice.is_paid
    })
    return {"status": "success", "remaining_balance": float(invoice.amount_due)}

# --- DYNAMIC REPORTS TIMELINE SELECTOR ---
@app.get("/api/reports/analytics")
async def extract_filtered_reports(range_filter: str = "daily", db: Session = Depends(get_db)):
    now = datetime.utcnow()
    delta_map = {"daily": 1, "weekly": 7, "monthly": 30, "yearly": 365}
    days_back = delta_map.get(range_filter, 1)
    threshold = now - timedelta(days=days_back)

    # Bug fix: previously `threshold` was computed but never applied to the
    # queries below, so every range filter (daily/weekly/monthly/yearly)
    # returned identical all-time totals.
    sales_in_range = db.query(SalesLog).filter(SalesLog.created_at >= threshold).all()

    total_rev = sum(float(s.total_price) for s in sales_in_range)
    total_profit = sum(s.profit for s in sales_in_range)
    units_dispatched = sum(s.quantity_sold for s in sales_in_range)

    depleted_rows = db.query(Product).filter(Product.stock_count == 0).all()

    # Top 5 performers within the selected range, by units sold
    top_by_qty: dict = {}
    profit_by_item: dict = {}
    for s in sales_in_range:
        top_by_qty[s.product_name] = top_by_qty.get(s.product_name, 0) + s.quantity_sold
        profit_by_item[s.product_name] = profit_by_item.get(s.product_name, 0) + s.profit
    top_items = sorted(top_by_qty.items(), key=lambda x: x[1], reverse=True)[:5]

    # Itemized daily sales list (report terminal "list of daily sales and total")
    daily_sales_list = [
        {
            "id": s.id,
            "sale_ref": s.sale_ref,
            "product_name": s.product_name,
            "quantity_sold": s.quantity_sold,
            "total_price": float(s.total_price),
            "profit": s.profit,
            "sold_by": s.sold_by,
            "payment_method": s.payment_method,
            "created_at": s.created_at
        }
        for s in sorted(sales_in_range, key=lambda x: x.created_at, reverse=True)
    ]

    return {
        "range": range_filter,
        "revenue": round(total_rev, 2),
        "profit": round(total_profit, 2),
        "units_sold": int(units_dispatched),
        "depleted_count": len(depleted_rows),
        "depleted_list": [p.name for p in depleted_rows],
        "top_moving_labels": [r[0] for r in top_items],
        "top_moving_values": [int(r[1]) for r in top_items],
        "top_moving_profit": [round(profit_by_item.get(r[0], 0), 2) for r in top_items],
        "daily_sales_list": daily_sales_list
    }


# --- DEDICATED OUT-OF-STOCK REPORT ---
@app.get("/api/reports/out-of-stock")
async def out_of_stock_report(db: Session = Depends(get_db)):
    depleted = db.query(Product).filter(Product.stock_count == 0).all()
    return {
        "count": len(depleted),
        "items": [{"id": p.id, "name": p.name, "part_number": p.part_number} for p in depleted]
    }

# --- OTHER STANDARD COMPONENT RETRIEVAL CHANNELS ---
@app.get("/api/products")
async def get_all_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@app.get("/api/products/lookup")
async def lookup_single_product(q: str, db: Session = Depends(get_db)):
    """Used by the counter search box / barcode scanner: exact barcode match
    first (fast path for hardware scans), then a fuzzy name match."""
    product = db.query(Product).filter(Product.barcode == q).first()
    if not product:
        product = db.query(Product).filter(Product.name.ilike(f"%{q}%")).first()
    if not product:
        raise HTTPException(status_code=404, detail="No matching product found.")
    return product

@app.get("/api/invoices")
async def get_all_invoices(db: Session = Depends(get_db)):
    return db.query(Invoice).all()

# --- EMBEDDED REAL TIME CHAT COMPANION ROUTE ---
class CopilotPromptSchema(BaseModel):
    prompt: str

@app.post("/api/ai/copilot-chat")
async def execute_runtime_ai_copilot(payload: CopilotPromptSchema, db: Session = Depends(get_db)):
    products = db.query(Product).all()
    context = "System Store Products:\n" + "".join([f"- {p.name}: Stock {p.stock_count} units\n" for p in products])
    
    completion = client.chat.completions.create(
        messages=[{"role": "system", "content": f"You are the POS window helper asset widget. Answer questions briefly.\n{context}"},
                  {"role": "user", "content": payload.prompt}],
        model="llama-3.3-70b-versatile"
    )
    return {"reply": completion.choices[0].message.content}

@app.get("/dashboard", response_class=HTMLResponse)
async def serve_unified_dashboard_ui(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard.html", context={})

@app.get("/pos", response_class=HTMLResponse)
async def serve_counter_pos_terminal(request: Request):
    return templates.TemplateResponse(request=request, name="pos.html", context={})