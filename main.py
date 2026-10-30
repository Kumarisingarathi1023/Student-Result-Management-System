import sqlite3


# Get valid marks from the user
def get_marks(subject):
    while True:
        try:
            marks = int(input(f"Enter {subject} marks: "))

            if 0 <= marks <= 100:
                return marks

            print("Marks must be between 0 and 100.")

        except ValueError:
            print("Please enter a valid number.")


# Calculate grade
def calculate_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"


# Add a new student
def add_student():
    try:
        student_id = int(input("Enter Student ID: "))
    except ValueError:
        print("Student ID must be a number.")
        return

    name = input("Enter Student Name: ").strip()

    if not name:
        print("Student name cannot be empty.")
        return

    python_marks = get_marks("Python")
    sql_marks = get_marks("SQL")
    dsa_marks = get_marks("DSA")

    # Calculate result
    total = python_marks + sql_marks + dsa_marks
    percentage = round(total / 3, 2)
    grade = calculate_grade(percentage)

    connection = sqlite3.connect("students.db")
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO students
            (id, name, python_marks, sql_marks, dsa_marks,
             total, percentage, grade)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            student_id,
            name,
            python_marks,
            sql_marks,
            dsa_marks,
            total,
            percentage,
            grade
        ))

        connection.commit()

        print("\nStudent added successfully!")
        print("Total:", total)
        print("Percentage:", percentage)
        print("Grade:", grade)

    except sqlite3.IntegrityError:
        print("\nStudent ID already exists.")

    finally:
        connection.close()


# View all students
def view_students():
    connection = sqlite3.connect("students.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM students
        ORDER BY id
    """)

    students = cursor.fetchall()

    connection.close()

    if not students:
        print("\nNo students found.")
        return

    print("\n========== ALL STUDENTS ==========")

    for student in students:
        print("----------------------------------")
        print("Student ID :", student[0])
        print("Name       :", student[1])
        print("Python     :", student[2])
        print("SQL        :", student[3])
        print("DSA        :", student[4])
        print("Total      :", student[5])
        print("Percentage :", student[6])
        print("Grade      :", student[7])

    print("----------------------------------")


# Search student by ID
def search_student():
    try:
        student_id = int(input("Enter Student ID to search: "))
    except ValueError:
        print("Student ID must be a number.")
        return

    connection = sqlite3.connect("students.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    )

    student = cursor.fetchone()

    connection.close()

    if student:
        print("\n========== STUDENT FOUND ==========")
        print("Student ID :", student[0])
        print("Name       :", student[1])
        print("Python     :", student[2])
        print("SQL        :", student[3])
        print("DSA        :", student[4])
        print("Total      :", student[5])
        print("Percentage :", student[6])
        print("Grade      :", student[7])
    else:
        print("\nStudent not found.")


# Update student marks
def update_student():
    try:
        student_id = int(input("Enter Student ID to update: "))
    except ValueError:
        print("Student ID must be a number.")
        return

    connection = sqlite3.connect("students.db")
    cursor = connection.cursor()

    # Check whether student exists
    cursor.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    )

    student = cursor.fetchone()

    if not student:
        print("\nStudent not found.")
        connection.close()
        return

    print("\nEnter new marks:")

    python_marks = get_marks("Python")
    sql_marks = get_marks("SQL")
    dsa_marks = get_marks("DSA")

    # Recalculate result
    total = python_marks + sql_marks + dsa_marks
    percentage = round(total / 3, 2)
    grade = calculate_grade(percentage)

    cursor.execute("""
        UPDATE students
        SET python_marks = ?,
            sql_marks = ?,
            dsa_marks = ?,
            total = ?,
            percentage = ?,
            grade = ?
        WHERE id = ?
    """, (
        python_marks,
        sql_marks,
        dsa_marks,
        total,
        percentage,
        grade,
        student_id
    ))

    connection.commit()
    connection.close()

    print("\nStudent updated successfully!")
    print("New Total:", total)
    print("New Percentage:", percentage)
    print("New Grade:", grade)


# Delete student
def delete_student():
    try:
        student_id = int(input("Enter Student ID to delete: "))
    except ValueError:
        print("Student ID must be a number.")
        return

    connection = sqlite3.connect("students.db")
    cursor = connection.cursor()

    # Check whether student exists
    cursor.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    )

    student = cursor.fetchone()

    if not student:
        print("\nStudent not found.")
        connection.close()
        return

    # Ask for confirmation
    confirm = input(
        f"Are you sure you want to delete {student[1]}? (yes/no): "
    ).lower()

    if confirm != "yes":
        print("Delete operation cancelled.")
        connection.close()
        return

    cursor.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    connection.commit()
    connection.close()

    print("\nStudent deleted successfully!")


# Find top student
def top_student():
    connection = sqlite3.connect("students.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM students
        ORDER BY percentage DESC
        LIMIT 1
    """)

    student = cursor.fetchone()

    connection.close()

    if not student:
        print("\nNo students found.")
        return

    print("\n========== TOP STUDENT ==========")
    print("Student ID :", student[0])
    print("Name       :", student[1])
    print("Python     :", student[2])
    print("SQL        :", student[3])
    print("DSA        :", student[4])
    print("Total      :", student[5])
    print("Percentage :", student[6])
    print("Grade      :", student[7])


# Main menu
while True:

    print("\n==========================================")
    print("     STUDENT RESULT MANAGEMENT SYSTEM")
    print("==========================================")
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Find Top Student")
    print("7. Exit")
    print("==========================================")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_student()

    elif choice == "2":
        view_students()

    elif choice == "3":
        search_student()

    elif choice == "4":
        update_student()

    elif choice == "5":
        delete_student()

    elif choice == "6":
        top_student()

    elif choice == "7":
        print("\nThank you for using the Student Result Management System!")
        break

    else:
        print("\nInvalid choice. Please select 1-7.")