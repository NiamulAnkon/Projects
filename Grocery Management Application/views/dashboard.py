from models.database import Database
from main import *
from PyQt5.QtWidgets import QMessageBox
class Dashboard:
    def __init__(self, ui):
        self.ui = ui
        self.db = Database()
        self.load_products()
        self.ui.add_product_btn.clicked.connect(self.add_product)
        self.ui.dlt_product_btn.clicked.connect(self.delete_selected_product)

    def load_products(self):
        products = self.db.get_products()
        self.ui.tableWidget.setRowCount(0)
        for row_idx, product in enumerate(products):
            self.ui.tableWidget.insertRow(row_idx)
            for col_idx, data in enumerate(product[1:]):  
                self.ui.tableWidget.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(data)))

    def add_product(self):
        name, ok = QtWidgets.QInputDialog.getText(None, "Add Product", "Enter product name:")
        if not ok or not name:
            return
        price, ok = QtWidgets.QInputDialog.getDouble(None, "Add Product", "Enter price:", min=0)
        if not ok:
            return
        stock, ok = QtWidgets.QInputDialog.getInt(None, "Add Product", "Enter stock:", min=0)
        if not ok:
            return
        self.db.add_product(name, price, stock)
        self.load_products()

    def delete_selected_product(self):
        selected_row = self.ui.tableWidget.currentRow()
        
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "No product selected!")
            return
        
        item = self.ui.tableWidget.item(selected_row, 0)  # Get the first column item

        if item is None or item.text().strip() == "":
            QMessageBox.warning(self, "Error", "Invalid product ID!")
            return
        
        try:
            product_id = int(item.text())  # Convert to integer
        except ValueError:
            QMessageBox.warning(self, "Error", "Product ID must be a number!")
            return

        # Now you can safely delete the row
        self.ui.tableWidget.removeRow(selected_row)
        QMessageBox.information(self, "Success", f"Product {product_id} deleted.")
