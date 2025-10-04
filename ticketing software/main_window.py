from PyQt5 import QtCore, QtGui, QtWidgets
from db import get_connection, init_db, add_ticket, delete_ticket, get_all_tickets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        init_db()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 600)
        MainWindow.setStyleSheet("""
            QMainWindow {
                background-color: rgb(17, 35, 51);
                color: white;
            }
            QTableWidget {
                background-color: rgb(25, 45, 65);
                gridline-color: gray;
                color: white;
                alternate-background-color: rgb(30, 60, 90);
            }
            QPushButton {
                background-color: rgb(40, 80, 120);
                border-radius: 6px;
                padding: 8px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgb(60, 100, 140);
            }
        """)

        # --- Central Widget ---
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Main layout
        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)

        # --- Ticket Table ---
        self.ticket_table = QtWidgets.QTableWidget()
        self.ticket_table.setObjectName("ticket_table")
        self.ticket_table.setColumnCount(3)
        self.ticket_table.setRowCount(0)
        self.ticket_table.setAlternatingRowColors(True)
        self.ticket_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.ticket_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.ticket_table.horizontalHeader().setStretchLastSection(True)
        self.ticket_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        item = QtWidgets.QTableWidgetItem()
        self.ticket_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.ticket_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.ticket_table.setHorizontalHeaderItem(2, item)

        self.main_layout.addWidget(self.ticket_table)

        # --- Button Layout ---
        self.button_layout = QtWidgets.QHBoxLayout()
        # Add Ticket Button
        self.add_ticket_btn = QtWidgets.QPushButton("Add Ticket")
        self.add_ticket_btn.clicked.connect(self.add_ticket)
        # Delete Ticket Button
        self.dlt_btn = QtWidgets.QPushButton("Delete Ticket")
        self.dlt_btn.clicked.connect(self.delete_ticket)

        # Add spacer between buttons
        self.button_layout.addWidget(self.add_ticket_btn)
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.dlt_btn)

        self.main_layout.addLayout(self.button_layout)

        MainWindow.setCentralWidget(self.centralwidget)

        # Load initial tickets
        self.load_tickets()

        # --- Menu Bar ---
        self.setup_menu()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    

    def setup_menu(self):
        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        file_menu = self.menubar.addMenu("File")
        exit_action = QtWidgets.QAction("Exit", self.menubar)
        exit_action.triggered.connect(QtWidgets.qApp.quit)
        file_menu.addAction(exit_action)

        help_menu = self.menubar.addMenu("Help")
        about_action = QtWidgets.QAction("About", self.menubar)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def show_about(self):
        QtWidgets.QMessageBox.information(None, "About", "What You Need Help For It's Not Rocket Science!\n You can see it how easy it is to use -_- \n Stoooooooobid")
    

    def TicketDialog(self):
        from ticket_dialog import TicketDialog
        return TicketDialog()

    def add_ticket(self):
        dialog =  self.TicketDialog()
        if dialog.exec_():
            tittle, description = dialog.get_data()
            if tittle.strip():
                conn = get_connection("tickets.db")
                add_ticket(conn, tittle, description)
                self.load_tickets()
                self.load_tickets()
    def load_tickets(self):
        conn = get_connection("tickets.db")
        tickets = get_all_tickets(conn)
        self.ticket_table.setRowCount(0)
        for row_data in tickets:
            row_number = self.ticket_table.rowCount()
            self.ticket_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(data))
                self.ticket_table.setItem(row_number, column_number, item)
    def delete_ticket(self):
        selected_items = self.ticket_table.selectedItems()
        if selected_items:
            ticket_id = int(selected_items[0].text())
            conn = get_connection("tickets.db")
            delete_ticket(conn, ticket_id)
            self.load_tickets()
    

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Ticketing Software"))
        item = self.ticket_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID"))
        item = self.ticket_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Title"))
        item = self.ticket_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Status"))
        item = self.add_ticket_btn
        item.setText(_translate("MainWindow", "Add Ticket"))
        item = self.dlt_btn
        item.setText(_translate("MainWindow", "Delete Ticket"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())