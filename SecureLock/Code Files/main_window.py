from PyQt5 import QtCore, QtGui, QtWidgets
from themes import * 
from locker import *
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QMessageBox
from PyQt5.QtCore import Qt

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: rgb(243, 244, 246);")
        MainWindow.setWindowTitle("SecureLock")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        self.header = QtWidgets.QLabel("SecureLock")
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(18)
        font.setBold(True)
        self.header.setFont(font)
        self.header.setStyleSheet("background-color: rgb(31, 41, 55); color: #FFFFFF; padding: 20px;")
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        self.main_layout.addWidget(self.header)

        self.buttons_layout = QtWidgets.QVBoxLayout()
        self.buttons_layout.setSpacing(20)

        self.Lock_file_btn = QtWidgets.QPushButton("🔐 Lock File")
        self.Lock_file_btn.setFont(QtGui.QFont("", 16, QtGui.QFont.Bold))
        self.Lock_file_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Lock_file_btn.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                padding: 15px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
        """)
        self.buttons_layout.addWidget(self.Lock_file_btn)

        self.Lock_folder_btn = QtWidgets.QPushButton("🔐 Lock Folder")
        self.Lock_folder_btn.setFont(QtGui.QFont("", 16, QtGui.QFont.Bold))
        self.Lock_folder_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Lock_folder_btn.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                padding: 15px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
        """)
        self.buttons_layout.addWidget(self.Lock_folder_btn)

        self.unlock_btn = QtWidgets.QPushButton("🔓 Unlock File")
        self.unlock_btn.setFont(QtGui.QFont("", 16, QtGui.QFont.Bold))
        self.unlock_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.unlock_btn.setStyleSheet("""
            QPushButton {
                background-color: #10B981;
                color: white;
                padding: 15px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        self.buttons_layout.addWidget(self.unlock_btn)

        self.unlock_folder_btn = QtWidgets.QPushButton("🔓 Unlock Folder")
        self.unlock_folder_btn.setFont(QtGui.QFont("", 16, QtGui.QFont.Bold))
        self.unlock_folder_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.unlock_folder_btn.setStyleSheet("""
            QPushButton {
                background-color: #10B981;
                color: white;
                padding: 15px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        self.buttons_layout.addWidget(self.unlock_folder_btn)

        self.main_layout.addLayout(self.buttons_layout)
        self.main_layout.addStretch()

        self.theme_layout = QtWidgets.QHBoxLayout()
        self.theme_layout.addStretch()

        self.theme_label = QtWidgets.QLabel("Themes")
        self.theme_layout.addWidget(self.theme_label)

        self.themes = QtWidgets.QComboBox()
        self.themes.addItems([
            "Default", "Shadow Night", "Crystal Sky", "Midnight Vault",
            "Mint Steel", "Desert Copper", "Ocean Guard", "Neon Lock"
        ])
        self.themes.setFixedWidth(160)
        # self.themes.currentTextChanged.connect(self.apply_theme)
        self.theme_layout.addWidget(self.themes)

        self.main_layout.addLayout(self.theme_layout)

        MainWindow.setCentralWidget(self.centralwidget)
        # self.connect_functions()
    
    # def connect_functions(self):
    #     self.Lock_file_btn.clicked.connect(self.lock_file)
    #     self.Lock_folder_btn.clicked.connect(self.lock_folder)
    #     self.unlock_btn.clicked.connect(self.unlock_file)
    #     self.unlock_folder_btn.clicked.connect(self.unlock_folder)
    # def apply_theme(self, name):
    #     theme = Themes.get(name, "")
    #     self.centralwidget.setStyleSheet(theme)
    # def lock_file(self):
    #     path, _ = QFileDialog.getOpenFileName(None, "Select File to Lock")
    #     if path:
    #         pwd, ok = QInputDialog.getText(None, "Set Password", "Enter password to lock file:", QtWidgets.QLineEdit.Password)
    #         if ok and pwd:
    #             confirm_pwd, ok2 = QInputDialog.getText(None, "Confirm Password", "Re-enter password:", QtWidgets.QLineEdit.Password)
    #             if ok2 and confirm_pwd == pwd:
    #                 try:
    #                     lock_file(path, pwd)
    #                     QMessageBox.information(None, "Success", "File locked successfully.")
    #                 except Exception as e:
    #                     QMessageBox.critical(None, "Error", str(e))
    #             else:
    #                 QMessageBox.warning(None, "Mismatch", "Passwords do not match.")

    # def lock_folder(self):
    #     folder = QFileDialog.getExistingDirectory(None, "Select Folder to Lock")
    #     if folder:
    #         pwd, ok = QInputDialog.getText(None, "Set Password", "Enter password to lock folder:", QtWidgets.QLineEdit.Password)
    #         if ok and pwd:
    #             confirm_pwd, ok2 = QInputDialog.getText(None, "Confirm Password", "Re-enter password:", QtWidgets.QLineEdit.Password)
    #             if ok2 and confirm_pwd == pwd:
    #                 try:
    #                     lock_folder(folder, pwd)
    #                     QMessageBox.information(None, "Success", "Folder locked successfully.")
    #                 except Exception as e:
    #                     QMessageBox.critical(None, "Error", str(e))
    #             else:
    #                 QMessageBox.warning(None, "Mismatch", "Passwords do not match.")

    # def unlock_file(self):
    #     path, _ = QFileDialog.getOpenFileName(None, "Select Locked File", filter="*.locked")
    #     if path:
    #         pwd, ok = QInputDialog.getText(None, "Enter Password", "Password to unlock file:", QtWidgets.QLineEdit.Password)
    #         if ok and pwd:
    #             try:
    #                 unlock_file(path, pwd)
    #                 QMessageBox.information(None, "Success", "File unlocked successfully.")
    #             except ValueError:
    #                 QMessageBox.critical(None, "Error", "Incorrect password or corrupted file.")
    #             except Exception as e:
    #                 QMessageBox.critical(None, "Error", str(e))
    # def unlock_folder(self):
    #     folder = QFileDialog.getExistingDirectory(None, "Select Locked Folder")
    #     if folder:
    #         pwd, ok = QInputDialog.getText(None, "Enter Password", "Password to unlock folder:", QtWidgets.QLineEdit.Password)
    #         if ok and pwd:
    #             try:
    #                 unlock_folder(folder, pwd)
    #                 QMessageBox.information(None, "Success", "Folder unlocked successfully.")
    #             except ValueError:
    #                 QMessageBox.critical(None, "Error", "Incorrect password or corrupted lock metadata.")
    #             except Exception as e:
    #                 QMessageBox.critical(None, "Error", str(e))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
