from entity.Course import Course
from dao.interfaces.AllInterfaces import ICourseService
from util.DBConnUtil import DBConnUtil
from util.DBPropertyUtil import DBPropertyUtil
from util.DBConnUtil import DBConnUtil
from exception.CustomExceptions import CourseNotFoundException, InvalidCourseDataException


class CourseDAO(ICourseService):
    def __init__(self):
        self.connection = DBConnUtil.get_connection(DBPropertyUtil.get_connection_string('resources/db.properties'))

    def get_course_by_id(self, course_id):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Courses WHERE course_id = %s", (course_id,))
            course_data = cursor.fetchone()

            if not course_data:
                raise CourseNotFoundException(f"Course with ID {course_id} not found")

            course = Course(
                course_data['course_id'],
                course_data['course_name'],
                course_data['credits'],
                course_data['teacher_id'],
                course_data['course_code']
            )
            return course
        except Exception as e:
            print(f"Error getting course by ID: {e}")
            raise
        finally:
            cursor.close()

    def get_course_by_code(self, course_code):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Courses WHERE course_code = %s", (course_code,))
            course_data = cursor.fetchone()

            if not course_data:
                raise CourseNotFoundException(f"Course with code {course_code} not found")

            course = Course(
                course_data['course_id'],
                course_data['course_name'],
                course_data['credits'],
                course_data['teacher_id'],
                course_data['course_code']
            )
            return course
        except Exception as e:
            print(f"Error getting course by code: {e}")
            raise
        finally:
            cursor.close()

    def get_all_courses(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Courses")
            courses = []

            for course_data in cursor.fetchall():
                course = Course(
                    course_data['course_id'],
                    course_data['course_name'],
                    course_data['credits'],
                    course_data['teacher_id'],
                    course_data['course_code']
                )
                courses.append(course)

            return courses
        except Exception as e:
            print(f"Error getting all courses: {e}")
            raise
        finally:
            cursor.close()

    def add_course(self, course):
        try:
            cursor = self.connection.cursor()

            # Validate course data
            if not all([course.course_name, course.credits, course.course_code]):
                raise InvalidCourseDataException("Course name, credits, and code are required")

            if not isinstance(course.credits, int) or course.credits <= 0:
                raise InvalidCourseDataException("Credits must be a positive integer")

            cursor.execute(
                "INSERT INTO Courses (course_name, credits, teacher_id, course_code) VALUES (%s, %s, %s, %s)",
                (course.course_name, course.credits, course.teacher_id, course.course_code)
            )
            self.connection.commit()
            course.course_id = cursor.lastrowid
            return course
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding course: {e}")
            raise
        finally:
            cursor.close()

    def update_course(self, course):
        try:
            cursor = self.connection.cursor()

            # Check if course exists
            if not self.get_course_by_id(course.course_id):
                raise CourseNotFoundException(f"Course with ID {course.course_id} not found")

            cursor.execute(
                "UPDATE Courses SET course_name = %s, credits = %s, teacher_id = %s, course_code = %s WHERE course_id = %s",
                (course.course_name, course.credits, course.teacher_id, course.course_code, course.course_id)
            )
            self.connection.commit()
            return course
        except Exception as e:
            self.connection.rollback()
            print(f"Error updating course: {e}")
            raise
        finally:
            cursor.close()

    def delete_course(self, course_id):
        try:
            cursor = self.connection.cursor()

            # Check if course exists
            if not self.get_course_by_id(course_id):
                raise CourseNotFoundException(f"Course with ID {course_id} not found")

            # First delete dependent records (enrollments)
            cursor.execute("DELETE FROM Enrollments WHERE course_id = %s", (course_id,))

            # Then delete the course
            cursor.execute("DELETE FROM Courses WHERE course_id = %s", (course_id,))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error deleting course: {e}")
            raise
        finally:
            cursor.close()