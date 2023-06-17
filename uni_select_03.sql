-- 3. Знайти середню оцінку у групах з певного предмета.

SELECT sb.title, gr.codename, ROUND(AVG(gd.grade),2)
FROM grades gd
INNER JOIN subjects sb ON sb.id = gd.subject_id 
INNER JOIN students st ON gd.student_id = st.id
INNER JOIN groups gr ON st.group_id = gr.id
WHERE gd.subject_id = 1 AND gr.id = 3
-- SUBJECT -----------^     GROUP --^
