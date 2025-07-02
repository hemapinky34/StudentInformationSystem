from entity.Teacher import Teacher
from dao.interfaces.AllInterfaces import ITeacherService
from util.DBConnUtil import DBConnUtil
from util.DBPropertyUtil import DBPropertyUtil
from util.DBConnUtil import DBConnUtil
from exception.CustomExceptions import TeacherNotFoundException, InvalidTeacherDataException


class TeacherDAO(ITeacherService):
    def __init__(self):
        self.connection = DBConnUtil.get_connection(DBPropertyUtil.get_connection_string('resources/db.properties'))

    def get_teacher_by_id(self, teacher_id):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Teacher WHERE teacher_id = %s", (teacher_id,))
            teacher_data = cursor.fetchone()

            if not teacher_data:
                raise TeacherNotFoundException(f"Teacher with ID {teacher_id} not found")

            teacher = Teacher(
                teacher_data['teacher_id'],
                teacher_data['first_name'],
                teacher_data['last_name'],
                teacher_data['email']
            )
            return teacher
        except Exception as e:
            print(f"Error getting teacher by ID: {e}")
            raise
        finally:
            cursor.close()

    def get_all_teachers(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Teacher")
            teachers = []

            for teacher_data in cursor.fetchall():
                teacher = Teacher(
                    teacher_data['teacher_id'],
                    teacher_data['first_name'],
                    teacher_data['last_name'],
                    teacher_data['email']
                )
                teachers.append(teacher)

            return teachers
        except Exception as e:
            print(f"Error getting all teachers: {e}")
            raise
        finally:
            cursor.close()

    def add_teacher(self, teacher):
        try:
            cursor = self.connection.cursor()

            # Validate teacher data
            if not all([teacher.first_name, teacher.last_name, teacher.email]):
                raise InvalidTeacherDataException("All teacher fields are required")

            # Validate email format
            if '@' not in teacher.email or '.' not in teacher.email:
                raise InvalidTeacherDataException("Invalid email format")

            cursor.execute(
                "INSERT INTO Teacher (first_name, last_name, email) VALUES (%s, %s, %s)",
                (teacher.first_name, teacher.last_name, teacher.email)
            )
            self.connection.commit()
            teacher.teacher_id = cursor.lastrowid
            return teacher
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding teacher: {e}")
            raise
        finally:
            cursor.close()

    def update_teacher(self, teacher):
        try:
            cursor = self.connection.cursor()

            # Check if teacher exists
            if not self.get_teacher_by_id(teacher.teacher_id):
                raise TeacherNotFoundException(f"Teacher with ID {teacher.teacher_id} not found")

            cursor.execute(
                "UPDATE Teacher SET first_name = %s, last_name = %s, email = %s WHERE teacher_id = %s",
                (teacher.first_name, teacher.last_name, teacher.email, teacher.teacher_id)
            )
            self.connection.commit()
            return teacher
        except Exception as e:
            self.connection.rollback()
            print(f"Error updating teacher: {e}")
            raise
        finally:
            cursor.close()

    def delete_teacher(self, teacher_id):
        try:
            cursor = self.connection.cursor()

            # Check if teacher exists
            if not self.get_teacher_by_id(teacher_id):
                raise TeacherNotFoundException(f"Teacher with ID {teacher_id} not found")

            # First update courses that have this teacher assigned
            cursor.execute("UPDATE Courses SET teacher_id = NULL WHERE teacher_id = %s", (teacher_id,))

            # Then delete the teacher
            cursor.execute("DELETE FROM Teacher WHERE teacher_id = %s", (teacher_id,))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error deleting teacher: {e}")
            raise
        finally:
            cursor.close()