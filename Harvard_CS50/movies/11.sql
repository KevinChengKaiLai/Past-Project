SELECT m.title
FROM movies m
JOIN stars s ON m.id = s.movie_id
JOIN people p ON s.person_id = p.id
WHERE p.name = 'Chadwick Boseman'
ORDER BY m.rating DESC
LIMIT 5;
