import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import Qt
from main_window import Ui_MainWindow
from settings_window import SettingsWindow  
from logic import *
from dialogs import AddEventDialog, confirm_delete
from resource_window import ResourceWindow, confirm_resource_delete


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.refresh_events()
        self.refresh_resources()
        self.update_todays_events()

        # Load settings & events
        self.settings = load_settings()
        self.events = load_events()

        # Apply theme from settings
        if "theme" in self.settings:
            apply_theme(self, self.settings["theme"])

        # Connect buttons (make sure these names match your .ui)
        self.ui.setting_btn.clicked.connect(self.open_settings)
        self.ui.add_event_btn.clicked.connect(self.add_event)
        self.ui.dlt_event_btn.clicked.connect(self.delete_event)
        #----------------------------------------------------------------------#
        self.ui.add_resource_btn.clicked.connect(self.add_resource)  
        self.ui.edit_resource_btn.clicked.connect(self.edit_resource)
        self.ui.dlt_resource_btn.clicked.connect(self.remove_resource)

    def refresh_events(self):
        """Reload events into the list widget."""
        self.ui.event_list.clear()
        self.events = load_events()  # reload fresh
        for ev in self.events:
            title = ev.get("title", "(no title)")
            date = ev.get("date", "")
            self.ui.event_list.addItem(f"{date} — {title}")

    def update_todays_events(self):
        events = load_events()
        todays_event = get_todays_events(events)
        if not todays_event:
            self.ui.todays_event.setText("No events for today.")
        else:
            text = ""
            for event in todays_event:
                text += f"- {event['title']} at {event.get('time', 'All Day')}\n"
            self.ui.todays_event.setText(text.strip())


    def refresh_resources(self):
        """Reload resources into the list widget."""
        self.ui.resource.clear()
        resources = load_resources()
        for res in resources:
            rtype = res.get("type", "(no type)")
            value = res.get("value", "(no value)")
            self.ui.resource.addItem(f"{rtype}: {value}")
    
    def add_resource(self):
        dlg = ResourceWindow(self)
        if dlg.exec_():
            self.refresh_resources()

    def remove_resource(self):
        row = self.ui.resource.currentRow()
        if row >= 0:
            resources = load_resources()
            resource = resources[row]
            if confirm_resource_delete(self, resource):
                remove_resource(row)
                self.refresh_resources()

    def edit_resource(self):
        row = self.ui.resource.currentRow()
        if row >= 0:
            resources = load_resources()
            resource = resources[row]
            dlg = ResourceWindow(self)
            dlg.type_box.setCurrentText(resource.get("type", "link"))
            dlg.value_input.setText(resource.get("value", ""))
            if dlg.exec_():
                new_type = dlg.type_box.currentText()
                new_value = dlg.value_input.text().strip()
                if new_value:
                    edit_resource(row, new_type, new_value)
                    self.refresh_resources()
#---------------------------------------------------------------------#
    def add_event(self):
        dlg = AddEventDialog(self)
        if dlg.exec_():
            self.refresh_events()

    def edit_event(self):
        row = self.ui.event_list.currentRow()
        if row >= 0:
            event = self.events[row]
            dlg = AddEventDialog(self, event)
            if dlg.exec_():
                self.refresh_events()

    def delete_event(self):
        row = self.ui.event_list.currentRow()
        if row >= 0:
            event = self.events[row]
            if confirm_delete(self, event):
                self.refresh_events()
    def load_events(self):
        self.ui.event_list.clear()
        events = load_events()
        for event in events:
            self.ui.event_list.addItem(f"{event['date']} — {event['title']}")

    def open_settings(self):
        """Open settings window from your settings_window module."""
        # Your SettingsWindow might accept different constructor args.
        # Try common signatures gracefully:
        dlg = None
        try:
            dlg = SettingsWindow(self)
        except TypeError:
            try:
                dlg = SettingsWindow(self.settings)     # (settings)
            except TypeError:
                dlg = SettingsWindow(self)              # (parent)
        self.setting_window = dlg

        # If your dialog emits theme_changed, connect it
        # if hasattr(self.setting_window, "theme_changed"):
        #     self.setting_window.theme_changed.connect(self.change_theme)

        self.setting_window.show()

    # def change_theme(self, theme):
    #     """Apply theme & persist it."""
    #     apply_theme(self, theme)
    #     self.settings["theme"] = theme
    #     save_settings(self.settings)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())