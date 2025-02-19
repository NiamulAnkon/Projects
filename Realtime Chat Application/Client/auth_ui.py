from PyQt5 import QtCore, QtGui, QtWidgets

class AuthUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: white;")

        layout = QtWidgets.QVBoxLayout()

        self.header = QtWidgets.QLabel("Login to Chat")
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.header.setFont(font)
        
        self.username_input = QtWidgets.QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        
        self.password_input = QtWidgets.QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        
        self.login_btn = QtWidgets.QPushButton("Login")
        self.signup_btn = QtWidgets.QPushButton("Signup")

        layout.addWidget(self.header)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.signup_btn)
        
        self.setLayout(layout)
