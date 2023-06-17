#!/usr/bin/env python3

import sqlite3


def execute_query(sql: str) -> list:
    with sqlite3.connect('uni.db') as con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchall()


sql = """
SELECT grd.date_of, grp.codename, sub.title, stu.fullname, grd.grade
FROM grades grd
INNER JOIN students stu ON stu.id = grd.student_id
INNER JOIN groups grp ON grp.id = stu.group_id
INNER JOIN subjects sub ON sub.id = grd.subject_id
WHERE grd.date_of = (
    SELECT MAX(gd.date_of)
    FROM grades gd
    WHERE gd.subject_id = grd.subject_id
)
GROUP BY grd.subject_id, grd.student_id
ORDER BY grp.codename, sub.title, stu.fullname
"""

if __name__ == "__main__":
    print("-- 12. Оцінки студентів у певній групі з певного предмета на останньому занятті.")

    group0 = ""
    for date_of, group, subject, student, grade in execute_query(sql):
        if group0 != group:
            group0 = group
            print()
        print("%10s | %7s | %40s | %1s | %-s" % (date_of, group, subject, grade, student))
