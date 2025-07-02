This is a  Student Information System (SIS) project developed using Python (OOP) and MySQL. It manages students, courses, enrollments, teachers, and payments with a complete back-end database and object-oriented implementation.

Features Implemented:
Entity Layer: Defined domain classes (Student, Course, Teacher, Enrollment, Payment) with constructors and methods to model real-world entities.

 DAO Layer: Interfaces and implementations for database CRUD operations using MySQL.
 
 Exception Handling: Custom exceptions like StudentNotFoundException, DuplicateEnrollmentException, PaymentValidationException, etc., to handle logical errors.

 Utility Layer: DBConnUtil and DBPropertyUtil classes for database connection management and config file handling.

 Reports: Enrollment reports, payment summaries, course statistics generated through both OOP and SQL queries.
 
 Structured Directory:
  entity/

  dao/

  exception/

  util/

  main/ (Menu-driven app)

Advanced SQL: Includes joins, aggregates, subqueries, and dynamic query builder to support reporting and insights.

Key Functionalities:
Add/update/delete students, teachers, courses.

Student enrollment in courses.

Teacher assignment to courses.

Student payment recording and tracking.

Generation of custom reports and queries.

Data validation and integrity checks through custom exceptions.

Database:
Database: SISDB

Tables: Students, Courses, Enrollments, Teachers, Payments

ERD and relationships implemented with primary & foreign keys.
