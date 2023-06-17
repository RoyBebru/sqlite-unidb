-- 11. Середня оцінка, яку певний викладач ставить певному студентові.

SELECT st.fullname, tr.fullname, ROUND(AVG(gd.grade),2), COUNT(*)
FROM grades gd
INNER JOIN teacher_subjects ts ON ts.subject_id = gd.subject_id
INNER JOIN teachers tr ON tr.id = ts.teacher_id
INNER JOIN students st ON st.id = gd.student_id
WHERE gd.student_id = 37 AND ts.teacher_id = 2
--          STUDENT --^            TEACHER --^
ORDER BY st.fullname, tr.fullname
