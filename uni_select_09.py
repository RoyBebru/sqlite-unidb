#!/usr/bin/env python3

import sqlite3


def execute_query(sql: str) -> list:
    with sqlite3.connect('uni.db') as con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchall()


sql = """
SELECT st.fullname, sb.title
FROM student_subjects ss
INNER JOIN subjects sb ON sb.id = ss.subject_id
INNER JOIN students st ON st.id = ss.student_id 
WHERE ss.student_id=st.id
ORDER BY st.fullname, sb.title
"""

if __name__ == "__main__":
    print("-- 9. Знайти список предметів, на які записаний студент.")
    print("-- --------------------------+--------------------------")
    print("#N                   STUDENT | SUBJECT")
    print("-- --------------------------+--------------------------")
    student0 = ""
    i = 0
    for student, subject in execute_query(sql):
        i += 1
        student1 = ""
        if student0 != student:
            student1 = student
            student0 = student
            print()
        print("%2d %25s | %-s" % (i, student1, subject))
