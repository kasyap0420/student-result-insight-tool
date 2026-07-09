# Student Result Insight Tool

A Python and MySQL console application for managing students, storing marks, calculating results, generating basic reports, and exporting result data to CSV.

## Features

* Add, view, search, update, and delete students
* Add, view, search, update, and delete student results
* Calculate total marks
* Calculate percentage
* Calculate grade
* Calculate pass/fail status
* View dashboard summary
* View department-wise report
* View grade-wise report
* Export full result report to CSV
* Store data in MySQL

## Tech Stack

* Python
* MySQL
* mysql-connector-python
* VS Code
* PowerShell

## Project Structure

```text
Student Result Insight Tool
│
├── config
│   └── db_config.py
│
├── database
│   ├── database.py
│   ├── schema.sql
│   └── seed.sql
│
├── models
│   ├── student.py
│   └── result.py
│
├── services
│   ├── student_service.py
│   ├── result_service.py
│   └── report_service.py
│
├── utils
│   ├── constants.py
│   ├── validator.py
│   ├── exceptions.py
│   ├── grade.py
│   └── csv_export.py
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Database Tables

### students

Stores student details such as roll number, name, department, academic year, email, and phone number.

### results

Stores subject marks, total marks, percentage, grade, and pass/fail status.

## Setup Instructions

### 1. Open the project folder

```powershell
cd "C:\Users\kasya\OneDrive\Documents\Student Result Insight Tool"
```

### 2. Create virtual environment

```powershell
python -m venv venv
```

### 3. Activate virtual environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If script execution is blocked:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

### 5. Create MySQL database and tables

Use one of the following methods.

#### Option 1: MySQL Workbench

1. Open MySQL Workbench.
2. Open this file:

```text
database/schema.sql
```

3. Execute the full SQL script.

#### Option 2: MySQL Command Line

Login to MySQL:

```powershell
mysql -u root -p
```

Then manually copy and run the SQL from:

```text
database/schema.sql
```

The script creates:

* `student_result_insight_db`
* `students` table
* `results` table

### 6. Configure database credentials

Update database credentials in:

```text
config/db_config.py
```

Example:

```python
HOST = "localhost"
PORT = 3306
USER = "root"
PASSWORD = "root"
DATABASE = "student_result_insight_db"
```

### 7. Run the application

```powershell
python main.py
```

## Application Menu

```text
1.  Add Student
2.  View All Students
3.  Search Student
4.  Update Student
5.  Delete Student
6.  Add Result
7.  View All Results
8.  Search Result
9.  Update Result
10. Delete Result
11. Dashboard Summary
12. Department Report
13. Grade Report
14. Export Full Result Report CSV
0.  Exit
```

## Validation Rules

* Roll number example: `23CSE001`
* Name must contain at least 3 characters
* Department must be from the allowed department list
* Academic year must be between 1 and 4
* Email must be valid
* Phone number must be a valid Indian mobile number
* Marks must be between 0 and 100

## Grade Rules

| Percentage                        | Grade |
| --------------------------------- | ----- |
| 90 and above                      | A+    |
| 80 to 89.99                       | A     |
| 70 to 79.99                       | B+    |
| 60 to 69.99                       | B     |
| 50 to 59.99                       | C     |
| 35 to 49.99                       | D     |
| Below 35 or failed in any subject | F     |

A student must score at least 35 marks in every subject to pass.

## CSV Export

CSV files are generated inside the `exports` folder.

Example:

```text
exports/student_result_report_YYYYMMDD_HHMMSS.csv
```

## Current Status

Implemented:

* Student management
* Result management
* Grade calculation
* Basic reports
* CSV export
* MySQL database connection
* Console-based menu

## Author

Yanamandra Venkat rama kasyap
