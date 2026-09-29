#!/usr/bin/env python3
"""
File Integrity Monitor

Creates SHA-256 hashes for files and compares them with a previously
saved baseline to detect additions, modifications, or deletions.

Use only on files and directories you are authorized to monitor.
"""

import argparse
import hashlib
import json
from pathlib import Path


def calculate_hash(file_path, chunk_size=8192):
    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        while chunk := file.read(chunk_size):
            sha256.update(chunk)

    return sha256.hexdigest()


def collect_hashes(directory):
    directory = Path(directory)
    hashes = {}

    for file_path in sorted(directory.rglob("*")):
        if file_path.is_file():
            hashes[str(file_path.relative_to(directory))] = calculate_hash(file_path)

    return hashes


def save_baseline(hashes, baseline_path):
    with baseline_path.open("w", encoding="utf-8") as file:
        json.dump(hashes, file, indent=4)


def load_baseline(baseline_path):
    with baseline_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def compare_hashes(baseline, current):
    baseline_files = set(baseline)
    current_files = set(current)

    added = sorted(current_files - baseline_files)
    deleted = sorted(baseline_files - current_files)
    modified = sorted(
        path for path in baseline_files & current_files
        if baseline[path] != current[path]
    )

    return added, modified, deleted


def main():
    parser = argparse.ArgumentParser(
        description="Monitor files using SHA-256 integrity hashes."
    )
    parser.add_argument("directory", help="Directory to monitor")
    parser.add_argument(
        "--baseline",
        default="baseline.json",
        help="Path to the baseline JSON file",
    )
    parser.add_argument(
        "--init",
        action="store_true",
        help="Create or replace the baseline",
    )

    args = parser.parse_args()

    directory = Path(args.directory).resolve()
    baseline_path = Path(args.baseline).resolve()

    if not directory.is_dir():
        raise SystemExit(f"Directory not found: {directory}")

    current = collect_hashes(directory)

    if args.init or not baseline_path.exists():
        save_baseline(current, baseline_path)
        print(f"Baseline created: {baseline_path}")
        print(f"Files recorded: {len(current)}")
        return

    baseline = load_baseline(baseline_path)
    added, modified, deleted = compare_hashes(baseline, current)

    print("File Integrity Report")
    print("=" * 24)

    print(f"Added:     {len(added)}")
    for path in added:
        print(f"  + {path}")

    print(f"Modified:  {len(modified)}")
    for path in modified:
        print(f"  * {path}")

    print(f"Deleted:   {len(deleted)}")
    for path in deleted:
        print(f"  - {path}")

    if not added and not modified and not deleted:
        print("\nNo integrity changes detected.")


if __name__ == "__main__":
    main()
