"""
Main Application

Console entry point for Student Result Insight Tool.
"""

from __future__ import annotations

from typing import Any

from models.result import Result
from models.student import Student
from services.report_service import (
    get_dashboard_summary,
    get_department_report,
    get_grade_report,
)
from services.result_service import (
    add_result_by_roll_number,
    delete_result_by_roll_number,
    get_all_results,
    get_required_result_by_roll_number,
    update_result_by_roll_number,
)
from services.student_service import (
    add_student,
    delete_student,
    get_all_students,
    get_required_student_by_roll_number,
    update_student,
)
from utils.csv_export import export_full_result_report_to_csv
from utils.exceptions import (
    StudentAlreadyExistsError,
    StudentNotFoundError,
)


def print_header(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def truncate(value: str, width: int) -> str:
    value = str(value)

    if len(value) <= width:
        return value

    return value[: width - 3] + "..."


def read_int(prompt: str) -> int:
    value = input(prompt).strip()

    if not value:
        raise ValueError("Input cannot be empty.")

    return int(value)


def print_student(student: Student) -> None:
    print(
        f"{student.student_id:<5} "
        f"{student.roll_number:<12} "
        f"{truncate(student.full_name, 25):<25} "
        f"{student.department:<10} "
        f"Year {student.academic_year:<2} "
        f"{truncate(student.email, 28):<28} "
        f"{student.phone}"
    )


def print_result(result: Result, student: Student | None = None) -> None:
    roll_number = "-"
    full_name = "-"

    if student is not None:
        roll_number = student.roll_number
        full_name = student.full_name

    print(
        f"{result.result_id:<5} "
        f"{roll_number:<12} "
        f"{truncate(full_name, 25):<25} "
        f"{result.math:<6} "
        f"{result.science:<8} "
        f"{result.english:<8} "
        f"{result.computer:<9} "
        f"{result.total:<7} "
        f"{result.percentage:<10.2f} "
        f"{result.grade:<6} "
        f"{result.status}"
    )


def read_student_input(existing_roll_number: str | None = None) -> Student:
    if existing_roll_number is None:
        roll_number = input("Enter Roll Number     : ")
    else:
        roll_number = existing_roll_number

    full_name = input("Enter Full Name       : ")
    department = input("Enter Department      : ")
    academic_year = read_int("Enter Academic Year   : ")
    email = input("Enter Email           : ")
    phone = input("Enter Phone           : ")

    return Student(
        roll_number=roll_number,
        full_name=full_name,
        department=department,
        academic_year=academic_year,
        email=email,
        phone=phone,
    )


def read_marks_input() -> tuple[int, int, int, int]:
    math = read_int("Enter Math Marks      : ")
    science = read_int("Enter Science Marks   : ")
    english = read_int("Enter English Marks   : ")
    computer = read_int("Enter Computer Marks  : ")

    return math, science, english, computer


def add_student_menu() -> None:
    print_header("ADD STUDENT")

    try:
        student = read_student_input()
        saved_student = add_student(student)

        print("\nStudent added successfully.")
        print_student(saved_student)

    except StudentAlreadyExistsError as error:
        print(f"\n{error}")

    except ValueError as error:
        print(f"\nInvalid input: {error}")

    except Exception as error:
        print(f"\nUnexpected error: {error}")


def view_all_students_menu() -> None:
    print_header("ALL STUDENTS")

    try:
        students = get_all_students()

        if not students:
            print("\nNo students found.")
            return

        print(
            f"{'ID':<5} "
            f"{'Roll No':<12} "
            f"{'Name':<25} "
            f"{'Dept':<10} "
            f"{'Year':<7} "
            f"{'Email':<28} "
            f"{'Phone'}"
        )
        print("-" * 140)

        for student in students:
            print_student(student)

    except Exception as error:
        print(f"\nUnexpected error: {error}")


def search_student_menu() -> None:
    print_header("SEARCH STUDENT")

    try:
        roll_number = input("Enter Roll Number: ")
        student = get_required_student_by_roll_number(roll_number)

        print("\nStudent found:")
        print_student(student)

    except StudentNotFoundError as error:
        print(f"\n{error}")

    except ValueError as error:
        print(f"\nInvalid input: {error}")

    except Exception as error:
        print(f"\nUnexpected error: {error}")


def update_student_menu() -> None:
    print_header("UPDATE STUDENT")

    try:
        roll_number = input("Enter Roll Number to Update: ")
        existing_student = get_required_student_by_roll_number(roll_number)

        print("\nCurrent Student Details:")
        print_student(existing_student)

        print("\nEnter New Details:")
        updated_input = read_student_input(existing_student.roll_number)
        updated_student = update_student(updated_input)

        print("\nStudent updated successfully.")
        print_student(updated_student)

    except StudentNotFoundError as error:
        print(f"\n{error}")

    except ValueError as error:
        print(f"\nInvalid input: {error}")

    except Exception as error:
        print(f"\nUnexpected error: {error}")


def delete_student_menu() -> None:
    print_header("DELETE STUDENT")

    try:
        roll_number = input("Enter Roll Number to Delete: ")
        student = get_required_student_by_roll_number(roll_number)

        print("\nStudent Details:")
        print_student(student)

        confirm = input("\nAre you sure you want to delete this student? (yes/no): ")

        if confirm.strip().lower() != "yes":
            print("\nDelete cancelled.")
            return

        delete_student(roll_number)

        print("\nStudent deleted successfully.")

    except StudentNotFoundError as error:
        print(f"\n{error}")

    except ValueError as error:
        print(f"\nInvalid input: {error}")

    except Exception as error:
        print(f"\nUnexpected error: {error}")


def add_result_menu() -> None:
    print_header("ADD RESULT")

    try:
        roll_number = input("Enter Roll Number: ")
        student = get_required_student_by_roll_number(roll_number)

        print("\nStudent Details:")
        print_student(student)

        print("\nEnter Marks:")
        math, science, english, computer = read_marks_input()

        result = add_result_by_roll_number(
            roll_number=student.roll_number,
            math=math,
            science=science,
            english=english,
            computer=computer,
        )

        print("\nResult added successfully.")
        print_result(result, student)

    except StudentNotFoundError as error:
        print(f"\n{error}")

    except ValueError as error:
        print(f"\nInvalid input: {error}")

    except Exception as error:
        print(f"\nUnexpected error: {error}")


def view_all_results_menu() -> None:
    print_header("ALL RESULTS")

    try:
        results = get_all_results()

        if not results:
            print("\nNo results found.")
            return

        students = get_all_students()
        student_map = {
            student.student_id: student
            for student in students
            if student.student_id is not None
        }

        print(
            f"{'ID':<5} "
            f"{'Roll No':<12} "
            f"{'Name':<25} "
            f"{'Math':<6} "
            f"{'Science':<8} "
            f"{'English':<8} "
            f"{'Computer':<9} "
            f"{'Total':<7} "
            f"{'Percent':<10} "
            f"{'Grade':<6} "
            f"{'Status'}"
        )
        print("-" * 145)

        for result in results:
            student = student_map.get(result.student_id)
            print_result(result, student)

    except Exception as error:
        print(f"\nUnexpected error: {error}")


def search_result_menu() -> None:
    print_header("SEARCH RESULT")

    try:
        roll_number = input("Enter Roll Number: ")
        student = get_required_student_by_roll_number(roll_number)
        result = get_required_result_by_roll_number(student.roll_number)

        print("\nResult found:")
        print_result(result, student)

    except StudentNotFoundError as error:
        print(f"\n{error}")

    except ValueError as error:
        print(f"\n{error}")

    except Exception as error:
        print(f"\nUnexpected error: {error}")


def update_result_menu() -> None:
    print_header("UPDATE RESULT")

    try:
        roll_number = input("Enter Roll Number to Update Result: ")
        student = get_required_student_by_roll_number(roll_number)
        existing_result = get_required_result_by_roll_number(student.roll_number)

        print("\nCurrent Result:")
        print_result(existing_result, student)

        print("\nEnter New Marks:")
        math, science, english, computer = read_marks_input()

        updated_result = update_result_by_roll_number(
            roll_number=student.roll_number,
            math=math,
            science=science,
            english=english,
            computer=computer,
        )

        print("\nResult updated successfully.")
        print_result(updated_result, student)

    except StudentNotFoundError as error:
        print(f"\n{error}")

    except ValueError as error:
        print(f"\n{error}")

    except Exception as error:
        print(f"\nUnexpected error: {error}")


def delete_result_menu() -> None:
    print_header("DELETE RESULT")

    try:
        roll_number = input("Enter Roll Number to Delete Result: ")
        student = get_required_student_by_roll_number(roll_number)
        result = get_required_result_by_roll_number(student.roll_number)

        print("\nResult Details:")
        print_result(result, student)

        confirm = input("\nAre you sure you want to delete this result? (yes/no): ")

        if confirm.strip().lower() != "yes":
            print("\nDelete cancelled.")
            return

        delete_result_by_roll_number(student.roll_number)

        print("\nResult deleted successfully.")

    except StudentNotFoundError as error:
        print(f"\n{error}")

    except ValueError as error:
        print(f"\n{error}")

    except Exception as error:
        print(f"\nUnexpected error: {error}")


def print_score_row(label: str, row: dict[str, Any] | None) -> None:
    print(f"\n{label}")

    if row is None:
        print("No data available.")
        return

    print(f"Roll Number : {row['roll_number']}")
    print(f"Name        : {row['full_name']}")
    print(f"Department  : {row['department']}")
    print(f"Total       : {row['total']}")
    print(f"Percentage  : {float(row['percentage']):.2f}%")
    print(f"Grade       : {row['grade']}")
    print(f"Status      : {row['status']}")


def dashboard_summary_menu() -> None:
    print_header("DASHBOARD SUMMARY")

    try:
        summary = get_dashboard_summary()

        print(f"Total Students      : {summary['total_students']}")
        print(f"Total Results       : {summary['total_results']}")
        print(f"Passed Students     : {summary['pass_count']}")
        print(f"Failed Students     : {summary['fail_count']}")
        print(f"Average Percentage  : {summary['average_percentage']:.2f}%")

        print_score_row("Top Scorer", summary["top_scorer"])
        print_score_row("Lowest Scorer", summary["lowest_scorer"])

    except Exception as error:
        print(f"\nUnexpected error: {error}")


def department_report_menu() -> None:
    print_header("DEPARTMENT REPORT")

    try:
        rows = get_department_report()

        if not rows:
            print("\nNo department report found.")
            return

        print(
            f"{'Department':<15} "
            f"{'Results':<10} "
            f"{'Average %':<12} "
            f"{'Pass':<8} "
            f"{'Fail'}"
        )
        print("-" * 60)

        for row in rows:
            print(
                f"{row['department']:<15} "
                f"{row['total_results']:<10} "
                f"{row['average_percentage']:<12.2f} "
                f"{row['pass_count']:<8} "
                f"{row['fail_count']}"
            )

    except Exception as error:
        print(f"\nUnexpected error: {error}")


def grade_report_menu() -> None:
    print_header("GRADE REPORT")

    try:
        rows = get_grade_report()

        if not rows:
            print("\nNo grade report found.")
            return

        print(
            f"{'Grade':<10} "
            f"{'Total Students'}"
        )
        print("-" * 30)

        for row in rows:
            print(
                f"{row['grade']:<10} "
                f"{row['total_students']}"
            )

    except Exception as error:
        print(f"\nUnexpected error: {error}")


def export_csv_report_menu() -> None:
    print_header("EXPORT FULL RESULT REPORT CSV")

    try:
        file_path = export_full_result_report_to_csv()

        print("\nCSV report exported successfully.")
        print(f"File Path: {file_path}")

    except ValueError as error:
        print(f"\n{error}")

    except Exception as error:
        print(f"\nUnexpected error: {error}")


def show_menu() -> None:
    print("\n")
    print("=" * 80)
    print("STUDENT RESULT INSIGHT TOOL")
    print("=" * 80)
    print("1.  Add Student")
    print("2.  View All Students")
    print("3.  Search Student")
    print("4.  Update Student")
    print("5.  Delete Student")
    print("6.  Add Result")
    print("7.  View All Results")
    print("8.  Search Result")
    print("9.  Update Result")
    print("10. Delete Result")
    print("11. Dashboard Summary")
    print("12. Department Report")
    print("13. Grade Report")
    print("14. Export Full Result Report CSV")
    print("0.  Exit")
    print("=" * 80)


def main() -> None:
    while True:
        show_menu()

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_student_menu()

        elif choice == "2":
            view_all_students_menu()

        elif choice == "3":
            search_student_menu()

        elif choice == "4":
            update_student_menu()

        elif choice == "5":
            delete_student_menu()

        elif choice == "6":
            add_result_menu()

        elif choice == "7":
            view_all_results_menu()

        elif choice == "8":
            search_result_menu()

        elif choice == "9":
            update_result_menu()

        elif choice == "10":
            delete_result_menu()

        elif choice == "11":
            dashboard_summary_menu()

        elif choice == "12":
            department_report_menu()

        elif choice == "13":
            grade_report_menu()

        elif choice == "14":
            export_csv_report_menu()

        elif choice == "0":
            print("\nApplication closed.")
            break

        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()