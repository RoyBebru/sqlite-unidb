#!/usr/bin/env python3

import sqlite3


def execute_query(sql: str) -> list:
    with sqlite3.connect('uni.db') as con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchall()


sql = """
SELECT AVG(gd.grade)
FROM grades gd
"""

if __name__ == "__main__":
    print("-- 4. Знайти середній бал по всім студентам (по всій таблиці оцінок).")
    aver_grade, = execute_query(sql)[0]
    print(aver_grade)
