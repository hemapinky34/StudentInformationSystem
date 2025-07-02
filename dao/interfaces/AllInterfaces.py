from abc import ABC, abstractmethod


class IStudentService(ABC):
    @abstractmethod
    def get_student_by_id(self, student_id):
        pass

    @abstractmethod
    def get_all_students(self):
        pass

    @abstractmethod
    def add_student(self, student):
        pass

    @abstractmethod
    def update_student(self, student):
        pass

    @abstractmethod
    def delete_student(self, student_id):
        pass


class ICourseService(ABC):
    @abstractmethod
    def get_course_by_id(self, course_id):
        pass

    @abstractmethod
    def get_all_courses(self):
        pass

    @abstractmethod
    def add_course(self, course):
        pass

    @abstractmethod
    def update_course(self, course):
        pass

    @abstractmethod
    def delete_course(self, course_id):
        pass


class ITeacherService(ABC):
    @abstractmethod
    def get_teacher_by_id(self, teacher_id):
        pass

    @abstractmethod
    def get_all_teachers(self):
        pass

    @abstractmethod
    def add_teacher(self, teacher):
        pass

    @abstractmethod
    def update_teacher(self, teacher):
        pass

    @abstractmethod
    def delete_teacher(self, teacher_id):
        pass


class IEnrollmentService(ABC):
    @abstractmethod
    def get_enrollment_by_id(self, enrollment_id):
        pass

    @abstractmethod
    def get_all_enrollments(self):
        pass

    @abstractmethod
    def enroll_student(self, enrollment):
        pass

    @abstractmethod
    def update_enrollment(self, enrollment):
        pass

    @abstractmethod
    def delete_enrollment(self, enrollment_id):
        pass


class IPaymentService(ABC):
    @abstractmethod
    def get_payment_by_id(self, payment_id):
        pass

    @abstractmethod
    def get_all_payments(self):
        pass

    @abstractmethod
    def record_payment(self, payment):
        pass

    @abstractmethod
    def update_payment(self, payment):
        pass

    @abstractmethod
    def delete_payment(self, payment_id):
        pass