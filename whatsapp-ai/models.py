from sqlalchemy import Column, Integer, String, Numeric, Text, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from database import Base

# 1. CENTRAL SAAS TENANT TABLE
class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False) 
    currency = Column(String(10), default="KSH")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # All parent relationships live inside this class block
    users = relationship("User", back_populates="business")
    products = relationship("Product", back_populates="business")
    invoices = relationship("Invoice", back_populates="business")
    restock_requests = relationship("RestockRequest", back_populates="business")
    suppliers = relationship("Supplier", back_populates="business")


# 2. USER MANAGEMENT TABLE
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), unique=True, nullable=False)
    role = Column(String(20), nullable=False)
    name = Column(String(100))
    
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=True)
    business = relationship("Business", back_populates="users")


# 3. GLOBAL FLEXIBLE INVENTORY TABLE
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)  # kept for backward compat, mirrors selling_price
    buying_price = Column(Numeric(10, 2), nullable=False, default=0)
    selling_price = Column(Numeric(10, 2), nullable=False, default=0)
    stock_count = Column(Integer, nullable=False)
    description = Column(Text)
    part_number = Column(String(100))
    barcode = Column(String(100))  # Add this exact line
    
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=True)
    business = relationship("Business", back_populates="products")


# 4. OVERDUE TRACKING ENGINE
class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100), nullable=False)
    customer_phone = Column(String(20), nullable=False)
    amount_due = Column(Numeric(10, 2), nullable=False)
    description = Column(Text)
    due_date = Column(Date, nullable=False)
    is_paid = Column(Boolean, default=False)
    # Real column (was previously faked via setattr/getattr and never persisted to DB)
    debtor_items_json = Column(Text, default="[]")
    
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=True)
    business = relationship("Business", back_populates="invoices")


# 5. SUPPLY CHAIN APPROVAL PIPELINE
class RestockRequest(Base):
    __tablename__ = "restock_requests"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(100), nullable=False)
    quantity_requested = Column(Integer, nullable=False)
    requested_by = Column(String(100), nullable=False)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=True)
    business = relationship("Business", back_populates="restock_requests")


# 6. SUPPLIER DIRECTORY TABLE
class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False)
    product_supplied = Column(String(100), nullable=False)
    
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=True)
    business = relationship("Business", back_populates="suppliers")

class SalesLog(Base):
    __tablename__ = "sales_log"

    id = Column(Integer, primary_key=True, index=True)
    sale_ref = Column(String(40), index=True, nullable=True)  # groups line items from one checkout for reprinting
    product_name = Column(String(100), nullable=False)
    quantity_sold = Column(Integer, nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)  # what the customer actually paid (may include ETR tax)
    # Snapshots taken at time of sale, so profit stays accurate even if the
    # Product's prices change later, and isn't distorted by ETR tax.
    unit_selling_price = Column(Numeric(10, 2), nullable=False, default=0)
    unit_buying_price = Column(Numeric(10, 2), nullable=False, default=0)
    payment_method = Column(String(30), default="Cash")
    bank_name = Column(String(100), nullable=True)
    sold_by = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=True)

    @property
    def profit(self):
        """Profit for this line item: (selling - buying) * qty, unaffected by ETR tax."""
        return round((float(self.unit_selling_price) - float(self.unit_buying_price)) * self.quantity_sold, 2)