from PyQt5.QtWidgets import (
    QMainWindow, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget, QAction, QToolBar, QMessageBox, QPushButton
)
from PyQt5.QtCore import Qt
from ticket_dialog import TicketDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ticketing Software")
        self.setGeometry(200, 200, 800, 500)

        # Setup menu
        self.setup_menu()

        # Setup toolbar
        self.setup_toolbar()

        # Ticket Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Title", "Status"])
        self.table.horizontalHeader().setStretchLastSection(True)

        layout = QVBoxLayout()
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def setup_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menubar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def setup_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        add_ticket_btn = QAction("Add Ticket", self)
        add_ticket_btn.triggered.connect(self.add_ticket)
        toolbar.addAction(add_ticket_btn)

        refresh_btn = QAction("Refresh", self)
        refresh_btn.triggered.connect(self.load_tickets)
        toolbar.addAction(refresh_btn)

    def add_ticket(self):
        dialog = TicketDialog(self)
        if dialog.exec_():
            title, description = dialog.get_data()
            # For now, just append to table (DB hookup later)
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(str(row_position + 1)))
            self.table.setItem(row_position, 1, QTableWidgetItem(title))
            self.table.setItem(row_position, 2, QTableWidgetItem("Open"))

    def load_tickets(self):
        QMessageBox.information(self, "Refresh", "This will load tickets from the database")

    def show_about(self):
        QMessageBox.information(self, "About", "Ticketing Software\nBuilt with PyQt5")

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())