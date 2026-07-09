"""
Grade Utilities

Calculates total, percentage, grade, and pass/fail status.
"""

from __future__ import annotations


PASS_MARK = 35
MAX_MARK = 100
TOTAL_SUBJECTS = 4
MAX_TOTAL = MAX_MARK * TOTAL_SUBJECTS

PASS = "PASS"
FAIL = "FAIL"


def validate_mark(mark: int) -> None:
    if not isinstance(mark, int):
        raise ValueError("Marks must be integers.")

    if mark < 0 or mark > MAX_MARK:
        raise ValueError("Marks must be between 0 and 100.")


def validate_marks(
    math: int,
    science: int,
    english: int,
    computer: int,
) -> None:
    validate_mark(math)
    validate_mark(science)
    validate_mark(english)
    validate_mark(computer)


def calculate_total(
    math: int,
    science: int,
    english: int,
    computer: int,
) -> int:
    validate_marks(math, science, english, computer)

    return math + science + english + computer


def calculate_percentage(total: int) -> float:
    if total < 0 or total > MAX_TOTAL:
        raise ValueError("Invalid total marks.")

    return round((total / MAX_TOTAL) * 100, 2)


def calculate_status(
    math: int,
    science: int,
    english: int,
    computer: int,
) -> str:
    validate_marks(math, science, english, computer)

    if (
        math >= PASS_MARK
        and science >= PASS_MARK
        and english >= PASS_MARK
        and computer >= PASS_MARK
    ):
        return PASS

    return FAIL


def calculate_grade(percentage: float, status: str) -> str:
    if status == FAIL:
        return "F"

    if percentage >= 90:
        return "A+"

    if percentage >= 80:
        return "A"

    if percentage >= 70:
        return "B+"

    if percentage >= 60:
        return "B"

    if percentage >= 50:
        return "C"

    if percentage >= 35:
        return "D"

    return "F"


def calculate_result_summary(
    math: int,
    science: int,
    english: int,
    computer: int,
) -> dict[str, int | float | str]:
    validate_marks(math, science, english, computer)

    total = calculate_total(math, science, english, computer)
    percentage = calculate_percentage(total)
    status = calculate_status(math, science, english, computer)
    grade = calculate_grade(percentage, status)

    return {
        "total": total,
        "percentage": percentage,
        "grade": grade,
        "status": status,
    }