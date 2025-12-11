from PyQt5 import QtCore, QtGui, QtWidgets
import os
import shutil
from pathlib import Path
import icons_rc


# Worker thread for copying files/folders so UI stays responsive
class CopyWorker(QtCore.QThread):
    progress = QtCore.pyqtSignal(int)
    finished = QtCore.pyqtSignal(list)  # list of copied names
    errors = QtCore.pyqtSignal(list)     # list of error messages

    def __init__(self, items, dest_dir, parent=None):
        super().__init__(parent)
        self.items = [Path(i) for i in items]
        self.dest_dir = Path(dest_dir)

    def run(self):
        copied = []
        errors = []
        total = len(self.items)
        for idx, src in enumerate(self.items):
            try:
                if src.is_dir():
                    dest = self.dest_dir.joinpath(src.name)
                    dest = self._unique_path(dest)
                    shutil.copytree(src, dest)
                    copied.append(dest.name)
                elif src.is_file():
                    dest = self.dest_dir.joinpath(src.name)
                    dest = self._unique_path(dest)
                    shutil.copy2(src, dest)
                    copied.append(dest.name)
                else:
                    errors.append(f"{src}: not found")
            except Exception as e:
                errors.append(f"{src.name}: {e}")
            # emit progress as count completed
            self.progress.emit(idx + 1)

        if errors:
            self.errors.emit(errors)
        self.finished.emit(copied)

    def _unique_path(self, dest: Path) -> Path:
        if not dest.exists():
            return dest
        stem = dest.stem
        suffix = dest.suffix
        i = 1
        while True:
            candidate = dest.with_name(f"{stem}({i}){suffix}")
            if not candidate.exists():
                return candidate
            i += 1


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, username):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(950, 600)
        MainWindow.setStyleSheet("background-color: rgb(30, 30, 47);")

        # Keep a reference to the parent/main window
        self.MainWindow = MainWindow

        # Central widget + Main layout
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.central_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.central_layout.setContentsMargins(10, 10, 10, 10)
        self.central_layout.setSpacing(10)

        # ===== HEADER =====
        self.header_frame = QtWidgets.QFrame(self.centralwidget)
        self.header_frame.setStyleSheet("background-color: rgb(23, 28, 45); border-radius: 8px;")
        self.header_layout = QtWidgets.QHBoxLayout(self.header_frame)
        self.header_layout.setContentsMargins(15, 5, 15, 5)

        self.name_text = QtWidgets.QLabel("📁 NebulaShare", self.header_frame)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.name_text.setFont(font)
        self.name_text.setStyleSheet("color: white;")
        self.header_layout.addWidget(self.name_text, alignment=QtCore.Qt.AlignLeft)

        self.header_layout.addStretch()
    
        # Show the provided username (if passed) so the main window greets the user
        try:
            display_name = username
        except Exception:
            display_name = "USER"
        self.usr_name = QtWidgets.QLabel(display_name, self.header_frame)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.usr_name.setFont(font)
        self.usr_name.setStyleSheet("color: white; margin-right: 10px;")
        self.header_layout.addWidget(self.usr_name)

        self.usr_icon = QtWidgets.QPushButton(self.header_frame)
        self.usr_icon.setStyleSheet("background: none; border: none;")
        icon4 = QtGui.QIcon(":/icons/icons/icons8-user-100.png")
        self.usr_icon.setIcon(icon4)
        self.usr_icon.setIconSize(QtCore.QSize(40, 40))
        self.header_layout.addWidget(self.usr_icon)

        self.central_layout.addWidget(self.header_frame)

        # ===== CONTENT AREA =====
        self.content_layout = QtWidgets.QHBoxLayout()
        self.central_layout.addLayout(self.content_layout)

        # Sidebar
        self.side_bar_frame = QtWidgets.QFrame(self.centralwidget)
        self.side_bar_frame.setStyleSheet("""
            background-color: rgb(14, 17, 31);
            border-radius: 10px;
        """)
        self.sidebar_layout = QtWidgets.QVBoxLayout(self.side_bar_frame)
        self.sidebar_layout.setContentsMargins(10, 20, 10, 20)
        self.sidebar_layout.setSpacing(20)

        button_style = """
            QPushButton {
                background-color: transparent;
                color: white;
                font-weight: bold;
                border-radius: 6px;
                padding: 8px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: rgb(72, 89, 222);
                color: white;
            }
            QPushButton:pressed {
                background-color: rgb(52, 69, 180);
            }
        """

        self.my_file_btn = QtWidgets.QPushButton("  My Files", self.side_bar_frame)
        self.my_file_btn.setStyleSheet(button_style)
        self.my_file_btn.setIcon(QtGui.QIcon(":/icons/icons/icons8-folder-100.png"))
        self.my_file_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.sidebar_layout.addWidget(self.my_file_btn)

        self.share_with_me_btn = QtWidgets.QPushButton("  Share/shared with me", self.side_bar_frame)
        self.share_with_me_btn.setStyleSheet(button_style)
        self.share_with_me_btn.setIcon(QtGui.QIcon(":/icons/icons/icons8-share-60.png"))
        self.share_with_me_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.sidebar_layout.addWidget(self.share_with_me_btn)

        self.settings_btn = QtWidgets.QPushButton("  Settings", self.side_bar_frame)
        self.settings_btn.setStyleSheet(button_style)
        self.settings_btn.setIcon(QtGui.QIcon(":/icons/icons/icons8-setting-100.png"))
        self.settings_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.sidebar_layout.addWidget(self.settings_btn)

        self.sidebar_layout.addStretch()
        self.content_layout.addWidget(self.side_bar_frame, 1)

        # File/Folder list + Bottom frame
        self.main_area_layout = QtWidgets.QVBoxLayout()

        self.file_or_folder_list = QtWidgets.QListWidget(self.centralwidget)
        self.file_or_folder_list.setStyleSheet("""
            QListWidget {
                background-color: rgb(14, 17, 31);
                border: 1px solid rgb(46, 46, 64);
                border-radius: 8px;
                color: white;
                padding: 5px;
            }
            QListWidget::item {
                padding: 10px;
            }
            QListWidget::item:hover {
                background-color: rgb(52, 69, 180);
                border-radius: 5px;
            }
            QScrollBar:vertical {
                background: rgb(23, 28, 45);
                width: 12px;
                margin: 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: rgb(72, 89, 222);
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgb(100, 120, 255);
            }
        """)
        # allow multiple selection for delete operations
        self.file_or_folder_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.main_area_layout.addWidget(self.file_or_folder_list, 10)

        # Populate list from storage on startup
        try:
            self.refresh_file_list()
        except Exception:
            pass

        self.bottom_frame = QtWidgets.QFrame(self.centralwidget)
        self.bottom_frame.setStyleSheet("background-color: rgb(14, 17, 31); border-radius: 8px;")
        self.bottom_layout = QtWidgets.QHBoxLayout(self.bottom_frame)

        self.bottom_layout.addStretch()

        # Upload button
        self.upload_btn = QtWidgets.QPushButton("Upload", self.bottom_frame)
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(72, 89, 222);
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: rgb(100, 120, 255);
            }
            QPushButton:pressed {
                background-color: rgb(52, 69, 180);
            }
        """)
        self.upload_btn.setIcon(QtGui.QIcon(":/icons/icons/icons8-upload-100.png"))
        self.upload_btn.setIconSize(QtCore.QSize(25, 25))
        self.upload_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bottom_layout.addWidget(self.upload_btn)
        self.upload_btn.clicked.connect(self.upload_file_or_folder)

        # Save (download) button beside Upload: blue with white text
        self.save_btn = QtWidgets.QPushButton("Save", self.bottom_frame)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(52, 120, 255);
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: rgb(72, 140, 255);
            }
            QPushButton:pressed {
                background-color: rgb(32, 100, 235);
            }
        """)
        self.save_btn.setIcon(QtGui.QIcon(":/icons/icons/icons8-download-100.png"))
        self.save_btn.setIconSize(QtCore.QSize(25, 25))
        self.save_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bottom_layout.addWidget(self.save_btn)
        self.save_btn.clicked.connect(self.save_selected_items)

        # Delete button
        self.delete_btn = QtWidgets.QPushButton("Delete", self.bottom_frame)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(200, 60, 60);
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: rgb(230, 80, 80);
            }
            QPushButton:pressed {
                background-color: rgb(170, 40, 40);
            }
        """)
        self.delete_btn.setIcon(QtGui.QIcon(":/icons/icons/icons8-trash-128.png"))
        self.delete_btn.setIconSize(QtCore.QSize(25, 25))
        self.delete_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bottom_layout.addWidget(self.delete_btn)
        self.delete_btn.clicked.connect(self.delete_selected_items)

        self.main_area_layout.addWidget(self.bottom_frame)
        self.content_layout.addLayout(self.main_area_layout, 4)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    #============================#
    # Upload Folder/file function
    #============================#
    def upload_file_or_folder(self):

        parent = getattr(self, 'MainWindow', None)

        # Simple chooser for File(s) vs Folder using an input dialog (more reliable)
        choice, ok = QtWidgets.QInputDialog.getItem(parent, "Upload", "Upload a file or a folder?", ["File(s)", "Folder"], 0, False)
        if not ok:
            return

        storage_dir = Path(__file__).parent.joinpath('storage')
        storage_dir.mkdir(parents=True, exist_ok=True)

        def unique_path(dest: Path) -> Path:
            if not dest.exists():
                return dest
            stem = dest.stem
            suffix = dest.suffix
            i = 1
            while True:
                candidate = dest.with_name(f"{stem}({i}){suffix}")
                if not candidate.exists():
                    return candidate
                i += 1

        try:
            if choice == "File(s)":
                files, _ = QtWidgets.QFileDialog.getOpenFileNames(parent, "Select file(s) to upload", "", "All Files (*)")
                if not files:
                    return
                uploaded = []
                for f in files:
                    src = Path(f)
                    dest = storage_dir.joinpath(src.name)
                    dest = unique_path(dest)
                    shutil.copy2(src, dest)
                    uploaded.append(dest.name)

                if uploaded:
                    self.refresh_file_list()
                    QtWidgets.QMessageBox.information(parent or self, "Upload", f"Uploaded: {', '.join(uploaded)}")

            elif choice == "Folder":
                folder = QtWidgets.QFileDialog.getExistingDirectory(parent, "Select folder to upload", "")
                if not folder:
                    return
                src_folder = Path(folder)
                dest_folder = storage_dir.joinpath(src_folder.name)
                dest_folder = unique_path(dest_folder)
                shutil.copytree(src_folder, dest_folder)
                self.refresh_file_list()
                QtWidgets.QMessageBox.information(parent or self, "Upload", f"Uploaded folder: {dest_folder.name}")

        except Exception as e:
            QtWidgets.QMessageBox.critical(parent or self, "Upload Failed", f"Could not upload: {str(e)}")

    def refresh_file_list(self):
        """Refresh the displayed list from the local `storage/` directory."""
        storage_dir = Path(__file__).parent.joinpath('storage')
        storage_dir.mkdir(parents=True, exist_ok=True)
        self.file_or_folder_list.clear()
        # list top-level files and folders
        for p in sorted(storage_dir.iterdir()):
            self.file_or_folder_list.addItem(p.name)

    def delete_selected_items(self):
        parent = getattr(self, 'MainWindow', None)
        items = self.file_or_folder_list.selectedItems()
        if not items:
            QtWidgets.QMessageBox.warning(parent or self, "Delete", "No items selected to delete.")
            return

        names = [it.text() for it in items]
        reply = QtWidgets.QMessageBox.question(parent or self, "Confirm Delete",
                                               f"Delete selected: {', '.join(names)}?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply != QtWidgets.QMessageBox.Yes:
            return

        storage_dir = Path(__file__).parent.joinpath('storage')
        errors = []
        for name in names:
            p = storage_dir.joinpath(name)
            try:
                if p.is_dir():
                    shutil.rmtree(p)
                elif p.exists():
                    p.unlink()
                else:
                    errors.append(f"{name}: not found")
            except Exception as e:
                errors.append(f"{name}: {e}")

        self.refresh_file_list()

        if errors:
            QtWidgets.QMessageBox.warning(parent or self, "Delete Results", "Some items could not be deleted:\n" + "\n".join(errors))
        else:
            QtWidgets.QMessageBox.information(parent or self, "Delete", f"Deleted: {', '.join(names)}")

    def save_selected_items(self):
        """Copy selected stored items to a user-chosen destination (does not remove originals)."""
        parent = getattr(self, 'MainWindow', None)
        items = self.file_or_folder_list.selectedItems()
        if not items:
            QtWidgets.QMessageBox.warning(parent or self, "Save", "No items selected to save.")
            return

        names = [it.text() for it in items]
        storage_dir = Path(__file__).parent.joinpath('storage')
        sources = [storage_dir.joinpath(n) for n in names]

        dest = QtWidgets.QFileDialog.getExistingDirectory(parent, "Select destination folder", "")
        if not dest:
            return

        # Progress dialog
        progress = QtWidgets.QProgressDialog("Saving...", "Cancel", 0, len(sources), parent or self)
        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setMinimumDuration(200)
        progress.setValue(0)

        # Start background copy thread
        worker = CopyWorker(sources, dest)

        def on_progress(v):
            progress.setValue(v)

        def on_finished(copied):
            progress.setValue(progress.maximum())
            if copied:
                QtWidgets.QMessageBox.information(parent or self, "Save", f"Saved: {', '.join(copied)}")

        def on_errors(errs):
            QtWidgets.QMessageBox.warning(parent or self, "Save Errors", "Some items failed to save:\n" + "\n".join(errs))

        worker.progress.connect(on_progress)
        worker.finished.connect(on_finished)
        worker.errors.connect(on_errors)

        # Start thread
        worker.start()

        # Keep a reference so it doesn't get GC'd until finished
        if not hasattr(self, '_workers'):
            self._workers = []
        self._workers.append(worker)

        # Remove worker reference when done
        def cleanup():
            try:
                self._workers.remove(worker)
            except Exception:
                pass

        worker.finished.connect(cleanup)
        worker.errors.connect(cleanup)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("NebulaShare")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())