from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Date
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    company = Column(String(100))
    email = Column(String(100))
    phone = Column(String(20))
    address = Column(Text)
    # New Fields
    project_description = Column(Text)
    due_date = Column(Date)
    price = Column(Float, default=0.0)
    status = Column(String(20), default="pending")  # completed, pending, cancelled
    
    invoices = relationship("Invoice", back_populates="client")

class Invoice(Base):
    __tablename__ = 'invoices'
    id = Column(Integer, primary_key=True)
    invoice_number = Column(String(20), unique=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    issue_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(Date)
    status = Column(String(20), default="Sent")
    # Totals
    subtotal = Column(Float, default=0.0)
    tax_total = Column(Float, default=0.0)
    total = Column(Float, default=0.0)
    # New Fields
    payment_method = Column(String(50)) # PayPal, Stripe, Bank, etc.
    notes = Column(Text)
    terms = Column(Text)
    
    client = relationship("Client", back_populates="invoices")
    lines = relationship("InvoiceLine", back_populates="invoice", cascade="all, delete-orphan")

class InvoiceLine(Base):
    __tablename__ = 'invoice_lines'
    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'))
    description = Column(String(200)) # This is the "Service" field
    qty = Column(Float, default=1.0)
    unit_price = Column(Float, default=0.0)
    tax_percent = Column(Float, default=0.0)
    line_total = Column(Float, default=0.0)
    
    invoice = relationship("Invoice", back_populates="lines")