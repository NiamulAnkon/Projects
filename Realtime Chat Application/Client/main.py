import sys
from PyQt5 import QtWidgets
from auth_ui import AuthUI
from chat_ui import ChatUI
from client_logic import authenticate_user, send_message
from client_logic import signup_user

def handle_signup(self):
    username = self.ui.usr_name.text().strip()
    password = self.ui.password.text().strip()

    if not username or not password:
        self.show_message("Error", "Please fill all fields.", QtWidgets.QMessageBox.Critical)
        return

    response = signup_user(username, password)
    
    if response.get("status") == "success":
        self.show_message("Success", "Signup successful!", QtWidgets.QMessageBox.Information)
    else:
        self.show_message("Signup Failed", response.get("message", "Error occurred"), QtWidgets.QMessageBox.Critical)
class LoginApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = AuthUI()
        self.setCentralWidget(self.ui)

        self.ui.login_btn.clicked.connect(self.handle_login)

    def handle_login(self):
        username = self.ui.username_input.text().strip()
        password = self.ui.password_input.text().strip()

        if not username or not password:
            self.show_message("Error", "Please fill all fields.", QtWidgets.QMessageBox.Critical)
            return

        response = authenticate_user(username, password)
        
        if response.get("status") == "success":
            self.show_message("Success", "Login successful!", QtWidgets.QMessageBox.Information)
            self.open_chat(username)
        else:
            self.show_message("Login Failed", response.get("message", "Invalid credentials"), QtWidgets.QMessageBox.Critical)

    def show_message(self, title, message, icon):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

    def open_chat(self, username):
        self.chat_window = ChatApp(username)
        self.chat_window.show()
        self.close()

class ChatApp(QtWidgets.QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.ui = ChatUI()
        self.setCentralWidget(self.ui)

        self.ui.send_btn.clicked.connect(self.handle_send)

    def handle_send(self):
        message = self.ui.message_input.text().strip()
        if message:
            response = send_message(self.username, message)
            if response.get("status") == "success":
                self.ui.chat_display.append(f"{self.username}: {message}")
                self.ui.message_input.clear()
            else:
                self.ui.chat_display.append("[Error sending message]")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = LoginApp()
    main_window.show()
    sys.exit(app.exec_())
