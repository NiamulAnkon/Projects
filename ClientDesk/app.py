import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from src.main_window import MainWindow
from src.db import init_db

def main():
    # Initialize Database
    init_db()
    
    app = QApplication(sys.argv)
    app.setApplicationName("ClientDesk")
    app.setWindowIcon(QIcon("assets/logo.ico"))
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()