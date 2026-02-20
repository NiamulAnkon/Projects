def calculate_line_total(qty, unit_price, tax_percent):
    """Calculates the total for a single invoice line."""
    base = qty * unit_price
    tax = base * (tax_percent / 100)
    return round(base + tax, 2)

def generate_invoice_number(session, year):
    """Generates auto-incrementing invoice number: INV-YYYY-XXXX"""
    from src.models import Invoice
    count = session.query(Invoice).filter(Invoice.invoice_number.like(f"INV-{year}-%")).count()
    return f"INV-{year}-{(count + 1):04d}"