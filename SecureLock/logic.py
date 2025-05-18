from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QMessageBox
from PyQt5.QtCore import Qt
from main_window import *
import os
import json
from themes import *
from locker import *

#--------------------------------------------------------------------------------------------------#
class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connect_logic()
    def connect_logic(self):
            self.ui.Lock_file_btn.clicked.connect(self.lock_file)
            self.ui.Lock_folder_btn.clicked.connect(self.lock_folder)
            self.ui.unlock_btn.clicked.connect(self.unlock_file)
            self.ui.unlock_folder_btn.clicked.connect(self.unlock_folder)
            self.ui.themes.currentTextChanged.connect(self.apply_theme)

    def apply_theme(self, name):
        theme = Themes.get(name, "")
        self.ui.centralwidget.setStyleSheet(theme)

    def lock_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select File to Lock")
        if path:
            pwd, ok = QInputDialog.getText(self, "Password", "Set password:", QtWidgets.QLineEdit.Password)
            if ok and pwd:
                try:
                    lock_file(path, pwd)
                    QMessageBox.information(self, "Success", "File locked.")
                except Exception as e:
                    QMessageBox.critical(self, "Error", str(e))

    def lock_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Lock")
        if folder:
            pwd, ok = QInputDialog.getText(self, "Password", "Set password:", QtWidgets.QLineEdit.Password)
            if ok and pwd:
                try:
                    lock_folder(folder, pwd)
                    QMessageBox.information(self, "Success", "Folder locked.")
                except Exception as e:
                    QMessageBox.critical(self, "Error", str(e))

    def unlock_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Locked File", filter="*.locked")
        if path:
            pwd, ok = QInputDialog.getText(self, "Password", "Enter password:", QtWidgets.QLineEdit.Password)
            if ok and pwd:
                try:
                    unlock_file(path, pwd)
                    QMessageBox.information(self, "Success", "File unlocked.")
                except ValueError:
                    QMessageBox.critical(self, "Error", "Incorrect password or corrupted file.")
                except Exception as e:
                    QMessageBox.critical(self, "Error", str(e))

    def unlock_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Locked Folder")
        if folder:
            pwd, ok = QInputDialog.getText(self, "Password", "Enter password:", QtWidgets.QLineEdit.Password)
            if ok and pwd:
                try:
                    unlock_folder(folder, pwd)
                    QMessageBox.information(self, "Success", "Folder unlocked.")
                except ValueError:
                    QMessageBox.critical(self, "Error", "Incorrect password or corrupted folder.")
                except Exception as e:
                    QMessageBox.critical(self, "Error", str(e))
#--------------------------------------------------------------------------------------------------#
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())