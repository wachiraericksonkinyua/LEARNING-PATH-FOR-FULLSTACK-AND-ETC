import os
from datetime import date
from dotenv import load_dotenv
from twilio.rest import Client
from database import SessionLocal
from models import Invoice

load_dotenv()

# Initialize Twilio Client
twilio_client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))

def check_and_send_reminders():
    db = SessionLocal()
    try:
        # Fetch all unpaid invoices where the due date has passed or is today
        unpaid_invoices = db.query(Invoice).filter(
            Invoice.is_paid == False,
            Invoice.due_date <= date.today()
        ).all()

        if not unpaid_invoices:
            print("No overdue invoices found today.")
            return

        for invoice in unpaid_invoices:
            reminder_message = (
                f"Hello {invoice.customer_name},\n\n"
                f"This is a friendly reminder from our store regarding your unpaid invoice for *{invoice.description}*.\n"
                f"Amount Due: *KSH {invoice.amount_due}*\n"
                f"Due Date: {invoice.due_date}\n\n"
                f"Please arrange for payment at your earliest convenience. Thank you!"
            )

            # Send the reminder via WhatsApp
            twilio_client.messages.create(
                from_='whatsapp:+14155238886',
                body=reminder_message,
                to=f"whatsapp:{invoice.customer_phone}"
            )
            print(f"Sent reminder to {invoice.customer_name} ({invoice.customer_phone})")

    except Exception as e:
        print(f"Error running reminders: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Running Monday Invoice Follow-up Job...")
    check_and_send_reminders()