from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: qlineargradient(spread:repeat, x1:0, y1:1, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(147, 131, 0, 255));")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(250, 60, 281, 451))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.frame.setFont(font)
        self.frame.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"border-radius: 25px")
        self.current_text = ""
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setGeometry(QtCore.QRect(10, 80, 261, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("background-color: rgb(222, 222, 222);\n"
"border: 25 px solid rgb(222, 222, 222);\n"
"border-radius: 15px;")
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.zero_btn = QtWidgets.QPushButton(self.frame)
        self.zero_btn.setGeometry(QtCore.QRect(30, 400, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.zero_btn.setFont(font)
        self.zero_btn.setStyleSheet("background-color: rgb(208, 208, 208);\n"
"border: 15 px solid rgb(208, 208, 208);\n"
"border-radius: 15px;")
        self.zero_btn.setObjectName("zero_btn")
        self.dot_btn = QtWidgets.QPushButton(self.frame)
        self.dot_btn.setGeometry(QtCore.QRect(110, 400, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.dot_btn.setFont(font)
        self.dot_btn.setStyleSheet("background-color: rgb(208, 208, 208);\n"
"border: 15 px solid rgb(208, 208, 208);\n"
"border-radius: 15px;")
        self.dot_btn.setObjectName("dot_btn")
        self.equal_btn = QtWidgets.QPushButton(self.frame)
        self.equal_btn.setGeometry(QtCore.QRect(200, 400, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.equal_btn.setFont(font)
        self.equal_btn.setStyleSheet("background-color: rgb(208, 208, 208);\n"
"border: 15 px solid rgb(208, 208, 208);\n"
"border-radius: 15px;")
        self.equal_btn.setObjectName("equal_btn")
        self.plus_btn = QtWidgets.QPushButton(self.frame)
        self.plus_btn.setGeometry(QtCore.QRect(200, 350, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.plus_btn.setFont(font)
        self.plus_btn.setStyleSheet("background-color: rgb(208, 208, 208);\n"
"border: 15 px solid rgb(208, 208, 208);\n"
"border-radius: 15px;")
        self.plus_btn.setObjectName("plus_btn")
        self.minus_btn = QtWidgets.QPushButton(self.frame)
        self.minus_btn.setGeometry(QtCore.QRect(200, 300, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.minus_btn.setFont(font)
        self.minus_btn.setStyleSheet("background-color: rgb(208, 208, 208);\n"
"border: 15 px solid rgb(208, 208, 208);\n"
"border-radius: 15px;")
        self.minus_btn.setObjectName("minus_btn")
        self.into_btn = QtWidgets.QPushButton(self.frame)
        self.into_btn.setGeometry(QtCore.QRect(200, 250, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.into_btn.setFont(font)
        self.into_btn.setStyleSheet("background-color: rgb(208, 208, 208);\n"
"border: 15 px solid rgb(208, 208, 208);\n"
"border-radius: 15px;")
        self.into_btn.setObjectName("into_btn")
        self.divide_btn = QtWidgets.QPushButton(self.frame)
        self.divide_btn.setGeometry(QtCore.QRect(200, 210, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.divide_btn.setFont(font)
        self.divide_btn.setStyleSheet("background-color: rgb(208, 208, 208);\n"
"border: 15 px solid rgb(208, 208, 208);\n"
"border-radius: 15px;")
        self.divide_btn.setObjectName("divide_btn")
        self.clear_btn = QtWidgets.QPushButton(self.frame)
        self.clear_btn.setGeometry(QtCore.QRect(200, 170, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.clear_btn.setFont(font)
        self.clear_btn.setStyleSheet("background-color: rgb(255, 138, 60);\n"
"border: 15 px solid rgb(208, 208, 208);\n"
"border-radius: 15px;")
        self.clear_btn.setObjectName("clear_btn")
        self.one_btn = QtWidgets.QPushButton(self.frame)
        self.one_btn.setGeometry(QtCore.QRect(30, 350, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.one_btn.setFont(font)
        self.one_btn.setStyleSheet("background-color: rgb(208, 208, 208);\n"
"border: 15 px solid rgb(208, 208, 208);\n"
"border-radius: 15px;")
        self.one_btn.setObjectName("one_btn")
        self.two_btn = QtWidgets.QPushButton(self.frame)
        self.two_btn.setGeometry(QtCore.QRect(110, 350, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.two_btn.setFont(font)
        self.two_btn.setStyleSheet("background-color: rgb(208, 208, 208);\n"
"border: 15 px solid rgb(208, 208, 208);\n"
"border-radius: 15px;")
        self.two_btn.setObjectName("two_btn")
        self.three_btn = QtWidgets.QPushButton(self.frame)
        self.three_btn.setGeometry(QtCore.QRect(30, 300, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.three_btn.setFont(font)
        self.three_btn.setStyleSheet("background-color: rgb(208, 208, 208);\n"
"border: 15 px solid rgb(208, 208, 208);\n"
"border-radius: 15px;")
        self.three_btn.setObjectName("three_btn")
        self.four_btn = QtWidgets.QPushButton(self.frame)
        self.four_btn.setGeometry(QtCore.QRect(110, 300, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.four_btn.setFont(font)
        self.four_btn.setStyleSheet("background-color: rgb(208, 208, 208);\n"
"border: 15 px solid rgb(208, 208, 208);\n"
"border-radius: 15px;")
        self.four_btn.setObjectName("four_btn")
        self.five_btn = QtWidgets.QPushButton(self.frame)
        self.five_btn.setGeometry(QtCore.QRect(30, 250, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.five_btn.setFont(font)
        self.five_btn.setStyleSheet("background-color: rgb(208, 208, 208);\n"
"border: 15 px solid rgb(208, 208, 208);\n"
"border-radius: 15px;")
        self.five_btn.setObjectName("five_btn")
        self.six_btn = QtWidgets.QPushButton(self.frame)
        self.six_btn.setGeometry(QtCore.QRect(110, 250, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.six_btn.setFont(font)
        self.six_btn.setStyleSheet("background-color: rgb(208, 208, 208);\n"
"border: 15 px solid rgb(208, 208, 208);\n"
"border-radius: 15px;")
        self.six_btn.setObjectName("six_btn")
        self.seven_btn = QtWidgets.QPushButton(self.frame)
        self.seven_btn.setGeometry(QtCore.QRect(30, 210, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.seven_btn.setFont(font)
        self.seven_btn.setStyleSheet("background-color: rgb(208, 208, 208);\n"
"border: 15 px solid rgb(208, 208, 208);\n"
"border-radius: 15px;")
        self.seven_btn.setObjectName("seven_btn")
        self.eight_btn = QtWidgets.QPushButton(self.frame)
        self.eight_btn.setGeometry(QtCore.QRect(110, 210, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.eight_btn.setFont(font)
        self.eight_btn.setStyleSheet("background-color: rgb(208, 208, 208);\n"
"border: 15 px solid rgb(208, 208, 208);\n"
"border-radius: 15px;")
        self.eight_btn.setObjectName("eight_btn")
        self.nine_btn = QtWidgets.QPushButton(self.frame)
        self.nine_btn.setGeometry(QtCore.QRect(30, 170, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.nine_btn.setFont(font)
        self.nine_btn.setStyleSheet("background-color: rgb(208, 208, 208);\n"
"border: 15 px solid rgb(208, 208, 208);\n"
"border-radius: 15px;")
        self.nine_btn.setObjectName("nine_btn")
        self.all_clear_btn = QtWidgets.QPushButton(self.frame)
        self.all_clear_btn.setGeometry(QtCore.QRect(110, 170, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.all_clear_btn.setFont(font)
        self.all_clear_btn.setStyleSheet("background-color: rgb(208, 208, 208);\n"
"border: 15 px solid rgb(208, 208, 208);\n"
"border-radius: 15px;")
        self.all_clear_btn.setObjectName("all_clear_btn")
        self.header = QtWidgets.QLabel(self.frame)
        self.header.setGeometry(QtCore.QRect(30, 20, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.header.setFont(font)
        self.header.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        self.header.setObjectName("header")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Connect buttons to functions
        self.zero_btn.clicked.connect(lambda: self.button_click('0'))
        self.one_btn.clicked.connect(lambda: self.button_click('1'))
        self.two_btn.clicked.connect(lambda: self.button_click('2'))
        self.three_btn.clicked.connect(lambda: self.button_click('3'))
        self.four_btn.clicked.connect(lambda: self.button_click('4'))
        self.five_btn.clicked.connect(lambda: self.button_click('5'))
        self.six_btn.clicked.connect(lambda: self.button_click('6'))
        self.seven_btn.clicked.connect(lambda: self.button_click('7'))
        self.eight_btn.clicked.connect(lambda: self.button_click('8'))
        self.nine_btn.clicked.connect(lambda: self.button_click('9'))
        self.dot_btn.clicked.connect(lambda: self.button_click('.'))
        self.plus_btn.clicked.connect(lambda: self.operator_click('+'))
        self.minus_btn.clicked.connect(lambda: self.operator_click('-'))
        self.into_btn.clicked.connect(lambda: self.operator_click('*'))
        self.divide_btn.clicked.connect(lambda: self.operator_click('/'))
        self.equal_btn.clicked.connect(self.equal_click)
        self.clear_btn.clicked.connect(self.clear_click)
        self.all_clear_btn.clicked.connect(self.all_clear_click)

    def button_click(self, value):
        current_text = self.lineEdit.text()
        new_text = current_text + str(value)
        self.lineEdit.setText(new_text)

    def operator_click(self, value):
        current_text = self.lineEdit.text()
        new_text = current_text + str(value)
        self.lineEdit.setText(new_text)

    def clear_click(self):
        current_text = self.lineEdit.text()
        new_text = current_text[:-1]
        self.lineEdit.setText(new_text)

    def all_clear_click(self):
        self.lineEdit.setText("")

    def equal_click(self):
        try:
            result = eval(self.lineEdit.text())
            self.lineEdit.setText(str(result))
        except Exception as e:
            self.lineEdit.setText("Error")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.zero_btn.setText(_translate("MainWindow", "0"))
        self.dot_btn.setText(_translate("MainWindow", "."))
        self.equal_btn.setText(_translate("MainWindow", "="))
        self.plus_btn.setText(_translate("MainWindow", "+"))
        self.minus_btn.setText(_translate("MainWindow", "-"))
        self.into_btn.setText(_translate("MainWindow", "X"))
        self.divide_btn.setText(_translate("MainWindow", "÷"))
        self.clear_btn.setText(_translate("MainWindow", "C"))
        self.one_btn.setText(_translate("MainWindow", "1"))
        self.two_btn.setText(_translate("MainWindow", "2"))
        self.three_btn.setText(_translate("MainWindow", "3"))
        self.four_btn.setText(_translate("MainWindow", "4"))
        self.five_btn.setText(_translate("MainWindow", "5"))
        self.six_btn.setText(_translate("MainWindow", "6"))
        self.seven_btn.setText(_translate("MainWindow", "7"))
        self.eight_btn.setText(_translate("MainWindow", "8"))
        self.nine_btn.setText(_translate("MainWindow", "9"))
        self.all_clear_btn.setText(_translate("MainWindow", "AC"))
        self.header.setText(_translate("MainWindow", "Calculator"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
