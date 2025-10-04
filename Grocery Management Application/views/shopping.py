from models.cart import Cart
from models.database import Database
from PyQt5.QtWidgets import QListWidgetItem
from main import QtWidgets

class Shopping:
    def __init__(self, ui):
        self.ui = ui
        self.cart = Cart()
        self.db = Database()
        self.load_products()
        self.ui.procced_topayment_btn.clicked.connect(self.proceed_to_payment)

    def load_products(self):
        products = self.db.get_products()
        self.ui.cart_item_list.clear()
        for product in products:
            item = QListWidgetItem(f"{product[1]} - ${product[2]}")
            self.ui.cart_item_list.addItem(item)
            item.setData(32, product)  

    def proceed_to_payment(self):
        if not self.cart.get_items():
            QtWidgets.QMessageBox.warning(None, "Payment", "Cart is empty!")
            return
        self.ui.total_amount.setText(f"Total Amount: {self.cart.get_total()}")
        self.ui.stackedWidget.setCurrentIndex(2)
