from PyQt5 import QtCore, QtGui, QtWidgets
import os
import shutil
from pathlib import Path
import icons_rc
import file_db


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
            # allow cooperative cancellation
            if self.isInterruptionRequested():
                errors.append("Operation cancelled by user")
                break

            try:
                if not src.exists():
                    errors.append(f"{src}: not found")
                else:
                    dest = self.dest_dir.joinpath(src.name)
                    # avoid copying into a subpath of the source (would cause recursion/errors)
                    try:
                        if dest.resolve().is_relative_to(src.resolve()):
                            raise Exception("destination is inside source")
                    except Exception:
                        # if Path.is_relative_to not supported (older py), fall back to string check
                        if str(dest.resolve()).startswith(str(src.resolve()) + os.sep):
                            raise Exception("destination is inside source")

                    dest = self._unique_path(dest)

                    if src.is_dir():
                        shutil.copytree(src, dest)
                        copied.append(dest.name)
                    elif src.is_file():
                        shutil.copy2(src, dest)
                        copied.append(dest.name)
            except Exception as e:
                # src may not have .name if it's a string; use safe formatting
                try:
                    n = src.name
                except Exception:
                    n = str(src)
                errors.append(f"{n}: {e}")

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
    
        # Store the username and show the provided username so the main window greets the user
        self.username = username or "USER"
        self.usr_name = QtWidgets.QLabel(f"{self.username} 👋", self.header_frame)
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

        self.share_with_me_btn = QtWidgets.QPushButton("  Shared With Me", self.side_bar_frame)
        self.share_with_me_btn.setStyleSheet(button_style)
        self.share_with_me_btn.setIcon(QtGui.QIcon(":/icons/icons/icons8-share-60.png"))
        self.share_with_me_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.sidebar_layout.addWidget(self.share_with_me_btn)
        self.share_with_me_btn.clicked.connect(self.open_shared_with_me_dialog)

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

        # Initialize files DB and populate list from DB for this user on startup
        try:
            file_db.init_db()
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

        # Share button (share selected items with another user)
        self.share_btn = QtWidgets.QPushButton("Share", self.bottom_frame)
        self.share_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(48, 160, 88);
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: rgb(68, 180, 108);
            }
            QPushButton:pressed {
                background-color: rgb(38, 140, 68);
            }
        """)
        self.share_btn.setIcon(QtGui.QIcon(":/icons/icons/icons8-share-60.png"))
        self.share_btn.setIconSize(QtCore.QSize(25, 25))
        self.share_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bottom_layout.addWidget(self.share_btn)
        self.share_btn.clicked.connect(self.share_selected_items)

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

        # Simple chooser for File(s) vs Folder using a styled input dialog
        dlg = QtWidgets.QInputDialog(parent)
        dlg.setWindowTitle("Upload")
        dlg.setLabelText("Upload a file or a folder?")
        dlg.setComboBoxItems(["File(s)", "Folder"])
        dlg.setComboBoxEditable(False)
        dlg.setStyleSheet("QDialog{background-color: rgb(30,30,47);} QLabel{color: white;} QComboBox, QListView, QAbstractItemView{color: white;} QPushButton{color: white;}")
        if dlg.exec_() != QtWidgets.QDialog.Accepted:
            return
        choice = dlg.textValue()

        storage_dir = Path(__file__).parent.joinpath(f'storage/users/{self.username}/my_files/')
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
                files = self._get_open_files(parent, "Select file(s) to upload", "All Files (*)")
                if not files:
                    return
                uploaded = []
                for f in files:
                    src = Path(f)
                    dest = storage_dir.joinpath(src.name)
                    dest = unique_path(dest)
                    shutil.copy2(src, dest)
                    uploaded.append(dest.name)
                    # persist metadata
                    try:
                        try:
                            rel = str(dest.relative_to(storage_dir))
                        except Exception:
                            rel = dest.name
                        file_db.insert_file(self.username, rel, str(dest.resolve()), dest.is_dir())
                    except Exception:
                        pass

                if uploaded:
                    self.refresh_file_list()
                    self._show_message(parent or self, "Upload", f"Uploaded: {', '.join(uploaded)}", QtWidgets.QMessageBox.Information)

            elif choice == "Folder":
                folder = self._get_directory(parent, "Select folder to upload")
                if not folder:
                    return
                src_folder = Path(folder)
                dest_folder = storage_dir.joinpath(src_folder.name)
                dest_folder = unique_path(dest_folder)
                shutil.copytree(src_folder, dest_folder)
                # insert metadata for folder and all contained items (relative paths)
                try:
                    base = storage_dir
                    file_db.insert_file(self.username, str(dest_folder.relative_to(base)), str(dest_folder.resolve()), True)
                    for child in dest_folder.rglob('*'):
                        rel = str(child.relative_to(base))
                        file_db.insert_file(self.username, rel, str(child.resolve()), child.is_dir())
                except Exception:
                    pass
                self.refresh_file_list()
                self._show_message(parent or self, "Upload", f"Uploaded folder: {dest_folder.name}", QtWidgets.QMessageBox.Information)

        except Exception as e:
            self._show_message(parent or self, "Upload Failed", f"Could not upload: {str(e)}", QtWidgets.QMessageBox.Critical)

    def refresh_file_list(self):
        """Refresh the displayed list from the local `storage/` directory."""
        # List files from the metadata DB for the logged-in user
        storage_dir = Path(__file__).parent.joinpath(f'storage/users/{self.username}/my_files/')
        storage_dir.mkdir(parents=True, exist_ok=True)
        self.file_or_folder_list.clear()
        rows = file_db.list_files_by_owner(self.username)
        for _id, file_name, file_path, is_folder, created_at in rows:
            p = Path(file_path)
            if not p.exists():
                # remove stale DB entry
                try:
                    file_db.delete_file_by_path(file_path)
                except Exception:
                    pass
                continue
            item = QtWidgets.QListWidgetItem(file_name)
            # store the absolute path so delete/save operate on it
            item.setData(QtCore.Qt.UserRole, file_path)
            if is_folder:
                item.setIcon(QtGui.QIcon(":/icons/icons/icons8-folder-100.png"))
            self.file_or_folder_list.addItem(item)

    def delete_selected_items(self):
        parent = getattr(self, 'MainWindow', None)
        items = self.file_or_folder_list.selectedItems()
        if not items:
            self._show_message(parent or self, "Delete", "No items selected to delete.", QtWidgets.QMessageBox.Warning)
            return

        names = [it.text() for it in items]
        reply = self._ask_question(parent or self, "Confirm Delete",
                                               f"Delete selected: {', '.join(names)}?")
        if reply != QtWidgets.QMessageBox.Yes:
            return

        storage_dir = Path(__file__).parent.joinpath(f'storage/users/{self.username}/my_files/')
        errors = []
        entries = [(it.text(), it.data(QtCore.Qt.UserRole)) for it in items]
        for name, pth in entries:
            p = Path(pth) if pth else storage_dir.joinpath(name)
            try:
                if p.is_dir():
                    shutil.rmtree(p)
                elif p.exists():
                    p.unlink()
                else:
                    errors.append(f"{name}: not found")
            except Exception as e:
                errors.append(f"{name}: {e}")
            # remove DB entry if present
            try:
                file_db.delete_file_by_path(str(p.resolve()))
            except Exception:
                pass

        self.refresh_file_list()

        if errors:
            self._show_message(parent or self, "Delete Results", "Some items could not be deleted:\n" + "\n".join(errors), QtWidgets.QMessageBox.Warning)
        else:
            self._show_message(parent or self, "Delete", f"Deleted: {', '.join(names)}", QtWidgets.QMessageBox.Information)

    def share_selected_items(self):
        parent = getattr(self, 'MainWindow', None)
        items = self.file_or_folder_list.selectedItems()
        if not items:
            self._show_message(parent or self, "Share", "No items selected to share.", QtWidgets.QMessageBox.Warning)
            return

        target, ok = self._get_text_input(parent, "Share", "Enter username to share with:")
        if not ok or not target.strip():
            return
        target = target.strip()

        entries = [(it.text(), it.data(QtCore.Qt.UserRole)) for it in items]
        failed = []
        for name, pth in entries:
            fp = Path(pth) if pth else Path(__file__).parent.joinpath(f'storage/users/{self.username}/my_files/').joinpath(name)
            if not fp.exists():
                failed.append(name)
                continue
            try:
                file_db.share_file(self.username, str(fp.resolve()), target)
            except Exception as e:
                failed.append(f"{name}: {e}")

        if failed:
            self._show_message(parent or self, "Share", "Some items could not be shared:\n" + "\n".join(failed), QtWidgets.QMessageBox.Warning)
        else:
            self._show_message(parent or self, "Share", "Shared successfully.", QtWidgets.QMessageBox.Information)

    def open_shared_with_me_dialog(self):
        parent = getattr(self, 'MainWindow', None)
        dlg = QtWidgets.QDialog(parent)
        dlg.setWindowTitle("Shared With Me")
        dlg.setModal(True)
        dlg.setMinimumSize(600, 400)
        dlg.setStyleSheet("""
                          background-color: rgb(30, 30, 47); 
                          color: white;
                          QPushButton {
                             background-color: rgb(72, 89, 222);
                             color: white;
                             font-weight: bold;
                            }
            """)

        layout = QtWidgets.QVBoxLayout(dlg)
        list_widget = QtWidgets.QListWidget()
        list_widget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        layout.addWidget(list_widget)

        btn_layout = QtWidgets.QHBoxLayout()
        download_btn = QtWidgets.QPushButton("Download")
        reshare_btn = QtWidgets.QPushButton("Re-share")
        close_btn = QtWidgets.QPushButton("Close")
        btn_layout.addWidget(download_btn)
        btn_layout.addWidget(reshare_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

        # populate list
        rows = file_db.list_shared_with_user(self.username)
        for sid, owner, target, file_path, shared_at in rows:
            # attempt to get file name from path
            name = Path(file_path).name
            item = QtWidgets.QListWidgetItem(f"{name}  (from {owner})")
            item.setData(QtCore.Qt.UserRole, (sid, owner, file_path))
            list_widget.addItem(item)

        def on_download():
            sel = list_widget.selectedItems()
            if not sel:
                self._show_message(dlg, "Download", "No items selected to download.", QtWidgets.QMessageBox.Warning)
                return
            entries = [it.data(QtCore.Qt.UserRole) for it in sel]
            # reuse save logic: ask destination and copy
            dest = self._get_directory(dlg, "Select destination folder")
            if not dest:
                return
            sources = [Path(fp) for (_sid, _owner, fp) in entries]

            # filter out missing sources and inform the user
            existing = [s for s in sources if s.exists()]
            missing = [str(s) for s in sources if not s.exists()]
            if not existing:
                self._show_message(dlg, "Download", "Selected items are no longer available on the server.", QtWidgets.QMessageBox.Warning)
                return
            if missing:
                self._show_message(dlg, "Download", "Some items are no longer available and will be skipped:\n" + "\n".join(missing), QtWidgets.QMessageBox.Warning)

            # use worker to copy; keep reference on dialog to avoid GC
            worker = CopyWorker(existing, dest, parent=dlg)
            if not hasattr(dlg, '_workers'):
                dlg._workers = []
            dlg._workers.append(worker)

            progress = QtWidgets.QProgressDialog("Downloading...", "Cancel", 0, len(existing), dlg)
            progress.setStyleSheet("QProgressDialog{background-color: rgb(30,30,47);} QLabel{color: white;} QPushButton{color: white;}")
            progress.setWindowModality(QtCore.Qt.WindowModal)
            progress.setMinimumDuration(200)
            progress.setValue(0)

            # wire cancel to requestInterruption on the worker
            try:
                progress.canceled.connect(worker.requestInterruption)
            except Exception:
                pass

            def on_progress(v):
                progress.setValue(v)

            def on_finished(copied):
                progress.setValue(progress.maximum())
                if copied:
                    self._show_message(dlg, "Download", f"Downloaded: {', '.join(copied)}", QtWidgets.QMessageBox.Information)

            def on_errors(errs):
                self._show_message(dlg, "Download Errors", "Some items failed:\n" + "\n".join(errs), QtWidgets.QMessageBox.Warning)

            def cleanup():
                try:
                    dlg._workers.remove(worker)
                except Exception:
                    pass

            worker.progress.connect(on_progress)
            worker.finished.connect(on_finished)
            worker.errors.connect(on_errors)
            worker.finished.connect(progress.close)
            worker.finished.connect(cleanup)
            worker.errors.connect(cleanup)
            worker.start()

        def on_reshare():
            sel = list_widget.selectedItems()
            if not sel:
                self._show_message(dlg, "Re-share", "No items selected to re-share.", QtWidgets.QMessageBox.Warning)
                return
            target, ok = self._get_text_input(dlg, "Re-share", "Enter username to share with:")
            if not ok or not target.strip():
                return
            target = target.strip()
            failed = []
            for it in sel:
                sid, owner, fp = it.data(QtCore.Qt.UserRole)
                try:
                    file_db.share_file(owner, fp, target)
                except Exception as e:
                    failed.append(f"{Path(fp).name}: {e}")
            if failed:
                self._show_message(dlg, "Re-share", "Some items could not be re-shared:\n" + "\n".join(failed), QtWidgets.QMessageBox.Warning)
            else:
                self._show_message(dlg, "Re-share", "Re-shared successfully.", QtWidgets.QMessageBox.Information)

        download_btn.clicked.connect(on_download)
        reshare_btn.clicked.connect(on_reshare)
        close_btn.clicked.connect(dlg.accept)

        dlg.exec_()

    def save_selected_items(self):
        """Copy selected stored items to a user-chosen destination (does not remove originals)."""
        parent = getattr(self, 'MainWindow', None)
        items = self.file_or_folder_list.selectedItems()
        if not items:
            self._show_message(parent or self, "Save", "No items selected to save.", QtWidgets.QMessageBox.Warning)
            return

        entries = [(it.text(), it.data(QtCore.Qt.UserRole)) for it in items]
        names = [name for name, _ in entries]
        storage_dir = Path(__file__).parent.joinpath(f'storage/users/{self.username}/my_files/')
        # Prefer the path stored in the UserRole, fall back to the standard storage path.
        sources = [Path(fp) if fp else storage_dir.joinpath(name) for name, fp in entries]

        dest = self._get_directory(parent, "Select destination folder")
        if not dest:
            return

        # Progress dialog
        progress = QtWidgets.QProgressDialog("Saving...", "Cancel", 0, len(sources), parent or self)
        progress.setStyleSheet("QProgressDialog{background-color: rgb(30,30,47);} QLabel{color: white;} QPushButton{color: white;}")
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
                self._show_message(parent or self, "Save", f"Saved: {', '.join(copied)}", QtWidgets.QMessageBox.Information)

        def on_errors(errs):
            self._show_message(parent or self, "Save Errors", "Some items failed to save:\n" + "\n".join(errs), QtWidgets.QMessageBox.Warning)

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

    def _show_message(self, parent, title, text, icon=QtWidgets.QMessageBox.Warning):
        dlg = QtWidgets.QMessageBox(parent)
        dlg.setWindowTitle(title)
        dlg.setText(text)
        dlg.setIcon(icon)
        dlg.setStyleSheet("QMessageBox{background-color: rgb(23, 28, 45);} QMessageBox QLabel{color: white;} QMessageBox QPushButton{color: white;}")
        dlg.exec_()

    def _ask_question(self, parent, title, text):
        dlg = QtWidgets.QMessageBox(parent)
        dlg.setWindowTitle(title)
        dlg.setText(text)
        dlg.setIcon(QtWidgets.QMessageBox.Question)
        dlg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        dlg.setStyleSheet("QMessageBox{background-color: rgb(23, 28, 45);} QMessageBox QLabel{color: white;} QMessageBox QPushButton{color: white;}")
        return dlg.exec_()

    def _get_text_input(self, parent, title, label):
        dlg = QtWidgets.QInputDialog(parent)
        dlg.setWindowTitle(title)
        dlg.setLabelText(label)
        dlg.setStyleSheet("QDialog{background-color: rgb(30,30,47);} QLabel{color: white;} QLineEdit{color: white;} QPushButton{color: white;}")
        if dlg.exec_() != QtWidgets.QDialog.Accepted:
            return "", False
        return dlg.textValue(), True

    def _get_directory(self, parent, title, start_dir=""):
        dlg = QtWidgets.QFileDialog(parent)
        dlg.setWindowTitle(title)
        dlg.setFileMode(QtWidgets.QFileDialog.Directory)
        dlg.setOptions(QtWidgets.QFileDialog.ShowDirsOnly)
        if start_dir:
            try:
                dlg.setDirectory(start_dir)
            except Exception:
                pass
        dlg.setStyleSheet("QDialog{background-color: rgb(30,30,47);} QLabel{color: white;} QListView{color: white;} QTreeView{color: white;} QPushButton{color: white;}")
        if dlg.exec_() != QtWidgets.QDialog.Accepted:
            return ""
        sel = dlg.selectedFiles()
        return sel[0] if sel else ""

    def _get_open_files(self, parent, title, filter_str="All Files (*)"):
        dlg = QtWidgets.QFileDialog(parent)
        dlg.setWindowTitle(title)
        dlg.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        dlg.setNameFilter(filter_str)
        dlg.setStyleSheet("QDialog{background-color: rgb(30,30,47);} QLabel{color: white;} QListView{color: white;} QTreeView{color: white;} QPushButton{color: white;}")
        if dlg.exec_() != QtWidgets.QDialog.Accepted:
            return []
        return dlg.selectedFiles()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())