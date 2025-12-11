from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
import sys
import auth_db
from usr_auth_window import Ui_AuthWindow
from main_window import Ui_MainWindow

auth_db.init_db()

class AuthWindow(QtWidgets.QMainWindow, Ui_AuthWindow):
    login_success = pyqtSignal(str)  # emits the username

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def register_user(self, username, email, password, confirm):
        # normalize inputs to avoid accidental whitespace mismatches
        username = username.strip() if isinstance(username, str) else username
        email = email.strip() if isinstance(email, str) else email
        password = password or ""
        confirm = confirm or ""

        if not username or not email or not password or not confirm:
            QtWidgets.QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        if "@" not in email or "." not in email:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Invalid email format.")
            return

        if len(password) < 6:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Password must be at least 6 characters.")
            return

        if password != confirm:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Passwords do not match.")
            return

        success, message = auth_db.register_user(username, email, password)

        if not success:
            QtWidgets.QMessageBox.warning(self, "Registration Failed", message)
        else:
            QtWidgets.QMessageBox.information(self, "Success", message)
            # Emit the signal and let the connected slot open the main window
            self.login_success.emit(username)

    def login_user(self, username, password):
        # normalize inputs
        username = username.strip() if isinstance(username, str) else username
        password = password or ""

        if not username or not password:
            QtWidgets.QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        success, message, user_data = auth_db.login_user(username, password)

        if not success:
            QtWidgets.QMessageBox.warning(self, "Login Failed", message)
        else:
            QtWidgets.QMessageBox.information(self, "Success", message)
            # Emit the signal and let the connected slot open the main window
            self.login_success.emit(username)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # Ensure dialog text is readable on dark theme: make dialog text white
    app.setStyleSheet(
        "QDialog, QMessageBox, QInputDialog, QFileDialog { color: white; }"
    )
    auth_window = AuthWindow()
    def open_main(username):
        # keep a reference so the window isn't garbage-collected
        global main_window_ref
        main_window_ref = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(main_window_ref, username)
        # keep ui alive as well to preserve signal/slot bindings
        global main_ui_ref
        main_ui_ref = ui
        # also attach to the window object for convenience
        main_window_ref._ui = ui
        main_window_ref.show()
        # Close the auth window so the main window is visible and focused
        try:
            auth_window.close()
        except Exception:
            pass

    # Connect login/register success to main window
    auth_window.login_success.connect(open_main)

    auth_window.show()
    sys.exit(app.exec_())