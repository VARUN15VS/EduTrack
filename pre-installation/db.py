import os
import mysql.connector
from mysql.connector import errorcode
import dotenv

dotenv.load_dotenv()

def get_db_connection():
    """Fetch MySQL connection using environment variables."""
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
    )


def create_database(cursor, db_name="edutrack"):
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Database '{db_name}' ensured.")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)


def main():
    DB_NAME = "edutrack"

    TABLES = {}

    TABLES["users"] = (
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL,
            role ENUM('student','teacher','admin','government') NOT NULL,
            college_id INT
        )
        """
    )

    TABLES["colleges"] = (
        """
        CREATE TABLE IF NOT EXISTS colleges (
            college_id INT AUTO_INCREMENT PRIMARY KEY,
            college_name VARCHAR(200) NOT NULL,
            location VARCHAR(100)
        )
        """
    )

    TABLES["students"] = (
        """
        CREATE TABLE IF NOT EXISTS students (
            student_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT UNIQUE,
            dob DATE,
            skills TEXT,
            income DECIMAL(10,2),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
        """
    )

    TABLES["teachers"] = (
        """
        CREATE TABLE IF NOT EXISTS teachers (
            teacher_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT UNIQUE,
            subject VARCHAR(100),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
        """
    )

    TABLES["attendance"] = (
        """
        CREATE TABLE IF NOT EXISTS attendance (
            attendance_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            teacher_id INT,
            date DATE,
            status ENUM('present','absent'),
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
        )
        """
    )

    TABLES["marks"] = (
        """
        CREATE TABLE IF NOT EXISTS marks (
            mark_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            subject VARCHAR(100),
            marks_obtained INT,
            total_marks INT,
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
        """
    )

    TABLES["scholarships"] = (
        """
        CREATE TABLE IF NOT EXISTS scholarships (
            scholarship_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            status ENUM('pending','approved','rejected'),
            criteria TEXT,
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
        """
    )

    TABLES["complaints"] = (
        """
        CREATE TABLE IF NOT EXISTS complaints (
            complaint_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            complaint_text TEXT,
            status ENUM('open','resolved') DEFAULT 'open',
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
        """
    )

    TABLES["timetable"] = (
        """
        CREATE TABLE IF NOT EXISTS timetable (
            timetable_id INT AUTO_INCREMENT PRIMARY KEY,
            teacher_id INT,
            subject VARCHAR(100),
            day VARCHAR(20),
            time_slot VARCHAR(20),
            FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
        )
        """
    )

    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()

        create_database(cursor, DB_NAME)
        cnx.database = DB_NAME

        for name, ddl in TABLES.items():
            try:
                print(f"Creating table {name}... ", end="")
                cursor.execute(ddl)
                print("OK")
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)

        cursor.close()
        cnx.close()
        print("Database setup complete ✅")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        exit(1)


if __name__ == "__main__":
    main()
