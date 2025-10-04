# from PyQt5.QtWidgets import (
#     QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
#     QLabel, QPushButton, QProgressBar, QStackedWidget, QMessageBox, QScrollArea
# )
# from PyQt5.QtCore import Qt
# import sys

# class GoalCard(QWidget):
#     def __init__(self, name, target_amount, saved_amount, switch_to_detail):
#         super().__init__()
#         self.name = name
#         self.target_amount = target_amount
#         self.saved_amount = saved_amount

#         layout = QVBoxLayout()
#         self.setLayout(layout)
#         layout.addWidget(QLabel(f"<b>{self.name}</b>"))
#         layout.addWidget(QLabel(f"₹{self.target_amount}"))

#         progress = QProgressBar()
#         progress.setValue(int((self.saved_amount / self.target_amount) * 100))
#         layout.addWidget(progress)

#         self.setStyleSheet("border: 1px solid gray; padding: 10px; border-radius: 10px;")
#         self.mousePressEvent = lambda e: switch_to_detail(self.name)

# class GoalDetailView(QWidget):
#     def __init__(self, name, go_back_callback):
#         super().__init__()
#         layout = QVBoxLayout()
#         self.setLayout(layout)

#         layout.addWidget(QLabel(f"<h2>{name}</h2>"))
#         layout.addWidget(QLabel("Target: ₹10,500"))  # Placeholder
#         layout.addWidget(QLabel("Saved: ₹3,200"))    # Placeholder
#         layout.addWidget(QLabel("Lent Out: ₹500"))   # Placeholder
#         layout.addWidget(QPushButton("Add Money"))
#         layout.addWidget(QPushButton("Lend Money"))
#         layout.addWidget(QPushButton("Receive Money"))

#         back_btn = QPushButton("Go Back")
#         back_btn.clicked.connect(go_back_callback)
#         layout.addWidget(back_btn)

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("GoalSaver")

#         self.stack = QStackedWidget()
#         self.setCentralWidget(self.stack)

#         self.main_page = QWidget()
#         self.goal_details = {}  # goal name -> GoalDetailView

#         main_layout = QVBoxLayout()
#         scroll = QScrollArea()
#         scroll.setWidgetResizable(True)
#         container = QWidget()
#         grid = QHBoxLayout()
#         container.setLayout(grid)

#         # Example goals
#         goals = [
#             ("Gaming Phone", 10500, 3000),
#             ("Holiday Trip", 6000, 1800),
#             ("Guitar", 8000, 1200),
#         ]

#         for name, target, saved in goals:
#             card = GoalCard(name, target, saved, self.show_goal_detail)
#             grid.addWidget(card)

#         create_card = QPushButton("+ Create New Goal")
#         create_card.clicked.connect(lambda: QMessageBox.information(self, "Coming Soon", "Create Goal UI coming soon!"))
#         grid.addWidget(create_card)

#         scroll.setWidget(container)
#         main_layout.addWidget(QLabel("<h1>Select a Goal</h1>", alignment=Qt.AlignCenter))
#         main_layout.addWidget(scroll)
#         self.main_page.setLayout(main_layout)
#         self.stack.addWidget(self.main_page)

#     def show_goal_detail(self, name):
#         if name not in self.goal_details:
#             detail = GoalDetailView(name, self.go_back_to_main)
#             self.goal_details[name] = detail
#             self.stack.addWidget(detail)
#         self.stack.setCurrentWidget(self.goal_details[name])

#     def go_back_to_main(self):
#         self.stack.setCurrentWidget(self.main_page)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.resize(600, 400)
#     window.show()
#     sys.exit(app.exec_())

#---------------------------------------------------------------------------------------------------------------------------------------------#
# import sys
# import json
# import os
# from PyQt5.QtWidgets import (
#     QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
#     QLabel, QPushButton, QProgressBar, QStackedWidget, QLineEdit,
#     QMessageBox, QScrollArea, QFormLayout, QSpacerItem, QSizePolicy
# )
# from PyQt5.QtCore import Qt

# DB_FILE = "goals.json"


# def load_goals():
#     if os.path.exists(DB_FILE):
#         with open(DB_FILE, 'r') as f:
#             return json.load(f)
#     return []


# def save_goals(goals):
#     with open(DB_FILE, 'w') as f:
#         json.dump(goals, f, indent=4)


# class GoalCard(QWidget):
#     def __init__(self, goal, switch_to_detail):
#         super().__init__()
#         self.goal = goal
#         layout = QVBoxLayout()
#         self.setLayout(layout)

#         layout.addWidget(QLabel(f"<b>{goal['name']}</b>"))
#         layout.addWidget(QLabel(f"Target: ৳{goal['target']}"))

#         # progress = QProgressBar()
#         # progress.setValue(int((goal['saved'] / goal['target']) * 100))
#         # layout.addWidget(progress)

#         self.setStyleSheet("border: 1px solid gray; padding: 10px; border-radius: 10px;")
#         self.mousePressEvent = lambda e: switch_to_detail(goal['name'])


# class GoalDetailView(QWidget):
#     def __init__(self, goal, go_back_callback):
#         super().__init__()
#         self.goal = goal
#         self.go_back_callback = go_back_callback

#         layout = QVBoxLayout()
#         self.setLayout(layout)

#         progress = QProgressBar()
#         progress.setValue(int((goal['saved'] / goal['target']) * 100))
#         layout.addWidget(progress)

#         layout.addWidget(QLabel(f"<h2>{goal['name']}</h2>"))
#         layout.addWidget(QLabel(f"Target: ৳{goal['target']}"))
#         layout.addWidget(QLabel(f"Saved: ৳{goal['saved']}"))
#         layout.addWidget(QLabel(f"Lent Out: ৳{goal.get('lent', 0)}"))

#         layout.addWidget(QPushButton("Add Money"))
#         layout.addWidget(QPushButton("Lend Money"))
#         layout.addWidget(QPushButton("Receive Money"))

#         back_btn = QPushButton("Go Back")
#         back_btn.clicked.connect(go_back_callback)
#         layout.addWidget(back_btn)


# class CreateGoalView(QWidget):
#     def __init__(self, create_callback):
#         super().__init__()
#         self.create_callback = create_callback

#         layout = QVBoxLayout()
#         self.setLayout(layout)

#         self.form_layout = QFormLayout()
#         self.goal_name_input = QLineEdit()
#         self.target_input = QLineEdit()
#         self.saved_input = QLineEdit()

#         self.form_layout.addRow("Goal Name:", self.goal_name_input)
#         self.form_layout.addRow("Target Amount:", self.target_input)
#         self.form_layout.addRow("Saved Amount:", self.saved_input)

#         layout.addLayout(self.form_layout)

#         self.create_btn = QPushButton("Create Goal")
#         self.create_btn.clicked.connect(self.handle_create)
#         layout.addWidget(self.create_btn)

#         layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

#     def handle_create(self):
#         name = self.goal_name_input.text().strip()
#         try:
#             target = float(self.target_input.text())
#             saved = float(self.saved_input.text())
#         except ValueError:
#             QMessageBox.warning(self, "Input Error", "Please enter valid numbers for target and saved amount.")
#             return

#         if not name:
#             QMessageBox.warning(self, "Input Error", "Goal name cannot be empty.")
#             return

#         goal = {"name": name, "target": target, "saved": saved, "lent": 0}
#         self.create_callback(goal)


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("GoalSaver")
#         self.stack = QStackedWidget()
#         self.setCentralWidget(self.stack)

#         self.goals = load_goals()
#         self.goal_views = {}

#         self.main_page = QWidget()
#         self.main_layout = QVBoxLayout(self.main_page)

#         scroll = QScrollArea()
#         scroll.setWidgetResizable(True)
#         self.scroll_content = QWidget()
#         self.goal_list_layout = QHBoxLayout(self.scroll_content)
#         scroll.setWidget(self.scroll_content)

#         self.main_layout.addWidget(QLabel("<h1>Select a Goal</h1>", alignment=Qt.AlignCenter))
#         self.main_layout.addWidget(scroll)

#         self.create_button = QPushButton("+ Create New Goal")
#         self.create_button.clicked.connect(self.show_create_goal)
#         self.goal_list_layout.addWidget(self.create_button)

#         self.stack.addWidget(self.main_page)
#         self.populate_goals()

#     def populate_goals(self):
#         for goal in self.goals:
#             card = GoalCard(goal, self.show_goal_detail)
#             self.goal_list_layout.addWidget(card)

#     def show_goal_detail(self, name):
#         goal = next((g for g in self.goals if g['name'] == name), None)
#         if not goal:
#             return
#         if name not in self.goal_views:
#             view = GoalDetailView(goal, self.go_back)
#             self.goal_views[name] = view
#             self.stack.addWidget(view)
#         self.stack.setCurrentWidget(self.goal_views[name])

#     def show_create_goal(self):
#         self.create_view = CreateGoalView(self.add_goal)
#         self.stack.addWidget(self.create_view)
#         self.stack.setCurrentWidget(self.create_view)

#     def add_goal(self, goal):
#         self.goals.append(goal)
#         save_goals(self.goals)
#         self.stack.removeWidget(self.create_view)
#         card = GoalCard(goal, self.show_goal_detail)
#         self.goal_list_layout.insertWidget(len(self.goal_list_layout.children()) - 1, card)
#         self.stack.setCurrentWidget(self.main_page)

#     def go_back(self):
#         self.stack.setCurrentWidget(self.main_page)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.resize(700, 500)
#     window.show()
#     sys.exit(app.exec_())

#--------------------------------------------------------------------------------------------------------------------------------------#

import sys
import json
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar,
    QStackedWidget, QLineEdit, QMessageBox, QScrollArea,
    QFormLayout, QSpacerItem, QSizePolicy, QWidget,
)
from PyQt5.QtCore import Qt, QSize

DB_FILE = "goals.json"

def load_goals():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return []

def save_goals(goals):
    with open(DB_FILE, 'w') as f:
        json.dump(goals, f, indent=4)

class GoalCard(QtWidgets.QWidget):
    def __init__(self, goal, switch_to_detail):
        super().__init__()
        self.goal = goal
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QtWidgets.QLabel(f"<b>{goal['name']}</b>"))
        layout.addWidget(QtWidgets.QLabel(f"Target: ৳{goal['target']}"))

        progress = QtWidgets.QProgressBar()
        progress.setValue(int((goal['saved'] / goal['target']) * 100))
        layout.addWidget(progress)

        self.setStyleSheet("border: 1px solid gray; padding: 10px; border-radius: 10px;")
        self.mousePressEvent = lambda e: switch_to_detail(goal['name'])

class GoalDetailView(QtWidgets.QWidget):
    def __init__(self, goal, go_back_callback):
        super().__init__()
        self.goal = goal
        self.go_back_callback = go_back_callback

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        progress = QtWidgets.QProgressBar()
        progress.setValue(int((goal['saved'] / goal['target']) * 100))
        layout.addWidget(progress)

        layout.addWidget(QtWidgets.QLabel(f"<h2>{goal['name']}</h2>"))
        layout.addWidget(QtWidgets.QLabel(f"Target: ৳{goal['target']}"))
        layout.addWidget(QtWidgets.QLabel(f"Saved: ৳{goal['saved']}"))
        layout.addWidget(QtWidgets.QLabel(f"Lent Out: ৳{goal.get('lent', 0)}"))

        layout.addWidget(QtWidgets.QPushButton("Add Money"))
        layout.addWidget(QtWidgets.QPushButton("Lend Money"))
        layout.addWidget(QtWidgets.QPushButton("Receive Money"))

        back_btn = QtWidgets.QPushButton("Go Back")
        back_btn.clicked.connect(go_back_callback)
        layout.addWidget(back_btn)

class CreateGoalView(QtWidgets.QWidget):
    def __init__(self, create_callback):
        super().__init__()
        self.create_callback = create_callback

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.form_layout = QFormLayout()
        self.goal_name_input = QLineEdit()
        self.target_input = QLineEdit()
        self.saved_input = QLineEdit()

        self.form_layout.addRow("Goal Name:", self.goal_name_input)
        self.form_layout.addRow("Target Amount:", self.target_input)
        self.form_layout.addRow("Saved Amount:", self.saved_input)

        layout.addLayout(self.form_layout)

        self.create_btn = QPushButton("Create Goal")
        self.create_btn.clicked.connect(self.handle_create)
        layout.addWidget(self.create_btn)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def handle_create(self):
        name = self.goal_name_input.text().strip()
        try:
            target = float(self.target_input.text())
            saved = float(self.saved_input.text())
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numbers for target and saved amount.")
            return

        if not name:
            QMessageBox.warning(self, "Input Error", "Goal name cannot be empty.")
            return

        goal = {"name": name, "target": target, "saved": saved, "lent": 0}
        self.create_callback(goal)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: rgb(52, 58, 60);")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.stack = QStackedWidget()

        # Main Layout
        self.main_page = QtWidgets.QWidget()
        self.main_layout = QVBoxLayout(self.main_page)
        self.header = QLabel("Add/Select a Goal")
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.header.setFont(font)
        self.header.setStyleSheet("color: rgb(209, 211, 213);")
        self.header.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.goal_list_layout = QHBoxLayout(self.scroll_content)
        scroll.setWidget(self.scroll_content)

        self.main_layout.addWidget(scroll)
        self.create_goal_btn = QPushButton("+ Create New Goal")
        self.create_goal_btn.clicked.connect(self.show_create_goal)
        self.goal_list_layout.addWidget(self.create_goal_btn)

        self.stack.addWidget(self.main_page)
        self.stack.setCurrentWidget(self.main_page)

        layout = QVBoxLayout(self.centralwidget)
        layout.addWidget(self.stack)

        MainWindow.setCentralWidget(self.centralwidget)

        self.goals = load_goals()
        self.goal_views = {}
        self.populate_goals()

    def populate_goals(self):
        for goal in self.goals:
            card = GoalCard(goal, self.show_goal_detail)
            self.goal_list_layout.insertWidget(self.goal_list_layout.count() - 1, card)

    def show_goal_detail(self, name):
        goal = next((g for g in self.goals if g['name'] == name), None)
        if not goal:
            return
        if name not in self.goal_views:
            view = GoalDetailView(goal, self.go_back)
            self.goal_views[name] = view
            self.stack.addWidget(view)
        self.stack.setCurrentWidget(self.goal_views[name])

    def show_create_goal(self):
        self.create_view = CreateGoalView(self.add_goal)
        self.stack.addWidget(self.create_view)
        self.stack.setCurrentWidget(self.create_view)

    def add_goal(self, goal):
        self.goals.append(goal)
        save_goals(self.goals)
        self.stack.removeWidget(self.create_view)
        card = GoalCard(goal, self.show_goal_detail)
        self.goal_list_layout.insertWidget(self.goal_list_layout.count() - 1, card)
        self.stack.setCurrentWidget(self.main_page)

    def go_back(self):
        self.stack.setCurrentWidget(self.main_page)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

