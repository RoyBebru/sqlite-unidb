-- 6. Знайти список студентів у певній групі.

SELECT gr.codename, st.fullname
FROM students st
INNER JOIN groups gr ON gr.id = st.group_id 
WHERE gr.id = 2
--    GROUP --^
ORDER BY st.fullname
