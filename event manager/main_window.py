from PyQt5 import QtCore, QtGui, QtWidgets
import source_rc  

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(780, 669)
        MainWindow.setStyleSheet("background-color: rgb(38, 43, 50);")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        main_layout = QtWidgets.QHBoxLayout(self.centralwidget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)

        left_layout = QtWidgets.QVBoxLayout()

        self.calendar = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendar.setObjectName("calendar")
        self.calendar.setStyleSheet("""
            QCalendarWidget QWidget {
                alternate-background-color: rgb(38, 43, 50);
                background-color: rgb(38, 43, 50);
                color: white;
            }
            QCalendarWidget QAbstractItemView:enabled {
                color: white;
                selection-background-color: #0078d7;
                selection-color: white;
                background-color: rgb(38, 43, 50);
            }
            QCalendarWidget QTableView#qt_calendar_calendarview QHeaderView::section {
                background-color: rgb(38, 43, 50);
                color: white;
                font-weight: 600;
                padding: 4px;
                border: none;
            }
        """)
        left_layout.addWidget(self.calendar)

        self.todays_event_label = QtWidgets.QLabel("Today's event:", self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.todays_event_label.setFont(font)
        self.todays_event_label.setStyleSheet("""
            color: white;
""")
        left_layout.addWidget(self.todays_event_label)

        self.todays_event = QtWidgets.QTextEdit(self.centralwidget)
        self.todays_event.setReadOnly(True)
        self.todays_event.setStyleSheet("""
            color: white;
        """)
        left_layout.addWidget(self.todays_event)

        main_layout.addLayout(left_layout, 1) 

        middle_layout = QtWidgets.QVBoxLayout()

        top_events_layout = QtWidgets.QHBoxLayout()
        self.event_label = QtWidgets.QLabel("Events:", self.centralwidget)
        self.event_label.setFont(font)
        self.event_label.setStyleSheet("color: white;")
        top_events_layout.addWidget(self.event_label)

        self.add_event_btn = QtWidgets.QPushButton(self.centralwidget)
        self.add_event_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.add_event_btn.setStyleSheet("background: #262b32; border: none;")
        self.add_event_btn.setIcon(QtGui.QIcon(":/newPrefix/plus.png"))
        self.add_event_btn.setIconSize(QtCore.QSize(30, 30))
        top_events_layout.addWidget(self.add_event_btn)
        middle_layout.addLayout(top_events_layout)

        self.event_list = QtWidgets.QListWidget(self.centralwidget)
        self.event_list.setStyleSheet("""
            color: white;
    """)
        middle_layout.addWidget(self.event_list)


        bottom_events_layout = QtWidgets.QHBoxLayout()
        self.edit_event_btn = QtWidgets.QPushButton("Edit", self.centralwidget)
        self.edit_event_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.edit_event_btn.setStyleSheet(
            "color: white; background-color: rgb(54, 57, 67); border: 1px solid rgb(54, 57, 67); border-radius: 10px;"
        )
        bottom_events_layout.addWidget(self.edit_event_btn)

        self.dlt_event_btn = QtWidgets.QPushButton("Delete", self.centralwidget)
        self.dlt_event_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.dlt_event_btn.setStyleSheet(
            "color: white; background-color: rgb(54, 57, 67); border: 1px solid rgb(54, 57, 67); border-radius: 10px;"
        )
        bottom_events_layout.addWidget(self.dlt_event_btn)

        middle_layout.addLayout(bottom_events_layout)
        main_layout.addLayout(middle_layout, 1)

        # ---- Right: Resources ----
        right_layout = QtWidgets.QVBoxLayout()

        top_res_layout = QtWidgets.QHBoxLayout()
        self.resource_label = QtWidgets.QLabel("Resources:", self.centralwidget)
        self.resource_label.setFont(font)
        self.resource_label.setStyleSheet("color: white;")
        top_res_layout.addWidget(self.resource_label)

        self.add_resource_btn = QtWidgets.QPushButton(self.centralwidget)
        self.add_resource_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.add_resource_btn.setStyleSheet("background: #262b32; border: none;")
        self.add_resource_btn.setIcon(QtGui.QIcon(":/newPrefix/plus.png"))
        self.add_resource_btn.setIconSize(QtCore.QSize(30, 30))
        top_res_layout.addWidget(self.add_resource_btn)
        right_layout.addLayout(top_res_layout)

        self.resource = QtWidgets.QListWidget(self.centralwidget)
        self.resource.setStyleSheet("""
            color: white;
""")
        right_layout.addWidget(self.resource)

        bottom_res_layout = QtWidgets.QHBoxLayout()
        self.edit_resource_btn = QtWidgets.QPushButton("Edit", self.centralwidget)
        self.edit_resource_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.edit_resource_btn.setStyleSheet(
            "color: white; background-color: rgb(54, 57, 67); border: 1px solid rgb(54, 57, 67); border-radius: 10px;"
        )
        bottom_res_layout.addWidget(self.edit_resource_btn)

        self.dlt_resource_btn = QtWidgets.QPushButton("Delete", self.centralwidget)
        self.dlt_resource_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.dlt_resource_btn.setStyleSheet(
            "color: white; background-color: rgb(54, 57, 67); border: 1px solid rgb(54, 57, 67); border-radius: 10px;"
        )
        bottom_res_layout.addWidget(self.dlt_resource_btn)

        right_layout.addLayout(bottom_res_layout)
        main_layout.addLayout(right_layout, 1)

        # ---- Bottom line + Settings button ----
        bottom_layout = QtWidgets.QHBoxLayout()
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        bottom_layout.addWidget(self.line)

        self.setting_btn = QtWidgets.QPushButton(self.centralwidget)
        self.setting_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setting_btn.setStyleSheet("border: none;")
        self.setting_btn.setIcon(QtGui.QIcon(":/newPrefix/settings.png"))
        self.setting_btn.setIconSize(QtCore.QSize(30, 30))
        bottom_layout.addWidget(self.setting_btn)

        # Place bottom bar under everything
        outer_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        outer_layout.addLayout(main_layout)
        outer_layout.addLayout(bottom_layout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Event Manager"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
