from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AuthWindow(object):
    def setupUi(self, AuthWindow):
        AuthWindow.setObjectName("AuthWindow")
        AuthWindow.setFixedSize(400, 500)
        AuthWindow.setStyleSheet("background-color: rgb(30, 30, 47);")

        # Central widget
        self.centralwidget = QtWidgets.QWidget(AuthWindow)
        self.central_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.central_layout.setContentsMargins(30, 30, 30, 30)
        self.central_layout.setSpacing(20)

        # Title
        self.title = QtWidgets.QLabel("🔐 NebulaShare", self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.title.setFont(font)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setStyleSheet("color: white; margin-bottom: 10px;")
        self.central_layout.addWidget(self.title)

        # Stacked widget for Login & Register
        self.stack = QtWidgets.QStackedWidget(self.centralwidget)
        self.central_layout.addWidget(self.stack, stretch=1)

        # ===== LOGIN PAGE =====
        self.login_page = QtWidgets.QWidget()
        self.login_layout = QtWidgets.QVBoxLayout(self.login_page)
        self.login_layout.setSpacing(15)

        self.login_username = self.create_icon_input("👤", "Username")
        self.login_layout.addWidget(self.login_username)

        self.login_password = self.create_icon_input("🔒", "Password", password=True)
        self.login_layout.addWidget(self.login_password)

        self.login_btn = self.create_button("Login")
        self.login_layout.addWidget(self.login_btn)

        self.login_toggle = QtWidgets.QLabel("Don't have an account? <a href='#'>Register</a>", self.login_page)
        self.set_link_style(self.login_toggle)
        self.login_layout.addWidget(self.login_toggle, alignment=QtCore.Qt.AlignCenter)

        self.stack.addWidget(self.login_page)

        # ===== REGISTER PAGE =====
        self.register_page = QtWidgets.QWidget()
        self.register_layout = QtWidgets.QVBoxLayout(self.register_page)
        self.register_layout.setSpacing(15)

        self.reg_username = self.create_icon_input("👤", "Username")
        self.register_layout.addWidget(self.reg_username)

        self.reg_email = self.create_icon_input("✉️", "Email")
        self.register_layout.addWidget(self.reg_email)

        self.reg_password = self.create_icon_input("🔒", "Password", password=True)
        self.register_layout.addWidget(self.reg_password)

        self.reg_confirm = self.create_icon_input("🔒", "Confirm Password", password=True)
        self.register_layout.addWidget(self.reg_confirm)

        self.register_btn = self.create_button("Register")
        self.register_layout.addWidget(self.register_btn)

        self.register_toggle = QtWidgets.QLabel("Already have an account? <a href='#'>Login</a>", self.register_page)
        self.set_link_style(self.register_toggle)
        self.register_layout.addWidget(self.register_toggle, alignment=QtCore.Qt.AlignCenter)

        self.stack.addWidget(self.register_page)

        AuthWindow.setCentralWidget(self.centralwidget)

        # Switch signals
        self.login_toggle.linkActivated.connect(lambda: self.stack.setCurrentWidget(self.register_page))
        self.register_toggle.linkActivated.connect(lambda: self.stack.setCurrentWidget(self.login_page))

        self.retranslateUi(AuthWindow)
        QtCore.QMetaObject.connectSlotsByName(AuthWindow)

    def create_icon_input(self, icon_text, placeholder, password=False):
        """Creates a styled input with an emoji/icon at the left"""
        container = QtWidgets.QFrame()
        layout = QtWidgets.QHBoxLayout(container)
        layout.setContentsMargins(10, 0, 10, 0)

        label = QtWidgets.QLabel(icon_text)
        label.setStyleSheet("color: white; font-size: 18px;")
        layout.addWidget(label)

        line_edit = QtWidgets.QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        if password:
            line_edit.setEchoMode(QtWidgets.QLineEdit.Password)

        line_edit.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid rgb(72, 89, 222);
                border-radius: 8px;
                background-color: rgb(14, 17, 31);
                color: white;
            }
            QLineEdit:focus {
                border: 2px solid rgb(100, 120, 255);
            }
        """)
        layout.addWidget(line_edit)
        return container

    def create_button(self, text):
        btn = QtWidgets.QPushButton(text)
        btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(72, 89, 222);
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: rgb(100, 120, 255);
            }
            QPushButton:pressed {
                background-color: rgb(52, 69, 180);
            }
        """)
        return btn

    def set_link_style(self, label):
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setStyleSheet("color: white;")
        label.setOpenExternalLinks(False)

    def retranslateUi(self, AuthWindow):
        AuthWindow.setWindowTitle("NebulaShare - Authentication")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AuthWindow = QtWidgets.QMainWindow()
    ui = Ui_AuthWindow()
    ui.setupUi(AuthWindow)
    AuthWindow.show()
    sys.exit(app.exec_())