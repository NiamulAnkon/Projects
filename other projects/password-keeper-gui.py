from PyQt5 import QtWidgets, QtGui, QtCore
from cryptography.fernet import *
import sqlite3
import sys

def load_key():
    try:
        with open("key.key", "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        print("Encryption key file not found! Generate one and save it as 'key.key'.")
        exit()

key = load_key()
cipher = Fernet(key)

def initialize_db():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_name TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

class PasswordKeeper(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Keeper")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #E8F6F3;")

        # Main UI elements
        self.header = QtWidgets.QLabel("Password Keeper", self)
        self.header.setGeometry(150, 20, 300, 50)
        self.header.setFont(QtGui.QFont("Arial", 18, QtGui.QFont.Bold))
        self.header.setAlignment(QtCore.Qt.AlignCenter)

        self.account_label = QtWidgets.QLabel("Account Name:", self)
        self.account_label.setGeometry(50, 100, 120, 30)
        self.account_input = QtWidgets.QLineEdit(self)
        self.account_input.setGeometry(180, 100, 350, 30)

        self.username_label = QtWidgets.QLabel("Username:", self)
        self.username_label.setGeometry(50, 150, 120, 30)
        self.username_input = QtWidgets.QLineEdit(self)
        self.username_input.setGeometry(180, 150, 350, 30)

        self.password_label = QtWidgets.QLabel("Password:", self)
        self.password_label.setGeometry(50, 200, 120, 30)
        self.password_input = QtWidgets.QLineEdit(self)
        self.password_input.setGeometry(180, 200, 350, 30)

        self.add_button = QtWidgets.QPushButton("Add Password", self)
        self.add_button.setGeometry(50, 250, 200, 40)
        self.add_button.setStyleSheet("background-color: #A3E4D7;")
        self.add_button.clicked.connect(self.add_password)

        self.retrieve_button = QtWidgets.QPushButton("Retrieve Password", self)
        self.retrieve_button.setGeometry(300, 250, 230, 40)
        self.retrieve_button.setStyleSheet("background-color: #A3E4D7;")
        self.retrieve_button.clicked.connect(self.retrieve_password)

        self.result_area = QtWidgets.QTextBrowser(self)
        self.result_area.setGeometry(50, 310, 500, 70)

    def add_password(self):
        account_name = self.account_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not account_name or not username or not password:
            self.result_area.setText("All fields are required!")
            return

        encrypted_password = cipher.encrypt(password.encode()).decode()
        conn = sqlite3.connect("passwords.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO passwords (account_name, username, password) VALUES (?, ?, ?)",
                       (account_name, username, encrypted_password))
        conn.commit()
        conn.close()

        self.result_area.setText(f"Password for '{account_name}' added successfully!")
        self.account_input.clear()
        self.username_input.clear()
        self.password_input.clear()

    def retrieve_password(self):
        account_name = self.account_input.text().strip()

        if not account_name:
            self.result_area.setText("Please enter the account name!")
            return

        conn = sqlite3.connect("passwords.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username, password FROM passwords WHERE account_name=?", (account_name,))
        result = cursor.fetchone()
        conn.close()

        if result:
            username, encrypted_password = result
            decrypted_password = cipher.decrypt(encrypted_password.encode()).decode()
            self.result_area.setText(f"Account: {account_name}\nUsername: {username}\nPassword: {decrypted_password}")
        else:
            self.result_area.setText(f"No password found for account '{account_name}'.")

if __name__ == "__main__":
    initialize_db()
    app = QtWidgets.QApplication(sys.argv)
    window = PasswordKeeper()
    window.show()
    sys.exit(app.exec_())
