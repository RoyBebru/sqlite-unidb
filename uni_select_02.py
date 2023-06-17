#!/usr/bin/env python3

import sqlite3


def execute_query(sql: str) -> list:
    with sqlite3.connect('uni.db') as con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchall()


sql = """
SELECT sb.title || CHAR(9) || (
    SELECT st.fullname || CHAR(9) || ROUND(AVG(gd.grade),2)
    FROM grades gd
    INNER JOIN students st ON gd.student_id = st.id
    GROUP BY gd.student_id
    HAVING gd.subject_id = sb.id
    ORDER BY AVG(gd.grade) DESC, COUNT(*) DESC
    LIMIT 1
) AS max_avr_by_subject
FROM subjects sb
"""

if __name__ == "__main__":
    print("-- 2. Знайти студента із найвищою середньою оцінкою з певного предмета.")
    print("-- Якщо оцінка однакова - найвищою вважається середня оцінка з найбільшої кількості оцінок.")
    print("-- -----------------------------------------+---------------------------+------------------")
    print("#N                            SUBJECT TITLE |              STUDENT NAME | MAX AVER GRADE")
    print("-- -----------------------------------------+---------------------------+------------------")
    i = 0
    for data in execute_query(sql):
        subject, student, aver_grade = data[0].split(chr(9))
        i += 1
        print("%2d %40s | %25s | %s" % (i, subject, student, aver_grade))
