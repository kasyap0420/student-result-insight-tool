"""
Student Model

Defines the Student data model used throughout the
Student Result Insight Tool.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True, frozen=True)
class Student:
    """
    Represents a student record.

    Attributes:
        student_id: Database primary key.
        roll_number: Unique university roll number.
        full_name: Student's full name.
        department: Department name (e.g., CSE, ECE).
        academic_year: Current academic year.
        email: Student email address.
        phone: Student mobile number.
    """

    student_id: Optional[int] = None

    roll_number: str = ""
    full_name: str = ""
    department: str = ""
    academic_year: int = 1
    email: str = ""
    phone: str = ""

    def __str__(self) -> str:
        """
        Return a human-readable representation of a student.
        """

        return (
            f"{self.roll_number} | "
            f"{self.full_name} | "
            f"{self.department} | "
            f"Year {self.academic_year}"
        )