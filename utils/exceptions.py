"""
Custom Exceptions
"""


class StudentError(Exception):
    """Base exception for student operations."""


class StudentAlreadyExistsError(StudentError):
    """Raised when a duplicate roll number is found."""


class StudentNotFoundError(StudentError):
    """Raised when a student does not exist."""