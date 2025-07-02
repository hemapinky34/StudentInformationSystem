from entity.Student import Student
from dao.interfaces.AllInterfaces import IStudentService
from util.DBPropertyUtil import DBPropertyUtil
from util.DBConnUtil import DBConnUtil
from datetime import datetime
from exception.CustomExceptions import StudentNotFoundException, InvalidStudentDataException


class StudentDAO(IStudentService):
    def __init__(self):
        self.connection = DBConnUtil.get_connection(DBPropertyUtil.get_connection_string('resources/db.properties'))

    def get_student_by_id(self, student_id):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Students WHERE student_id = %s", (student_id,))
            student_data = cursor.fetchone()

            if not student_data:
                raise StudentNotFoundException(f"Student with ID {student_id} not found")

            student = Student(
                student_data['student_id'],
                student_data['first_name'],
                student_data['last_name'],
                student_data['date_of_birth'],
                student_data['email'],
                student_data['phone_number']
            )
            return student
        except Exception as e:
            print(f"Error getting student by ID: {e}")
            raise
        finally:
            cursor.close()

    def get_all_students(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Students")
            students = []

            for student_data in cursor.fetchall():
                student = Student(
                    student_data['student_id'],
                    student_data['first_name'],
                    student_data['last_name'],
                    student_data['date_of_birth'],
                    student_data['email'],
                    student_data['phone_number']
                )
                students.append(student)

            return students
        except Exception as e:
            print(f"Error getting all students: {e}")
            raise
        finally:
            cursor.close()

    def add_student(self, student):
        try:
            cursor = self.connection.cursor()

            # Validate student data
            if not all([student.first_name, student.last_name, student.date_of_birth, student.email,
                        student.phone_number]):
                raise InvalidStudentDataException("All student fields are required")

            # Validate email format
            if '@' not in student.email or '.' not in student.email:
                raise InvalidStudentDataException("Invalid email format")

            # Validate date format
            try:
                datetime.strptime(str(student.date_of_birth), '%Y-%m-%d')
            except ValueError:
                raise InvalidStudentDataException("Invalid date format. Use YYYY-MM-DD")

            cursor.execute(
                "INSERT INTO Students (first_name, last_name, date_of_birth, email, phone_number) VALUES (%s, %s, %s, %s, %s)",
                (student.first_name, student.last_name, student.date_of_birth, student.email, student.phone_number)
            )
            self.connection.commit()
            student.student_id = cursor.lastrowid
            return student
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding student: {e}")
            raise
        finally:
            cursor.close()

    def update_student(self, student):
        try:
            cursor = self.connection.cursor()

            # Check if student exists
            if not self.get_student_by_id(student.student_id):
                raise StudentNotFoundException(f"Student with ID {student.student_id} not found")

            cursor.execute(
                "UPDATE Students SET first_name = %s, last_name = %s, date_of_birth = %s, email = %s, phone_number = %s WHERE student_id = %s",
                (student.first_name, student.last_name, student.date_of_birth, student.email, student.phone_number,
                 student.student_id)
            )
            self.connection.commit()
            return student
        except Exception as e:
            self.connection.rollback()
            print(f"Error updating student: {e}")
            raise
        finally:
            cursor.close()

    def delete_student(self, student_id):
        try:
            cursor = self.connection.cursor()

            # Check if student exists
            if not self.get_student_by_id(student_id):
                raise StudentNotFoundException(f"Student with ID {student_id} not found")

            # First delete dependent records (enrollments and payments)
            cursor.execute("DELETE FROM Enrollments WHERE student_id = %s", (student_id,))
            cursor.execute("DELETE FROM Payments WHERE student_id = %s", (student_id,))

            # Then delete the student
            cursor.execute("DELETE FROM Students WHERE student_id = %s", (student_id,))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error deleting student: {e}")
            raise
        finally:
            cursor.close()