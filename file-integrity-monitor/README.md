# 🔐 File Integrity Monitor

A Python-based security tool that uses **SHA-256 hashing** to monitor files and detect unauthorized or unexpected changes.

## Features

- Creates a cryptographic SHA-256 baseline for files
- Detects modified files
- Detects newly added files
- Detects deleted files
- Stores the baseline in JSON format
- Uses only Python standard-library modules
- Includes a simple command-line interface

## How It Works

1. Select a directory to monitor.
2. Generate a baseline containing SHA-256 hashes.
3. Run the monitor again later.
4. Compare the current hashes with the baseline.
5. Report added, modified, and deleted files.

## Requirements

- Python 3.8+
- No external packages required

## Usage

### 1. Create a baseline

```bash
python file_integrity_monitor.py ./sample_data --init
```

### 2. Check for changes

```bash
python file_integrity_monitor.py ./sample_data
```

### Example Output

```text
File Integrity Report
========================
Added:     1
  + notes.txt
Modified:  1
  * config.json
Deleted:   0
```

## Security Concepts

- Cryptographic hashing
- SHA-256
- File integrity monitoring
- Change detection
- Baseline comparison
- Security auditing

## Learning Objectives

This project demonstrates how file hashes can be used to identify changes to digital files and introduces a fundamental technique used in cybersecurity monitoring and digital forensics.

> **Security note:** Use this tool only on files and directories you are authorized to monitor.

## Author

**Sakshi Aru**  
MCA — Cybersecurity & Digital Forensics
