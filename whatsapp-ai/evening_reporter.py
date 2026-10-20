import os
from datetime import date, datetime, time
from dotenv import load_dotenv
from twilio.rest import Client
from database import SessionLocal
from models import SalesLog, Product, User

load_dotenv()
twilio_client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))

def generate_daily_report():
    db = SessionLocal()
    try:
        # 1. Define bounds for "Today" (from midnight to 11:59 PM)
        today_start = datetime.combine(date.today(), time.min)
        today_end = datetime.combine(date.today(), time.max)

        # Query all sales made today
        todays_sales = db.query(SalesLog).filter(
            SalesLog.created_at >= today_start,
            SalesLog.created_at <= today_end
        ).all()

        total_revenue = sum([sale.total_price for sale in todays_sales])
        total_items_sold = sum([sale.quantity_sold for sale in todays_sales])

        # 2. Check for Critical Out-of-Stock Items (Stock == 0)
        out_of_stock_items = db.query(Product).filter(Product.stock_count == 0).all()
        
        scarcity_list = ""
        if out_of_stock_items:
            for item in out_of_stock_items:
                scarcity_list += f"⚠️ *{item.name}* (Out of stock)\n"
        else:
            scarcity_list = "✅ All products are currently healthy and in stock!"

        # 3. Format the Executive Snapshot Briefing Card
        report_message = (
            f"📊 *DAILY STORE PERFORMANCE SUMMARY*\n"
            f"📅 Date: {date.today().strftime('%B %d, %Y')}\n"
            f"───────────────────────\n\n"
            f"💰 *Total Revenue:* KSH {total_revenue:,.2f}\n"
            f"📦 *Total Units Sold:* {total_items_sold} units\n\n"
            f"🔍 *CRITICAL INVENTORY ALERT:*\n"
            f"{scarcity_list}\n"
            f"───────────────────────\n"
            f"End of daily reporting execution loop."
        )

        # Find the Admin phone number dynamically to route the payload
        admin_user = db.query(User).filter(User.role == "admin").first()
        if admin_user:
            twilio_client.messages.create(
                from_='whatsapp:+14155238886',
                body=report_message,
                to=f"whatsapp:{admin_user.phone_number}"
            )
            print("Daily evening status notification processed successfully.")
        else:
            print("Admin user entry not located inside current database indexes.")

    except Exception as e:
        print(f"Error compiling daily operations report metrics: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    generate_daily_report()