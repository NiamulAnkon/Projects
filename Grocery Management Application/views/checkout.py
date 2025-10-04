from models.database import Database
from main import *
class Checkout:
    def __init__(self, ui):
        self.ui = ui
        self.db = Database()
        self.ui.confirm_payment_btn.clicked.connect(self.confirm_payment)

    def confirm_payment(self):
        payment_method = self.ui.payment_method.currentText()
        total_amount = self.ui.total_amount.text().split(":")[1].strip()
        items = "\n".join([item.text() for item in self.ui.cart_item_list.selectedItems()])

        if not items:
            QtWidgets.QMessageBox.warning(None, "Payment", "No items selected.")
            return

        self.db.add_order(items, float(total_amount), payment_method)

        self.ui.recipt.setText(f"Receipt:\n{items}\nTotal: {total_amount}\nPayment: {payment_method}")
        QtWidgets.QMessageBox.information(None, "Success", "Payment Completed!")
