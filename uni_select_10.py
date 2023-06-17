#!/usr/bin/env python3

import sqlite3


def execute_query(sql: str) -> list:
    with sqlite3.connect('uni.db') as con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchall()


sql = """
SELECT st.fullname, tr.fullname, sb.id, sb.title
FROM student_subjects ss, teacher_subjects ts
INNER JOIN students st ON st.id = ss.student_id
INNER JOIN teachers tr ON tr.id = ts.teacher_id
INNER JOIN subjects sb ON sb.id = ss.subject_id
WHERE ss.subject_id = ts.subject_id
ORDER BY st.fullname, tr.fullname
"""

if __name__ == "__main__":
    print("-- 10. Список предметів, які певному студенту читає певний викладач.")

    TFLEN = 25

    student0 = ""
    teacher0 = ""
    teachers = [] # all teachers which are collected from response
    subjects = {} # all subjects which are collected from response
    studsubs = {} # for current student all subjects per teacher

    print("-"*23+"+")
    print("%23s|" % "STUDENTS ")
    print("-"*23+"+")

    for student, teacher, subject_id, subject in execute_query(sql):
        subjects[subject_id] = subject
        if teacher not in teachers:
            teachers.append(teacher)

        if student0 != "" and student0 != student:
            # The next student starts
            teacher0 = ""
            line = ""
            for i in range(len(teachers)):
                if i in studsubs.keys():
                    line += ("|{:^"+str(TFLEN-1)+"}").format(",".join(map(lambda x: str(x),studsubs[i])))
                else:
                    line += "|" + " "*(TFLEN-1)
            print("%23s%s" % (student0, line))
            studsubs = {}

        student0 = student

        if teacher0 != teacher:
            teacher0 = teacher
            ix = teachers.index(teacher)

        if ix not in studsubs.keys():
            studsubs[ix] = [subject_id]
        else:
            studsubs[ix].append(subject_id)

    print("-"*23+("+" + "-"*(TFLEN-1))*len(teachers))
    line = "%23s" % "TEACHERS -> "
    for teacher in teachers:
        line += ("|{:^"+str(TFLEN-1)+"s}").format(teacher)
    print(line)
    print("-"*23+("+" + "-"*(TFLEN-1))*len(teachers))

    sk = list(subjects.keys())
    sk.sort()
    for k in sk:
        print(f"{k}  {subjects[k]}")
