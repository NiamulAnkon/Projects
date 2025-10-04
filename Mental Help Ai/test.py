from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QThread, pyqtSignal, Qt, QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QLabel, QVBoxLayout, QPushButton
from config import API_KEY
import google.generativeai as genai 
import pyttsx3
import speech_recognition as sr

genai.configure(api_key=API_KEY)

# ---------------- Typing Popup ----------------
class TypingDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MindMate")
        self.setModal(True)
        self.setFixedSize(220, 80)
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.CustomizeWindowHint)

        layout = QVBoxLayout()
        self.label = QLabel("MindMate is typing")
        self.label.setAlignment(Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label.setFont(font)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.dot_count = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_dots)
        self.timer.start(500)  # Blink speed

    def animate_dots(self):
        self.dot_count = (self.dot_count + 1) % 4
        self.label.setText("MindMate is typing" + "." * self.dot_count)


# ---------------- AI Chat Thread ----------------
class ChatThread(QThread):
    finished = pyqtSignal(str)

    def __init__(self, message):
        super().__init__()
        self.message = message

    def run(self):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(self.message)
            self.finished.emit(response.text)
        except Exception as e:
            self.finished.emit(f"Error: {str(e)}")


# ---------------- Main UI ----------------
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 600)
        MainWindow.setStyleSheet("background-color: #f7f9fb;")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        top_bar = QtWidgets.QHBoxLayout()
        self.mood_indicator = QtWidgets.QLabel("Mood: 😊 Neutral")
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.mood_indicator.setFont(font)
        self.voice_output_btn = self.create_button("🔊 Voice Output", "#4CAF50", "white", "#45a049")
        self.voice_input_btn = self.create_button("🎤 Voice Input", "#4CAF50", "white", "#45a049")
        self.setting_btn = self.create_button("⚙︎ Settings", "rgb(226,226,226)", "black", "rgb(200,200,200)")
        self.get_help_btn = self.create_button("🙋‍ Get Help", "#ff4b5c", "white", "#ff1f3a")
        self.get_help_btn.clicked.connect(self.show_help_dialog)

        top_bar.addWidget(self.mood_indicator)
        top_bar.addStretch()
        top_bar.addWidget(self.voice_output_btn)
        top_bar.addWidget(self.voice_input_btn)
        top_bar.addWidget(self.setting_btn)
        top_bar.addWidget(self.get_help_btn)
        main_layout.addLayout(top_bar)

        self.msg_box = QtWidgets.QTextEdit()
        self.msg_box.setStyleSheet("""
            background-color: white;
            border: 1px solid #d0d7de;
            border-radius: 15px;
            padding: 10px;
            font-size: 14px;
        """)
        self.msg_box.setPlaceholderText("💬 Your conversation will appear here...")
        self.msg_box.setReadOnly(True)
        main_layout.addWidget(self.msg_box, stretch=1)

        input_bar = QtWidgets.QHBoxLayout()
        self.usr_text = QtWidgets.QLineEdit()
        self.usr_text.setPlaceholderText(" ✍ Type your message here...")
        self.usr_text.setStyleSheet("""
            background-color: white;
            border: 1px solid #d0d7de;
            border-radius: 10px;
            font-size: 12px;
            padding: 5px;
        """)

        self.send_msg_btn = self.create_button("Send ➤", "#4CAF50", "white", "#45a049")
        self.send_msg_btn.clicked.connect(self.send_message)

        input_bar.addWidget(self.usr_text, stretch=1)
        input_bar.addWidget(self.send_msg_btn)
        main_layout.addLayout(input_bar)

        self.animate_entry(MainWindow)

    def create_button(self, text, bg_color, text_color, hover_color):
        btn = QtWidgets.QPushButton(text)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        btn.setFont(font)
        btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border-radius: 8px;
                padding: 5px 10px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """)
        return btn

    def animate_entry(self, MainWindow):
        MainWindow.setWindowOpacity(0.0)
        self.fade_animation = QPropertyAnimation(MainWindow, b"windowOpacity")
        self.fade_animation.setDuration(800)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.fade_animation.start()

    # ---------------- Typing and bubble chat Effect ----------------

    def show_typing_bubble(self):
        self.typing_label = QLabel("💬 MindMate is typing")
        self.typing_label.setStyleSheet("""
            background-color: #e1f5fe;
            border-radius: 10px;
            padding: 5px 10px;
            font-size: 13px;
        """)
        self.typing_label.setWordWrap(True)

        self.msg_box.append("")  # Just to keep space for alignment
        cursor = self.msg_box.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        self.msg_box.setTextCursor(cursor)
        self.msg_box.insertPlainText("MindMate is typing")  # Placeholder text

        self.dot_count = 0
        self.typing_timer = QTimer()
        self.typing_timer.timeout.connect(self.animate_typing_dots)
        self.typing_timer.start(500)

    def animate_typing_dots(self):
        self.dot_count = (self.dot_count + 1) % 4
        cursor = self.msg_box.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
        cursor.select(QtGui.QTextCursor.LineUnderCursor)
        cursor.removeSelectedText()
        cursor.insertText("MindMate is typing" + "." * self.dot_count)

    def remove_typing_bubble(self):
        if hasattr(self, "typing_timer"):
            self.typing_timer.stop()
        cursor = self.msg_box.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        self.msg_box.setTextCursor(cursor)

    def show_typing_effect(self, full_text, speed=30):
        current_index = 0

        def update_text():
            nonlocal current_index
            if current_index < len(full_text):
                self.msg_box.moveCursor(QtGui.QTextCursor.End)
                self.msg_box.insertPlainText(full_text[current_index])
                current_index += 1
            else:
                timer.stop()

        timer = QTimer()
        timer.timeout.connect(update_text)
        timer.start(speed)

    # ---------------- AI Chat Function ----------------
    def send_message(self):
        user_text = self.usr_text.text().strip()
        if user_text:
            self.msg_box.append(f"<b>You:</b> {user_text}")
            self.usr_text.clear()

            # Show typing popup
            self.show_typing_bubble()

            # Run AI in a separate thread
            self.thread = ChatThread(user_text)
            self.thread.finished.connect(self.display_ai_response)
            self.thread.start()

    def display_ai_response(self, response):
        self.remove_typing_bubble()
        self.msg_box.append("<b>MIND MATE:</b> ")
        self.show_typing_effect(response, speed=25)
    
    def show_help_dialog(self):
        help_dialog = QDialog(self)
        help_dialog.setWindowTitle("MindMate Help")
        help_dialog.setFixedSize(400, 300)

        layout = QVBoxLayout()
        label = QLabel("""
        <b>How to use MindMate:</b><br><br>
        • Type your question in the box below.<br>
        • Use Voice Input 🎤 for hands-free chatting.<br>
        • Click Voice Output 🔊 to hear the reply.<br>
        • Your mood is shown at the top.<br>
        • 'Get Help' shows this guide.<br><br>
       If you ever feel like hurting yourself or thinking about ending your life, please reach out to someone who can bring you comfort. And if you feel like there’s no one,<br> remember — Mind Mate is here for you. You matter in this world, and you are not alone.
        """)
        label.setWordWrap(True)
        layout.addWidget(label)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(help_dialog.close)
        layout.addWidget(close_btn, alignment=Qt.AlignRight)

        help_dialog.setLayout(layout)
        help_dialog.exec_()


# ---------------- Main Window ----------------
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


# ---------------- Hover Bounce ----------------
class HoverBounce(QtCore.QObject):
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Enter and isinstance(obj, QtWidgets.QPushButton):
            animation = QPropertyAnimation(obj, b"geometry")
            animation.setDuration(150)
            animation.setStartValue(obj.geometry())
            animation.setEndValue(obj.geometry().adjusted(-2, -2, 2, 2))
            animation.setEasingCurve(QEasingCurve.OutBounce)
            animation.start()
            obj.animation = animation
        elif event.type() == QtCore.QEvent.Leave and isinstance(obj, QtWidgets.QPushButton):
            animation = QPropertyAnimation(obj, b"geometry")
            animation.setDuration(150)
            animation.setStartValue(obj.geometry())
            animation.setEndValue(obj.geometry().adjusted(2, 2, -2, -2))
            animation.setEasingCurve(QEasingCurve.OutBounce)
            animation.start()
            obj.animation = animation
        return super().eventFilter(obj, event)


# ---------------- Run App ----------------
# if __name__ == "__main__":
#     import sys
#     app = QApplication(sys.argv)
#     window = MainWindow()

#     hover_filter = HoverBounce()
#     window.send_msg_btn.installEventFilter(hover_filter)
#     window.get_help_btn.installEventFilter(hover_filter)
#     window.setting_btn.installEventFilter(hover_filter)

#     window.show()
#     sys.exit(app.exec_())