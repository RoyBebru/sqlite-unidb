-- 5. Знайти, які предмети читає певний викладач.

SELECT tr.fullname, sb.title, sb.id
FROM teacher_subjects ts
INNER JOIN teachers tr ON tr.id = ts.teacher_id
INNER JOIN subjects sb ON sb.id = ts.subject_id
WHERE ts.teacher_id = 4
-- TEACHER -----------^
