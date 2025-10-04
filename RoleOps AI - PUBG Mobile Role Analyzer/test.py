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
        slider.setMinimum(1)
        slider.setMaximum(10)
        slider.setTickInterval(10)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setValue(1)

        value_label = QLabel("1")
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


# def predict_role(answers):
#     role_scores = {
#         "IGL": 0,
#         "Entry Fragger": 0,
#         "Support": 0,
#         "Freestyle": 0,
#         "Fragger": 0,
#         "Sniper": 0
#     }

#     # Q1: Push style
#     ans = answers.get(0)
#     if ans == "Call shots ":
#         role_scores["IGL"] += 3
#     elif ans == "Follow team ":
#         role_scores["Support"] += 2
#     elif ans == "Flank wide ":
#         role_scores["Freestyle"] += 3
#     elif ans == "Push aggressively ":
#         role_scores["Entry Fragger"] += 3

#     # Q2: Positioning vs fragging
#     ans = answers.get(1)
#     if ans == "Positioning ":
#         role_scores["IGL"] += 2
#         role_scores["Support"] += 1
#     elif ans == "Fragging ":
#         role_scores["Entry Fragger"] += 2
#         role_scores["Fragger"] += 2
#     elif ans == "Both equally ":
#         role_scores["Freestyle"] += 2
#     elif ans == "Situational ":
#         role_scores["IGL"] += 1
#         role_scores["Freestyle"] += 2

#     # Q3: Zone rotation awareness (slider)
#     val = answers.get(2)
#     if val:
#         role_scores["IGL"] += val
#         role_scores["Support"] += val // 2

#     # Q4: Vehicle rotation caller
#     ans = answers.get(3)
#     if ans == "I always call ":
#         role_scores["IGL"] += 3
#     elif ans == "Sometimes ":
#         role_scores["Support"] += 1
#     elif ans == "Rarely ":
#         role_scores["Freestyle"] += 1
#     elif ans == "I follow others ":
#         role_scores["Support"] += 2

#     # Q5: Knock handling
#     ans = answers.get(4)
#     if ans == "Clear threats first ":
#         role_scores["Fragger"] += 2
#     elif ans == "Revive instantly ":
#         role_scores["Support"] += 3
#     elif ans == "Call decision based on situation ":
#         role_scores["IGL"] += 2
#     elif ans == "Try to bait enemy ":
#         role_scores["Freestyle"] += 2

#     # Q6: Comms during fights (slider)
#     val = answers.get(5)
#     if val:
#         role_scores["IGL"] += val
#         role_scores["Entry Fragger"] += val // 2

#     # Q7: Zone guiding (slider)
#     val = answers.get(6)
#     if val:
#         role_scores["IGL"] += val
#         role_scores["Support"] += val // 2

#     # Q8: Fight review
#     ans = answers.get(7)
#     if ans == "Always analyze ":
#         role_scores["IGL"] += 3
#     elif ans == "Sometimes think over ":
#         role_scores["Support"] += 2
#     elif ans == "Forget and move on ":
#         role_scores["Entry Fragger"] += 1
#     elif ans == "Only major fights ":
#         role_scores["Freestyle"] += 1

#     # Q9: Decision role
#     ans = answers.get(8)
#     if ans == "Decision-maker ":
#         role_scores["IGL"] += 3
#     elif ans == "Executor ":
#         role_scores["Entry Fragger"] += 2
#     elif ans == "Silent executor ":
#         role_scores["Sniper"] += 2
#     elif ans == "Independent thinker ":
#         role_scores["Freestyle"] += 2

#     # Q10: Area control vs timing
#     ans = answers.get(9)
#     if ans == "Area control ":
#         role_scores["IGL"] += 2
#         role_scores["Support"] += 2
#     elif ans == "Fight timing ":
#         role_scores["Entry Fragger"] += 2
#     elif ans == "Both ":
#         role_scores["Freestyle"] += 2
#     elif ans == "Pick off timings ":
#         role_scores["Sniper"] += 3

#     # Final role
#     best_role = max(role_scores, key=role_scores.get)
#     return best_role