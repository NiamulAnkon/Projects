import os
from datetime import datetime
from sqlalchemy import func
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, 
    QTableWidget, QTableWidgetItem, QPushButton, QFrame, QHeaderView, 
    QDialog, QLineEdit, QFormLayout, QMessageBox, QComboBox, QDateEdit, QFileDialog
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Local Imports
from src.db import SessionLocal
from src.models import Client, Invoice, InvoiceLine
from src.invoice_generator import InvoiceGenerator
from src.utils import generate_invoice_number, calculate_line_total
from src.backup import create_backup, restore_backup
# --- Helper Dialogs ---

class ClientDialog(QDialog):
    def __init__(self, parent=None, client_data=None):
        super().__init__(parent)
        self.setWindowTitle("Client Details")
        self.setMinimumWidth(400)
        self.layout = QFormLayout(self)
        
        # Fields
        self.name = QLineEdit()
        self.company = QLineEdit()
        self.email = QLineEdit()
        self.phone = QLineEdit()
        self.address = QLineEdit()
        self.project_desc = QLineEdit()
        self.due_date = QDateEdit(QDate.currentDate())
        self.due_date.setCalendarPopup(True)
        self.price = QLineEdit("0.00")
        self.status = QComboBox()
        self.status.addItems(["pending", "completed", "cancelled"])

        self.layout.addRow("Client Name *:", self.name)
        self.layout.addRow("Company:", self.company)
        self.layout.addRow("Email:", self.email)
        self.layout.addRow("Phone:", self.phone)
        self.layout.addRow("Address:", self.address)
        self.layout.addRow("Project Description:", self.project_desc)
        self.layout.addRow("Project Due Date:", self.due_date)
        self.layout.addRow("Project Price ($):", self.price)
        self.layout.addRow("Status:", self.status)
        
        # Pre-fill if editing
        if client_data:
            self.name.setText(client_data.name)
            self.company.setText(client_data.company)
            self.email.setText(client_data.email or "")
            self.phone.setText(client_data.phone or "")
            self.address.setText(client_data.address or "")
            self.project_desc.setText(client_data.project_description or "")
            if client_data.due_date:
                self.due_date.setDate(client_data.due_date)
            self.price.setText(str(client_data.price))
            self.status.setCurrentText(client_data.status or "pending")

        self.save_btn = QPushButton("Save Client")
        self.save_btn.clicked.connect(self.accept)
        self.layout.addRow(self.save_btn)

# --- Sub-Widgets (Tabs) ---

class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.db = SessionLocal()
        
        # 1. KPI Section
        self.kpi_layout = QHBoxLayout()
        self.layout.addLayout(self.kpi_layout)

        # 2. Chart Section (The "Dashboard" feel)
        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.layout.addWidget(self.canvas)
        
        # 3. Recent Activity Table
        self.layout.addWidget(QLabel("\nRecent Activity"))
        self.invoice_table = QTableWidget(0, 5)
        self.invoice_table.setHorizontalHeaderLabels(["Inv #", "Client", "Date", "Total", "Status"])
        self.invoice_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.invoice_table)
        
        self.refresh_data()

    def refresh_data(self):
        # Stats Logic
        clients_count = self.db.query(Client).count()
        outstanding = self.db.query(func.sum(Client.price)).filter(Client.status == "pending").scalar() or 0.0
        revenue = self.db.query(func.sum(Client.price)).filter(Client.status == "completed").scalar() or 0.0

        # Update KPI Cards
        for i in reversed(range(self.kpi_layout.count())): 
            self.kpi_layout.itemAt(i).widget().setParent(None)
        self.kpi_layout.addWidget(self.create_kpi_card("Total Clients", clients_count, "#3498db"))
        self.kpi_layout.addWidget(self.create_kpi_card("Outstanding", f"${outstanding:,.2f}", "#e74c3c"))
        self.kpi_layout.addWidget(self.create_kpi_card("Total Revenue", f"${revenue:,.2f}", "#27ae60"))

        # Update Chart
        self.update_chart(revenue, outstanding)
        
        # Update Table (Latest 5)
        recent = self.db.query(Invoice).join(Client).order_by(Invoice.issue_date.desc()).limit(5).all()
        self.invoice_table.setRowCount(len(recent))
        for i, inv in enumerate(recent):
            self.invoice_table.setItem(i, 0, QTableWidgetItem(inv.invoice_number))
            self.invoice_table.setItem(i, 1, QTableWidgetItem(inv.client.name))
            self.invoice_table.setItem(i, 2, QTableWidgetItem(inv.issue_date.strftime("%Y-%m-%d")))
            self.invoice_table.setItem(i, 3, QTableWidgetItem(f"${inv.total:,.2f}"))
            self.invoice_table.setItem(i, 4, QTableWidgetItem(inv.status))

    def update_chart(self, revenue, outstanding):
        self.canvas.figure.clf()
        ax = self.canvas.figure.add_subplot(111)
        labels = ['Collected Revenue', 'Outstanding']
        values = [revenue, outstanding]
        colors = ['#27ae60', '#e74c3c']
        
        ax.bar(labels, values, color=colors)
        ax.set_title("Financial Performance")
        self.canvas.draw()

    def create_kpi_card(self, title, value, color):
        card = QWidget()
        card.setStyleSheet(f"""
            QWidget {{
                background-color: {color};
                border-radius: 8px;
                padding: 10px;
                margin: 5px;
            }}
        """)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        
        value_label = QLabel(str(value))
        value_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        value_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        return card

class ClientManagerWidget(QWidget):
    """List and manage your freelance clients."""
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.db = SessionLocal()
        
        self.toolbar = QHBoxLayout()
        self.add_btn = QPushButton("+ Add Client")
        self.add_btn.clicked.connect(self.add_client)
        self.toolbar.addWidget(self.add_btn)
        self.toolbar.addStretch()
        self.layout.addLayout(self.toolbar)
        
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Name", "Company", "Email", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table)
        
        self.load_clients()

    def load_clients(self):
        # Update headers to match your request
        headers = ["Name", "Email", "Company", "Phone", "Address", "Project Desc", "Price", "Status", "Actions"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        clients = self.db.query(Client).all()
        self.table.setRowCount(len(clients))
        
        for i, client in enumerate(clients):
            self.table.setItem(i, 0, QTableWidgetItem(client.name))
            self.table.setItem(i, 1, QTableWidgetItem(client.email or ""))
            self.table.setItem(i, 2, QTableWidgetItem(client.company or ""))
            self.table.setItem(i, 3, QTableWidgetItem(client.phone or ""))
            self.table.setItem(i, 4, QTableWidgetItem(client.address or ""))
            self.table.setItem(i, 5, QTableWidgetItem(client.project_description or ""))
            self.table.setItem(i, 6, QTableWidgetItem(f"${client.price:,.2f}"))
            self.table.setItem(i, 7, QTableWidgetItem(client.status or "pending"))
            
            # Action Buttons (Edit/Delete)
            actions = QWidget()
            l = QHBoxLayout(actions)
            l.setContentsMargins(2, 2, 2, 2)
            
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda ch, c=client: self.edit_client(c))
            del_btn = QPushButton("Del")
            del_btn.clicked.connect(lambda ch, c=client: self.delete_client(c))
            
            l.addWidget(edit_btn)
            l.addWidget(del_btn)
            self.table.setCellWidget(i, 8, actions)

    def add_client(self):
        dialog = ClientDialog(self)
        if dialog.exec_():
            new_client = Client(
                name=dialog.name.text(), 
                company=dialog.company.text(),
                email=dialog.email.text(), 
                phone=dialog.phone.text(),
                address=dialog.address.text(),
                project_description=dialog.project_desc.text(),
                due_date=dialog.due_date.date().toPyDate(),
                price=float(dialog.price.text()),
                status=dialog.status.currentText()
            )
            self.db.add(new_client)
            self.db.commit()
            self.load_clients()

    def delete_client(self, client):
        reply = QMessageBox.question(self, 'Confirm', f"Delete {client.name}?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.db.delete(client)
            self.db.commit()
            self.load_clients()

    def edit_client(self, client):
        # Open the dialog and pass the existing client object
        dialog = ClientDialog(self, client_data=client)
        
        if dialog.exec_():
            try:
                # Update the database object with the new values from the dialog
                client.name = dialog.name.text()
                client.company = dialog.company.text()
                client.phone = dialog.phone.text()
                client.address = dialog.address.text()
                client.project_description = dialog.project_desc.text()
                client.due_date = dialog.due_date.date().toPyDate()
                client.price = float(dialog.price.text())
                client.status = dialog.status.currentText()
                
                self.db.commit() # Save changes
                self.load_clients() # Refresh the table
                QMessageBox.information(self, "Success", "Client details updated.")
            except ValueError:
                QMessageBox.warning(self, "Error", "Invalid price format. Please enter a number.")
            except Exception as e:
                self.db.rollback()
                QMessageBox.critical(self, "Error", f"Could not update: {str(e)}")

class InvoiceEditorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.db = SessionLocal()
        self.save_success = False
        
        # Toolbar
        self.toolbar = QHBoxLayout()
        self.add_inv_btn = QPushButton("+ Create New Invoice")
        self.add_inv_btn.setStyleSheet("background-color: #3498db; color: white; padding: 10px;")
        self.add_inv_btn.clicked.connect(self.open_invoice_editor)
        self.toolbar.addWidget(self.add_inv_btn)
        self.toolbar.addStretch()
        self.layout.addLayout(self.toolbar)

        # Invoice List
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Inv #", "Client", "Total", "Status", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table)
        
        self.load_invoices()

    def load_invoices(self):
        invoices = self.db.query(Invoice).all()
        self.table.setRowCount(len(invoices))
        for i, inv in enumerate(invoices):
            self.table.setItem(i, 0, QTableWidgetItem(inv.invoice_number))
            # self.table.setItem(i, 1, QTableWidgetItem(inv.client.name))
            self.table.setItem(i, 2, QTableWidgetItem(f"${inv.total:,.2f}"))
            self.table.setItem(i, 3, QTableWidgetItem(inv.status))
            
            actions = QWidget()
            l = QHBoxLayout(actions)
            l.setContentsMargins(2, 2, 2, 2)
            
            pdf_btn = QPushButton("View PDF")
            pdf_btn.clicked.connect(lambda ch, inv_no=inv.invoice_number: self.view_pdf(inv_no))
            del_btn = QPushButton("Delete")
            del_btn.clicked.connect(lambda ch, c=inv: self.delete_invoice(c))
            
            l.addWidget(pdf_btn)
            l.addWidget(del_btn)
            self.table.setCellWidget(i, 4, actions)

    def open_invoice_editor(self):
        # We open the form in a Popup Dialog now
        dialog = QDialog(self)
        dialog.setWindowTitle("Create New Invoice")
        dialog.setMinimumSize(800, 600)
        layout = QVBoxLayout(dialog)
        
        editor = InvoiceEditorWidget() # This is the form class we wrote earlier
        layout.addWidget(editor)
        
        # Close dialog when invoice is successfully saved
        editor.save_btn.clicked.connect(lambda: dialog.accept() if editor.save_success else None)
        
        if dialog.exec_():
            self.load_invoices()

    def view_pdf(self, inv_no):
        path = f"invoices/{inv_no}.pdf"
        if os.path.exists(path):
            os.startfile(path) # Opens the PDF in your computer's viewer
        else:
            QMessageBox.warning(self, "Error", "PDF file not found.")

    def delete_invoice(self, invoice):
        reply = QMessageBox.question(self, 'Confirm Delete', f"Delete invoice {invoice.invoice_number}?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                # Delete the PDF file if it exists
                pdf_path = f"invoices/{invoice.invoice_number}.pdf"
                if os.path.exists(pdf_path):
                    os.remove(pdf_path)
                
                # Delete from database
                self.db.delete(invoice)
                self.db.commit()
                self.load_invoices()
                QMessageBox.information(self, "Success", "Invoice deleted successfully.")
            except Exception as e:
                self.db.rollback()
                QMessageBox.critical(self, "Error", f"Could not delete invoice: {str(e)}")

# --- Main Application Shell ---

class MainWindow(QMainWindow):
    """The root container for the app."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Freelance Client Manager")
        self.resize(1100, 750)
        
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        self.dashboard = DashboardWidget()
        self.client_manager = ClientManagerWidget()
        self.invoice_editor = InvoiceEditorWidget()
        
        self.tabs.addTab(self.dashboard, "Dashboard")
        self.tabs.addTab(self.client_manager, "Clients")
        self.tabs.addTab(self.invoice_editor, "Create Invoice")
        
        self.tabs.currentChanged.connect(self.on_tab_change)
        self.apply_styles()
                # Inside MainWindow.__init__
        self.settings_tab = SettingsWidget()
        self.tabs.addTab(self.settings_tab, "Settings")

    def on_tab_change(self, index):
        """Refreshes the active tab's data whenever the user clicks it."""
        if index == 0: self.dashboard.refresh_data()
        elif index == 1: self.client_manager.load_clients()
        elif index == 2: self.invoice_editor.load_invoices()

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f6fa; }
            QTabWidget::pane { border: none; background: white; }
            QTabBar::tab { background: #dcdde1; padding: 12px 30px; margin: 2px; border-top-left-radius: 8px; border-top-right-radius: 8px; }
            QTabBar::tab:selected { background: #3498db; color: white; font-weight: bold; }
            QPushButton { border-radius: 4px; padding: 6px; }
            QTableWidget { gridline-color: #ecf0f1; background: white; }
        """)

class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        title = QLabel("Application Settings & Backup")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        self.layout.addWidget(title)
        
        # Backup Section
        backup_group = QFrame()
        backup_group.setFrameShape(QFrame.StyledPanel)
        group_layout = QVBoxLayout(backup_group)
        
        group_layout.addWidget(QLabel("Data Management:"))
        
        self.export_btn = QPushButton("Export Full Backup (.zip)")
        self.export_btn.clicked.connect(self.run_export)
        group_layout.addWidget(self.export_btn)
        
        self.import_btn = QPushButton("Import/Restore Backup")
        self.import_btn.clicked.connect(self.run_import)
        group_layout.addWidget(self.import_btn)
        
        self.layout.addWidget(backup_group)
        self.layout.addStretch()

    def run_export(self):
        try:
            path = create_backup("freelance_manager.db", "invoices", "backups")
            QMessageBox.information(self, "Backup Successful", f"Backup created at:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Backup Failed", str(e))

    def run_import(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Backup Zip", "backups", "Zip Files (*.zip)")
        if file_path:
            confirm = QMessageBox.question(self, "Confirm Restore", 
                                         "This will overwrite your current database and invoices. Continue?",
                                         QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                try:
                    restore_backup(file_path, "freelance_manager.db", "invoices")
                    QMessageBox.information(self, "Success", "Data restored successfully! Please restart the app.")
                except Exception as e:
                    QMessageBox.critical(self, "Restore Failed", str(e))