-- 9. Знайти список предметів, на які записаний студент.

SELECT st.fullname, sb.title
FROM student_subjects ss
INNER JOIN subjects sb ON sb.id = ss.subject_id
INNER JOIN students st ON st.id = ss.student_id 
WHERE ss.student_id=9
--        STUDENT --^
ORDER BY st.fullname, sb.title
