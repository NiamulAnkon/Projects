from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QHBoxLayout

class TicketDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Ticket")
        self.setFixedSize(400, 250)

        layout = QVBoxLayout()

        # Title
        self.title_input = QLineEdit()
        layout.addWidget(QLabel("Title:"))
        layout.addWidget(self.title_input)

        # Description
        self.description_input = QTextEdit()
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.description_input)

        # Buttons
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def get_data(self):
        return self.title_input.text(), self.description_input.toPlainText()
