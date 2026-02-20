from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

class InvoiceGenerator:
    def __init__(self, invoice_data):
        self.invoice = invoice_data

    def generate_pdf(self, file_path):
        c = canvas.Canvas(file_path, pagesize=LETTER)
        width, height = LETTER

        # Header
        c.setFont("Helvetica-Bold", 20)
        c.drawString(50, height - 50, "INVOICE")
        
        c.setFont("Helvetica", 10)
        c.drawRightString(width - 50, height - 50, f"Invoice #: {self.invoice.invoice_number}")
        c.drawRightString(width - 50, height - 65, f"Date: {self.invoice.issue_date.strftime('%Y-%m-%d')}")

        # Client Info
        c.drawString(50, height - 100, "Bill To:")
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, height - 115, self.invoice.client.name)
        c.setFont("Helvetica", 10)
        c.drawString(50, height - 130, self.invoice.client.address or "")

        # Table Data
        data = [["Description", "Qty", "Unit Price", "Tax %", "Total"]]
        for line in self.invoice.lines:
            data.append([
                line.description,
                str(line.qty),
                f"{line.unit_price:.2f}",
                f"{line.tax_percent}%",
                f"{line.line_total:.2f}"
            ])

        table = Table(data, colWidths=[250, 50, 80, 50, 80])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]))

        table.wrapOn(c, width, height)
        table.drawOn(c, 50, height - 300)

        # Totals
        c.drawRightString(width - 50, height - 350, f"Subtotal: {self.invoice.subtotal:.2f}")
        c.drawRightString(width - 50, height - 365, f"Tax: {self.invoice.tax_total:.2f}")
        c.setFont("Helvetica-Bold", 12)
        c.drawRightString(width - 50, height - 385, f"TOTAL: {self.invoice.total:.2f}")
        # (Inside generate_pdf after the Totals section)
        
        y_position = height - 420 # Move below the totals
        
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y_position, "Payment Method:")
        c.setFont("Helvetica", 10)
        c.drawString(150, y_position, self.invoice.payment_method or "N/A")

        if self.invoice.notes:
            y_position -= 20
            c.setFont("Helvetica-Bold", 10)
            c.drawString(50, y_position, "Notes:")
            c.setFont("Helvetica", 10)
            c.drawString(50, y_position - 15, self.invoice.notes)
            y_position -= 20

        if self.invoice.terms:
            y_position -= 30
            c.setFont("Helvetica-Bold", 10)
            c.drawString(50, y_position, "Terms & Conditions:")
            c.setFont("Helvetica", 10)
            c.drawString(50, y_position - 15, self.invoice.terms)

        c.save()