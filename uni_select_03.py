#!/usr/bin/env python3

import sqlite3


def execute_query(sql: str) -> list:
    with sqlite3.connect('uni.db') as con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchall()


sql = """
SELECT sb.title, gr.codename, ROUND(AVG(gd.grade),2)
FROM grades gd, subjects sb
INNER JOIN students st ON gd.student_id = st.id
INNER JOIN groups gr ON st.group_id = gr.id
WHERE gd.subject_id = sb.id
GROUP BY sb.id, gr.id
"""

if __name__ == "__main__":
    print("-- 3. Знайти середню оцінку у групах з певного предмета.")
    print("-- -----------------------------------------+----------+---------------------")
    print("#N                            SUBJECT TITLE |    GROUP | AVER GRADE")
    print("-- -----------------------------------------+----------+---------------------")
    i = 0
    for subject, group, aver_grade in execute_query(sql):
        i += 1
        print("%2d %40s | %8s | %s" % (i, subject, group, aver_grade))
