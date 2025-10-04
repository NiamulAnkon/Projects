from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit,
    QDateEdit, QTimeEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import QDate, QTime
import logic


class AddEventDialog(QDialog):
    def __init__(self, parent=None, event=None):
        super().__init__(parent)
        self.setWindowTitle("Add Event" if event is None else "Edit Event")
        self.setFixedSize(400, 350)

        self.event = event  # if provided, we're editing
        layout = QVBoxLayout()

        # Title
        layout.addWidget(QLabel("Title:"))
        self.title_input = QLineEdit()
        if event:
            self.title_input.setText(event.get("title", ""))
        layout.addWidget(self.title_input)

        # Date
        layout.addWidget(QLabel("Date:"))
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        if event:
            self.date_input.setDate(QDate.fromString(event.get("date", ""), "yyyy-MM-dd"))
        layout.addWidget(self.date_input)

        # Time
        layout.addWidget(QLabel("Time:"))
        self.time_input = QTimeEdit()
        self.time_input.setDisplayFormat("HH:mm")
        self.time_input.setTime(QTime.currentTime())
        if event:
            self.time_input.setTime(QTime.fromString(event.get("time", ""), "HH:mm"))
        layout.addWidget(self.time_input)

        # Description
        layout.addWidget(QLabel("Description:"))
        self.desc_input = QTextEdit()
        if event:
            self.desc_input.setText(event.get("description", ""))
        layout.addWidget(self.desc_input)

        # Save Button
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_event)
        layout.addWidget(save_btn)

        self.setStyleSheet("""
            QLabel{
                 color: white;
            }
            QPushButton {
                color: white;
            }
            QLineEdit, QTextEdit, QDateEdist, QTimeEdit {
                color: white;
            }
        """)

        self.setLayout(layout)

    def save_event(self):
        title = self.title_input.text().strip()
        date = self.date_input.date().toString("yyyy-MM-dd")
        time = self.time_input.time().toString("HH:mm")
        desc = self.desc_input.toPlainText().strip()

        if not title:
            QMessageBox.warning(self, "Error", "Title is required!")
            return

        if self.event:  # Editing
            logic.edit_event(self.event["id"], title, date, time, desc)
        else:  # Adding
            logic.add_event(title, date, time, desc)

        QMessageBox.information(self, "Success", "Event saved!")
        self.accept()


# ---- Delete confirmation ----
def confirm_delete(parent, event):
    reply = QMessageBox.question(
        parent,
        "Delete Event",
        f"Are you sure you want to delete 'it'?",
        QMessageBox.Yes | QMessageBox.No
    )
    if reply == QMessageBox.Yes:
        logic.delete_event(event["id"])
        QMessageBox.information(parent, "Deleted", "Event deleted successfully!")
        return True
    return False
