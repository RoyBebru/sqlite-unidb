#!/usr/bin/env python3

import sqlite3


def execute_query(sql: str) -> list:
    with sqlite3.connect('uni.db') as con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchall()


sql = """
SELECT st.fullname, tr.fullname, ROUND(AVG(gd.grade),2), COUNT(*)
FROM grades gd
INNER JOIN teacher_subjects ts ON ts.subject_id = gd.subject_id
INNER JOIN teachers tr ON tr.id = ts.teacher_id
INNER JOIN students st ON st.id = gd.student_id
GROUP BY gd.student_id, ts.teacher_id
ORDER BY st.fullname, tr.fullname
"""

if __name__ == "__main__":
    print("-- 11. Середня оцінка, яку певний викладач ставить певному студентові.")

    TFLEN = 25

    student0 = ""
    teacherx = ""
    teachers = []

    grades = 0

    print("-"*23+"+")
    print("%23s|" % "STUDENTS ")
    print("-"*23+"+")

    for (student, teacher, aver_grade, count_grade) in execute_query(sql):
        grades += count_grade
        if teacher not in teachers:
            teachers.append(teacher)
            teacherx += "|" + " "*(TFLEN-1)

        if student0 != "" and student0 != student:
            print("%23s%s" % (student0, teacherx))
            teacherx = ("|" + " "*(TFLEN-1)) * len(teachers)

        student0 = student
        tix = teachers.index(teacher)
        tix = TFLEN*tix
        teacherx = teacherx[:tix] + \
            ("|{:^"+str(TFLEN-1)+"s}").format(f"{aver_grade} ({count_grade})") + \
            teacherx[tix+TFLEN:]

    print("-"*23+("+" + "-"*(TFLEN-1))*len(teachers))
    teacherx = "%23s" % "TEACHERS -> "
    for teacher in teachers:
        teacherx += ("|{:^"+str(TFLEN-1)+"s}").format(teacher)
    print(teacherx)
    print("-"*23+("+" + "-"*(TFLEN-1))*len(teachers))
    print(f"Total grades: {grades}")
