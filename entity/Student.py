# entity/Student.py
class Student:
    def __init__(self, student_id=None, first_name=None, last_name=None, date_of_birth=None, email=None, phone_number=None):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.email = email
        self.phone_number = phone_number

    def __str__(self):
        return f"Student ID: {self.student_id}, Name: {self.first_name} {self.last_name}, Email: {self.email}, Phone: {self.phone_number}"