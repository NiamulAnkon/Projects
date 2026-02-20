import os
import zipfile
import shutil
from datetime import datetime

def create_backup(db_path, invoices_dir, backup_dir):
    """Packages the DB and all PDFs into a single .zip file."""
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"freelance_backup_{timestamp}.zip"
    backup_path = os.path.join(backup_dir, backup_filename)

    with zipfile.ZipFile(backup_path, 'w') as zipf:
        # 1. Add the Database
        if os.path.exists(db_path):
            zipf.write(db_path, arcname=os.path.basename(db_path))

        # 2. Add the Invoices folder
        if os.path.exists(invoices_dir):
            for root, dirs, files in os.walk(invoices_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Store files relative to the 'invoices' folder inside the zip
                    arcname = os.path.join("invoices", file)
                    zipf.write(file_path, arcname=arcname)

    return backup_path

def restore_backup(zip_path, target_db_path, target_invoices_dir):
    """Extracts a zip and replaces current data."""
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        # Extract everything to a temp folder first to avoid corruption
        temp_dir = "temp_restore"
        zipf.extractall(temp_dir)

        # Restore DB
        db_name = os.path.basename(target_db_path)
        temp_db = os.path.join(temp_dir, db_name)
        if os.path.exists(temp_db):
            shutil.copy2(temp_db, target_db_path)

        # Restore Invoices
        temp_invoices = os.path.join(temp_dir, "invoices")
        if os.path.exists(temp_invoices):
            if os.path.exists(target_invoices_dir):
                shutil.rmtree(target_invoices_dir)
            shutil.copytree(temp_invoices, target_invoices_dir)

        # Cleanup
        shutil.rmtree(temp_dir)