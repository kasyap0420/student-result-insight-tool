"""
CSV Export Utility

Exports student result reports to CSV files.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Any

from services.report_service import get_full_result_report


EXPORT_DIR = "exports"


def _create_export_directory() -> Path:
    export_path = Path(EXPORT_DIR)
    export_path.mkdir(exist_ok=True)

    return export_path


def _generate_file_name() -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"student_result_report_{timestamp}.csv"


def _format_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "Roll Number": row["roll_number"],
        "Full Name": row["full_name"],
        "Department": row["department"],
        "Academic Year": row["academic_year"],
        "Math": row["math"],
        "Science": row["science"],
        "English": row["english"],
        "Computer": row["computer"],
        "Total": row["total"],
        "Percentage": f"{float(row['percentage']):.2f}",
        "Grade": row["grade"],
        "Status": row["status"],
    }


def export_full_result_report_to_csv() -> str:
    rows = get_full_result_report()

    if not rows:
        raise ValueError("No result data available to export.")

    export_path = _create_export_directory()
    file_path = export_path / _generate_file_name()

    formatted_rows = [_format_row(row) for row in rows]

    fieldnames = [
        "Roll Number",
        "Full Name",
        "Department",
        "Academic Year",
        "Math",
        "Science",
        "English",
        "Computer",
        "Total",
        "Percentage",
        "Grade",
        "Status",
    ]

    with file_path.open(
        mode="w",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(formatted_rows)

    return str(file_path)