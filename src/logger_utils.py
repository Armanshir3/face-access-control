"""Lightweight CSV-based access logger."""

import csv
import os
from datetime import datetime

from . import config


def log_access(name, status, confidence=None):
    """Append a single access attempt to the CSV log file."""
    file_exists = os.path.isfile(config.ACCESS_LOG_PATH)

    with open(config.ACCESS_LOG_PATH, mode="a", newline="", encoding="utf-8") as log_file:
        writer = csv.writer(log_file)

        if not file_exists:
            writer.writerow(["timestamp", "name", "status", "confidence"])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            name,
            status,
            f"{confidence:.2f}" if confidence is not None else "",
        ])
