CREATE DATABASE IF NOT EXISTS student_result_insight_db;
USE student_result_insight_db;
CREATE TABLE IF NOT EXISTS students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    roll_number VARCHAR(20) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL,
    academic_year TINYINT UNSIGNED NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS results (
    result_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    math TINYINT UNSIGNED NOT NULL CHECK (math <= 100),
    science TINYINT UNSIGNED NOT NULL CHECK (science <= 100),
    english TINYINT UNSIGNED NOT NULL CHECK (english <= 100),
    computer TINYINT UNSIGNED NOT NULL CHECK (computer <= 100),
    total SMALLINT UNSIGNED NOT NULL,
    percentage DECIMAL(5,2) NOT NULL,
    grade CHAR(2) NOT NULL,
    status ENUM('PASS', 'FAIL') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_results_student
        FOREIGN KEY (student_id)
        REFERENCES students(student_id)
        ON DELETE CASCADE
);