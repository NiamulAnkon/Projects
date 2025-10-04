from PyQt5 import QtCore, QtGui, QtWidgets
from forex_python.converter import CurrencyRates, CurrencyCodes
from forex_python.bitcoin import BtcConverter

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: rgb(202, 220, 220);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.fc_label = QtWidgets.QLabel(self.centralwidget)
        self.fc_label.setGeometry(QtCore.QRect(20, 140, 211, 81))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.fc_label.setFont(font)
        self.fc_label.setAlignment(QtCore.Qt.AlignCenter)
        self.fc_label.setObjectName("fc_label")
        self.frm_currecny = QtWidgets.QLineEdit(self.centralwidget)
        self.frm_currecny.setGeometry(QtCore.QRect(30, 230, 171, 31))
        self.frm_currecny.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 30x solid #000;\n"
"border-radius: 15px;")
        self.frm_currecny.setObjectName("frm_currecny")
        self.tc_label = QtWidgets.QLabel(self.centralwidget)
        self.tc_label.setGeometry(QtCore.QRect(550, 130, 211, 81))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.tc_label.setFont(font)
        self.tc_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tc_label.setObjectName("tc_label")
        self.to_currecny = QtWidgets.QLineEdit(self.centralwidget)
        self.to_currecny.setGeometry(QtCore.QRect(590, 230, 161, 31))
        self.to_currecny.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 30x solid #000;\n"
"border-radius: 15px;")
        self.to_currecny.setObjectName("to_currecny")
        self.amount = QtWidgets.QLineEdit(self.centralwidget)
        self.amount.setGeometry(QtCore.QRect(250, 230, 301, 31))
        self.amount.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 30x solid #000;\n"
"border-radius: 15px;")
        self.amount.setObjectName("amount")
        self.amnt_label = QtWidgets.QLabel(self.centralwidget)
        self.amnt_label.setGeometry(QtCore.QRect(290, 130, 211, 81))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.amnt_label.setFont(font)
        self.amnt_label.setAlignment(QtCore.Qt.AlignCenter)
        self.amnt_label.setObjectName("amnt_label")
        self.convert_btn = QtWidgets.QPushButton(self.centralwidget)
        self.convert_btn.setGeometry(QtCore.QRect(320, 310, 141, 41))
        self.convert_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.convert_btn.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 30px solid #ffff;\n"
"border-radius:15px")
        self.convert_btn.setObjectName("convert_btn")
        self.header = QtWidgets.QLabel(self.centralwidget)
        self.header.setGeometry(QtCore.QRect(230, 20, 321, 101))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.header.setFont(font)
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        self.header.setObjectName("header")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.convert_btn.clicked.connect(self.convert_currency)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Currency Converter"))
        self.fc_label.setText(_translate("MainWindow", "From Currency"))
        self.frm_currecny.setPlaceholderText(_translate("MainWindow", "Enter from currency e.g., USD, EUR"))
        self.tc_label.setText(_translate("MainWindow", "To Currency"))
        self.to_currecny.setPlaceholderText(_translate("MainWindow", "Enter to currency e.g., USD, EUR"))
        self.amount.setPlaceholderText(_translate("MainWindow", "Enter the amount"))
        self.amnt_label.setText(_translate("MainWindow", "Amount"))
        self.convert_btn.setText(_translate("MainWindow", "Convert"))
        self.header.setText(_translate("MainWindow", "Currency Converter"))

    def convert_currency(self):
        from_currency = self.frm_currecny.text().strip().upper()
        to_currency = self.to_currecny.text().strip().upper()
        amount = self.amount.text().strip()

        if not from_currency or not to_currency or not amount:
            self.show_message("Error", "Please fill in all fields!")
            return

        try:
            amount = float(amount)
            converter = CurrencyRates()
            result = converter.convert(from_currency, to_currency, amount)
            self.show_message("Conversion Result", f"{amount} {from_currency} = {result:.2f} {to_currency}")
        except ValueError:
            self.show_message("Error", "Invalid amount. Please enter a valid number.")
        except Exception as e:
            self.show_message("Error", f"Conversion failed: {e}")

    def show_message(self, title, message):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
