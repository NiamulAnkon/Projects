from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication


class Ui_Disclaimer(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("DisclaimerWindow")
        Dialog.resize(800, 500)
        Dialog.setMinimumSize(QtCore.QSize(800, 500))
        Dialog.setMaximumSize(QtCore.QSize(800, 500))
        Dialog.setStyleSheet("""
            QWidget {
                background-color: #f4f6f8;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel {
                color: #333;
            }
            QPushButton {
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton#agree_btn {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton#agree_btn:hover {
                background-color: #45a049;
            }
            QPushButton#ext_btn {
                background-color: #f44336;
                color: white;
            }
            QPushButton#ext_btn:hover {
                background-color: #d32f2f;
            }
        """)

        # Main vertical layout
        self.main_layout = QtWidgets.QVBoxLayout(Dialog)
        self.main_layout.setContentsMargins(40, 30, 40, 30)
        self.main_layout.setSpacing(20)

        # Header
        self.header = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.header.setFont(font)
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        self.header.setWordWrap(True)
        self.header.setText("Important: Please Read Before Using MindMate AI")
        self.main_layout.addWidget(self.header)

        # Body text
        self.body_text = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.body_text.setFont(font)
        self.body_text.setAlignment(QtCore.Qt.AlignTop)
        self.body_text.setWordWrap(True)
        self.body_text.setText(
            "MindMate AI is a wellness companion, not a medical or crisis service.\n"
            "It does not diagnose or treat mental health conditions.\n\n"
            "If you are in crisis, feeling suicidal, or thinking about harming yourself, "
            "please contact a suicide prevention hotline or local emergency services immediately.\n\n"
            "Your privacy is very important to us. However, in rare cases where there is a serious "
            "risk of harm, relevant information may be shared with authorities to help keep you safe.\n\n"
            "All conversations are stored securely and treated with confidentiality.\n\n"
            "By clicking “I Agree”, you confirm that you understand and accept these terms."
        )
        self.main_layout.addWidget(self.body_text)

        # Button row
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addStretch()

        self.agree_btn = QtWidgets.QPushButton("I Agree")
        self.agree_btn.setObjectName("agree_btn")
        self.button_layout.addWidget(self.agree_btn)

        self.ext_btn = QtWidgets.QPushButton("Exit")
        self.ext_btn.setObjectName("ext_btn")
        self.button_layout.addWidget(self.ext_btn)

        self.button_layout.addStretch()
        self.main_layout.addLayout(self.button_layout)


class DisclaimerDialog(QDialog, Ui_Disclaimer):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Disclaimer")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dialog = DisclaimerDialog()
    if dialog.exec_() == QDialog.Accepted:
        print("User agreed")
    else:
        print("User exited")
    sys.exit(0)
