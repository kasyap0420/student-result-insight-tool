"""
Student Service

Provides CRUD operations for the students table.
"""

from __future__ import annotations

from typing import Any, Optional

from mysql.connector import Error, IntegrityError

from database.database import get_connection
from models.student import Student
from utils.exceptions import (
    StudentAlreadyExistsError,
    StudentNotFoundError,
)
from utils.validator import (
    validate_academic_year,
    validate_department,
    validate_email,
    validate_name,
    validate_phone,
    validate_roll_number,
)


INSERT_STUDENT_QUERY = """
INSERT INTO students
(
    roll_number,
    full_name,
    department,
    academic_year,
    email,
    phone
)
VALUES (%s, %s, %s, %s, %s, %s)
"""

SELECT_ALL_STUDENTS_QUERY = """
SELECT
    student_id,
    roll_number,
    full_name,
    department,
    academic_year,
    email,
    phone
FROM students
ORDER BY roll_number
"""

SELECT_STUDENT_BY_ROLL_QUERY = """
SELECT
    student_id,
    roll_number,
    full_name,
    department,
    academic_year,
    email,
    phone
FROM students
WHERE roll_number = %s
"""

UPDATE_STUDENT_QUERY = """
UPDATE students
SET
    full_name = %s,
    department = %s,
    academic_year = %s,
    email = %s,
    phone = %s
WHERE roll_number = %s
"""

DELETE_STUDENT_QUERY = """
DELETE FROM students
WHERE roll_number = %s
"""


def _get_db_connection():
    connection = get_connection()

    if connection is None:
        raise ConnectionError("Unable to connect to the database.")

    return connection


def _normalize_student(student: Student) -> Student:
    return Student(
        student_id=student.student_id,
        roll_number=student.roll_number.strip().upper(),
        full_name=" ".join(student.full_name.strip().split()),
        department=student.department.strip().upper(),
        academic_year=student.academic_year,
        email=student.email.strip().lower(),
        phone=student.phone.strip(),
    )


def _validate_student(student: Student) -> None:
    if not validate_roll_number(student.roll_number):
        raise ValueError("Invalid roll number.")

    if not validate_name(student.full_name):
        raise ValueError("Invalid student name.")

    if not validate_department(student.department):
        raise ValueError("Invalid department.")

    if not validate_academic_year(student.academic_year):
        raise ValueError("Invalid academic year.")

    if not validate_email(student.email):
        raise ValueError("Invalid email address.")

    if not validate_phone(student.phone):
        raise ValueError("Invalid phone number.")


def _validate_roll_number(roll_number: str) -> str:
    cleaned_roll_number = roll_number.strip().upper()

    if not validate_roll_number(cleaned_roll_number):
        raise ValueError("Invalid roll number.")

    return cleaned_roll_number


def _row_to_student(row: dict[str, Any]) -> Student:
    return Student(
        student_id=row["student_id"],
        roll_number=row["roll_number"],
        full_name=row["full_name"],
        department=row["department"],
        academic_year=row["academic_year"],
        email=row["email"] or "",
        phone=row["phone"] or "",
    )


def add_student(student: Student) -> Student:
    student = _normalize_student(student)
    _validate_student(student)

    connection = _get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            INSERT_STUDENT_QUERY,
            (
                student.roll_number,
                student.full_name,
                student.department,
                student.academic_year,
                student.email,
                student.phone,
            ),
        )

        connection.commit()

        return Student(
            student_id=cursor.lastrowid,
            roll_number=student.roll_number,
            full_name=student.full_name,
            department=student.department,
            academic_year=student.academic_year,
            email=student.email,
            phone=student.phone,
        )

    except IntegrityError as error:
        connection.rollback()

        if error.errno == 1062:
            raise StudentAlreadyExistsError(
                f"Student already exists with roll number: "
                f"{student.roll_number}"
            ) from error

        raise

    except Error:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def get_all_students() -> list[Student]:
    connection = _get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(SELECT_ALL_STUDENTS_QUERY)

        rows = cursor.fetchall()

        return [_row_to_student(row) for row in rows]

    finally:
        cursor.close()
        connection.close()


def get_student_by_roll_number(roll_number: str) -> Optional[Student]:
    cleaned_roll_number = _validate_roll_number(roll_number)

    connection = _get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            SELECT_STUDENT_BY_ROLL_QUERY,
            (cleaned_roll_number,),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return _row_to_student(row)

    finally:
        cursor.close()
        connection.close()


def get_required_student_by_roll_number(roll_number: str) -> Student:
    student = get_student_by_roll_number(roll_number)

    if student is None:
        raise StudentNotFoundError(
            f"Student not found with roll number: {roll_number.strip().upper()}"
        )

    return student


def update_student(student: Student) -> Student:
    student = _normalize_student(student)
    _validate_student(student)

    connection = _get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            UPDATE_STUDENT_QUERY,
            (
                student.full_name,
                student.department,
                student.academic_year,
                student.email,
                student.phone,
                student.roll_number,
            ),
        )

        if cursor.rowcount == 0:
            connection.rollback()
            raise StudentNotFoundError(
                f"Student not found with roll number: {student.roll_number}"
            )

        connection.commit()

        updated_student = get_student_by_roll_number(student.roll_number)

        if updated_student is None:
            raise StudentNotFoundError(
                f"Student not found with roll number: {student.roll_number}"
            )

        return updated_student

    except Error:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def delete_student(roll_number: str) -> bool:
    cleaned_roll_number = _validate_roll_number(roll_number)

    connection = _get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            DELETE_STUDENT_QUERY,
            (cleaned_roll_number,),
        )

        if cursor.rowcount == 0:
            connection.rollback()
            raise StudentNotFoundError(
                f"Student not found with roll number: {cleaned_roll_number}"
            )

        connection.commit()

        return True

    except Error:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()