#!/usr/bin/env python3

import sqlite3


def execute_query(sql: str) -> list:
    with sqlite3.connect('uni.db') as con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchall()


sql = """
SELECT gr.codename, st.fullname
FROM students st
INNER JOIN groups gr ON gr.id = st.group_id 
GROUP BY gr.id, st.id
ORDER BY gr.codename
"""

if __name__ == "__main__":
    print("-- 6. Знайти список студентів у певній групі.")
    print("-- --------+-------------------------------")
    print("#N   GROUP | STUDENT ")
    print("-- --------+-------------------------------")
    i = 0
    group0 =""
    for group, student in execute_query(sql):
        i += 1
        group1 = ""
        if group0 != group:
            group1 = group
            group0 = group
            print()
        print("%2d %7s | %s" % (i, group1, student))
