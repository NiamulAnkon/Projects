from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        MainWindow.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Search bar
        self.search_filter = QtWidgets.QLineEdit(self.centralwidget)
        self.search_filter.setGeometry(QtCore.QRect(40, 30, 571, 31))
        self.search_filter.setStyleSheet("border: 3px solid Green; background-color: rgb(255, 255, 255); border-radius: 15px;")
        self.search_filter.setObjectName("search_filter")
        
        self.search_btn = QtWidgets.QPushButton("Search", self.centralwidget)
        self.search_btn.setGeometry(QtCore.QRect(620, 30, 101, 31))
        self.search_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.search_btn.setStyleSheet("background-color: rgb(25, 255, 0); border: 3px solid; border-radius: 10px;")
        self.search_btn.setObjectName("search_btn")
        
        # Playlist section
        self.label = QtWidgets.QLabel("Playlist:", self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 80, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet("color: White;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        
        self.playlist_widget = QtWidgets.QListWidget(self.centralwidget)
        self.playlist_widget.setGeometry(QtCore.QRect(10, 120, 256, 331))
        self.playlist_widget.setStyleSheet("background-color: white; color: black; border-radius: 10px; padding: 5px;")
        
        self.add_playlist_btn = QtWidgets.QPushButton("Add Playlist", self.centralwidget)
        self.add_playlist_btn.setGeometry(QtCore.QRect(10, 470, 101, 31))
        self.add_playlist_btn.setStyleSheet("background-color: rgb(25, 255, 0); border: 3px solid; border-radius: 10px;")
        
        self.dlt_playlist_btn = QtWidgets.QPushButton("Delete Playlist", self.centralwidget)
        self.dlt_playlist_btn.setGeometry(QtCore.QRect(130, 470, 101, 31))
        self.dlt_playlist_btn.setStyleSheet("background-color: rgb(25, 255, 0); border: 3px solid; border-radius: 10px;")
        
        # Songs list
        self.songs_list = QtWidgets.QListWidget(self.centralwidget)
        self.songs_list.setGeometry(QtCore.QRect(295, 120, 481, 331))
        self.songs_list.setStyleSheet("background-color: white; color: black; border-radius: 10px; padding: 5px;")
        
        # Controls
        self.import_song_btn = QtWidgets.QPushButton("Import Song", self.centralwidget)
        self.import_song_btn.setGeometry(QtCore.QRect(320, 470, 101, 31))
        self.import_song_btn.setStyleSheet("background-color: rgb(25, 255, 0); border: 3px solid; border-radius: 10px;")
        
        self.download_song_btn = QtWidgets.QPushButton("Download Song", self.centralwidget)
        self.download_song_btn.setGeometry(QtCore.QRect(470, 470, 101, 31))
        self.download_song_btn.setStyleSheet("background-color: rgb(25, 255, 0); border: 3px solid; border-radius: 10px;")
        
        self.play_btn = QtWidgets.QPushButton("▶", self.centralwidget)
        self.play_btn.setGeometry(QtCore.QRect(410, 510, 51, 41))
        self.play_btn.setStyleSheet("background-color: #27ae60; border-radius: 15px;")
        
        self.pause_btn = QtWidgets.QPushButton("⏸", self.centralwidget)
        self.pause_btn.setGeometry(QtCore.QRect(490, 510, 51, 41))
        self.pause_btn.setStyleSheet("background-color: #27ae60; border-radius: 15px;")
        
        self.stop_btn = QtWidgets.QPushButton("⏹", self.centralwidget)
        self.stop_btn.setGeometry(QtCore.QRect(570, 510, 51, 41))
        self.stop_btn.setStyleSheet("background-color: #27ae60; border-radius: 15px;")
        
        MainWindow.setCentralWidget(self.centralwidget)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
