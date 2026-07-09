"""
Result Model

Defines the Result data model used throughout the
Student Result Insight Tool.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True, frozen=True)
class Result:
    """
    Represents a student result record.
    """

    result_id: Optional[int] = None
    student_id: int = 0

    math: int = 0
    science: int = 0
    english: int = 0
    computer: int = 0

    total: int = 0
    percentage: float = 0.0
    grade: str = ""
    status: str = ""

    def __str__(self) -> str:
        return (
            f"Student ID {self.student_id} | "
            f"Total {self.total} | "
            f"{self.percentage:.2f}% | "
            f"Grade {self.grade} | "
            f"{self.status}"
        )