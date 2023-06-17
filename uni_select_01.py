#!/usr/bin/env python3

import sqlite3


def execute_query(sql: str) -> list:
    with sqlite3.connect('uni.db') as con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchall()


sql = """
SELECT ss.fullname, AVG(gd.grade) as avgd
FROM grades gd
INNER JOIN students ss ON ss.id = gd.student_id
GROUP BY gd.student_id
ORDER BY avgd DESC, ss.fullname
LIMIT 5
"""

if __name__ == "__main__":
    print("-- 1. Знайти 5 студентів із найбільшою середньою оцінкою з усіх предметів.")
    print("-- --------------------------+------")
    print("#N              STUDENT_NAME | AVG")
    print("-- --------------------------+------")
    i = 0
    for fullname, avg in execute_query(sql):
        i += 1
        print("%2d %25s | %4.2f" % (i, fullname, avg))
