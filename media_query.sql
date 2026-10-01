-- Posts by users who joined in January 2026, with each post's author
SELECT u.username, u.email, p.title, p.posted_at
FROM posts AS p
JOIN users AS u ON p.user_id = u.user_id
WHERE u.created_at < '2026-02-01'
ORDER BY p.posted_at;
