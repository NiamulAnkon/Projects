import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from notice_window import Ui_Disclaimer
from main_window import Ui_MainWindow

SETTINGS_FILE = "settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f)

# Wrapper for your main window
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

# Wrapper for your disclaimer window as a QDialog
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