#!/usr/bin/env python3

import sqlite3


def execute_query(sql: str) -> list:
    with sqlite3.connect('uni.db') as con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchall()


sql = """
SELECT tr.fullname, ROUND(AVG(gd.grade),2), COUNT(*)
FROM grades gd
INNER JOIN teacher_subjects ts ON ts.teacher_id = tr.id
INNER JOIN teachers tr ON ts.teacher_id = tr.id
WHERE gd.subject_id = ts.subject_id
GROUP BY tr.id
ORDER BY tr.fullname
"""

if __name__ == "__main__":
    print("-- 8. Знайти середню оцінку, який ставить певний викладач зі своїх предметів.")
    print("-- --------------------------+-----+---------------------")
    print("#N                   TEACHER | N_e | AVER GRADE")
    print("-- --------------------------+-----+---------------------")
    i = 0
    for teacher, aver_eval, num_evals in execute_query(sql):
        i += 1
        print("%2d %25s | %3d | %s" % (i, teacher, num_evals, aver_eval))
