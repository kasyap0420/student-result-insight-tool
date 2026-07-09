"""
Result Service

Provides CRUD operations for the results table.
"""

from __future__ import annotations

from typing import Any, Optional

from mysql.connector import Error

from database.database import get_connection
from models.result import Result
from services.student_service import get_required_student_by_roll_number
from utils.grade import calculate_result_summary


INSERT_RESULT_QUERY = """
INSERT INTO results
(
    student_id,
    math,
    science,
    english,
    computer,
    total,
    percentage,
    grade,
    status
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

SELECT_RESULT_BY_STUDENT_ID_QUERY = """
SELECT
    result_id,
    student_id,
    math,
    science,
    english,
    computer,
    total,
    percentage,
    grade,
    status
FROM results
WHERE student_id = %s
"""

SELECT_ALL_RESULTS_QUERY = """
SELECT
    result_id,
    student_id,
    math,
    science,
    english,
    computer,
    total,
    percentage,
    grade,
    status
FROM results
ORDER BY result_id
"""

UPDATE_RESULT_BY_STUDENT_ID_QUERY = """
UPDATE results
SET
    math = %s,
    science = %s,
    english = %s,
    computer = %s,
    total = %s,
    percentage = %s,
    grade = %s,
    status = %s
WHERE student_id = %s
"""

DELETE_RESULT_BY_STUDENT_ID_QUERY = """
DELETE FROM results
WHERE student_id = %s
"""


def _get_db_connection():
    connection = get_connection()

    if connection is None:
        raise ConnectionError("Unable to connect to the database.")

    return connection


def _row_to_result(row: dict[str, Any]) -> Result:
    return Result(
        result_id=row["result_id"],
        student_id=row["student_id"],
        math=row["math"],
        science=row["science"],
        english=row["english"],
        computer=row["computer"],
        total=row["total"],
        percentage=float(row["percentage"]),
        grade=row["grade"],
        status=row["status"],
    )


def _build_result(
    student_id: int,
    math: int,
    science: int,
    english: int,
    computer: int,
    result_id: int | None = None,
) -> Result:
    summary = calculate_result_summary(
        math=math,
        science=science,
        english=english,
        computer=computer,
    )

    return Result(
        result_id=result_id,
        student_id=student_id,
        math=math,
        science=science,
        english=english,
        computer=computer,
        total=summary["total"],
        percentage=summary["percentage"],
        grade=summary["grade"],
        status=summary["status"],
    )


def _get_result_by_student_id(student_id: int) -> Optional[Result]:
    connection = _get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            SELECT_RESULT_BY_STUDENT_ID_QUERY,
            (student_id,),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return _row_to_result(row)

    finally:
        cursor.close()
        connection.close()


def add_result_by_roll_number(
    roll_number: str,
    math: int,
    science: int,
    english: int,
    computer: int,
) -> Result:
    student = get_required_student_by_roll_number(roll_number)

    if student.student_id is None:
        raise ValueError("Student ID is missing.")

    existing_result = _get_result_by_student_id(student.student_id)

    if existing_result is not None:
        raise ValueError(
            f"Result already exists for roll number: "
            f"{student.roll_number}"
        )

    result = _build_result(
        student_id=student.student_id,
        math=math,
        science=science,
        english=english,
        computer=computer,
    )

    connection = _get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            INSERT_RESULT_QUERY,
            (
                result.student_id,
                result.math,
                result.science,
                result.english,
                result.computer,
                result.total,
                result.percentage,
                result.grade,
                result.status,
            ),
        )

        connection.commit()

        return Result(
            result_id=cursor.lastrowid,
            student_id=result.student_id,
            math=result.math,
            science=result.science,
            english=result.english,
            computer=result.computer,
            total=result.total,
            percentage=result.percentage,
            grade=result.grade,
            status=result.status,
        )

    except Error:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def get_result_by_roll_number(roll_number: str) -> Optional[Result]:
    student = get_required_student_by_roll_number(roll_number)

    if student.student_id is None:
        raise ValueError("Student ID is missing.")

    return _get_result_by_student_id(student.student_id)


def get_required_result_by_roll_number(roll_number: str) -> Result:
    result = get_result_by_roll_number(roll_number)

    if result is None:
        raise ValueError(
            f"Result not found for roll number: "
            f"{roll_number.strip().upper()}"
        )

    return result


def get_all_results() -> list[Result]:
    connection = _get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(SELECT_ALL_RESULTS_QUERY)

        rows = cursor.fetchall()

        return [_row_to_result(row) for row in rows]

    finally:
        cursor.close()
        connection.close()


def update_result_by_roll_number(
    roll_number: str,
    math: int,
    science: int,
    english: int,
    computer: int,
) -> Result:
    student = get_required_student_by_roll_number(roll_number)

    if student.student_id is None:
        raise ValueError("Student ID is missing.")

    result = _build_result(
        student_id=student.student_id,
        math=math,
        science=science,
        english=english,
        computer=computer,
    )

    connection = _get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            UPDATE_RESULT_BY_STUDENT_ID_QUERY,
            (
                result.math,
                result.science,
                result.english,
                result.computer,
                result.total,
                result.percentage,
                result.grade,
                result.status,
                result.student_id,
            ),
        )

        if cursor.rowcount == 0:
            connection.rollback()
            raise ValueError(
                f"Result not found for roll number: "
                f"{student.roll_number}"
            )

        connection.commit()

        updated_result = _get_result_by_student_id(student.student_id)

        if updated_result is None:
            raise ValueError(
                f"Result not found for roll number: "
                f"{student.roll_number}"
            )

        return updated_result

    except Error:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def delete_result_by_roll_number(roll_number: str) -> bool:
    student = get_required_student_by_roll_number(roll_number)

    if student.student_id is None:
        raise ValueError("Student ID is missing.")

    connection = _get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            DELETE_RESULT_BY_STUDENT_ID_QUERY,
            (student.student_id,),
        )

        if cursor.rowcount == 0:
            connection.rollback()
            raise ValueError(
                f"Result not found for roll number: "
                f"{student.roll_number}"
            )

        connection.commit()

        return True

    except Error:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()