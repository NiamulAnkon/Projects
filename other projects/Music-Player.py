from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import pygame
import yt_dlp
import os
import json

DATA_FILE = "music_data.json"

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
        self.search_filter.textChanged.connect(self.search_song)
        
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
        self.add_playlist_btn.clicked.connect(self.add_playlist)
        self.add_playlist_btn.setStyleSheet("background-color: rgb(25, 255, 0); border: 3px solid; border-radius: 10px;")
        
        self.dlt_playlist_btn = QtWidgets.QPushButton("Delete Playlist", self.centralwidget)
        self.dlt_playlist_btn.setGeometry(QtCore.QRect(130, 470, 101, 31))
        self.dlt_playlist_btn.clicked.connect(self.delete_playlist)
        self.dlt_playlist_btn.setStyleSheet("background-color: rgb(25, 255, 0); border: 3px solid; border-radius: 10px;")
        
        # Songs list
        self.songs_list = QtWidgets.QListWidget(self.centralwidget)
        self.songs_list.setGeometry(QtCore.QRect(295, 120, 481, 331))
        self.songs_list.setStyleSheet("background-color: white; color: black; border-radius: 10px; padding: 5px;")
        self.songs_list.itemDoubleClicked.connect(self.play_song)
        
        # Controls
        self.import_song_btn = QtWidgets.QPushButton("Import Song", self.centralwidget)
        self.import_song_btn.setGeometry(QtCore.QRect(320, 470, 101, 31))
        self.import_song_btn.clicked.connect(self.import_song)
        self.import_song_btn.setStyleSheet("background-color: rgb(25, 255, 0); border: 3px solid; border-radius: 10px;")
        
        self.download_song_btn = QtWidgets.QPushButton("Download Song", self.centralwidget)
        self.download_song_btn.setGeometry(QtCore.QRect(470, 470, 101, 31))
        self.download_song_btn.clicked.connect(self.download_song)
        self.download_song_btn.setStyleSheet("background-color: rgb(25, 255, 0); border: 3px solid; border-radius: 10px;")
        
        self.play_btn = QtWidgets.QPushButton("▶", self.centralwidget)
        self.play_btn.setGeometry(QtCore.QRect(410, 510, 51, 41))
        self.play_btn.clicked.connect(self.resume_song)
        self.play_btn.setStyleSheet("background-color: #27ae60; border-radius: 15px;")
        
        self.pause_btn = QtWidgets.QPushButton("⏸", self.centralwidget)
        self.pause_btn.setGeometry(QtCore.QRect(490, 510, 51, 41))
        self.pause_btn.clicked.connect(self.pause_song)
        self.pause_btn.setStyleSheet("background-color: #27ae60; border-radius: 15px;")
        
        self.stop_btn = QtWidgets.QPushButton("⏹", self.centralwidget)
        self.stop_btn.setGeometry(QtCore.QRect(570, 510, 51, 41))
        self.stop_btn.clicked.connect(self.stop_song)
        self.stop_btn.setStyleSheet("background-color: #27ae60; border-radius: 15px;")
        
        MainWindow.setCentralWidget(self.centralwidget)

        pygame.mixer.init()
        self.current_song = None
        self.songs = []
        self.playlists = []

        self.load_data()  # Load saved data on startup

    def search_song(self):
        query = self.search_filter.text().lower()
        self.songs_list.clear()
        for song in self.songs:
            if query in song.lower():
                self.songs_list.addItem(song)
    
    def add_playlist(self):
        text, ok = QtWidgets.QInputDialog.getText(None, "New Playlist", "Enter playlist name:")
        if ok and text:
            self.playlists.append(text)
            self.playlist_widget.addItem(text)
            self.save_data()

    def delete_playlist(self):
        selected_item = self.playlist_widget.currentItem()
        if selected_item:
            self.playlists.remove(selected_item.text())
            self.playlist_widget.takeItem(self.playlist_widget.row(selected_item))
            self.save_data()
    
    def import_song(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Import Song", "", "Audio Files (*.mp3 *.wav)")
        if file_path:
            self.songs.append(file_path)
            self.songs_list.addItem(file_path.split("/")[-1])
            self.save_data()
    
    def play_song(self, item):
        song_name = item.text()
        song_path = next((s for s in self.songs if song_name in s), None)
        if song_path:
            self.current_song = song_path
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
    
    def resume_song(self):
        if self.current_song:
            pygame.mixer.music.unpause()
    
    def pause_song(self):
        pygame.mixer.music.pause()
    
    def stop_song(self):
        pygame.mixer.music.stop()

    def download_song(self):
        url, ok = QtWidgets.QInputDialog.getText(None, "Download Song", "Enter YouTube URL:")
        if ok and url:
            save_path = QFileDialog.getExistingDirectory(None, "Select Save Location")
            if save_path:
                ydl_opts = {'format': 'bestaudio/best', 'outtmpl': os.path.join(save_path, "%(title)s.%(ext)s")}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                QMessageBox.information(None, "Download Complete", "Song downloaded successfully!")

    def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump({"songs": self.songs, "playlists": self.playlists}, f)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.songs = data.get("songs", [])
                self.playlists = data.get("playlists", [])
                self.songs_list.addItems([os.path.basename(song) for song in self.songs])
                self.playlist_widget.addItems(self.playlists)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
