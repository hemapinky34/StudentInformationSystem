from entity.Enrollment import Enrollment
from dao.interfaces.AllInterfaces import IEnrollmentService
from util.DBConnUtil import DBConnUtil
from util.DBPropertyUtil import DBPropertyUtil
from util.DBConnUtil import DBConnUtil
from exception.CustomExceptions import DuplicateEnrollmentException, InvalidEnrollmentDataException, StudentNotFoundException, \
    CourseNotFoundException
from datetime import date


class EnrollmentDAO(IEnrollmentService):
    def __init__(self):
        self.connection = DBConnUtil.get_connection(DBPropertyUtil.get_connection_string('resources/db.properties'))

    def get_enrollment_by_id(self, enrollment_id):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Enrollments WHERE enrollment_id = %s", (enrollment_id,))
            enrollment_data = cursor.fetchone()

            if not enrollment_data:
                return None

            enrollment = Enrollment(
                enrollment_data['enrollment_id'],
                enrollment_data['student_id'],
                enrollment_data['course_id'],
                enrollment_data['enrollment_date']
            )
            return enrollment
        except Exception as e:
            print(f"Error getting enrollment by ID: {e}")
            raise
        finally:
            cursor.close()

    def get_enrollments_by_student(self, student_id):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Enrollments WHERE student_id = %s", (student_id,))
            enrollments = []

            for enrollment_data in cursor.fetchall():
                enrollment = Enrollment(
                    enrollment_data['enrollment_id'],
                    enrollment_data['student_id'],
                    enrollment_data['course_id'],
                    enrollment_data['enrollment_date']
                )
                enrollments.append(enrollment)

            return enrollments
        except Exception as e:
            print(f"Error getting enrollments by student: {e}")
            raise
        finally:
            cursor.close()

    def get_enrollments_by_course(self, course_id):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Enrollments WHERE course_id = %s", (course_id,))
            enrollments = []

            for enrollment_data in cursor.fetchall():
                enrollment = Enrollment(
                    enrollment_data['enrollment_id'],
                    enrollment_data['student_id'],
                    enrollment_data['course_id'],
                    enrollment_data['enrollment_date']
                )
                enrollments.append(enrollment)

            return enrollments
        except Exception as e:
            print(f"Error getting enrollments by course: {e}")
            raise
        finally:
            cursor.close()

    def get_all_enrollments(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Enrollments")
            enrollments = []

            for enrollment_data in cursor.fetchall():
                enrollment = Enrollment(
                    enrollment_data['enrollment_id'],
                    enrollment_data['student_id'],
                    enrollment_data['course_id'],
                    enrollment_data['enrollment_date']
                )
                enrollments.append(enrollment)

            return enrollments
        except Exception as e:
            print(f"Error getting all enrollments: {e}")
            raise
        finally:
            cursor.close()

    def enroll_student(self, enrollment):
        try:
            cursor = self.connection.cursor()

            # Validate enrollment data
            if not all([enrollment.student_id, enrollment.course_id]):
                raise InvalidEnrollmentDataException("Student ID and Course ID are required")

            # Check if student exists
            student_dao = StudentDAO()
            if not student_dao.get_student_by_id(enrollment.student_id):
                raise StudentNotFoundException(f"Student with ID {enrollment.student_id} not found")

            # Check if course exists
            course_dao = CourseDAO()
            if not course_dao.get_course_by_id(enrollment.course_id):
                raise CourseNotFoundException(f"Course with ID {enrollment.course_id} not found")

            # Check for duplicate enrollment
            cursor.execute(
                "SELECT * FROM Enrollments WHERE student_id = %s AND course_id = %s",
                (enrollment.student_id, enrollment.course_id)
            )
            if cursor.fetchone():
                raise DuplicateEnrollmentException(
                    f"Student {enrollment.student_id} is already enrolled in course {enrollment.course_id}")

            cursor.execute(
                "INSERT INTO Enrollments (student_id, course_id, enrollment_date) VALUES (%s, %s, %s)",
                (enrollment.student_id, enrollment.course_id, enrollment.enrollment_date)
            )
            self.connection.commit()
            enrollment.enrollment_id = cursor.lastrowid
            return enrollment
        except Exception as e:
            self.connection.rollback()
            print(f"Error enrolling student: {e}")
            raise
        finally:
            cursor.close()

    def update_enrollment(self, enrollment):
        try:
            cursor = self.connection.cursor()

            # Check if enrollment exists
            if not self.get_enrollment_by_id(enrollment.enrollment_id):
                return None

            cursor.execute(
                "UPDATE Enrollments SET student_id = %s, course_id = %s, enrollment_date = %s WHERE enrollment_id = %s",
                (enrollment.student_id, enrollment.course_id, enrollment.enrollment_date, enrollment.enrollment_id)
            )
            self.connection.commit()
            return enrollment
        except Exception as e:
            self.connection.rollback()
            print(f"Error updating enrollment: {e}")
            raise
        finally:
            cursor.close()

    def delete_enrollment(self, enrollment_id):
        try:
            cursor = self.connection.cursor()

            # Check if enrollment exists
            if not self.get_enrollment_by_id(enrollment_id):
                return False

            cursor.execute("DELETE FROM Enrollments WHERE enrollment_id = %s", (enrollment_id,))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error deleting enrollment: {e}")
            raise
        finally:
            cursor.close()