-- 10. Список предметів, які певному студенту читає певний викладач.

SELECT st.fullname, tr.fullname, sb.id, sb.title
FROM student_subjects ss, teacher_subjects ts
INNER JOIN students st ON st.id = ss.student_id
INNER JOIN teachers tr ON tr.id = ts.teacher_id
INNER JOIN subjects sb ON sb.id = ss.subject_id
WHERE ss.subject_id = ts.subject_id AND ss.student_id = 11 AND ts.teacher_id = 2
--                                            STUDENT --^            TEACHER --^
ORDER BY st.fullname, tr.fullname
