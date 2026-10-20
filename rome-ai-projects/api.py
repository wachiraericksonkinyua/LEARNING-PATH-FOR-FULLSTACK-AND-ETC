from fastapi import Body, FastAPI, Request

app = FastAPI()

# --- EXCHANGE #1: You call Safaricom ---
@app.post("/checkout")
def initiate_payment(phone: str, amount: int):
    # 1. Send request to Safaricom
    # 2. Get back CheckoutRequestID
    # 3. Save to DB: { checkout_id: "ws_CO_...", status: "PENDING" }
    return {"status": "Prompt sent to phone, waiting for PIN"}

# --- EXCHANGE #2: Safaricom calls You ---
@app.post("/api/mpesa/callback")
async def mpesa_callback(payload: dict = Body(...)):
    stk_data = payload.get("Body", {}).get("stkCallback", {})
    
    result_code = stk_data.get("ResultCode")
    checkout_id = stk_data.get("CheckoutRequestID")
    
    if result_code == 0:
        print(f"Transaction {checkout_id} paid successfully!")
    else:
        print(f"Transaction {checkout_id} failed!")
        
    return {"ResultCode": 0, "ResultDesc": "Accepted"}