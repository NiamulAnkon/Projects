import json
import os
import sys
import webbrowser
import shutil
from datetime import datetime, date, time, timedelta

from PyQt5.QtCore import Qt, QTimer, QStandardPaths, QDate
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QCalendarWidget, QListWidget, QListWidgetItem, QTextEdit, QLineEdit,
    QPushButton, QLabel, QMessageBox, QAction, QFileDialog, QDialog, QFormLayout,
    QDialogButtonBox, QComboBox, QGroupBox, QToolBar, QSystemTrayIcon, QMenu
)

APP_NAME = "Event Manager"
ORG_NAME = "ATHECAL"

# ---------- Storage helpers ----------

def app_data_dir():
    base = QStandardPaths.writableLocation(QStandardPaths.AppConfigLocation)
    # e.g., ~/.config/ATHECAL/Event Manager
    p = os.path.join(base, ORG_NAME, APP_NAME)
    os.makedirs(p, exist_ok=True)
    return p

DATA_PATH = os.path.join(app_data_dir(), "data.json")
BACKUP_DIR = os.path.join(app_data_dir(), "backups")

DEFAULT_DATA = {
    "events": {},  # {"YYYY-MM-DD": [ {"title":"...","notes":"...","resources":[{"name":"..","type":"text|link","content":"..."}]} ]}
    "settings": {"theme": "light", "notify_hour": 9}
}


def load_data():
    if not os.path.exists(DATA_PATH):
        return json.loads(json.dumps(DEFAULT_DATA))
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = json.loads(json.dumps(DEFAULT_DATA))
    # ensure keys
    data.setdefault("events", {})
    data.setdefault("settings", {"theme": "light", "notify_hour": 9})
    data["settings"].setdefault("theme", "light")
    data["settings"].setdefault("notify_hour", 9)
    return data


def save_data(data):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def make_backup():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    dst = os.path.join(BACKUP_DIR, f"backup-{ts}.json")
    shutil.copy2(DATA_PATH, dst) if os.path.exists(DATA_PATH) else save_data(DEFAULT_DATA)
    return dst


# ---------- Dialogs ----------

class EventDialog(QDialog):
    def __init__(self, parent=None, title="", notes=""):
        super().__init__(parent)
        self.setWindowTitle("Event")
        self.setModal(True)
        self.title_edit = QLineEdit(title)
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlainText(notes)

        form = QFormLayout()
        form.addRow("Title", self.title_edit)
        form.addRow("Notes", self.notes_edit)

        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(btns)

    def get_values(self):
        return self.title_edit.text().strip(), self.notes_edit.toPlainText().strip()


class ResourceDialog(QDialog):
    def __init__(self, parent=None, name="", rtype="text", content=""):
        super().__init__(parent)
        self.setWindowTitle("Resource")
        self.setModal(True)
        self.name_edit = QLineEdit(name)
        self.type_combo = QComboBox()
        self.type_combo.addItems(["text", "link"])  # simple
        if rtype in ("text", "link"):
            self.type_combo.setCurrentText(rtype)
        self.content_edit = QTextEdit()
        self.content_edit.setPlainText(content)

        form = QFormLayout()
        form.addRow("Name", self.name_edit)
        form.addRow("Type", self.type_combo)
        form.addRow("Content", self.content_edit)

        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(btns)

    def get_values(self):
        return (
            self.name_edit.text().strip(),
            self.type_combo.currentText(),
            self.content_edit.toPlainText().strip(),
        )


class SettingsDialog(QDialog):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.data = data

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["light", "dark"]) 
        self.theme_combo.setCurrentText(self.data["settings"].get("theme", "light"))

        self.hour_combo = QComboBox()
        for h in range(0, 24):
            self.hour_combo.addItem(f"{h:02d}:00", h)
        self.hour_combo.setCurrentIndex(self.data["settings"].get("notify_hour", 9))

        export_btn = QPushButton("Backup / Export…")
        export_btn.clicked.connect(self.export_backup)

        import_btn = QPushButton("Import / Restore…")
        import_btn.clicked.connect(self.import_backup)

        wipe_btn = QPushButton("Wipe All Data…")
        wipe_btn.clicked.connect(self.wipe_data)

        form = QFormLayout()
        form.addRow("Theme", self.theme_combo)
        form.addRow("Daily Reminder Time", self.hour_combo)

        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)

        tools = QHBoxLayout()
        tools.addWidget(export_btn)
        tools.addWidget(import_btn)
        tools.addWidget(wipe_btn)
        layout.addLayout(tools)
        layout.addWidget(btns)

    def export_backup(self):
        os.makedirs(BACKUP_DIR, exist_ok=True)
        suggested = os.path.join(BACKUP_DIR, "events-backup.json")
        path, _ = QFileDialog.getSaveFileName(self, "Save Backup", suggested, "JSON (*.json)")
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            QMessageBox.information(self, "Backup", f"Saved backup to:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Backup Failed", str(e))

    def import_backup(self):
        path, _ = QFileDialog.getOpenFileName(self, "Import Backup", BACKUP_DIR, "JSON (*.json)")
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                incoming = json.load(f)
            # basic validation
            if not isinstance(incoming, dict) or "events" not in incoming:
                raise ValueError("Invalid backup format")
            self.data.clear()
            self.data.update(incoming)
            save_data(self.data)
            QMessageBox.information(self, "Import", "Data restored. Restart app to ensure full refresh.")
        except Exception as e:
            QMessageBox.critical(self, "Import Failed", str(e))

    def wipe_data(self):
        if QMessageBox.question(self, "Confirm Wipe", "This will delete all events and settings. Continue?") == QMessageBox.Yes:
            self.data.clear()
            self.data.update(json.loads(json.dumps(DEFAULT_DATA)))
            save_data(self.data)
            QMessageBox.information(self, "Wipe", "All data reset.")

    def get_values(self):
        return self.theme_combo.currentText(), int(self.hour_combo.currentData())


# ---------- Main Window ----------

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(1000, 650)
        self.setWindowIcon(QIcon.fromTheme("office-calendar"))

        self.data = load_data()

        # UI
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.selectionChanged.connect(self.refresh_event_list)

        self.event_list = QListWidget()
        self.event_list.currentRowChanged.connect(self.refresh_event_details)

        self.event_title = QLabel("")
        self.event_title.setStyleSheet("font-weight:600; font-size:16px;")
        self.notes_view = QTextEdit()
        self.notes_view.setReadOnly(True)

        self.resources_list = QListWidget()
        self.resources_list.itemDoubleClicked.connect(self.open_resource)

        # Buttons
        self.add_event_btn = QPushButton("Add Event")
        self.edit_event_btn = QPushButton("Edit Event")
        self.del_event_btn = QPushButton("Delete Event")

        self.add_res_btn = QPushButton("Add Resource")
        self.edit_res_btn = QPushButton("Edit Resource")
        self.del_res_btn = QPushButton("Delete Resource")

        self.add_event_btn.clicked.connect(self.add_event)
        self.edit_event_btn.clicked.connect(self.edit_event)
        self.del_event_btn.clicked.connect(self.delete_event)

        self.add_res_btn.clicked.connect(self.add_resource)
        self.edit_res_btn.clicked.connect(self.edit_resource)
        self.del_res_btn.clicked.connect(self.delete_resource)

        # Layouts
        left = QWidget(); left_v = QVBoxLayout(left); left_v.addWidget(self.calendar)

        right_top = QWidget(); rt_v = QVBoxLayout(right_top)
        rt_v.addWidget(QLabel("Events on selected date:"))
        rt_v.addWidget(self.event_list)
        ev_btns = QHBoxLayout();
        for b in (self.add_event_btn, self.edit_event_btn, self.del_event_btn):
            ev_btns.addWidget(b)
        rt_v.addLayout(ev_btns)

        right_bottom = QWidget(); rb_v = QVBoxLayout(right_bottom)
        gb = QGroupBox("Selected Event Details")
        gb_v = QVBoxLayout(gb)
        gb_v.addWidget(self.event_title)
        gb_v.addWidget(QLabel("Notes:"))
        gb_v.addWidget(self.notes_view)
        gb_v.addWidget(QLabel("Resources (double‑click to open links):"))
        gb_v.addWidget(self.resources_list)
        res_btns = QHBoxLayout()
        for b in (self.add_res_btn, self.edit_res_btn, self.del_res_btn):
            res_btns.addWidget(b)
        gb_v.addLayout(res_btns)
        rb_v.addWidget(gb)

        right = QSplitter(Qt.Vertical)
        right.addWidget(right_top)
        right.addWidget(right_bottom)
        right.setSizes([300, 350])

        splitter = QSplitter()
        splitter.addWidget(left)
        splitter.addWidget(right)
        splitter.setSizes([350, 650])

        container = QWidget(); c_v = QVBoxLayout(container); c_v.addWidget(splitter)
        self.setCentralWidget(container)

        # Toolbar & Menu
        tb = QToolBar("Main")
        tb.setMovable(False)
        self.addToolBar(tb)

        act_settings = QAction("Settings", self)
        act_settings.triggered.connect(self.open_settings)
        act_backup = QAction("Quick Backup", self)
        act_backup.triggered.connect(self.quick_backup)
        act_quit = QAction("Quit", self)
        act_quit.triggered.connect(self.close)

        tb.addAction(act_settings)
        tb.addAction(act_backup)

        m = self.menuBar().addMenu("File")
        m.addAction(act_settings)
        m.addAction(act_backup)
        m.addSeparator()
        m.addAction(act_quit)

        # Tray
        self.tray = QSystemTrayIcon(self.windowIcon(), self)
        tray_menu = QMenu()
        tray_menu.addAction("Show", self.showNormal)
        tray_menu.addAction("Quit", self.close)
        self.tray.setContextMenu(tray_menu)
        self.tray.show()

        self.apply_theme(self.data["settings"].get("theme", "light"))

        # Initial load
        self.calendar.setSelectedDate(QDate.currentDate())
        self.refresh_event_list()

        # Notifications now and schedule daily
        QTimer.singleShot(500, self.notify_today)
        self.schedule_daily_notification()

    # ---------- Theme ----------
    def apply_theme(self, theme):
        app = QApplication.instance()
        if theme == "dark":
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(35, 35, 35))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.black)
            app.setPalette(palette)
        else:
            app.setPalette(app.style().standardPalette())

    # ---------- Notifications ----------
    def notify_today(self):
        today_key = date.today().isoformat()
        todays = self.data.get("events", {}).get(today_key, [])
        if not todays:
            return
        body_lines = [f"• {e.get('title','(No title)')}" for e in todays]
        msg = "\n".join(body_lines[:6])
        overflow = len(body_lines) - 6
        if overflow > 0:
            msg += f"\n…and {overflow} more"
        self.tray.showMessage("Today's Events", msg, QSystemTrayIcon.Information, 12000)

    def schedule_daily_notification(self):
        # fire at next settings hour (local time)
        target_hour = int(self.data["settings"].get("notify_hour", 9))
        now = datetime.now()
        target = datetime.combine(date.today(), time(target_hour, 0))
        if now >= target:
            target = target + timedelta(days=1)
        msec = int((target - now).total_seconds() * 1000)
        self.daily_timer = QTimer(self)
        self.daily_timer.setSingleShot(True)
        self.daily_timer.timeout.connect(self.on_daily_timer)
        self.daily_timer.start(max(msec, 1000))

    def on_daily_timer(self):
        self.notify_today()
        self.schedule_daily_notification()  # schedule next

    # ---------- Data helpers ----------
    def selected_key(self):
        qd = self.calendar.selectedDate()
        return date(qd.year(), qd.month(), qd.day()).isoformat()

    def events_for_selected(self):
        return self.data.setdefault("events", {}).setdefault(self.selected_key(), [])

    def refresh_event_list(self):
        lst = self.event_list
        lst.clear()
        for ev in self.events_for_selected():
            item = QListWidgetItem(ev.get("title", "(No title)"))
            lst.addItem(item)
        if lst.count():
            lst.setCurrentRow(0)
        else:
            self.refresh_event_details(-1)

    def refresh_event_details(self, row):
        events = self.events_for_selected()
        if 0 <= row < len(events):
            ev = events[row]
            self.event_title.setText(ev.get("title", "(No title)") )
            self.notes_view.setPlainText(ev.get("notes", ""))
            self.resources_list.clear()
            for r in ev.get("resources", []):
                label = f"{r.get('name','(no name)')}  —  {r.get('type','text')}"
                item = QListWidgetItem(label)
                item.setData(Qt.UserRole, r)
                self.resources_list.addItem(item)
        else:
            self.event_title.setText("")
            self.notes_view.clear()
            self.resources_list.clear()

    # ---------- Event CRUD ----------
    def add_event(self):
        dlg = EventDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            title, notes = dlg.get_values()
            new_ev = {"title": title or "Untitled", "notes": notes, "resources": []}
            self.events_for_selected().append(new_ev)
            save_data(self.data)
            self.refresh_event_list()

    def edit_event(self):
        row = self.event_list.currentRow()
        events = self.events_for_selected()
        if row < 0 or row >= len(events):
            return
        ev = events[row]
        dlg = EventDialog(self, ev.get("title",""), ev.get("notes",""))
        if dlg.exec_() == QDialog.Accepted:
            title, notes = dlg.get_values()
            ev["title"] = title or "Untitled"
            ev["notes"] = notes
            save_data(self.data)
            self.refresh_event_list()
            self.event_list.setCurrentRow(row)

    def delete_event(self):
        row = self.event_list.currentRow()
        events = self.events_for_selected()
        if row < 0 or row >= len(events):
            return
        if QMessageBox.question(self, "Delete Event", "Delete selected event?") == QMessageBox.Yes:
            events.pop(row)
            save_data(self.data)
            self.refresh_event_list()

    # ---------- Resource CRUD ----------
    def current_event(self):
        row = self.event_list.currentRow()
        events = self.events_for_selected()
        if 0 <= row < len(events):
            return events[row]
        return None

    def add_resource(self):
        ev = self.current_event()
        if not ev:
            return
        dlg = ResourceDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            name, rtype, content = dlg.get_values()
            ev.setdefault("resources", []).append({"name": name or "Resource", "type": rtype, "content": content})
            save_data(self.data)
            self.refresh_event_details(self.event_list.currentRow())

    def edit_resource(self):
        ev = self.current_event()
        if not ev:
            return
        idx = self.resources_list.currentRow()
        res = ev.get("resources", [])
        if 0 <= idx < len(res):
            r = res[idx]
            dlg = ResourceDialog(self, r.get("name",""), r.get("type","text"), r.get("content",""))
            if dlg.exec_() == QDialog.Accepted:
                name, rtype, content = dlg.get_values()
                r.update({"name": name or "Resource", "type": rtype, "content": content})
                save_data(self.data)
                self.refresh_event_details(self.event_list.currentRow())

    def delete_resource(self):
        ev = self.current_event()
        if not ev:
            return
        idx = self.resources_list.currentRow()
        res = ev.get("resources", [])
        if 0 <= idx < len(res):
            if QMessageBox.question(self, "Delete Resource", "Delete selected resource?") == QMessageBox.Yes:
                res.pop(idx)
                save_data(self.data)
                self.refresh_event_details(self.event_list.currentRow())

    def open_resource(self, item: QListWidgetItem):
        r = item.data(Qt.UserRole)
        if not r:
            return
        if r.get("type") == "link":
            url = r.get("content", "").strip()
            if url:
                webbrowser.open(url)
        else:
            # Show text in a simple dialog
            QMessageBox.information(self, r.get("name","Text"), r.get("content",""))

    # ---------- Settings / Backup ----------
    def open_settings(self):
        dlg = SettingsDialog(self, self.data)
        if dlg.exec_() == QDialog.Accepted:
            theme, hour = dlg.get_values()
            self.data["settings"]["theme"] = theme
            self.data["settings"]["notify_hour"] = int(hour)
            save_data(self.data)
            self.apply_theme(theme)
            self.schedule_daily_notification()

    def quick_backup(self):
        path = make_backup()
        QMessageBox.information(self, "Backup", f"Backup saved to\n{path}")

    # Close to tray behavior (optional, stays open in tray)
    def closeEvent(self, e):
        res = QMessageBox.question(self, "Quit", "Quit the application? (It will also exit the tray)")
        if res == QMessageBox.Yes:
            e.accept()
        else:
            e.ignore()


def main():
    QApplication.setApplicationName(APP_NAME)
    QApplication.setOrganizationName(ORG_NAME)
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()