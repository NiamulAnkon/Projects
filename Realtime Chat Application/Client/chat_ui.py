from PyQt5 import QtCore, QtGui, QtWidgets

class ChatUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat")
        self.setGeometry(100, 100, 500, 400)
        self.setStyleSheet("background-color: white;")

        layout = QtWidgets.QVBoxLayout()

        self.chat_display = QtWidgets.QTextEdit(self)
        self.chat_display.setReadOnly(True)
        
        self.message_input = QtWidgets.QLineEdit(self)
        self.message_input.setPlaceholderText("Type a message...")

        self.send_btn = QtWidgets.QPushButton("Send")

        layout.addWidget(self.chat_display)
        layout.addWidget(self.message_input)
        layout.addWidget(self.send_btn)
        
        self.setLayout(layout)
