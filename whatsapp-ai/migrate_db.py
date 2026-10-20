"""
One-time migration script.
Run this ONCE against your live database to add the new columns that
models.py now expects. Safe to run multiple times (uses IF NOT EXISTS).

Usage:
    cd ~/whatsapp-ai
    source venv/bin/activate
    python migrate_db.py
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

STATEMENTS = [
    # products: profit calculation needs both buying and selling price
    "ALTER TABLE products ADD COLUMN IF NOT EXISTS buying_price NUMERIC(10,2) NOT NULL DEFAULT 0",
    "ALTER TABLE products ADD COLUMN IF NOT EXISTS selling_price NUMERIC(10,2) NOT NULL DEFAULT 0",

    # invoices: real column for the debt drill-down item history
    "ALTER TABLE invoices ADD COLUMN IF NOT EXISTS debtor_items_json TEXT DEFAULT '[]'",

    # sales_log: receipt reprinting, profit snapshots, payment details
    "ALTER TABLE sales_log ADD COLUMN IF NOT EXISTS sale_ref VARCHAR(40)",
    "ALTER TABLE sales_log ADD COLUMN IF NOT EXISTS unit_selling_price NUMERIC(10,2) NOT NULL DEFAULT 0",
    "ALTER TABLE sales_log ADD COLUMN IF NOT EXISTS unit_buying_price NUMERIC(10,2) NOT NULL DEFAULT 0",
    "ALTER TABLE sales_log ADD COLUMN IF NOT EXISTS payment_method VARCHAR(30) DEFAULT 'Cash'",
    "ALTER TABLE sales_log ADD COLUMN IF NOT EXISTS bank_name VARCHAR(100)",
    "ALTER TABLE sales_log ADD COLUMN IF NOT EXISTS business_id INTEGER",

    # Backfill: existing products had no selling_price, so profit reports
    # would show 0 revenue for them. Copy the old `price` column across.
    "UPDATE products SET selling_price = price WHERE selling_price = 0",
]

def run_migration():
    with engine.begin() as conn:
        for stmt in STATEMENTS:
            print(f"Running: {stmt}")
            conn.execute(text(stmt))
    print("\n✅ Migration complete. Your database schema now matches models.py.")
    print("⚠️  Note: buying_price for existing products is still 0 — edit those")
    print("   products (or run a manual UPDATE) to get accurate profit numbers.")

if __name__ == "__main__":
    run_migration()