# Final Report — Secure File Transfer Monitoring System

## 1. Project Overview

The Secure File Transfer Monitoring System is a Python-based cybersecurity project designed to monitor file movement and detect suspicious file transfer activity.

The system monitors selected folders, logs file activity, detects sensitive files, verifies file integrity using SHA256 hashing, and generates alerts when unauthorized or suspicious file movement is detected.

## 2. Architecture Diagram

![Secure File Transfer Monitoring System Architecture](screenshots/architecture-diagram.png)

The architecture diagram explains the complete monitoring workflow. It shows how file system events are captured, classified, checked for sensitivity, verified using SHA256 hashing, evaluated against the authorization policy, logged, and converted into security alerts or final audit evidence.

## 3. Problem Statement

File transfers can create security risks such as:

* data leakage
* unauthorized access
* insider misuse
* file tampering
* accidental exposure of sensitive files

This project provides a lightweight monitoring solution to identify suspicious file movement and maintain audit evidence.

## 4. Project Objectives

The main objectives of this project were to:

* monitor file creation, modification, deletion, and movement
* detect sensitive files using filename keywords and folder location
* identify unauthorized sensitive file transfers
* calculate SHA256 hashes for integrity verification
* detect hash mismatch after file modification
* generate persistent audit logs
* collect screenshot evidence for final reporting

## 5. Tools and Technologies Used

```text
Python          → main programming language
watchdog        → real-time file system monitoring
hashlib         → SHA256 hash calculation
Linux Terminal  → testing and execution
Virtualenv      → isolated Python environment
Windows         → documentation and final reporting
GitHub          → final repository hosting
```

## 6. Monitored Locations

The system monitored these folders:

```text
monitored-folder/
sensitive-data/
transfer-destination/
```

## 7. Sensitive File Detection Logic

A file was treated as sensitive if it matched either condition:

* the file was inside `sensitive-data/`
* the filename contained sensitive keywords

Sensitive keywords used:

```text
confidential
secret
password
salary
employee
restricted
```

## 8. Authorization Policy

Sensitive files were only authorized inside:

```text
sensitive-data/
```

If a sensitive file appeared inside:

```text
monitored-folder/
transfer-destination/
```

the system generated a critical alert.

## 9. Integrity Verification

The system used SHA256 hashing to verify file integrity.

When a file was created, its SHA256 hash was recorded.
When the file was modified, the new hash was compared with the previous hash.

If the hashes did not match, the system generated:

```text
ALERT: Hash mismatch detected
```

## 10. Testing Performed

### Test 1 — Monitor Running

The monitoring script was started successfully and watched the configured folders.

Evidence:

```text
01_monitor_running.jpg
```

### Test 2 — Normal File Event Detection

A normal file was created, modified, moved, and deleted inside the monitored folder.

The system detected normal file activity.

Evidence:

```text
02_normal_file_event.jpg
```

### Test 3 — Sensitive File Alert

A sensitive file was created inside the sensitive-data folder.

The system generated sensitive file alerts.

Evidence:

```text
03_sensitive_file_alert.jpg
```

### Test 4 — Hash Mismatch Detection

A test file was created and later modified.

The system detected a SHA256 hash mismatch and generated an integrity alert.

Evidence:

```text
04_integrity_mismatch.jpg
```

### Test 5 — Audit Log Verification

The audit log was checked to confirm that events and alerts were saved permanently.

Evidence:

```text
05_log_evidence.jpg
```

### Test 6 — Unauthorized Sensitive File Transfer

A restricted sensitive file was created inside the transfer destination folder.

The system detected this as an unauthorized sensitive file transfer and generated a critical alert.

Evidence:

```text
06_unauthorized_transfer_alert.jpg
```

### Test 7 — Final Log Evidence

The final audit log was verified to confirm that the critical alert was recorded.

Evidence:

```text
07_final_log_evidence.jpg
```

### Test 8 — Project Structure Verification

The final project folder structure was checked to confirm that files and folders were organized correctly.

Evidence:

```text
08_project_structure.jpg
```

## 11. Sample Alert Output

```text
ALERT: Sensitive file created
ALERT: Sensitive file modified
ALERT: Hash mismatch detected
CRITICAL ALERT: Unauthorized sensitive file transfer detected
```

## 12. Findings

The project successfully detected:

* normal file activity
* sensitive file creation and modification
* unauthorized sensitive file placement
* file tampering through hash mismatch
* persistent security events in audit logs

## 13. Limitations

This project is a lightweight monitoring system created for internship-level cybersecurity learning.

Current limitations:

* authorization policy is folder-based
* user identity tracking is not deeply implemented
* network transfer inspection is not included
* alerts are stored in logs but not sent by email or dashboard

## 14. Future Improvements

Possible improvements include:

* user/process tracking using `psutil`
* email or desktop alert notifications
* SFTP transfer monitoring
* dashboard for log visualization
* CSV or JSON audit log export
* stronger policy configuration using a separate config file

## 15. Conclusion

The Secure File Transfer Monitoring System successfully demonstrates how Python can be used to monitor file movement, detect suspicious file transfer behavior, verify file integrity, and generate audit evidence.

This project is useful for understanding file monitoring, data leakage detection, insider threat detection, and basic security auditing.
