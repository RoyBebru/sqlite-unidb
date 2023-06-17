#!/usr/bin/env python3


from datetime import date
from faker import Faker
import random
import sqlite3

fake = Faker()

def create_db(con, cur):
    cur.executescript("""
-- Table: subjects
DROP TABLE IF EXISTS subjects;
CREATE TABLE subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) UNIQUE NOT NULL
);

-- Table: groups
DROP TABLE IF EXISTS groups;
CREATE TABLE groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codename VARCHAR(255) UNIQUE NOT NULL
);

-- Table: teachers
DROP TABLE IF EXISTS teachers;
CREATE TABLE teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname VARCHAR(255) UNIQUE NOT NULL
);

-- Table: students
DROP TABLE IF EXISTS students;
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname VARCHAR(255) UNIQUE NOT NULL,
    group_id INTEGER,
    FOREIGN KEY (group_id) REFERENCES groups (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- Table: subject per student
DROP TABLE IF EXISTS student_subjects;
CREATE TABLE student_subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Table: subject per teacher
DROP TABLE IF EXISTS teacher_subjects;
CREATE TABLE teacher_subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES teachers (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Table: grades
DROP TABLE IF EXISTS grades;
CREATE TABLE grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_of DATE NOT NULL,
    grade TINYINT NOT NULL,
    student_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    teacher_id INTEGER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES teachers (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);""")

def fake_fill_db(con, cur):
    fake_subjects = [
        "Mathematical psychotherapy",
        "Quantum astrology",
        "Meteorology of infinity",
        "Archeology of logic",
        # "Introduction to hypercubic epicycles",
        "Differential geometry of programming",
        "Infinite structures calculus",
        # "The theory of complex integration of fractals",
        "Mirror calculations",
        # "Calculation of infinite cycles in finite time",
        # "The topology of the unknown",
        "Absurdology"
    ]
    random.shuffle(fake_subjects)

    fake_groups = [
        "GOIT-31",
        "GOIT-32",
        "GOIT-33"
    ]
    random.shuffle(fake_groups)

    fake_teachers = [f"{random.choice(['Dr.','Phd.'])} {fake.first_name()} {fake.last_name()}" for _ in range(5)]

    num_students = random.randint(30, 50)
    fake_students = [(f"{fake.last_name()}, {fake.first_name()}", random.randint(1,len(fake_groups))) for _ in range(num_students) ]

    cur = con.cursor()

    #{{{ Table: subjects -----------------------------------
    cur.executemany("INSERT INTO subjects (title) VALUES (?)", zip(fake_subjects))
    #}}}

    #{{{ Table: groups -------------------------------------
    cur.executemany("INSERT INTO groups (codename) VALUES (?)", zip(fake_groups))
    #}}}

    #{{{ Table: teachers -----------------------------------
    cur.executemany("INSERT INTO teachers (fullname) VALUES (?)", zip(fake_teachers))
    #}}}

    #{{{ Table: teacher_subjects ---------------------------
    subjects1 = list(range(1,len(fake_subjects)+1))
    subjects2 = []
    for _ in range(len(fake_subjects) - len(fake_teachers)):
        n = random.randint(0, len(subjects1)-1)
        subjects2.append(subjects1.pop(n))
    teacher_subjects = list(zip(subjects1, range(1,len(fake_teachers)+1)))
    teacher_subjects.extend(
            list(zip(subjects2,
                random.choices(range(1,len(fake_teachers)+1),k=len(subjects2)))))
    cur.executemany("INSERT INTO teacher_subjects (subject_id, teacher_id) VALUES (?,?)",
            teacher_subjects)
    #}}}

    #{{{ Table: students -----------------------------------
    cur.executemany("INSERT INTO students (fullname,group_id) VALUES (?,?)", fake_students)
    #}}}

    #{{{ Table: student_subjects ---------------------------
    # Each student must listen any 5 subjects
    SUBJECTS_PER_STUDENT = 5
    student_subjects = []
    for i in range(1, num_students+1):
        subjects1 = list(range(1,len(fake_subjects)+1))
        for _ in range(len(fake_subjects) - SUBJECTS_PER_STUDENT):
            subjects1.pop(random.randint(0, len(subjects1)-1))
        student_subjects.extend(zip(subjects1, [i] * SUBJECTS_PER_STUDENT))
    cur.executemany("INSERT INTO student_subjects (subject_id, student_id) VALUES (?,?)",
            student_subjects)
    #}}}

    #{{{ Table: grades -------------------------------------
    STADY_DAYS = 30 * 3
    ord_today = date.today().toordinal()
    grades = []
    for student_id in range(1, num_students+1):
        for _ in range(random.randint(1,20)):
            # date_of
            while True:
                date_of = date.fromordinal(ord_today - random.randint(0,STADY_DAYS-1))
                if date_of.weekday() < 5:
                    break # not Saturday and not Sunday
            # subject_id
            subject_id = student_subjects[
                student_id * SUBJECTS_PER_STUDENT - random.randint(1,SUBJECTS_PER_STUDENT)][0]
            # real life grades distribution
            grade = random.randint(1,100)
            if grade < 10:
                grade = 2
            elif grade < 25:
                grade = 3
            elif grade < 65:
                grade = 4
            else:
                grade = 5
            # what teacher who can conduct lecture on this subject
            teacher_ids = [t_id for s_id, t_id in teacher_subjects if s_id == subject_id ]
            teacher_id = random.choice(teacher_ids)
            grades.append((date_of, grade, student_id, subject_id, teacher_id))
    cur.executemany(
        "INSERT INTO grades (date_of,grade,student_id,subject_id,teacher_id) VALUES (?,?,?,?,?)",
        grades)
    #}}}

    con.commit()

if __name__ == "__main__":

    with sqlite3.connect('uni.db') as con:
        cur = con.cursor()
        create_db(con, cur)
        fake_fill_db(con, cur)
