from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from main_window import *
import os
import json
from themes import *
from locker import *

#--------------------------------------------------------------------------------------------------#
# Worker class for folder locking
class FolderWorker(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, path, password, mode):
        super().__init__()
        self.path = path
        self.password = password
        self.mode = mode  # 'lock' or 'unlock'

    def run(self):
        try:
            if self.mode == 'lock':
                lock_folder(self.path, self.password)
            elif self.mode == 'unlock':
                unlock_folder(self.path, self.password)
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))
#--------------------------------------------------------------------------------------------------#
# Main application class
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
                self.run_folder_worker(folder, pwd, mode="lock")


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
                self.run_folder_worker(folder, pwd, mode="unlock")
    def run_folder_worker(self, path, password, mode):
        self.thread = QThread()
        self.worker = FolderWorker(path, password, mode)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.worker.error.connect(lambda e: QMessageBox.critical(self, "Error", e))
        self.worker.finished.connect(lambda: QMessageBox.information(self, "Success", f"Folder {mode}ed successfully."))

        self.thread.start()

#--------------------------------------------------------------------------------------------------#
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())