# 创建一张成绩表.
CREATE TABLE if not exists colleges(
  id INT PRIMARY KEY auto_increment,
  name VARCHAR(20)
 ) auto_increment=1;
 INSERT INTO colleges VALUES (DEFAULT,'软件学院');
 INSERT INTO colleges VALUES (DEFAULT,'硬件学院');
 INSERT INTO colleges VALUES (DEFAULT,'外语学院');
 INSERT INTO colleges VALUES (DEFAULT,'音乐学院');

select * from colleges;



# 创建一张学生表.
CREATE TABLE if not exists students (
  id INT PRIMARY KEY auto_increment,
  name VARCHAR(20),
  age INT,
  college_id INT, 
  FOREIGN KEY(college_id) REFERENCES colleges(id)
)auto_increment=2019001;
INSERT INTO students VALUES (DEFAULT, 'Qiye', 16, 1);
INSERT INTO students VALUES (DEFAULT, 'JackLee', 17, 1);
INSERT INTO students VALUES (DEFAULT, 'Julia', 18, 1);
INSERT INTO students VALUES (DEFAULT, 'Stefer', 19, 1);
INSERT INTO students VALUES (DEFAULT, 'Steven', 20, 1);
INSERT INTO students VALUES (DEFAULT, 'Mark', 21, 2);

select * from students;



# 创建一张课程表.
CREATE TABLE if not exists courses (   
  id int PRIMARY KEY auto_increment,  
  course VARCHAR(30),
  college_id INT, 
  FOREIGN KEY(college_id) REFERENCES colleges(id)
)auto_increment=1;
INSERT INTO courses VALUES (DEFAULT, 'python',1);
INSERT INTO courses VALUES (DEFAULT, 'java',1);
INSERT INTO courses VALUES (DEFAULT, 'web',1);
INSERT INTO courses VALUES (DEFAULT, 'go',1);
INSERT INTO courses VALUES (DEFAULT, 'c++',1);

select * from courses;


# 创建一张选课表.
CREATE TABLE if not exists amongs (   
  student_id int,
  course_id int,
  PRIMARY KEY(student_id,course_id),
  FOREIGN KEY(student_id) REFERENCES students(id),
  FOREIGN KEY(course_id) REFERENCES courses(id)
);
INSERT INTO amongs VALUES (2019001,1);
INSERT INTO amongs VALUES (2019002,1);
INSERT INTO amongs VALUES (2019003,2);
INSERT INTO amongs VALUES (2019004,2);
INSERT INTO amongs VALUES (2019005,2);

select * from amongs;

