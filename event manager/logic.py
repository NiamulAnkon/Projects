from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QFileDialog,
    QTimeEdit, QComboBox, QMessageBox
)
from PyQt5.QtCore import QTime, pyqtSignal
import json
import os
import uuid
from datetime import date


DATA_DIR = "data"
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")
EVENTS_FILE = os.path.join(DATA_DIR, "events.json")
RESOURCE_FILE = os.path.join(DATA_DIR, "resources.json")

os.makedirs(DATA_DIR, exist_ok=True)


def save_settings(settings):
    os.makedirs("data", exist_ok=True)
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {"reminder_time": "08:00", "theme": "System Default"}


def backup_data(path):
    if os.path.exists(EVENTS_FILE):
        with open(EVENTS_FILE, "r") as f:
            data = json.load(f)
        with open(path, "w") as f:
            json.dump(data, f, indent=4)


def import_data(path):
    with open(path, "r") as f:
        data = json.load(f)
    with open(EVENTS_FILE, "w") as f:
        json.dump(data, f, indent=4)


def wipe_data():
    if os.path.exists(EVENTS_FILE):
        os.remove(EVENTS_FILE)

#------------------------ Show today's events -----------------------#
def get_todays_events(events):
    today = date.today().isoformat()
    todays_event = [event for event in events if event["date"] == today]
    return todays_event


#------------------------Resource data handling-----------------------#

def load_resources():
    if os.path.exists(RESOURCE_FILE):
        with open(RESOURCE_FILE, "r") as f:
            return json.load(f)
    return []

def save_resources(resources):
    with open(RESOURCE_FILE, "w") as f:
        json.dump(resources, f, indent=4)

def add_resource(resource_type, value):
    resources = load_resources()
    resources.append({
        "type": resource_type,  # "link" or "text"
        "value": value
    })
    save_resources(resources)

def remove_resource(index):
    resources = load_resources()
    if 0 <= index < len(resources):
        resources.pop(index)
        save_resources(resources)
def edit_resource(index, resource_type=None, value=None):
    resources = load_resources()
    if 0 <= index < len(resources):
        if resource_type:
            resources[index]["type"] = resource_type
        if value:
            resources[index]["value"] = value
        save_resources(resources)

# --------------------- Event Data Handling --------------------- #
def load_events():
    if not os.path.exists(EVENTS_FILE):
        with open(EVENTS_FILE, "w") as f:
            json.dump([], f)

    # If file is empty or broken, reset it to []
    try:
        with open(EVENTS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        with open(EVENTS_FILE, "w") as f:
            json.dump([], f)
        return []
    
def save_events(events):
    with open(EVENTS_FILE, "w") as f:
        json.dump(events, f, indent=4)


def add_event(title, date, time, description=""):
    events = load_events()
    new_event = {
        "id": str(uuid.uuid4()),
        "title": title,
        "date": date,
        "time": time,
        "description": description
    }
    events.append(new_event)
    save_events(events)
    return new_event


def edit_event(event_id, title=None, date=None, time=None, description=None):
    events = load_events()
    for event in events:
        if event["id"] == event_id:
            if title:
                event["title"] = title
            if date:
                event["date"] = date
            if time:
                event["time"] = time
            if description:
                event["description"] = description
            save_events(events)
            return event
    return None


def delete_event(event_id):
    events = load_events()
    updated_events = [event for event in events if event["id"] != event_id]
    save_events(updated_events)
    return len(events) != len(updated_events)


# --------------------- Settings Window --------------------- #
class SettingsWindow(QDialog):
    theme_changed = pyqtSignal(str)   # emit when theme changes

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        # Daily Reminder
        layout.addWidget(QLabel("Daily Reminder Time:"))
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setTime(QTime.currentTime())
        layout.addWidget(self.time_edit)

        # Backup Button
        self.backup_btn = QPushButton("Backup Data")
        self.backup_btn.clicked.connect(self.backup_data)
        layout.addWidget(self.backup_btn)

        # Import Button
        self.import_btn = QPushButton("Import Data")
        self.import_btn.clicked.connect(self.import_data)
        layout.addWidget(self.import_btn)

        # Wipe Button
        self.wipe_btn = QPushButton("Wipe All Data")
        self.wipe_btn.clicked.connect(self.wipe_data)
        layout.addWidget(self.wipe_btn)

        # Themes
        layout.addWidget(QLabel("Theme:"))
        self.theme_box = QComboBox()
        self.theme_box.addItems(["Light", "Dark", "System Default"])
        self.theme_box.currentIndexChanged.connect(self.change_theme)
        layout.addWidget(self.theme_box)

        self.setLayout(layout)

    # Backup function
    def backup_data(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Backup Data", "", "JSON Files (*.json)")
        if file_path:
            with open(EVENTS_FILE, "r") as f:
                data = json.load(f)
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)
            QMessageBox.information(self, "Success", "Backup completed!")

    # Import function
    def import_data(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Import Data", "", "JSON Files (*.json)")
        if file_path:
            with open(file_path, "r") as f:
                data = json.load(f)
            with open(EVENTS_FILE, "w") as f:
                json.dump(data, f, indent=4)
            QMessageBox.information(self, "Success", "Data imported successfully!")

    # Wipe data function
    def wipe_data(self):
        reply = QMessageBox.question(
            self, "Confirm", "Are you sure you want to delete all events?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            with open(EVENTS_FILE, "w") as f:
                json.dump([], f)
            QMessageBox.information(self, "Wiped", "All data has been cleared.")

    # Theme change
    def change_theme(self, index):
        theme = self.theme_box.currentText()
        self.theme_changed.emit(theme)   # emit signal instead of directly styling
        QMessageBox.information(self, "Theme Changed", f"Theme changed to {theme}.")
    
        # Themes dictionary
    themes = {
        "dark": """
            QWidget {
                background-color: #2b2b2b;
                color: white;
                font-size: 14px;
            }
            QPushButton {
                background-color: #3c3f41;
                border-radius: 6px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #505354;
            }
            QLineEdit, QTextEdit {
                background-color: #3c3f41;
                border: 1px solid #5c5f61;
                border-radius: 4px;
                padding: 4px;
            }
            QListWidget {
                background-color: #2b2b2b;
                border: 1px solid #5c5f61;
            }
        """,

        "light": """
            QWidget {
                background-color: #f0f0f0;
                color: black;
                font-size: 14px;
            }
            QPushButton {
                background-color: #e0e0e0;
                border-radius: 6px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #c0c0c0;
            }
            QLineEdit, QTextEdit {
                background-color: #ffffff;
                border: 1px solid #a0a0a0;
                border-radius: 4px;
                padding: 4px;
            }
            QListWidget {
                background-color: #ffffff;
                border: 1px solid #a0a0a0;
            }
        """
    }

    # Apply theme
def apply_theme(self, theme_name):
    pass
    # if theme_name == "Light":
#         self.parent().setStyleSheet(self)
#     elif theme_name == "Dark":
#         self.parent().setStyleSheet(self.themes["dark"])