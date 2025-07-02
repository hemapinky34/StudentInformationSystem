create database SISDB;
use SISDB;

create table Students
(
student_id int primary key ,
first_name varchar(50) ,
last_name varchar(50),
date_of_birth date,
email varchar(50),
phone_number int
);
desc Students;

create table Teacher(
teacher_id int primary key,
first_name varchar (50),
last_name varchar(50),
email varchar(50)
);

create table Courses
(
course_id int primary key ,
course_name varchar(50),
credits int ,
teacher_id int references Teacher (teacher_id)
);

create table Enrollments
(
enrollment_id int primary key,
student_id int references Students (student_id),

enrollment_date date 
);

create table Payments
(
payment_id int primary key,
student_id int references Students(student_id),
amount decimal(10,2),
payment_date date 
);

-- TASK-1

alter table Students modify phone_number varchar(20);

insert into Students values
(1, 'Amit', 'Sharma', '2000-01-01', 'amit@gmail.com', '9876543210'),
(2, 'Neha', 'Rao', '1999-02-05', 'neha@gmail.com', '9876543211'),
(3, 'Ravi', 'Patel', '1998-03-10', 'ravi@gmail.com', '9876543212'),
(4, 'Priya', 'Menon', '2001-04-15', 'priya@gmail.com', '9876543213'),
(5, 'Anil', 'Kumar', '2002-05-20', 'anil@gmail.com', '9876543214'),
(6, 'Sneha', 'Joshi', '2000-06-25', 'sneha@gmail.com', '9876543215'),
(7, 'Raj', 'Verma', '1999-07-30', 'raj@gmail.com', '9876543216'),
(8, 'Meena', 'Das', '2001-08-10', 'meena@gmail.com', '9876543217'),
(9, 'Arjun', 'Reddy', '2002-09-15', 'arjun@gmail.com', '9876543218'),
(10, 'Divya', 'Singh', '1998-10-20', 'divya@gmail.com', '9876543219');

select* from Students;

insert into Teacher values
(1, 'Rahul', 'Sen', 'rahul@abc.com'),
(2, 'Kavita', 'Naik', 'kavita@abc.com'),
(3, 'Nikhil', 'Das', 'nikhil@abc.com'),
(4, 'Reema', 'Jain', 'reema@abc.com'),
(5, 'Sandeep', 'Roy', 'sandeep@abc.com'),
(6, 'Geeta', 'Khan', 'geeta@abc.com'),
(7, 'Manoj', 'Yadav', 'manoj@abc.com'),
(8, 'Lata', 'Joshi', 'lata@abc.com'),
(9, 'Vinay', 'Rao', 'vinay@abc.com'),
(10, 'Rita', 'Mishra', 'rita@abc.com');
select*from Teacher ;

insert into Courses values
(101, 'Maths', 3, 1),
(102, 'Science', 4, 2),
(103, 'History', 2, 3),
(104, 'Geography', 2, 4),
(105, 'English', 3, 5),
(106, 'Physics', 4, 6),
(107, 'Chemistry', 4, 7),
(108, 'Biology', 3, 8),
(109, 'Computer', 3, 9),
(110, 'Economics', 2, 10);
select*from Courses;

insert into Enrollments values
(1, 1, 101, '2024-06-01'),
(2, 2, 102, '2024-06-01'),
(3, 3, 103, '2024-06-01'),
(4, 4, 104, '2024-06-01'),
(5, 5, 105, '2024-06-01'),
(6, 6, 106, '2024-06-01'),
(7, 7, 107, '2024-06-01'),
(8, 8, 108, '2024-06-01'),
(9, 9, 109, '2024-06-01'),
(10, 10, 110, '2024-06-01');
select * from Enrollments;
 
 insert into Payments values
 (1, 1, 5000, '2024-06-01'),
(2, 2, 6000, '2024-06-01'),
(3, 3, 7000, '2024-06-01'),
(4, 4, 5500, '2024-06-01'),
(5, 5, 6200, '2024-06-01'),
(6, 6, 5300, '2024-06-01'),
(7, 7, 4900, '2024-06-01'),
(8, 8, 7100, '2024-06-01'),
(9, 9, 6400, '2024-06-01'),
(10, 10, 5800, '2024-06-01');
select*from Payments;

-- TASK -2
-- 1.SQL query to insert a new student into the Students table 
	 insert into Students values(11,'john','doe','1995-08-15','john.doe@example.com','1234567890');
    
-- 2.Choose an existing student and course and insert a record into the "Enrollments" table with the enrollment date
     insert into Enrollments values(11,11,101,'2024-06-05');
   
-- 3.Update the email address of a specific teacher in the "Teacher" table. Choose any teacher and modify their email address. 
     update Teacher set email = 'kavi123@gmail.com '
	 where teacher_id =2;
     
	 select*from Teacher;
 
-- 4.delete a specific enrollment record from the "Enrollments" table. Select an enrollment record based on the student and course. 
     set sql_safe_updates=0;
     delete from Enrollments 
	 where student_id=10 and course_id =110;
 
-- 5.Update the "Courses" table to assign a specific teacher to a course. Choose any course and teacher from the respective tables. 
	 update Courses set teacher_id =5
	 where course_id=103;
 
     select*from Courses;

-- 6.Delete a specific student from the "Students" table and remove all their enrollment records from the "Enrollments" table. 
     delete from Enrollments
	 where student_id =9; 
     delete from Students
     where student_id=9;
      
-- 7.Update the payment amount for a specific payment record in the "Payments" table. Choose any payment record and modify the payment amount.       
	 update Payments set amount =6000
	 where payment_id=10;
-- =======================================================================================================================================
-- TASK-3

-- 1.calculate the total payments made by a specific student. You will need to join the "Payments" table with the "Students" table based on the student's ID. 
	 select s.first_name,s.last_name,sum(p.amount) as total_payment
	 from Students s
	 join payments p on s.student_id=p.student_id
     where s.student_id=1
	 group by s.student_id;
      
-- 2.retrieve a list of courses along with the count of students enrolled in each course. Use a JOIN operation between the "Courses" table and the "Enrollments" table. 
     select c.course_name,count(e.student_id) as student_count
     from Courses  c
     join enrollments  e on c.course_id=e.course_id
     group by c.course_id;
     
-- 3.find the names of students who have not enrolled in any course. Use a LEFT JOIN between the "Students" table and the "Enrollments" table to identify students without enrollments. 
     select s.first_name,s.last_name
     from Students s
     left join enrollments e on s.student_id=e.student_id
     where e.student_id is null;

-- 4.retrieve the first name, last name of students, and the names of the courses they are enrolled in. Use JOIN operations between the "Students" table and the "Enrollments" and "Courses" tables. 
     select s.first_name,s.last_name,c.course_name
     from Students s
     join enrollments e on s.student_id=e.student_id
     join Courses c on e.course_id=c.course_id
     
-- 5.list the names of teachers and the courses they are assigned to. Join the "Teacher" table with the "Courses" table
	 select t.first_name,t.last_name, c.course_name
     from teacher t
     join Courses c on t.teacher_id=c.teacher_id ;
     
-- 6.list of students and their enrollment dates for a specific course. You'll need to join the "Students" table with the "Enrollments" and "Courses" tables. 
	 select s.first_name,s.last_name,e.enrollment_date 
     from Students s
     join enrollments e on s.student_id=e.student_id
     join Courses c on e.course_id=c.course_id; 
     where c.course_id=101

-- 7.Find the names of students who have not made any payments. Use a LEFT JOIN between the "Students "table and the "Payments" table and filter for students with NULL payment records. 
     select s.first_name,s.last_name 
     from Students s 
     left join payments p on s.student_id=p.student_id
     where p.student_id is null;

-- 8.identify courses that have no enrollments. You'll need to use a LEFT JOIN between the "Courses" table and the "Enrollments" table and filter for courses with NULL enrollment records. 
     select c.course_name
     from Courses c
     left join enrollments e on c.course_id=e.course_id
     where e.course_id is null;
     
-- 9.Identify students who are enrolled in more than one course. Use a self-join on the "Enrollments" table to find students with multiple enrollment records. 
	 select distinct s.student_id, s.first_name, s.last_name
	 from enrollments e1
     join enrollments e2 on e1.student_id = e2.student_id and e1.course_id <> e2.course_id
     join Students s on s.student_id = e1.student_id;

-- 10.Find teachers who are not assigned to any courses. Use a LEFT JOIN between the "Teacher" table and the "Courses" table and filter for teachers with NULL course assignments. 
      select t.first_name,t.last_name
      from teacher t
      left join Courses c on t.teacher_id=c.teacher_id
      where c.course_id is null;
-- =======================================================================================================================================================================================

-- TASK-4
--  1. Calculate the average number of students enrolled in each course. Use aggregate functions and subqueries to achieve this. 
	   select avg( student_count) as avg_students_per_course
	   from (select course_id,count(student_id) as student_count 
       from enrollments
       group by course_id ) as sub;
   
-- 2.  Identify the student(s) who made the highest payment. Use a subquery to find the maximum payment amount and then retrieve the student(s) associated with that amount. 
       select s.student_id, s.first_name,s.last_name,p.amount
       from Students s
       join payments p on s.student_id=p.student_id
       where p.amount =( select max(amount) from payments);
	
-- 3.Retrieve a list of courses with the highest number of enrollments. Use subqueries to find the course(s) with the maximum enrollment count. 
	 select c.course_id,c.course_name, count(e.student_id) as tot_enrollments
     from courses c 
     join enrollments e on c.course_id=e.course_id
     group by c.course_id,c.course_name
     having count(e.student_id)=(select max(enroll_count)from(select course_id,count(*) as enroll_count
     from enrollments
     group by course_id) as sub
     );
	
-- 4.Calculate the total payments made to courses taught by each teacher. Use subqueries to sum payments for each teacher's courses. 
     select t.teacher_id,t.first_name,t.last_name,
	 (select sum(p.amount)
     from payments p
     join enrollments e on p.student_id=e.student_id
     join courses c2 on e.course_id=c2.course_id
     where c2.teacher_id=t.teacher_id) as total_payment_received
     from teacher t;
     
-- 5.Identify students who are enrolled in all available courses. Use subqueries to compare a student's enrollments with the total number of courses. 
	 select s.student_id,s.first_name,s.last_name
     from students s
     where (select count(course_id)
     from enrollments 
     where student_id=s.student_id)=(select count(course_id)
     from courses);
     
-- 6.Retrieve the names of teachers who have not been assigned to any courses. Use subqueries to find teachers with no course assignments. 
     select teacher_id,first_name,last_name
     from teacher
     where teacher_id not in(select teacher_id from courses where teacher_id is not null );
     
-- 7.Calculate the average age of all students. Use subqueries to calculate the age of each student based on their date of birth. 
     select avg(age) as average_age
     from(select timestampdiff(year,date_of_birth,curdate()) as age
     from students) as sub;
     
-- 8.Identify courses with no enrollments. Use subqueries to find courses without enrollment records. 
     select course_id,course_name
     from courses
     where course_id not in (select course_id from enrollments);
     
-- 9.Calculate the total payments made by each student for each course they are enrolled in. Use subqueries and aggregate functions to sum payments. 
     select s.student_id,s.first_name,c.course_id,c.course_name, 
     (select sum(p.amount)
     from payments p
     where p.student_id=s.student_id )as total_payment
     from students s
     join enrollments e on s.student_id=e.student_id
     join courses c on e.course_id=c.course_id;
     
-- 10.Identify students who have made more than one payment. Use subqueries and aggregate functions to count payments per student and filter for those with counts greater than one. 
	  select student_id,first_name,last_name
      from students
      where student_id in ( select student_id from payments group by student_id having count(payment_id)>1);
      
-- 11.11.Calculate the total payments made by each student. Join the "Students" table with the "Payments" table and use GROUP BY to calculate the sum of payments for each student. 
     select s.student_id,s.first_name,s.last_name,sum(p.amount) as total_payment
     from Students s
     join Payments p on s.student_id = p.student_id
     group by s.student_id, s.first_name, s.last_name;

-- 12.Retrieve a list of course names along with the count of students enrolled in each course. Use JOIN operations between the "Courses" table and the "Enrollments" table and GROUP BY to count enrollments. 
      select c.course_id,c.course_name,count(e.student_id) as total_students_enrolled
      from Courses c
      join Enrollments e on c.course_id = e.course_id
      group by c.course_id, c.course_name;
      
-- 13.Calculate the average payment amount made by students. Use JOIN operations between the "Students" table and the "Payments" table and GROUP BY to calculate the average. 
      select s.student_id,s.first_name,s.last_name,avg(p.amount) as average_payment
      from Students s
      join Payments p on s.student_id = p.student_id
      group by s.student_id, s.first_name, s.last_name;
      
-- ==================================================================================================================================================
     
     

     









