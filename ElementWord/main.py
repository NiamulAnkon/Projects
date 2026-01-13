from PyQt5 import QtCore, QtGui, QtWidgets
from pathlib import Path
from element_builder import ElementBuilder

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Use layouts instead of fixed geometry to make the window responsive
        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(12)

        # Header frame (keeps similar visual size but is responsive)
        self.header_frame = QtWidgets.QFrame(self.centralwidget)
        self.header_frame.setMinimumHeight(80)
        self.header_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.header_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.header_frame.setObjectName("header_frame")
        self.header_frame.setStyleSheet("background-color: #00A8E8; border-radius: 30px;")
        self.header_layout = QtWidgets.QVBoxLayout(self.header_frame)
        self.header_layout.setContentsMargins(20, 5, 20, 5)
        self.header = QtWidgets.QLabel(self.header_frame)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.header.setFont(font)
        self.header.setStyleSheet("color: white;")
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        self.header.setObjectName("header")
        self.header_layout.addWidget(self.header)
        self.main_layout.addWidget(self.header_frame)

        # Body frame
        self.body__frame = QtWidgets.QFrame(self.centralwidget)
        self.body__frame.setMinimumHeight(291)
        self.body__frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.body__frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.body__frame.setObjectName("body__frame")
        self.body__frame.setStyleSheet("background-color: #1EA8FF; border-radius: 30px;")
        self.body_layout = QtWidgets.QVBoxLayout(self.body__frame)
        self.body_layout.setContentsMargins(20, 12, 20, 12)
        self.body_layout.setSpacing(12)

        self.info = QtWidgets.QLabel(self.body__frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.info.setFont(font)
        self.info.setStyleSheet("color: white;")
        self.info.setAlignment(QtCore.Qt.AlignCenter)
        self.info.setObjectName("info")
        self.body_layout.addWidget(self.info)

        self.word = QtWidgets.QLineEdit(self.body__frame)
        self.word.setMinimumHeight(50)
        self.word.setStyleSheet("background-color: white; border: 2px solid #e0e0e0; border-radius: 10px; color: #000000; padding: 8px;")
        self.word.setObjectName("word")
        self.body_layout.addWidget(self.word)

        self.genarate_element_btn = QtWidgets.QPushButton(self.body__frame)
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.genarate_element_btn.setFont(font)
        self.genarate_element_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.genarate_element_btn.setStyleSheet("background-color: #FF7A59; color: white; border-radius: 12px; padding: 10px;")
        self.genarate_element_btn.setMinimumHeight(100)
        self.genarate_element_btn.setObjectName("genarate_element_btn")
        self.genarate_element_btn.clicked.connect(self.generate_element)
        self.body_layout.addWidget(self.genarate_element_btn)

        self.main_layout.addWidget(self.body__frame)

        # Result frame
        self.result_frame = QtWidgets.QFrame(self.centralwidget)
        self.result_frame.setMinimumHeight(191)
        self.result_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.result_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.result_frame.setObjectName("result_frame")
        self.result_frame.setStyleSheet("background-color: #6C63FF; border-radius: 30px;")
        self.result_layout = QtWidgets.QVBoxLayout(self.result_frame)
        self.result_layout.setContentsMargins(20, 10, 20, 10)
        self.result_layout.setSpacing(8)

        self.info_2 = QtWidgets.QLabel(self.result_frame)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.info_2.setFont(font)
        self.info_2.setStyleSheet("color: white;")
        self.info_2.setAlignment(QtCore.Qt.AlignCenter)
        self.info_2.setObjectName("info_2")
        self.result_layout.addWidget(self.info_2)

        self.result = QtWidgets.QLabel(self.result_frame)
        self.result.setStyleSheet("color: white;")
        self.result.setAlignment(QtCore.Qt.AlignCenter)
        self.result.setObjectName("result")
        self.result_layout.addWidget(self.result)

        self.main_layout.addWidget(self.result_frame)

        MainWindow.setCentralWidget(self.centralwidget)

        self.header.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.info.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.word.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.genarate_element_btn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.info_2.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.result.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        element_json_path = Path('elements.json')
        self.builder = ElementBuilder(element_json_path)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def generate_element(self):
        word = self.word.text().strip()
        if not word:
            self.result.setText("Please enter a word.")
            return
        if self.builder.can_build_word(word):
            result = self.builder.backtrack_word(word)
            self.result.setText(result)
        else:
                self.result.setText("❌ This word cannot be formed using periodic table elements.")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.header.setText(_translate("MainWindow", "Element To Word"))
        self.info.setText(_translate("MainWindow", "Build Words Using The Periodic Table"))
        self.word.setPlaceholderText(_translate("MainWindow", "Enter a Word (eg. cute, neon, science)"))
        self.genarate_element_btn.setText(_translate("MainWindow", "Generate Element"))
        self.info_2.setText(_translate("MainWindow", "Your Result Will Appear Here"))
        self.result.setText(_translate("MainWindow", "Enter a Word And click Generate to find out the result here"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())