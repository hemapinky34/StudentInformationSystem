class DuplicateEnrollmentException(Exception):
    """Raised when a student is already enrolled in a course"""
    pass

class CourseNotFoundException(Exception):
    """Raised when a course is not found"""
    pass

class StudentNotFoundException(Exception):
    """Raised when a student is not found"""
    pass

class TeacherNotFoundException(Exception):
    """Raised when a teacher is not found"""
    pass

class PaymentValidationException(Exception):
    """Raised when there's an issue with payment validation"""
    pass

class InvalidStudentDataException(Exception):
    """Raised when student data is invalid"""
    pass

class InvalidCourseDataException(Exception):
    """Raised when course data is invalid"""
    pass

class InvalidEnrollmentDataException(Exception):
    """Raised when enrollment data is invalid"""
    pass

class InvalidTeacherDataException(Exception):
    """Raised when teacher data is invalid"""
    pass

class InsufficientFundsException(Exception):
    """Raised when a student doesn't have enough funds"""
    pass