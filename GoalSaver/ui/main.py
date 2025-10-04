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

        progress = QtWidgets.QProgressBar()
        percent = int((goal['saved'] / goal['target']) * 100) if goal['target'] else 0
        progress.setValue(min(percent, 100))
        # layout.addWidget(progress)

        self.setStyleSheet("border: 1px solid gray; padding: 10px; border-radius: 10px;")
        self.mousePressEvent = lambda e: switch_to_detail(goal['name'])

class GoalDetailView(QtWidgets.QWidget):
    def __init__(self, goal, go_back_callback, remove_goal_callback, update_goal_callback):
        super().__init__()
        self.goal = goal
        self.go_back_callback = go_back_callback
        self.remove_goal_callback = remove_goal_callback
        self.update_goal_callback = update_goal_callback

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.progress = QtWidgets.QProgressBar()
        layout.addWidget(self.progress)

        self.info_label = QtWidgets.QLabel()
        layout.addWidget(self.info_label)

        self.update_info()

        add_money_btn = QtWidgets.QPushButton("➕ Add Money")
        add_money_btn.setStyleSheet("background-color: green; color: white;")
        add_money_btn.clicked.connect(self.add_money)
        layout.addWidget(add_money_btn)

        lend_money_btn = QtWidgets.QPushButton("💱 Lend Money")
        lend_money_btn.setStyleSheet("background-color: orange; color: white;")
        lend_money_btn.clicked.connect(self.lend_money)
        layout.addWidget(lend_money_btn)

        receive_money_btn = QtWidgets.QPushButton("🤝 Receive Money")
        receive_money_btn.setStyleSheet("background-color: blue; color: white;")
        receive_money_btn.clicked.connect(self.receive_money)
        layout.addWidget(receive_money_btn)

        remove_btn = QtWidgets.QPushButton("❌ Remove Goal")
        remove_btn.setStyleSheet("background-color: red; color: white;")
        remove_btn.clicked.connect(self.confirm_remove)
        layout.addWidget(remove_btn)

        back_btn = QtWidgets.QPushButton("Go Back")
        back_btn.clicked.connect(go_back_callback)
        layout.addWidget(back_btn)

    def update_info(self):
        percent = int((self.goal['saved'] / self.goal['target']) * 100) if self.goal['target'] else 0
        self.progress.setValue(min(percent, 100))
        self.info_label.setText(
            f"<h2>{self.goal['name']}</h2>"
            f"<p>Target: ৳{self.goal['target']}</p>"
            f"<p>Saved: ৳{self.goal['saved']}</p>"
            f"<p>Lent Out: ৳{self.goal.get('lent', 0)}</p>"
        )
        if self.goal['saved'] >= self.goal['target']:
            QMessageBox.information(self, "Goal Completed!", f"Congratulations! You have completed the goal: {self.goal['name']}.")

    def confirm_remove(self):
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete the goal '{self.goal['name']}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.remove_goal_callback(self.goal['name'])

    def add_money(self):
        amount, ok = QtWidgets.QInputDialog.getDouble(self, "Add Money", "Amount:", 0, 0)
        if ok:
            self.goal['saved'] += amount
            save_goals(ui.goals)
            self.update_info()
            self.update_goal_callback()

    def lend_money(self):
        amount, ok = QtWidgets.QInputDialog.getDouble(self, "Lend Money", "Amount:", 0, 0)
        if ok:
            self.goal['saved'] -= amount
            self.goal['lent'] += amount
            save_goals(ui.goals)
            self.update_info()
            self.update_goal_callback()

    def receive_money(self):
        amount, ok = QtWidgets.QInputDialog.getDouble(self, "Receive Money", "Amount:", 0, 0)
        if ok:
            self.goal['saved'] += amount
            self.goal['lent'] -= amount
            save_goals(ui.goals)
            self.update_info()
            self.update_goal_callback()

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
        MainWindow.setWindowTitle("Goal Saver")
        MainWindow.setWindowIcon(QtGui.QIcon("Logo.png"))
        MainWindow.setStyleSheet("background-color: rgb(52, 58, 60); color: rgb(209, 211, 213);")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.stack = QStackedWidget()

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
            view = GoalDetailView(goal, self.go_back, self.remove_goal, self.refresh_main_page)
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

    def remove_goal(self, name):
        self.goals = [g for g in self.goals if g['name'] != name]
        save_goals(self.goals)
        self.stack.setCurrentWidget(self.main_page)

        for i in reversed(range(self.goal_list_layout.count())):
            widget = self.goal_list_layout.itemAt(i).widget()
            if isinstance(widget, GoalCard) and widget.goal['name'] == name:
                self.goal_list_layout.removeWidget(widget)
                widget.setParent(None)

        if name in self.goal_views:
            view = self.goal_views[name]
            self.stack.removeWidget(view)
            view.setParent(None)
            del self.goal_views[name]

    def refresh_main_page(self):
        for i in reversed(range(self.goal_list_layout.count() - 1)):
            widget = self.goal_list_layout.itemAt(i).widget()
            self.goal_list_layout.removeWidget(widget)
            widget.setParent(None)
        self.populate_goals()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
