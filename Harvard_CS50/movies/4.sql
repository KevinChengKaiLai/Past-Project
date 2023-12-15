

-- cat 4.sql | sqlite3 movies.db

SELECT COUNT(*) FROM movies
JOIN ratings ON movies.id = ratings.movie_id
WHERE ratings.rating = 10.0;


