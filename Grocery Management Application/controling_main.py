from PyQt5.QtWidgets import QApplication, QMainWindow
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

        self.dashboard = Dashboard(self.ui)
        self.shopping = Shopping(self.ui)
        self.checkout = Checkout(self.ui)

        self.ui.dashboard_btn.clicked.connect(lambda: self.switch_page(0))
        self.ui.customer_windw_btn.clicked.connect(lambda: self.switch_page(1))
        self.ui.payment_windwo_btn.clicked.connect(lambda: self.switch_page(2))
        self.ui.cart_checkout_windwo_btn.clicked.connect(lambda: self.switch_page(3))

        self.show()

    def switch_page(self, index):
        self.ui.stackedWidget.setCurrentIndex(index)

app = QApplication(sys.argv)
window = Controller()
sys.exit(app.exec_())
