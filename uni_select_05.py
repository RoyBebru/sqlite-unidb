#!/usr/bin/env python3

import sqlite3


def execute_query(sql: str) -> list:
    with sqlite3.connect('uni.db') as con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchall()


sql = """
SELECT tr.fullname, sb.title, sb.id
FROM teacher_subjects ts
INNER JOIN teachers tr ON tr.id = ts.teacher_id
INNER JOIN subjects sb ON sb.id = ts.subject_id
ORDER BY ts.teacher_id
"""

if __name__ == "__main__":
    print("-- 5. Знайти, які предмети читає певний викладач.")
    print("-- ----------------------------------------+-----------------------------------------")
    print("id                                 SUBJECT | TEACHER")
    print("-- ----------------------------------------+-----------------------------------------")
    name0 = ""
    for teacher, subject, subject_id in execute_query(sql):
        if name0 == "":
            name0 = teacher
        if name0 != teacher:
            name0 = teacher
            print()
        print("%s %40s | %s" % (subject_id, subject, teacher))
    print()
