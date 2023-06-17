-- 12. Оцінки студентів у певній групі з певного предмета на останньому занятті.

SELECT grd.date_of, grp.codename, sub.title, stu.fullname, grd.grade
FROM grades grd
INNER JOIN students stu ON stu.id = grd.student_id
INNER JOIN groups grp ON grp.id = stu.group_id
INNER JOIN subjects sub ON sub.id = grd.subject_id
WHERE grd.date_of = (
    SELECT MAX(gd.date_of)
    FROM grades gd
    WHERE gd.subject_id = grd.subject_id
) AND grp.id = 2 AND grd.subject_id = 5 
--     GROUP --^            SUBJECT --^
ORDER BY grp.codename, sub.title, stu.fullname
