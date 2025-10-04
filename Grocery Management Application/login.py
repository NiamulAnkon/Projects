from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0.608, y2:0.448727, stop:0 #98ce4a, stop:1 #2a2d38);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.user_name = QtWidgets.QLineEdit(self.centralwidget)
        self.user_name.setGeometry(QtCore.QRect(220, 160, 341, 31))
        self.user_name.setStyleSheet("background:none;\n"
"border: 3px light white;\n"
"border-radius: 15px;\n"
"padding-left: 5px;")
        self.user_name.setObjectName("user_name")
        self.header = QtWidgets.QLabel(self.centralwidget)
        self.header.setGeometry(QtCore.QRect(210, 60, 361, 71))
        font = QtGui.QFont()
        font.setFamily("Mistral")
        font.setPointSize(24)
        self.header.setFont(font)
        self.header.setStyleSheet("background: None;\n"
"color: rgb(255, 255, 255);")
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        self.header.setObjectName("header")
        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(220, 230, 341, 31))
        self.password.setStyleSheet("background:none;\n"
"border: 3px light white;\n"
"border-radius: 15px;\n"
"padding-left: 5px;")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.login_btn = QtWidgets.QPushButton(self.centralwidget)
        self.login_btn.setGeometry(QtCore.QRect(290, 290, 181, 41))
        self.login_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.login_btn.setStyleSheet("border: 3 px solid green;\n"
"border-radius: 20px;\n"
"background-color: #98ce4a;;")
        self.login_btn.setObjectName("login_btn")
        self.usernm_label = QtWidgets.QLabel(self.centralwidget)
        self.usernm_label.setGeometry(QtCore.QRect(230, 133, 221, 20))
        self.usernm_label.setStyleSheet("background: None;\n"
"color: rgb(255, 255, 255);")
        self.usernm_label.setObjectName("usernm_label")
        self.pass_label = QtWidgets.QLabel(self.centralwidget)
        self.pass_label.setGeometry(QtCore.QRect(230, 200, 221, 20))
        self.pass_label.setStyleSheet("background: None;\n"
"color: rgb(255, 255, 255);")
        self.pass_label.setObjectName("pass_label")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.user_name.setPlaceholderText(_translate("MainWindow", "Enter Your User Name here"))
        self.header.setText(_translate("MainWindow", "Login/Signup"))
        self.password.setPlaceholderText(_translate("MainWindow", "Enter Your password here"))
        self.login_btn.setText(_translate("MainWindow", "Login/Signup"))
        self.usernm_label.setText(_translate("MainWindow", "User Name:"))
        self.pass_label.setText(_translate("MainWindow", "Password:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
