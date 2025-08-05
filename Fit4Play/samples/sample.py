# from PyQt5.QtWidgets import (
#     QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
#     QComboBox, QCheckBox, QListWidget, QLineEdit, QGridLayout, QScrollArea,
#     QFrame, QTextEdit
# )
# from PyQt5.QtGui import QPixmap, QFont
# from PyQt5.QtCore import Qt
# import sys

# class Fit4PlayUI(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Fit4Play - Smart Game Discovery")
#         self.setGeometry(100, 100, 1200, 800)
#         self.setStyleSheet("font-family: Arial; font-size: 14px;")

#         main_layout = QVBoxLayout(self)
#         main_layout.setContentsMargins(10, 10, 10, 10)
#         main_layout.setSpacing(10)

#         # --- Top Header Bar --- #
#         header = QLabel("🎮 Fit4Play")
#         header.setFont(QFont("Arial", 24, QFont.Bold))
#         header.setAlignment(Qt.AlignCenter)
#         main_layout.addWidget(header)

#         # --- Filter Panel --- #
#         filter_layout = QHBoxLayout()

#         self.search_box = QLineEdit()
#         self.search_box.setPlaceholderText("Search for a game...")
#         self.search_box.setFixedWidth(250)
#         filter_layout.addWidget(self.search_box)

#         self.genre_box = QComboBox()
#         self.genre_box.addItems(["All Genres", "Action", "RPG", "Shooter", "Puzzle", "Indie"])
#         filter_layout.addWidget(self.genre_box)

#         self.platform_box = QComboBox()
#         self.platform_box.addItems(["All Platforms", "Steam", "Epic", "Origin"])
#         filter_layout.addWidget(self.platform_box)

#         self.price_type = QComboBox()
#         self.price_type.addItems(["All Types", "Free", "Paid", "Demo"])
#         filter_layout.addWidget(self.price_type)

#         self.compatibility_toggle = QCheckBox("Only show compatible")
#         filter_layout.addWidget(self.compatibility_toggle)

#         self.refresh_button = QPushButton("🔄 Refresh")
#         filter_layout.addWidget(self.refresh_button)

#         main_layout.addLayout(filter_layout)

#         # --- Game List Grid (Scrollable) --- #
#         scroll_area = QScrollArea()
#         scroll_area.setWidgetResizable(True)
#         game_container = QWidget()
#         self.grid_layout = QGridLayout(game_container)
#         self.grid_layout.setSpacing(20)
#         scroll_area.setWidget(game_container)
#         main_layout.addWidget(scroll_area)

#         # Sample 6 game cards (placeholder visuals)
#         for i in range(6):
#             card = self.create_game_card(f"Game {i+1}")
#             self.grid_layout.addWidget(card, i // 3, i % 3)

#         # --- Wishlist and Export Section --- #
#         action_layout = QHBoxLayout()

#         self.view_wishlist = QPushButton("⭐ View Wishlist")
#         action_layout.addWidget(self.view_wishlist)

#         self.export_btn = QPushButton("📤 Export List")
#         action_layout.addWidget(self.export_btn)

#         self.settings_btn = QPushButton("⚙ Settings")
#         action_layout.addWidget(self.settings_btn)

#         self.dark_mode = QCheckBox("🌙 Dark Mode")
#         action_layout.addWidget(self.dark_mode)

#         main_layout.addLayout(action_layout)

#     def create_game_card(self, title):
#         frame = QFrame()
#         frame.setFixedSize(300, 200)
#         frame.setFrameShape(QFrame.StyledPanel)
#         layout = QVBoxLayout(frame)

#         img = QLabel()
#         img.setPixmap(QPixmap("assets/icons/sample_thumb.png").scaled(280, 100, Qt.KeepAspectRatio))
#         layout.addWidget(img)

#         name = QLabel(title)
#         name.setStyleSheet("font-weight: bold;")
#         layout.addWidget(name)

#         desc = QLabel("Short description of the game.")
#         desc.setWordWrap(True)
#         layout.addWidget(desc)

#         btn = QPushButton("View Details")
#         layout.addWidget(btn)

#         return frame

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = Fit4PlayUI()
#     window.show()
#     sys.exit(app.exec_())


# from PyQt5.QtWidgets import (
#     QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
#     QComboBox, QCheckBox, QLineEdit, QGridLayout, QScrollArea,
#     QFrame, QDialog
# )
# from PyQt5.QtGui import QPixmap, QFont, QColor, QPalette
# from PyQt5.QtCore import Qt
# import sys

# class SettingsDialog(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Settings")
#         self.setFixedSize(300, 200)

#         layout = QVBoxLayout()
#         label = QLabel("Settings coming soon...\nDark Mode toggle is on main screen.")
#         label.setAlignment(Qt.AlignCenter)
#         layout.addWidget(label)
#         self.setLayout(layout)

# class Fit4PlayUI(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Fit4Play - Smart Game Discovery")
#         self.setGeometry(100, 100, 1200, 800)

#         self.is_dark_mode = False
#         self.setStyleSheet(self.load_stylesheet())

#         self.main_layout = QVBoxLayout(self)
#         self.main_layout.setContentsMargins(20, 20, 20, 20)
#         self.main_layout.setSpacing(15)

#         self.init_ui()

#     def init_ui(self):
#         header = QLabel("Fit4Play")
#         header.setFont(QFont("Segoe UI", 28, QFont.Bold))
#         header.setAlignment(Qt.AlignCenter)
#         header.setStyleSheet("color: #00FFB2;")
#         self.main_layout.addWidget(header)

#         filter_layout = QHBoxLayout()

#         self.search_box = QLineEdit()
#         self.search_box.setPlaceholderText("🔍 Search games...")
#         self.search_box.setFixedWidth(250)
#         self.search_box.setStyleSheet("padding: 8px; border-radius: 12px;")
#         filter_layout.addWidget(self.search_box)

#         self.genre_box = QComboBox()
#         self.genre_box.addItems(["All Genres", "Action", "RPG", "Shooter", "Puzzle", "Indie"])
#         self.genre_box.setStyleSheet("padding: 6px; border-radius: 10px;")
#         filter_layout.addWidget(self.genre_box)

#         self.platform_box = QComboBox()
#         self.platform_box.addItems(["All Platforms", "Steam", "Epic", "Origin"])
#         self.platform_box.setStyleSheet("padding: 6px; border-radius: 10px;")
#         filter_layout.addWidget(self.platform_box)

#         self.price_type = QComboBox()
#         self.price_type.addItems(["All Types", "Free", "Paid", "Demo"])
#         self.price_type.setStyleSheet("padding: 6px; border-radius: 10px;")
#         filter_layout.addWidget(self.price_type)

#         self.compatibility_toggle = QCheckBox("Compatible Only")
#         filter_layout.addWidget(self.compatibility_toggle)

#         self.refresh_button = QPushButton("🔄")
#         self.refresh_button.setFixedWidth(40)
#         self.refresh_button.clicked.connect(self.refresh_ui)
#         filter_layout.addWidget(self.refresh_button)

#         self.main_layout.addLayout(filter_layout)

#         scroll_area = QScrollArea()
#         scroll_area.setWidgetResizable(True)
#         self.grid_container = QWidget()
#         self.grid_layout = QGridLayout(self.grid_container)
#         self.grid_layout.setSpacing(16)
#         scroll_area.setWidget(self.grid_container)
#         self.main_layout.addWidget(scroll_area)

#         for i in range(6):
#             card = self.create_game_card(f"Game {i+1}")
#             self.grid_layout.addWidget(card, i // 3, i % 3)

#         action_layout = QHBoxLayout()

#         self.view_wishlist = QPushButton("⭐ Wishlist")
#         action_layout.addWidget(self.view_wishlist)

#         self.export_btn = QPushButton("📤 Export")
#         action_layout.addWidget(self.export_btn)

#         self.settings_btn = QPushButton("⚙ Settings")
#         self.settings_btn.clicked.connect(self.open_settings_dialog)
#         action_layout.addWidget(self.settings_btn)

#         self.dark_mode = QCheckBox("🌙 Dark Mode")
#         self.dark_mode.stateChanged.connect(self.toggle_dark_mode)
#         action_layout.addWidget(self.dark_mode)

#         self.main_layout.addLayout(action_layout)

#     def create_game_card(self, title):
#         frame = QFrame()
#         frame.setFixedSize(300, 200)
#         frame.setStyleSheet("border-radius: 15px; background-color: rgba(255,255,255,0.05);")
#         layout = QVBoxLayout(frame)

#         img = QLabel()
#         img.setPixmap(QPixmap("assets/icons/sample_thumb.png").scaled(280, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
#         layout.addWidget(img)

#         name = QLabel(title)
#         name.setStyleSheet("font-weight: bold; font-size: 16px;")
#         layout.addWidget(name)

#         desc = QLabel("An epic game you might love.")
#         desc.setWordWrap(True)
#         layout.addWidget(desc)

#         btn = QPushButton("Details")
#         layout.addWidget(btn)

#         return frame

#     def load_stylesheet(self):
#         if self.is_dark_mode:
#             return """
#                 QWidget {
#                     background-color: #121212;
#                     color: #EEEEEE;
#                 }
#                 QPushButton {
#                     background-color: #1E1E1E;
#                     color: white;
#                     padding: 6px 12px;
#                     border-radius: 8px;
#                 }
#                 QPushButton:hover {
#                     background-color: #333;
#                 }
#                 QLineEdit, QComboBox {
#                     background-color: #1C1C1C;
#                     color: white;
#                     border: 1px solid #333;
#                     padding: 6px;
#                     border-radius: 8px;
#                 }
#             """
#         else:
#             return """
#                 QWidget {
#                     background-color: #F5F5F5;
#                     color: #222;
#                 }
#                 QPushButton {
#                     background-color: #00C8A4;
#                     color: white;
#                     padding: 6px 12px;
#                     border-radius: 8px;
#                 }
#                 QPushButton:hover {
#                     background-color: #00A98E;
#                 }
#                 QLineEdit, QComboBox {
#                     background-color: white;
#                     color: black;
#                     border: 1px solid #CCC;
#                     padding: 6px;
#                     border-radius: 8px;
#                 }
#             """

#     def toggle_dark_mode(self):
#         self.is_dark_mode = self.dark_mode.isChecked()
#         self.setStyleSheet(self.load_stylesheet())

#     def open_settings_dialog(self):
#         dialog = SettingsDialog()
#         dialog.exec_()

#     def refresh_ui(self):
#         print("Refreshed UI")

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = Fit4PlayUI()
#     window.show()
#     sys.exit(app.exec_())


from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QComboBox, QCheckBox, QLineEdit, QGridLayout, QScrollArea,
    QFrame, QDialog, QGraphicsOpacityEffect
)
from PyQt5.QtGui import QPixmap, QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize
import sys

class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()
        label = QLabel("Settings coming soon...\nDark Mode toggle is on main screen.")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)

class HoverFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setGraphicsEffect(QGraphicsOpacityEffect())
        self.setMouseTracking(True)
        self.anim = QPropertyAnimation(self.graphicsEffect(), b"opacity")
        self.anim.setDuration(300)
        self.anim.setStartValue(0.9)
        self.anim.setEndValue(1.0)
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)

    def enterEvent(self, event):
        self.anim.setDirection(QPropertyAnimation.Forward)
        self.anim.start()
        self.setStyleSheet(self.styleSheet() + "border: 2px solid #00FFD1;")
        return super().enterEvent(event)

    def leaveEvent(self, event):
        self.anim.setDirection(QPropertyAnimation.Backward)
        self.anim.start()
        self.setStyleSheet(self.styleSheet().replace("border: 2px solid #00FFD1;", ""))
        return super().leaveEvent(event)

class Fit4PlayUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fit4Play - Smart Game Discovery")
        self.setGeometry(100, 100, 1200, 800)

        self.is_dark_mode = False
        self.setStyleSheet(self.load_stylesheet())

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        self.init_ui()

    def init_ui(self):
        header = QLabel("Fit4Play")
        header.setFont(QFont("Segoe UI", 28, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: #00FFB2;")
        self.main_layout.addWidget(header)

        filter_layout = QHBoxLayout()

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍 Search games...")
        self.search_box.setFixedWidth(250)
        self.search_box.setStyleSheet("padding: 8px; border-radius: 12px;")
        filter_layout.addWidget(self.search_box)

        self.genre_box = QComboBox()
        self.genre_box.addItems(["All Genres", "Action", "RPG", "Shooter", "Puzzle", "Indie"])
        self.genre_box.setStyleSheet("padding: 6px; border-radius: 10px;")
        filter_layout.addWidget(self.genre_box)

        self.platform_box = QComboBox()
        self.platform_box.addItems(["All Platforms", "Steam", "Epic", "Origin"])
        self.platform_box.setStyleSheet("padding: 6px; border-radius: 10px;")
        filter_layout.addWidget(self.platform_box)

        self.price_type = QComboBox()
        self.price_type.addItems(["All Types", "Free", "Paid", "Demo"])
        self.price_type.setStyleSheet("padding: 6px; border-radius: 10px;")
        filter_layout.addWidget(self.price_type)

        self.compatibility_toggle = QCheckBox("Compatible Only")
        filter_layout.addWidget(self.compatibility_toggle)

        self.refresh_button = QPushButton("🔄")
        self.refresh_button.setFixedWidth(40)
        self.refresh_button.clicked.connect(self.refresh_ui)
        filter_layout.addWidget(self.refresh_button)

        self.main_layout.addLayout(filter_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(16)
        scroll_area.setWidget(self.grid_container)
        self.main_layout.addWidget(scroll_area)

        for i in range(6):
            card = self.create_game_card(f"Game {i+1}")
            self.grid_layout.addWidget(card, i // 3, i % 3)

        action_layout = QHBoxLayout()

        self.view_wishlist = QPushButton("⭐ Wishlist")
        action_layout.addWidget(self.view_wishlist)

        self.export_btn = QPushButton("📤 Export")
        action_layout.addWidget(self.export_btn)

        self.settings_btn = QPushButton("⚙ Settings")
        self.settings_btn.clicked.connect(self.open_settings_dialog)
        action_layout.addWidget(self.settings_btn)

        self.dark_mode = QCheckBox("🌙 Dark Mode")
        self.dark_mode.stateChanged.connect(self.toggle_dark_mode)
        action_layout.addWidget(self.dark_mode)

        self.main_layout.addLayout(action_layout)

    def create_game_card(self, title):
        frame = HoverFrame()
        frame.setFixedSize(300, 200)
        frame.setStyleSheet("border-radius: 15px; background-color: rgba(255,255,255,0.05);")
        layout = QVBoxLayout(frame)

        img = QLabel()
        img.setPixmap(QPixmap("assets/icons/sample_thumb.png").scaled(280, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        layout.addWidget(img)

        name = QLabel(title)
        name.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(name)

        desc = QLabel("An epic game you might love.")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        btn = QPushButton("Details")
        layout.addWidget(btn)

        return frame

    def load_stylesheet(self):
        if self.is_dark_mode:
            return """
                QWidget {
                    background-color: #121212;
                    color: #EEEEEE;
                }
                QPushButton {
                    background-color: #1E1E1E;
                    color: white;
                    padding: 6px 12px;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #333;
                }
                QLineEdit, QComboBox {
                    background-color: #1C1C1C;
                    color: white;
                    border: 1px solid #333;
                    padding: 6px;
                    border-radius: 8px;
                }
            """
        else:
            return """
                QWidget {
                    background-color: #F5F5F5;
                    color: #222;
                }
                QPushButton {
                    background-color: #00C8A4;
                    color: white;
                    padding: 6px 12px;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #00A98E;
                }
                QLineEdit, QComboBox {
                    background-color: white;
                    color: black;
                    border: 1px solid #CCC;
                    padding: 6px;
                    border-radius: 8px;
                }
            """

    def toggle_dark_mode(self):
        self.is_dark_mode = self.dark_mode.isChecked()
        self.setStyleSheet(self.load_stylesheet())

    def open_settings_dialog(self):
        dialog = SettingsDialog()
        dialog.exec_()

    def refresh_ui(self):
        print("Refreshed UI")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Fit4PlayUI()
    window.show()
    sys.exit(app.exec_())
