"""
Report Service

Provides summary reports and insights for students and results.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any

from database.database import get_connection


STUDENT_COUNT_QUERY = """
SELECT COUNT(*) AS total_students
FROM students
"""

RESULT_COUNT_QUERY = """
SELECT COUNT(*) AS total_results
FROM results
"""

PASS_FAIL_COUNT_QUERY = """
SELECT
    SUM(CASE WHEN status = 'PASS' THEN 1 ELSE 0 END) AS pass_count,
    SUM(CASE WHEN status = 'FAIL' THEN 1 ELSE 0 END) AS fail_count
FROM results
"""

AVERAGE_PERCENTAGE_QUERY = """
SELECT AVG(percentage) AS average_percentage
FROM results
"""

TOP_SCORER_QUERY = """
SELECT
    s.roll_number,
    s.full_name,
    s.department,
    r.total,
    r.percentage,
    r.grade,
    r.status
FROM results r
JOIN students s ON r.student_id = s.student_id
ORDER BY r.percentage DESC, r.total DESC
LIMIT 1
"""

LOWEST_SCORER_QUERY = """
SELECT
    s.roll_number,
    s.full_name,
    s.department,
    r.total,
    r.percentage,
    r.grade,
    r.status
FROM results r
JOIN students s ON r.student_id = s.student_id
ORDER BY r.percentage ASC, r.total ASC
LIMIT 1
"""

DEPARTMENT_REPORT_QUERY = """
SELECT
    s.department,
    COUNT(*) AS total_results,
    AVG(r.percentage) AS average_percentage,
    SUM(CASE WHEN r.status = 'PASS' THEN 1 ELSE 0 END) AS pass_count,
    SUM(CASE WHEN r.status = 'FAIL' THEN 1 ELSE 0 END) AS fail_count
FROM results r
JOIN students s ON r.student_id = s.student_id
GROUP BY s.department
ORDER BY s.department
"""

GRADE_REPORT_QUERY = """
SELECT
    grade,
    COUNT(*) AS total_students
FROM results
GROUP BY grade
ORDER BY
    CASE grade
        WHEN 'A+' THEN 1
        WHEN 'A' THEN 2
        WHEN 'B+' THEN 3
        WHEN 'B' THEN 4
        WHEN 'C' THEN 5
        WHEN 'D' THEN 6
        WHEN 'F' THEN 7
        ELSE 8
    END
"""

FULL_RESULT_REPORT_QUERY = """
SELECT
    s.roll_number,
    s.full_name,
    s.department,
    s.academic_year,
    r.math,
    r.science,
    r.english,
    r.computer,
    r.total,
    r.percentage,
    r.grade,
    r.status
FROM results r
JOIN students s ON r.student_id = s.student_id
ORDER BY r.percentage DESC, s.roll_number
"""


def _get_db_connection():
    connection = get_connection()

    if connection is None:
        raise ConnectionError("Unable to connect to the database.")

    return connection


def _to_float(value: Any) -> float:
    if value is None:
        return 0.0

    if isinstance(value, Decimal):
        return float(value)

    return float(value)


def _fetch_one(query: str) -> dict[str, Any] | None:
    connection = _get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(query)
        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()


def _fetch_all(query: str) -> list[dict[str, Any]]:
    connection = _get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(query)
        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def get_total_students() -> int:
    row = _fetch_one(STUDENT_COUNT_QUERY)

    if row is None:
        return 0

    return int(row["total_students"])


def get_total_results() -> int:
    row = _fetch_one(RESULT_COUNT_QUERY)

    if row is None:
        return 0

    return int(row["total_results"])


def get_pass_fail_count() -> dict[str, int]:
    row = _fetch_one(PASS_FAIL_COUNT_QUERY)

    if row is None:
        return {
            "pass_count": 0,
            "fail_count": 0,
        }

    return {
        "pass_count": int(row["pass_count"] or 0),
        "fail_count": int(row["fail_count"] or 0),
    }


def get_average_percentage() -> float:
    row = _fetch_one(AVERAGE_PERCENTAGE_QUERY)

    if row is None:
        return 0.0

    return round(_to_float(row["average_percentage"]), 2)


def get_top_scorer() -> dict[str, Any] | None:
    row = _fetch_one(TOP_SCORER_QUERY)

    if row is None:
        return None

    row["percentage"] = _to_float(row["percentage"])
    return row


def get_lowest_scorer() -> dict[str, Any] | None:
    row = _fetch_one(LOWEST_SCORER_QUERY)

    if row is None:
        return None

    row["percentage"] = _to_float(row["percentage"])
    return row


def get_department_report() -> list[dict[str, Any]]:
    rows = _fetch_all(DEPARTMENT_REPORT_QUERY)

    for row in rows:
        row["average_percentage"] = round(
            _to_float(row["average_percentage"]),
            2,
        )
        row["pass_count"] = int(row["pass_count"] or 0)
        row["fail_count"] = int(row["fail_count"] or 0)

    return rows


def get_grade_report() -> list[dict[str, Any]]:
    rows = _fetch_all(GRADE_REPORT_QUERY)

    for row in rows:
        row["total_students"] = int(row["total_students"] or 0)

    return rows


def get_full_result_report() -> list[dict[str, Any]]:
    rows = _fetch_all(FULL_RESULT_REPORT_QUERY)

    for row in rows:
        row["percentage"] = _to_float(row["percentage"])

    return rows


def get_dashboard_summary() -> dict[str, Any]:
    pass_fail = get_pass_fail_count()

    return {
        "total_students": get_total_students(),
        "total_results": get_total_results(),
        "pass_count": pass_fail["pass_count"],
        "fail_count": pass_fail["fail_count"],
        "average_percentage": get_average_percentage(),
        "top_scorer": get_top_scorer(),
        "lowest_scorer": get_lowest_scorer(),
    }