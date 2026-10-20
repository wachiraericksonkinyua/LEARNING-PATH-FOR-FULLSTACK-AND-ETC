import base64
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, Body, HTTPException, status
from pydantic import BaseModel
from supabase import create_client, Client

load_dotenv()

app = FastAPI(title="M-Pesa Integration Service")

# Configurations
CONSUMER_KEY = os.getenv("DARAJA_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("DARAJA_CONSUMER_SECRET")
SHORTCODE = os.getenv("DARAJA_SHORTCODE", "174379")
PASSKEY = os.getenv("DARAJA_PASSKEY", "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919")

# Supabase Initialization
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class STKPushRequest(BaseModel):
    phone_number: str
    amount: int
    callback_url: str


def get_oauth_token() -> str:
    auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(auth_url, auth=(CONSUMER_KEY, CONSUMER_SECRET), timeout=10)
    response.raise_for_status()
    return response.json()["access_token"]


def generate_password(timestamp: str) -> str:
    raw_str = f"{SHORTCODE}{PASSKEY}{timestamp}"
    return base64.b64encode(raw_str.encode()).decode("utf-8")


@app.post("/stk-push")
def initiate_stk_push(data: STKPushRequest):
    token = get_oauth_token()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = generate_password(timestamp)

    payload = {
        "BusinessShortCode": SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": str(data.amount),
        "PartyA": data.phone_number,
        "PartyB": SHORTCODE,
        "PhoneNumber": data.phone_number,
        "CallBackURL": data.callback_url,
        "AccountReference": "Order#101",
        "TransactionDesc": "Payment for Order"
    }

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    
    res = requests.post(url, json=payload, headers=headers, timeout=10)
    res_data = res.json()

    if res_data.get("ResponseCode") == "0":
        return {"message": "Success", "checkout_request_id": res_data.get("CheckoutRequestID")}

    raise HTTPException(status_code=400, detail="STK push failed")


@app.post("/mpesa-callback", status_code=status.HTTP_200_OK)
async def handle_mpesa_callback(payload: dict = Body(...)):
    stk_callback = payload.get("Body", {}).get("stkCallback", {})
    
    merchant_id = stk_callback.get("MerchantRequestID")
    checkout_id = stk_callback.get("CheckoutRequestID")
    result_code = stk_callback.get("ResultCode")
    result_desc = stk_callback.get("ResultDesc")

    receipt_number = None
    amount = None
    phone_number = None

    # Handle successful PIN entry
    if result_code == 0:
        metadata = stk_callback.get("CallbackMetadata", {}).get("Item", [])
        receipt_number = next((i["Value"] for i in metadata if i["Name"] == "MpesaReceiptNumber"), None)
        amount = next((i["Value"] for i in metadata if i["Name"] == "Amount"), None)
        phone_number = next((i["Value"] for i in metadata if i["Name"] == "PhoneNumber"), None)

    # Format database object
    db_data = {
        "merchant_request_id": merchant_id,
        "checkout_request_id": checkout_id,
        "result_code": result_code,
        "result_desc": result_desc,
        "mpesa_receipt": receipt_number,
        "amount": amount,
        "phone_number": str(phone_number) if phone_number else None
    }
    
    # Safely upsert to Supabase
    try:
        supabase.table("mpesa_transactions").upsert(db_data, on_conflict="checkout_request_id").execute()
        print(f"✅ Supabase Logged | CheckoutID: {checkout_id} | Code: {result_code}")
    except Exception as e:
        print(f"❌ Supabase Insert Error: {str(e)}")

    # Always return HTTP 200 OK to Safaricom
    return {"ResultCode": 0, "ResultDesc": "Accepted"}