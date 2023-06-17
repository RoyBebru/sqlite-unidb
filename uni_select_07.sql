-- 7. Знайти оцінки студентів в окремій групі з певного предмета.

SELECT gd.date_of, gr.codename, sb.title, st.fullname, gd.grade
FROM grades gd
INNER JOIN students st ON st.id = gd.student_id
INNER JOIN groups gr ON gr.id = st.group_id
INNER JOIN subjects sb ON sb.id = gd.subject_id
WHERE gr.id = 2 AND gd.subject_id = 7
--    GROUP --^           SUBJECT --^
ORDER BY st.fullname, gd.date_of
