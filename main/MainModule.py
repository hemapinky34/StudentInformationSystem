from entity.Student import Student
from entity.Course import Course
from entity.Teacher import Teacher
from entity.Enrollment import Enrollment
from entity.Payment import Payment
from dao.StudentDAO import StudentDAO
from dao.CourseDAO import CourseDAO
from dao.TeacherDAO import TeacherDAO
from dao.EnrollmentDAO import EnrollmentDAO
from dao.PaymentDAO import PaymentDAO

from exception.CustomExceptions import (
    DuplicateEnrollmentException, CourseNotFoundException,
    StudentNotFoundException, TeacherNotFoundException,
    PaymentValidationException, InvalidStudentDataException,
    InvalidCourseDataException, InvalidEnrollmentDataException,
    InvalidTeacherDataException, InsufficientFundsException
)
from datetime import datetime, date
import sys


class MainModule:
    def __init__(self):
        self.student_dao = StudentDAO()
        self.course_dao = CourseDAO()
        self.teacher_dao = TeacherDAO()
        self.enrollment_dao = EnrollmentDAO()
        self.payment_dao = PaymentDAO()

    def display_menu(self):
        print("\nStudent Information System (SIS)")
        print("1. Student Management")
        print("2. Course Management")
        print("3. Teacher Management")
        print("4. Enrollment Management")
        print("5. Payment Management")
        print("6. Reports")
        print("7. Exit")

    def student_management_menu(self):
        while True:
            print("\nStudent Management")
            print("1. Add Student")
            print("2. Update Student")
            print("3. Delete Student")
            print("4. View Student")
            print("5. View All Students")
            print("6. Back to Main Menu")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.add_student()
            elif choice == '2':
                self.update_student()
            elif choice == '3':
                self.delete_student()
            elif choice == '4':
                self.view_student()
            elif choice == '5':
                self.view_all_students()
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")

    def add_student(self):
        print("\nAdd New Student")
        try:
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            date_of_birth = input("Enter date of birth (YYYY-MM-DD): ")
            email = input("Enter email: ")
            phone_number = input("Enter phone number: ")

            student = Student(
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                email=email,
                phone_number=phone_number
            )

            added_student = self.student_dao.add_student(student)
            print(f"Student added successfully with ID: {added_student.student_id}")
        except InvalidStudentDataException as e:
            print(f"Validation error: {e}")
        except Exception as e:
            print(f"Error adding student: {e}")

    def update_student(self):
        print("\nUpdate Student")
        try:
            student_id = int(input("Enter student ID to update: "))
            student = self.student_dao.get_student_by_id(student_id)

            if not student:
                print("Student not found")
                return

            print(f"Current details: {student}")

            first_name = input(f"Enter first name ({student.first_name}): ") or student.first_name
            last_name = input(f"Enter last name ({student.last_name}): ") or student.last_name
            date_of_birth = input(f"Enter date of birth ({student.date_of_birth}): ") or student.date_of_birth
            email = input(f"Enter email ({student.email}): ") or student.email
            phone_number = input(f"Enter phone number ({student.phone_number}): ") or student.phone_number

            updated_student = Student(
                student_id=student_id,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                email=email,
                phone_number=phone_number
            )

            self.student_dao.update_student(updated_student)
            print("Student updated successfully")
        except StudentNotFoundException as e:
            print(f"Error: {e}")
        except InvalidStudentDataException as e:
            print(f"Validation error: {e}")
        except Exception as e:
            print(f"Error updating student: {e}")

    def delete_student(self):
        print("\nDelete Student")
        try:
            student_id = int(input("Enter student ID to delete: "))
            success = self.student_dao.delete_student(student_id)
            if success:
                print("Student deleted successfully")
            else:
                print("Failed to delete student")
        except StudentNotFoundException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error deleting student: {e}")

    # In the view_student method of MainModule.py
    def view_student(self):
        print("\nView Student")
        try:
            student_id = int(input("Enter student ID: "))
            student = self.student_dao.get_student_by_id(student_id)
            print(student)  # This will now show phone number automatically

            # Show enrollments
            enrollments = self.enrollment_dao.get_enrollments_by_student(student_id)
            if enrollments:
                print("\nEnrollments:")
                for enrollment in enrollments:
                    course = self.course_dao.get_course_by_id(enrollment.course_id)
                    print(f"- {course.course_name} (Enrolled on: {enrollment.enrollment_date})")
            else:
                print("No enrollments found")

            # Show payments
            payments = self.payment_dao.get_payments_by_student(student_id)
            if payments:
                print("\nPayments:")
                for payment in payments:
                    print(f"- Amount: ${payment.amount:.2f} (Date: {payment.payment_date})")
            else:
                print("No payments found")
        except StudentNotFoundException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error viewing student: {e}")

    def view_all_students(self):
        print("\nAll Students")
        try:
            students = self.student_dao.get_all_students()
            for student in students:
                print(student)
        except Exception as e:
            print(f"Error retrieving students: {e}")

    def course_management_menu(self):
        while True:
            print("\nCourse Management")
            print("1. Add Course")
            print("2. Update Course")
            print("3. Delete Course")
            print("4. View Course")
            print("5. View All Courses")
            print("6. Back to Main Menu")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.add_course()
            elif choice == '2':
                self.update_course()
            elif choice == '3':
                self.delete_course()
            elif choice == '4':
                self.view_course()
            elif choice == '5':
                self.view_all_courses()
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")

    def add_course(self):
        print("\nAdd New Course")
        try:
            course_name = input("Enter course name: ")
            credits = int(input("Enter credits: "))
            course_code = input("Enter course code: ")
            teacher_id = input("Enter teacher ID (leave blank if none): ")

            course = Course(
                course_name=course_name,
                credits=credits,
                course_code=course_code,
                teacher_id=int(teacher_id) if teacher_id else None
            )

            added_course = self.course_dao.add_course(course)
            print(f"Course added successfully with ID: {added_course.course_id}")
        except InvalidCourseDataException as e:
            print(f"Validation error: {e}")
        except Exception as e:
            print(f"Error adding course: {e}")

    def update_course(self):
        print("\nUpdate Course")
        try:
            course_id = int(input("Enter course ID to update: "))
            course = self.course_dao.get_course_by_id(course_id)

            if not course:
                print("Course not found")
                return

            print(f"Current details: {course}")

            course_name = input(f"Enter course name ({course.course_name}): ") or course.course_name
            credits = input(f"Enter credits ({course.credits}): ") or course.credits
            course_code = input(f"Enter course code ({course.course_code}): ") or course.course_code
            teacher_id = input(f"Enter teacher ID ({course.teacher_id}): ") or course.teacher_id

            updated_course = Course(
                course_id=course_id,
                course_name=course_name,
                credits=int(credits),
                course_code=course_code,
                teacher_id=int(teacher_id) if teacher_id else None
            )

            self.course_dao.update_course(updated_course)
            print("Course updated successfully")
        except CourseNotFoundException as e:
            print(f"Error: {e}")
        except InvalidCourseDataException as e:
            print(f"Validation error: {e}")
        except Exception as e:
            print(f"Error updating course: {e}")

    def delete_course(self):
        print("\nDelete Course")
        try:
            course_id = int(input("Enter course ID to delete: "))
            success = self.course_dao.delete_course(course_id)
            if success:
                print("Course deleted successfully")
            else:
                print("Failed to delete course")
        except CourseNotFoundException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error deleting course: {e}")

    def view_course(self):
        print("\nView Course")
        try:
            course_id = int(input("Enter course ID: "))
            course = self.course_dao.get_course_by_id(course_id)
            print(course)

            if course.teacher_id:
                teacher = self.teacher_dao.get_teacher_by_id(course.teacher_id)
                print(f"Instructor: {teacher.first_name} {teacher.last_name}")
            else:
                print("No instructor assigned")

            # Show enrollments
            enrollments = self.enrollment_dao.get_enrollments_by_course(course_id)
            if enrollments:
                print("\nEnrollments:")
                for enrollment in enrollments:
                    student = self.student_dao.get_student_by_id(enrollment.student_id)
                    print(f"- {student.first_name} {student.last_name} (Enrolled on: {enrollment.enrollment_date})")
            else:
                print("No enrollments found")
        except CourseNotFoundException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error viewing course: {e}")

    def view_all_courses(self):
        print("\nAll Courses")
        try:
            courses = self.course_dao.get_all_courses()
            for course in courses:
                print(course)
        except Exception as e:
            print(f"Error retrieving courses: {e}")

    def teacher_management_menu(self):
        while True:
            print("\nTeacher Management")
            print("1. Add Teacher")
            print("2. Update Teacher")
            print("3. Delete Teacher")
            print("4. View Teacher")
            print("5. View All Teachers")
            print("6. Back to Main Menu")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.add_teacher()
            elif choice == '2':
                self.update_teacher()
            elif choice == '3':
                self.delete_teacher()
            elif choice == '4':
                self.view_teacher()
            elif choice == '5':
                self.view_all_teachers()
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")

    def add_teacher(self):
        print("\nAdd New Teacher")
        try:
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            email = input("Enter email: ")

            teacher = Teacher(
                first_name=first_name,
                last_name=last_name,
                email=email
            )

            added_teacher = self.teacher_dao.add_teacher(teacher)
            print(f"Teacher added successfully with ID: {added_teacher.teacher_id}")
        except InvalidTeacherDataException as e:
            print(f"Validation error: {e}")
        except Exception as e:
            print(f"Error adding teacher: {e}")

    def update_teacher(self):
        print("\nUpdate Teacher")
        try:
            teacher_id = int(input("Enter teacher ID to update: "))
            teacher = self.teacher_dao.get_teacher_by_id(teacher_id)

            if not teacher:
                print("Teacher not found")
                return

            print(f"Current details: {teacher}")

            first_name = input(f"Enter first name ({teacher.first_name}): ") or teacher.first_name
            last_name = input(f"Enter last name ({teacher.last_name}): ") or teacher.last_name
            email = input(f"Enter email ({teacher.email}): ") or teacher.email

            updated_teacher = Teacher(
                teacher_id=teacher_id,
                first_name=first_name,
                last_name=last_name,
                email=email
            )

            self.teacher_dao.update_teacher(updated_teacher)
            print("Teacher updated successfully")
        except TeacherNotFoundException as e:
            print(f"Error: {e}")
        except InvalidTeacherDataException as e:
            print(f"Validation error: {e}")
        except Exception as e:
            print(f"Error updating teacher: {e}")

    def delete_teacher(self):
        print("\nDelete Teacher")
        try:
            teacher_id = int(input("Enter teacher ID to delete: "))
            success = self.teacher_dao.delete_teacher(teacher_id)
            if success:
                print("Teacher deleted successfully")
            else:
                print("Failed to delete teacher")
        except TeacherNotFoundException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error deleting teacher: {e}")

    def view_teacher(self):
        print("\nView Teacher")
        try:
            teacher_id = int(input("Enter teacher ID: "))
            teacher = self.teacher_dao.get_teacher_by_id(teacher_id)
            print(teacher)

            # Show assigned courses
            courses = self.course_dao.get_all_courses()
            assigned_courses = [c for c in courses if c.teacher_id == teacher_id]

            if assigned_courses:
                print("\nAssigned Courses:")
                for course in assigned_courses:
                    print(f"- {course.course_name} ({course.course_code})")
            else:
                print("No courses assigned")
        except TeacherNotFoundException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error viewing teacher: {e}")

    def view_all_teachers(self):
        print("\nAll Teachers")
        try:
            teachers = self.teacher_dao.get_all_teachers()
            for teacher in teachers:
                print(teacher)
        except Exception as e:
            print(f"Error retrieving teachers: {e}")

    def enrollment_management_menu(self):
        while True:
            print("\nEnrollment Management")
            print("1. Enroll Student in Course")
            print("2. View Enrollment")
            print("3. View All Enrollments")
            print("4. Delete Enrollment")
            print("5. Back to Main Menu")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.enroll_student()
            elif choice == '2':
                self.view_enrollment()
            elif choice == '3':
                self.view_all_enrollments()
            elif choice == '4':
                self.delete_enrollment()
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please try again.")

    def enroll_student(self):
        print("\nEnroll Student in Course")
        try:
            student_id = int(input("Enter student ID: "))
            course_id = int(input("Enter course ID: "))

            enrollment = Enrollment(
                student_id=student_id,
                course_id=course_id
            )

            added_enrollment = self.enrollment_dao.enroll_student(enrollment)
            print(f"Student enrolled successfully with enrollment ID: {added_enrollment.enrollment_id}")
        except DuplicateEnrollmentException as e:
            print(f"Error: {e}")
        except StudentNotFoundException as e:
            print(f"Error: {e}")
        except CourseNotFoundException as e:
            print(f"Error: {e}")
        except InvalidEnrollmentDataException as e:
            print(f"Validation error: {e}")
        except Exception as e:
            print(f"Error enrolling student: {e}")

    def view_enrollment(self):
        print("\nView Enrollment")
        try:
            enrollment_id = int(input("Enter enrollment ID: "))
            enrollment = self.enrollment_dao.get_enrollment_by_id(enrollment_id)

            if not enrollment:
                print("Enrollment not found")
                return

            student = self.student_dao.get_student_by_id(enrollment.student_id)
            course = self.course_dao.get_course_by_id(enrollment.course_id)

            print(f"Enrollment ID: {enrollment.enrollment_id}")
            print(f"Student: {student.first_name} {student.last_name} (ID: {student.student_id})")
            print(f"Course: {course.course_name} (ID: {course.course_id})")
            print(f"Enrollment Date: {enrollment.enrollment_date}")
        except Exception as e:
            print(f"Error viewing enrollment: {e}")

    def view_all_enrollments(self):
        print("\nAll Enrollments")
        try:
            enrollments = self.enrollment_dao.get_all_enrollments()
            for enrollment in enrollments:
                student = self.student_dao.get_student_by_id(enrollment.student_id)
                course = self.course_dao.get_course_by_id(enrollment.course_id)
                print(
                    f"Enrollment {enrollment.enrollment_id}: {student.first_name} {student.last_name} in {course.course_name} on {enrollment.enrollment_date}")
        except Exception as e:
            print(f"Error retrieving enrollments: {e}")

    def delete_enrollment(self):
        print("\nDelete Enrollment")
        try:
            enrollment_id = int(input("Enter enrollment ID to delete: "))
            success = self.enrollment_dao.delete_enrollment(enrollment_id)
            if success:
                print("Enrollment deleted successfully")
            else:
                print("Failed to delete enrollment")
        except Exception as e:
            print(f"Error deleting enrollment: {e}")

    def payment_management_menu(self):
        while True:
            print("\nPayment Management")
            print("1. Record Payment")
            print("2. View Payment")
            print("3. View All Payments")
            print("4. View Payments by Student")
            print("5. Delete Payment")
            print("6. Back to Main Menu")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.record_payment()
            elif choice == '2':
                self.view_payment()
            elif choice == '3':
                self.view_all_payments()
            elif choice == '4':
                self.view_payments_by_student()
            elif choice == '5':
                self.delete_payment()
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")

    def record_payment(self):
        print("\nRecord Payment")
        try:
            student_id = int(input("Enter student ID: "))
            amount = float(input("Enter payment amount: "))
            payment_date = input("Enter payment date (YYYY-MM-DD or leave blank for today): ")

            if not payment_date:
                payment_date = date.today()
            else:
                payment_date = datetime.strptime(payment_date, '%Y-%m-%d').date()

            payment = Payment(
                student_id=student_id,
                amount=amount,
                payment_date=payment_date
            )

            added_payment = self.payment_dao.record_payment(payment)
            print(f"Payment recorded successfully with ID: {added_payment.payment_id}")
        except PaymentValidationException as e:
            print(f"Validation error: {e}")
        except StudentNotFoundException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error recording payment: {e}")

    def view_payment(self):
        print("\nView Payment")
        try:
            payment_id = int(input("Enter payment ID: "))
            payment = self.payment_dao.get_payment_by_id(payment_id)

            if not payment:
                print("Payment not found")
                return

            student = self.student_dao.get_student_by_id(payment.student_id)

            print(f"Payment ID: {payment.payment_id}")
            print(f"Student: {student.first_name} {student.last_name} (ID: {student.student_id})")
            print(f"Amount: ${payment.amount:.2f}")
            print(f"Payment Date: {payment.payment_date}")
        except Exception as e:
            print(f"Error viewing payment: {e}")

    def view_all_payments(self):
        print("\nAll Payments")
        try:
            payments = self.payment_dao.get_all_payments()
            for payment in payments:
                student = self.student_dao.get_student_by_id(payment.student_id)
                print(
                    f"Payment {payment.payment_id}: {student.first_name} {student.last_name} paid ${payment.amount:.2f} on {payment.payment_date}")
        except Exception as e:
            print(f"Error retrieving payments: {e}")

    def view_payments_by_student(self):
        print("\nPayments by Student")
        try:
            student_id = int(input("Enter student ID: "))
            payments = self.payment_dao.get_payments_by_student(student_id)

            if not payments:
                print("No payments found for this student")
                return

            student = self.student_dao.get_student_by_id(student_id)
            print(f"Payments for {student.first_name} {student.last_name}:")

            total = 0
            for payment in payments:
                print(f"- ${payment.amount:.2f} on {payment.payment_date}")
                total += payment.amount

            print(f"\nTotal payments: ${total:.2f}")
        except StudentNotFoundException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error retrieving payments: {e}")

    def delete_payment(self):
        print("\nDelete Payment")
        try:
            payment_id = int(input("Enter payment ID to delete: "))
            success = self.payment_dao.delete_payment(payment_id)
            if success:
                print("Payment deleted successfully")
            else:
                print("Failed to delete payment")
        except Exception as e:
            print(f"Error deleting payment: {e}")

    def reports_menu(self):
        while True:
            print("\nReports")
            print("1. Students Enrolled in a Course")
            print("2. Courses with Most Enrollments")
            print("3. Teachers with Their Courses")
            print("4. Students with No Payments")
            print("5. Courses with No Enrollments")
            print("6. Back to Main Menu")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.students_in_course_report()
            elif choice == '2':
                self.courses_with_most_enrollments()
            elif choice == '3':
                self.teachers_with_courses()
            elif choice == '4':
                self.students_with_no_payments()
            elif choice == '5':
                self.courses_with_no_enrollments()
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")

    def students_in_course_report(self):
        print("\nStudents Enrolled in a Course")
        try:
            course_id = int(input("Enter course ID: "))
            enrollments = self.enrollment_dao.get_enrollments_by_course(course_id)

            if not enrollments:
                print("No enrollments found for this course")
                return

            course = self.course_dao.get_course_by_id(course_id)
            print(f"\nStudents enrolled in {course.course_name}:")

            for enrollment in enrollments:
                student = self.student_dao.get_student_by_id(enrollment.student_id)
                print(f"- {student.first_name} {student.last_name} (Enrolled on: {enrollment.enrollment_date})")
        except CourseNotFoundException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error generating report: {e}")

    def courses_with_most_enrollments(self):
        print("\nCourses with Most Enrollments")
        try:
            # Get all courses and count their enrollments
            courses = self.course_dao.get_all_courses()
            course_enrollments = []

            for course in courses:
                enrollments = self.enrollment_dao.get_enrollments_by_course(course.course_id)
                course_enrollments.append((course, len(enrollments)))

            # Sort by enrollment count descending
            course_enrollments.sort(key=lambda x: x[1], reverse=True)

            print("\nCourses by enrollment count:")
            for course, count in course_enrollments:
                print(f"- {course.course_name}: {count} enrollments")
        except Exception as e:
            print(f"Error generating report: {e}")

    def teachers_with_courses(self):
        print("\nTeachers with Their Courses")
        try:
            teachers = self.teacher_dao.get_all_teachers()
            courses = self.course_dao.get_all_courses()

            if not teachers:
                print("No teachers found")
                return

            for teacher in teachers:
                print(f"\n{teacher.first_name} {teacher.last_name}:")
                assigned_courses = [c for c in courses if c.teacher_id == teacher.teacher_id]

                if assigned_courses:
                    for course in assigned_courses:
                        print(f"- {course.course_name} ({course.course_code})")
                else:
                    print("No courses assigned")
        except Exception as e:
            print(f"Error generating report: {e}")

    def students_with_no_payments(self):
        print("\nStudents with No Payments")
        try:
            students = self.student_dao.get_all_students()
            students_with_no_payments = []

            for student in students:
                payments = self.payment_dao.get_payments_by_student(student.student_id)
                if not payments:
                    students_with_no_payments.append(student)

            if students_with_no_payments:
                print("\nStudents with no payments:")
                for student in students_with_no_payments:
                    print(f"- {student.first_name} {student.last_name} (ID: {student.student_id})")
            else:
                print("All students have made at least one payment")
        except Exception as e:
            print(f"Error generating report: {e}")

    def courses_with_no_enrollments(self):
        print("\nCourses with No Enrollments")
        try:
            courses = self.course_dao.get_all_courses()
            courses_with_no_enrollments = []

            for course in courses:
                enrollments = self.enrollment_dao.get_enrollments_by_course(course.course_id)
                if not enrollments:
                    courses_with_no_enrollments.append(course)

            if courses_with_no_enrollments:
                print("\nCourses with no enrollments:")
                for course in courses_with_no_enrollments:
                    print(f"- {course.course_name} ({course.course_code})")
            else:
                print("All courses have at least one enrollment")
        except Exception as e:
            print(f"Error generating report: {e}")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")

            if choice == '1':
                self.student_management_menu()
            elif choice == '2':
                self.course_management_menu()
            elif choice == '3':
                self.teacher_management_menu()
            elif choice == '4':
                self.enrollment_management_menu()
            elif choice == '5':
                self.payment_management_menu()
            elif choice == '6':
                self.reports_menu()
            elif choice == '7':
                print("Exiting the system. Goodbye!")
                sys.exit()
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    sis = MainModule()
    sis.run()