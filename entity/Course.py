class Course:
    def __init__(self, course_id=None, course_name=None, credits=None, teacher_id=None, course_code=None):
        self.course_id = course_id
        self.course_name = course_name
        self.credits = credits
        self.teacher_id = teacher_id
        self.course_code = course_code

    def __str__(self):
        return f"Course ID: {self.course_id}, Name: {self.course_name}, Code: {self.course_code}"