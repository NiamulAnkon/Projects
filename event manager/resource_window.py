from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QComboBox, QMessageBox
import logic

class ResourceWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Resource")

        layout = QVBoxLayout(self)

        self.type_box = QComboBox()
        self.type_box.addItems(["link", "text"])

        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText("Enter link or text")

        self.add_btn = QPushButton("Add Resource")
        self.add_btn.clicked.connect(self.save_resource)

        layout.addWidget(QLabel("Resource Type:"))
        layout.addWidget(self.type_box)
        layout.addWidget(QLabel("Resource Value:"))
        layout.addWidget(self.value_input)
        layout.addWidget(self.add_btn)
        self.setStyleSheet("""
            QLabel{
                 color: white;
            }
            QPushButton {
                color: white;
            }
            QLineEdit, QComboBox {
                color: white;
            }
        """)

    def save_resource(self):
        resource_type = self.type_box.currentText()
        value = self.value_input.text().strip()
        if value:
            logic.add_resource(resource_type, value)
            self.accept()  # close dialog after saving

def confirm_resource_delete(parent, resource):
    reply = QMessageBox.question(
        parent,
        "Delete Resource",
        f"Are you sure you want to delete 'it'?",
        QMessageBox.Yes | QMessageBox.No
    )
    if reply == QMessageBox.Yes:
        return True
    return False