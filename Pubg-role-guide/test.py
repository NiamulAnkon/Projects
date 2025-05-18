import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QRadioButton,
    QButtonGroup, QSlider, QPushButton, QScrollArea, QGroupBox
)
from PyQt5.QtCore import Qt

class QuizApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PUBG Mobile Role Analyzer")
        self.resize(800, 600)
        self.layout = QVBoxLayout()

        self.questions = self.load_questions()
        self.responses = {}

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        self.generate_quiz_ui()

        self.scroll.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll)
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_answers)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def load_questions(self):
        with open("questions.json", "r") as file:
            return json.load(file)

    def generate_quiz_ui(self):
        for idx, question in enumerate(self.questions):
            question_text = question["question"]
            q_type = question.get("type", "mcq")

            group_box = QGroupBox()
            group_layout = QVBoxLayout()

            if q_type == "mcq":
                options = question["options"]
                group_layout.addWidget(QLabel(f"{idx+1}. {question_text}"))
                button_group = QButtonGroup(self)
                for opt in options:
                    rb = QRadioButton(opt)
                    button_group.addButton(rb)
                    group_layout.addWidget(rb)
                self.responses[idx] = button_group

            elif q_type == "slider":
                slider_widget, slider = self.create_slider_widget(f"{idx+1}. {question_text}")
                group_layout.addWidget(slider_widget)
                self.responses[idx] = slider

            group_box.setLayout(group_layout)
            self.scroll_layout.addWidget(group_box)


    def create_slider_widget(self, question_text):
        layout = QVBoxLayout()
        label = QLabel(question_text)
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setTickInterval(10)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setValue(50)

        value_label = QLabel("50")
        slider.valueChanged.connect(lambda val: value_label.setText(str(val)))

        layout.addWidget(label)
        layout.addWidget(slider)
        layout.addWidget(value_label)

        container = QWidget()
        container.setLayout(layout)
        return container, slider


    def submit_answers(self):
        answers = {}
        for idx, widget in self.responses.items():
            if isinstance(widget, QButtonGroup):
                checked = widget.checkedButton()
                answers[idx] = checked.text() if checked else None
            elif isinstance(widget, QSlider):
                answers[idx] = widget.value()

        print("User Answers:", answers)
        # Here you will later add logic to analyze and generate result.

if __name__ == '__main__':
    app = QApplication(sys.argv)
    quiz = QuizApp()
    quiz.show()
    sys.exit(app.exec_())
