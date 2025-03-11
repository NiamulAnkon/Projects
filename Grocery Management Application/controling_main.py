from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
import sys
from main import Ui_MainWindow
from views.dashboard import Dashboard
from views.shopping import Shopping
from views.checkout import Checkout

class Controller(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

        # Shared data structure for products
        self.products = {}  # Dictionary to store product data

        # Connect buttons to functions
        self.ui.add_product_btn.clicked.connect(self.add_product)
        self.ui.dlt_product_btn.clicked.connect(self.delete_selected_product)

        # Cart management
        self.ui.procced_topayment_btn.clicked.connect(self.update_cart)

        # Page Switching
        self.ui.dashboard_btn.clicked.connect(lambda: self.switch_page(0))
        self.ui.customer_windw_btn.clicked.connect(lambda: self.switch_page(1))
        self.ui.payment_windwo_btn.clicked.connect(lambda: self.switch_page(2))
        self.ui.cart_checkout_windwo_btn.clicked.connect(lambda: self.switch_page(3))

    def switch_page(self, index):
        self.ui.stackedWidget.setCurrentIndex(index)

    def add_product(self):
        # Example Product Data (Replace this with real input from a form)
        product_id = len(self.products) + 1  # Auto-increment ID
        product_name = "New Product"
        product_price = 100  # Sample price
        product_stock = 10    # Sample stock

        # Store product in dictionary
        self.products[product_id] = {
            "name": product_name,
            "price": product_price,
            "stock": product_stock
        }

        # Update Dashboard Table
        row_position = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(row_position)
        self.ui.tableWidget.setItem(row_position, 0, QTableWidgetItem(str(product_id)))
        self.ui.tableWidget.setItem(row_position, 1, QTableWidgetItem(product_name))
        self.ui.tableWidget.setItem(row_position, 2, QTableWidgetItem(str(product_price)))

        # Update Shopping Window & Cart
        self.update_cart()

    def delete_selected_product(self):
        selected_row = self.ui.tableWidget.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "No product selected!")
            return

        product_id = self.ui.tableWidget.item(selected_row, 0).text()
        
        if product_id.isdigit():
            product_id = int(product_id)
            if product_id in self.products:
                del self.products[product_id]  # Remove from dictionary
        
        self.ui.tableWidget.removeRow(selected_row)
        self.update_cart()

    def update_cart(self):
        """Update all list widgets to reflect product changes"""
        self.ui.cart_item_list.clear()  # Clear previous items
        
        for product_id, product in self.products.items():
            item_text = f"{product['name']} - ${product['price']} (Stock: {product['stock']})"
            self.ui.cart_item_list.addItem(item_text)



app = QApplication(sys.argv)
window = Controller()
sys.exit(app.exec_())
