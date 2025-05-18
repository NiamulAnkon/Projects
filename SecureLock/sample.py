import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QInputDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QMessageBox

class FolderLockerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Folder/File Locker")
        self.setFixedSize(400, 300)

        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        self.btn_lock_file = QPushButton("🔐 Lock File")
        self.btn_lock_folder = QPushButton("🔐 Lock Folder")
        self.btn_unlock = QPushButton("🔓 Unlock File/Folder")

        self.btn_lock_file.clicked.connect(self.lock_file)
        self.btn_lock_folder.clicked.connect(self.lock_folder)
        self.btn_unlock.clicked.connect(self.unlock_item)

        self.layout.addWidget(self.btn_lock_file)
        self.layout.addWidget(self.btn_lock_folder)
        self.layout.addWidget(self.btn_unlock)

        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def lock_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Lock")
        if file_path:
            password, ok = QInputDialog.getText(self, "Set Password", "Enter password:", echo=QInputDialog.Password)
            if ok and password:
                QMessageBox.information(self, "Lock", f"File locked: {file_path}\nPassword: {password}")
                # TODO: Integrate with lock logic

    def lock_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder to Lock")
        if folder_path:
            password, ok = QInputDialog.getText(self, "Set Password", "Enter password:", echo=QInputDialog.Password)
            if ok and password:
                QMessageBox.information(self, "Lock", f"Folder locked: {folder_path}\nPassword: {password}")
                # TODO: Integrate with lock logic

    def unlock_item(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Locked File/Folder")
        if file_path:
            password, ok = QInputDialog.getText(self, "Enter Password", "Enter unlock password:", echo=QInputDialog.Password)
            if ok and password:
                QMessageBox.information(self, "Unlock", f"Trying to unlock: {file_path}\nPassword entered: {password}")
                # TODO: Integrate with unlock logic

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FolderLockerApp()
    window.show()
    sys.exit(app.exec_())
