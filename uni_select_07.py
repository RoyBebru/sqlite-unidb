#!/usr/bin/env python3

import sqlite3


def execute_query(sql: str) -> list:
    with sqlite3.connect('uni.db') as con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchall()


sql = """
SELECT gd.date_of, gr.codename, sb.title, st.fullname, gd.grade
FROM grades gd
INNER JOIN students st ON st.id = gd.student_id
INNER JOIN groups gr ON gr.id = st.group_id
INNER JOIN subjects sb ON sb.id = gd.subject_id
GROUP BY gr.id, gd.subject_id, gd.student_id
ORDER BY gr.codename
"""

if __name__ == "__main__":
    print("-- 7. Знайти оцінки студентів в окремій групі з певного предмета.")
    print("--- -----------+---------+------------------------------------------+---+--------------------------")
    print(" #N     DATE   |  GROUP  |                                  SUBJECT |GRD| STUDENT")
    print("--- -----------+---------+------------------------------------------+---+--------------------------")
    i = 0
    group0 = ""
    for date_of, group, subject, student, grade in execute_query(sql):
        i += 1
        group1 = ""
        if group != group0:
            group1 = group
            group0 = group
            print()
        print("%3d %10s | %7s | %40s | %1s | %-25s" % (i, date_of, group1, subject, grade, student))
