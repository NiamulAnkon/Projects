import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from notice_window import Ui_Disclaimer
from main_window import Ui_MainWindow
from setting_window import SettingsWindow
from themes import LIGHT_THEME, DARK_THEME

SETTINGS_FILE = "settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Mental Help AI")

        self.settings = load_settings()
        self.apply_theme(self.settings.get("theme", "Light"))

    def apply_theme(self, theme):
        if theme == "Dark":
            self.setStyleSheet(DARK_THEME)
        else:
            self.setStyleSheet(LIGHT_THEME)
    

class DisclaimerDialog(QDialog, Ui_Disclaimer):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Disclaimer")
        self.agree_btn.clicked.connect(self.accept)
        self.ext_btn.clicked.connect(self.reject)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    settings = load_settings()

    if settings.get("disclaimer_accepted", False):
        window = MainWindow()
        window.show()
    else:
        disclaimer = DisclaimerDialog()
        if disclaimer.exec_() == QDialog.Accepted:
            save_settings({"disclaimer_accepted": True})
            window = MainWindow()
            window.show()
        else:
            sys.exit()

    sys.exit(app.exec_())