from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
import time
import os
import hashlib

MONITORED_PATH = "monitored-folder"
SENSITIVE_PATH = "sensitive-data"
TRANSFER_PATH = "transfer-destination"
LOG_FILE = "logs/file-transfer-audit-log.txt"

SENSITIVE_KEYWORDS = ["confidential", "secret", "password", "salary", "employee", "restricted"]

AUTHORIZED_SENSITIVE_DESTINATIONS = [
    SENSITIVE_PATH
]

file_hashes = {}


def write_log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"

    print(log_entry)

    with open(LOG_FILE, "a") as log:
        log.write(log_entry + "\n")


def calculate_sha256(file_path):
    try:
        sha256_hash = hashlib.sha256()

        with open(file_path, "rb") as file:
            for block in iter(lambda: file.read(4096), b""):
                sha256_hash.update(block)

        return sha256_hash.hexdigest()

    except FileNotFoundError:
        return None
    except PermissionError:
        write_log(f"ERROR: Permission denied while hashing file: {file_path}")
        return None


def is_sensitive_file(file_path):
    file_name = os.path.basename(file_path).lower()

    if file_path.startswith(SENSITIVE_PATH):
        return True

    for keyword in SENSITIVE_KEYWORDS:
        if keyword in file_name:
            return True

    return False


def is_authorized_destination(file_path):
    for allowed_path in AUTHORIZED_SENSITIVE_DESTINATIONS:
        if file_path.startswith(allowed_path):
            return True

    return False


def check_sensitive_alert(event_type, file_path):
    if is_sensitive_file(file_path):
        write_log(f"ALERT: Sensitive file {event_type}: {file_path}")


def check_unauthorized_transfer(file_path):
    if is_sensitive_file(file_path) and not is_authorized_destination(file_path):
        write_log(f"CRITICAL ALERT: Unauthorized sensitive file transfer detected: {file_path}")


def check_integrity(file_path):
    current_hash = calculate_sha256(file_path)

    if current_hash is None:
        return

    if file_path not in file_hashes:
        file_hashes[file_path] = current_hash
        write_log(f"HASH RECORDED: {file_path} | SHA256: {current_hash}")

    elif file_hashes[file_path] != current_hash:
        write_log(f"ALERT: Hash mismatch detected for {file_path}")
        write_log(f"OLD HASH: {file_hashes[file_path]}")
        write_log(f"NEW HASH: {current_hash}")
        file_hashes[file_path] = current_hash

    else:
        write_log(f"INTEGRITY OK: {file_path}")


class FileTransferHandler(FileSystemEventHandler):

    def on_created(self, event):
        if not event.is_directory:
            write_log(f"FILE CREATED: {event.src_path}")
            check_sensitive_alert("created", event.src_path)
            check_unauthorized_transfer(event.src_path)
            time.sleep(0.2)
            check_integrity(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            write_log(f"FILE MODIFIED: {event.src_path}")
            check_sensitive_alert("modified", event.src_path)
            check_unauthorized_transfer(event.src_path)
            time.sleep(0.2)
            check_integrity(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            write_log(f"FILE DELETED: {event.src_path}")
            check_sensitive_alert("deleted", event.src_path)

            if event.src_path in file_hashes:
                del file_hashes[event.src_path]

    def on_moved(self, event):
        if not event.is_directory:
            write_log(f"FILE MOVED: from {event.src_path} to {event.dest_path}")
            check_sensitive_alert("moved from", event.src_path)
            check_sensitive_alert("moved to", event.dest_path)
            check_unauthorized_transfer(event.dest_path)

            if event.src_path in file_hashes:
                file_hashes[event.dest_path] = file_hashes.pop(event.src_path)

            time.sleep(0.2)
            check_integrity(event.dest_path)


if __name__ == "__main__":
    os.makedirs(MONITORED_PATH, exist_ok=True)
    os.makedirs(SENSITIVE_PATH, exist_ok=True)
    os.makedirs(TRANSFER_PATH, exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    write_log("Secure File Transfer Monitoring System started.")
    write_log(f"Monitoring folder: {MONITORED_PATH}")
    write_log(f"Sensitive folder: {SENSITIVE_PATH}")
    write_log(f"Transfer destination: {TRANSFER_PATH}")
    write_log("Integrity verification enabled using SHA256.")
    write_log("Authorization policy enabled for sensitive file transfers.")

    event_handler = FileTransferHandler()
    observer = Observer()

    observer.schedule(event_handler, MONITORED_PATH, recursive=True)
    observer.schedule(event_handler, SENSITIVE_PATH, recursive=True)
    observer.schedule(event_handler, TRANSFER_PATH, recursive=True)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        write_log("Monitoring stopped by user.")

    observer.join()
