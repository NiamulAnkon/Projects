from PyQt5 import QtCore, QtGui, QtWidgets
import icons_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(950, 600)
        MainWindow.setStyleSheet("background-color: rgb(30, 30, 47);")

        # Central widget + Main layout
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.central_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.central_layout.setContentsMargins(10, 10, 10, 10)
        self.central_layout.setSpacing(10)

        # ===== HEADER =====
        self.header_frame = QtWidgets.QFrame(self.centralwidget)
        self.header_frame.setStyleSheet("background-color: rgb(23, 28, 45); border-radius: 8px;")
        self.header_layout = QtWidgets.QHBoxLayout(self.header_frame)
        self.header_layout.setContentsMargins(15, 5, 15, 5)

        self.name_text = QtWidgets.QLabel("📁 NebulaShare", self.header_frame)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.name_text.setFont(font)
        self.name_text.setStyleSheet("color: white;")
        self.header_layout.addWidget(self.name_text, alignment=QtCore.Qt.AlignLeft)

        self.header_layout.addStretch()

        self.usr_name = QtWidgets.QLabel("USER", self.header_frame)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.usr_name.setFont(font)
        self.usr_name.setStyleSheet("color: white; margin-right: 10px;")
        self.header_layout.addWidget(self.usr_name)

        self.usr_icon = QtWidgets.QPushButton(self.header_frame)
        self.usr_icon.setStyleSheet("background: none; border: none;")
        icon4 = QtGui.QIcon(":/icons/icons/icons8-user-100.png")
        self.usr_icon.setIcon(icon4)
        self.usr_icon.setIconSize(QtCore.QSize(40, 40))
        self.header_layout.addWidget(self.usr_icon)

        self.central_layout.addWidget(self.header_frame)

        # ===== CONTENT AREA =====
        self.content_layout = QtWidgets.QHBoxLayout()
        self.central_layout.addLayout(self.content_layout)

        # Sidebar
        self.side_bar_frame = QtWidgets.QFrame(self.centralwidget)
        self.side_bar_frame.setStyleSheet("""
            background-color: rgb(14, 17, 31);
            border-radius: 10px;
        """)
        self.sidebar_layout = QtWidgets.QVBoxLayout(self.side_bar_frame)
        self.sidebar_layout.setContentsMargins(10, 20, 10, 20)
        self.sidebar_layout.setSpacing(20)

        button_style = """
            QPushButton {
                background-color: transparent;
                color: white;
                font-weight: bold;
                border-radius: 6px;
                padding: 8px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: rgb(72, 89, 222);
                color: white;
            }
            QPushButton:pressed {
                background-color: rgb(52, 69, 180);
            }
        """

        self.my_file_btn = QtWidgets.QPushButton("  My Files", self.side_bar_frame)
        self.my_file_btn.setStyleSheet(button_style)
        self.my_file_btn.setIcon(QtGui.QIcon(":/icons/icons/icons8-folder-100.png"))
        self.my_file_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.sidebar_layout.addWidget(self.my_file_btn)

        self.share_with_me_btn = QtWidgets.QPushButton("  Shared With Me", self.side_bar_frame)
        self.share_with_me_btn.setStyleSheet(button_style)
        self.share_with_me_btn.setIcon(QtGui.QIcon(":/icons/icons/icons8-share-60.png"))
        self.share_with_me_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.sidebar_layout.addWidget(self.share_with_me_btn)

        self.trash_btn = QtWidgets.QPushButton("  Trash", self.side_bar_frame)
        self.trash_btn.setStyleSheet(button_style)
        self.trash_btn.setIcon(QtGui.QIcon(":/icons/icons/icons8-trash-128.png"))
        self.trash_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.sidebar_layout.addWidget(self.trash_btn)

        self.settings_btn = QtWidgets.QPushButton("  Settings", self.side_bar_frame)
        self.settings_btn.setStyleSheet(button_style)
        self.settings_btn.setIcon(QtGui.QIcon(":/icons/icons/icons8-setting-100.png"))
        self.settings_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.sidebar_layout.addWidget(self.settings_btn)

        self.sidebar_layout.addStretch()
        self.content_layout.addWidget(self.side_bar_frame, 1)

        # File/Folder list + Bottom frame
        self.main_area_layout = QtWidgets.QVBoxLayout()

        self.file_or_folder_list = QtWidgets.QListWidget(self.centralwidget)
        self.file_or_folder_list.setStyleSheet("""
            QListWidget {
                background-color: rgb(14, 17, 31);
                border: 1px solid rgb(46, 46, 64);
                border-radius: 8px;
                color: white;
                padding: 5px;
            }
            QListWidget::item {
                padding: 10px;
            }
            QListWidget::item:hover {
                background-color: rgb(52, 69, 180);
                border-radius: 5px;
            }
            QScrollBar:vertical {
                background: rgb(23, 28, 45);
                width: 12px;
                margin: 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: rgb(72, 89, 222);
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgb(100, 120, 255);
            }
        """)
        self.main_area_layout.addWidget(self.file_or_folder_list, 10)

        self.bottom_frame = QtWidgets.QFrame(self.centralwidget)
        self.bottom_frame.setStyleSheet("background-color: rgb(14, 17, 31); border-radius: 8px;")
        self.bottom_layout = QtWidgets.QHBoxLayout(self.bottom_frame)

        self.bottom_layout.addStretch()

        # Upload button
        self.upload_btn = QtWidgets.QPushButton("Upload", self.bottom_frame)
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(72, 89, 222);
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: rgb(100, 120, 255);
            }
            QPushButton:pressed {
                background-color: rgb(52, 69, 180);
            }
        """)
        self.upload_btn.setIcon(QtGui.QIcon(":/icons/icons/icons8-upload-100.png"))
        self.upload_btn.setIconSize(QtCore.QSize(25, 25))
        self.upload_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bottom_layout.addWidget(self.upload_btn)

        # Delete button
        self.delete_btn = QtWidgets.QPushButton("Delete", self.bottom_frame)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(200, 60, 60);
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: rgb(230, 80, 80);
            }
            QPushButton:pressed {
                background-color: rgb(170, 40, 40);
            }
        """)
        self.delete_btn.setIcon(QtGui.QIcon(":/icons/icons/icons8-trash-128.png"))
        self.delete_btn.setIconSize(QtCore.QSize(25, 25))
        self.delete_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bottom_layout.addWidget(self.delete_btn)

        self.main_area_layout.addWidget(self.bottom_frame)
        self.content_layout.addLayout(self.main_area_layout, 4)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("NebulaShare")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
