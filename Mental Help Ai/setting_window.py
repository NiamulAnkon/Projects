from PyQt5.QtWidgets import (
    QDialog, QTabWidget, QVBoxLayout, QWidget,
    QLabel, QComboBox, QSlider, QCheckBox, QPushButton,
    QHBoxLayout, QFormLayout, QMessageBox, QLineEdit, QTextEdit
)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt
from themes import LIGHT_THEME, DARK_THEME
import json
import os

SETTINGS_FILE = "window_setting.json"
CHAT_HISTORY_FILE = "chat_history.json"

def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f)

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {}


def clear_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "w") as f:
            json.dump([], f)

class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumSize(400, 300)

        layout = QVBoxLayout(self)

        # Tabs
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Add tabs
        self.tabs.addTab(self.createAppearanceTab(), "Appearance")
        self.tabs.addTab(self.createVoiceTab(), "Voice")
        self.tabs.addTab(self.createPrivacyTab(), "Privacy & Data")

        # Save & Cancel buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")

        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

        # Close on cancel
        self.cancel_button.clicked.connect(self.close)
        self.save_button.clicked.connect(self.saveSettings)

        # Load saved settings into UI
        self.loadSettingsIntoUI()


    def createAppearanceTab(self):
        tab = QWidget()
        form = QFormLayout()

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark"])
        form.addRow("Theme:", self.theme_combo)

        # Optional: live theme preview
        # self.theme_combo.currentTextChanged.connect(self.changeTheme)

        tab.setLayout(form)
        return tab

    def changeTheme(self, theme):
        if theme == "Light":
            self.setStyleSheet(LIGHT_THEME)
        else:
            self.setStyleSheet(DARK_THEME)

    def createVoiceTab(self):
        tab = QWidget()
        form = QFormLayout()

        self.voice_combo = QComboBox()
        self.voice_combo.addItems(["Male", "Female", "Robotic", "Natural"])
        form.addRow("Voice:", self.voice_combo)

        self.speech_rate = QSlider(Qt.Horizontal)
        self.speech_rate.setMinimum(50)
        self.speech_rate.setMaximum(200)
        self.speech_rate.setValue(100)
        form.addRow("Speech Rate:", self.speech_rate)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(80)
        form.addRow("Volume:", self.volume_slider)

        tab.setLayout(form)
        return tab

    def createPrivacyTab(self):
        tab = QWidget()
        form = QFormLayout()

        self.save_history_check = QCheckBox("Save chat history")
        form.addRow(self.save_history_check)

        self.clear_history_button = QPushButton("Clear conversation history")
        form.addRow(self.clear_history_button)

        tab.setLayout(form)

        # Connect button
        self.clear_history_button.clicked.connect(self.confirm_clear_history)

        return tab

    def saveSettings(self):
        settings = load_settings()
        settings["theme"] = self.theme_combo.currentText()
        settings["voice"] = self.voice_combo.currentText()
        settings["speech_rate"] = self.speech_rate.value()
        settings["volume"] = self.volume_slider.value()
        settings["save_history"] = self.save_history_check.isChecked()

        save_settings(settings)

        # Apply theme immediately to parent window
        if self.parent():
            self.parent().apply_theme(settings["theme"])

        self.close()

    def loadSettingsIntoUI(self):
        """Load saved settings into widgets when opening dialog"""
        settings = load_settings()
        if not settings:
            return

        self.theme_combo.setCurrentText(settings.get("theme", "Light"))
        self.voice_combo.setCurrentText(settings.get("voice", "Male"))
        self.speech_rate.setValue(settings.get("speech_rate", 100))
        self.volume_slider.setValue(settings.get("volume", 80))
        self.save_history_check.setChecked(settings.get("save_history", True))

    def confirm_clear_history(self):
        reply = QMessageBox.question(
            self,
            "Clear Chat History",
            "Are you sure you want to delete all conversation history?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            clear_chat_history()
            QMessageBox.information(self, "Cleared", "Chat history has been cleared.")
