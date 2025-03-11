from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import os
from main import *

class Controling(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()
        # ----------------------- Page Switching -----------------------#
        self.ui.dashboard_btn.clicked.connect(lambda: self.switch_page(0))
        self.ui.customer_windw_btn.clicked.connect(lambda: self.switch_page(1))
        self.ui.payment_windwo_btn.clicked.connect(lambda: self.switch_page(2))
        self.ui.cart_checkout_windwo_btn.clicked.connect(lambda: self.switch_page(3))

        #-------------------------Dashboard Window Setup-------------------------#
        
    
    def switch_page(self, index):
        self.ui.stackedWidget.setCurrentIndex(index)



app = QApplication(sys.argv)
window = Controling()
sys.exit(app.exec_())