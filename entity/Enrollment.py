from datetime import date

class Enrollment:
    def __init__(self, enrollment_id=None, student_id=None, course_id=None, enrollment_date=None):
        self.enrollment_id = enrollment_id
        self.student_id = student_id
        self.course_id = course_id
        self.enrollment_date = enrollment_date if enrollment_date else date.today()

    def __str__(self):
        return f"Enrollment ID: {self.enrollment_id}, Student ID: {self.student_id}, Course ID: {self.course_id}, Date: {self.enrollment_date}"