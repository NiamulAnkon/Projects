from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QTimeEdit, QComboBox, QFileDialog, QMessageBox,
)
from PyQt5.QtCore import QTime
import logic


class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Settings")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        # --- Daily Reminder Time ---
        layout.addWidget(QLabel("Daily Reminder Time:"))
        self.reminder_time = QTimeEdit()
        self.reminder_time.setDisplayFormat("HH:mm")
        self.reminder_time.setTime(QTime.currentTime())  # default
        layout.addWidget(self.reminder_time)

        # --- Theme Selection ---
        # layout.addWidget(QLabel("Theme:"))
        # self.theme_box = QComboBox()
        # self.theme_box.addItems(["System Default", "Light", "Dark"])
        # layout.addWidget(self.theme_box)

        # --- Backup Data ---
        self.backup_btn = QPushButton("Backup Data")
        self.backup_btn.clicked.connect(self.backup_data)
        layout.addWidget(self.backup_btn)

        # --- Import Data ---
        self.import_btn = QPushButton("Import Data")
        self.import_btn.clicked.connect(self.import_data)
        layout.addWidget(self.import_btn)

        # --- Wipe Data ---
        self.wipe_btn = QPushButton("Wipe All Data")
        self.wipe_btn.clicked.connect(self.wipe_data)
        layout.addWidget(self.wipe_btn)

        # --- Save ---
        self.save_btn = QPushButton("Save Settings")
        self.save_btn.clicked.connect(self.save_settings)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

        # Add styles
        self.setStyleSheet("""
            QLabel{
                           color: white;
                }
            QPushButton {
                color: white;
            }
            """)

    # ----------------- FUNCTIONS -----------------

    def save_settings(self):
        reminder = self.reminder_time.time().toString("HH:mm")
        theme = self.theme_box.currentText()
        logic.save_settings({
            "reminder_time": reminder,
            "theme": theme
        })
        QMessageBox.information(self, "Saved", "Settings saved successfully!")

    def backup_data(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Backup", "", "JSON Files (*.json)")
        if path:
            logic.backup_data(path)
            QMessageBox.information(self, "Backup", "Backup created successfully!")

    def import_data(self):
        path, _ = QFileDialog.getOpenFileName(self, "Import Data", "", "JSON Files (*.json)")
        if path:
            logic.import_data(path)
            QMessageBox.information(self, "Import", "Data imported successfully!")

    def wipe_data(self):
        confirm = QMessageBox.question(self, "Confirm", "Are you sure you want to wipe all data?")
        if confirm == QMessageBox.Yes:
            logic.wipe_data()
            QMessageBox.information(self, "Wiped", "All data wiped successfully!")
