"""
Validation utilities for Student Result Insight Tool.
"""

from __future__ import annotations

import re

from utils.constants import (
    MAX_YEAR,
    MIN_YEAR,
    VALID_DEPARTMENTS,
)

# ==========================================================
# Regular Expression Patterns
# ==========================================================

ROLL_NUMBER_PATTERN = re.compile(r"^\d{2}[A-Z]{2,10}\d{3}$")

EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

PHONE_PATTERN = re.compile(r"^[6-9]\d{9}$")


# ==========================================================
# Validation Functions
# ==========================================================

def validate_roll_number(roll_number: str) -> bool:
    """
    Validate the student roll number.

    Examples:
        23CSE001
        24ECE105
        24CSEAI001
    """

    roll_number = roll_number.strip().upper()

    return bool(ROLL_NUMBER_PATTERN.fullmatch(roll_number))


def validate_name(name: str) -> bool:
    """
    Validate student's full name.
    """

    name = name.strip()

    return len(name) >= 3


def validate_department(department: str) -> bool:
    """
    Validate department.
    """

    department = department.strip().upper()

    return department in VALID_DEPARTMENTS


def validate_academic_year(year: int) -> bool:
    """
    Validate academic year.
    """

    return MIN_YEAR <= year <= MAX_YEAR


def validate_email(email: str) -> bool:
    """
    Validate email address.
    """

    email = email.strip()

    return bool(EMAIL_PATTERN.fullmatch(email))


def validate_phone(phone: str) -> bool:
    """
    Validate Indian mobile number.
    """

    phone = phone.strip()

    return bool(PHONE_PATTERN.fullmatch(phone))