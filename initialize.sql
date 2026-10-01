-- initialize.sql
-- Creates the users and posts tables (one user has many posts) and fills them with sample data.
-- Safe to rerun: existing tables are dropped first.

-- Drop posts first because it depends on users (foreign key)
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id    INT PRIMARY KEY,
    username   VARCHAR(50) NOT NULL,
    email      VARCHAR(100) NOT NULL,
    created_at DATETIME
);

CREATE TABLE posts (
    post_id    INT PRIMARY KEY,
    user_id    INT NOT NULL,
    title      VARCHAR(200),
    body       TEXT,
    posted_at  DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Users (inserted first so posts can reference them)
INSERT INTO users (user_id, username, email, created_at) VALUES (1, 'alice', 'alice@example.com', '2026-01-05 10:00:00');
INSERT INTO users (user_id, username, email, created_at) VALUES (2, 'bob', 'bob@example.com', '2026-01-06 14:30:00');
INSERT INTO users (user_id, username, email, created_at) VALUES (3, 'carmen', 'carmen@example.com', '2026-01-09 08:15:00');
INSERT INTO users (user_id, username, email, created_at) VALUES (4, 'dev', 'dev@example.com', '2026-01-12 19:45:00');
INSERT INTO users (user_id, username, email, created_at) VALUES (5, 'elena', 'elena@example.com', '2026-01-15 11:20:00');
INSERT INTO users (user_id, username, email, created_at) VALUES (6, 'farid', 'farid@example.com', '2026-01-20 16:05:00');
INSERT INTO users (user_id, username, email, created_at) VALUES (7, 'grace', 'grace@example.com', '2026-01-24 09:40:00');
INSERT INTO users (user_id, username, email, created_at) VALUES (8, 'hiro', 'hiro@example.com', '2026-02-01 13:10:00');
INSERT INTO users (user_id, username, email, created_at) VALUES (9, 'isla', 'isla@example.com', '2026-02-04 17:55:00');
INSERT INTO users (user_id, username, email, created_at) VALUES (10, 'jamal', 'jamal@example.com', '2026-02-08 07:30:00');

-- Posts (every user_id matches an existing user)
INSERT INTO posts (post_id, user_id, title, body, posted_at) VALUES (1, 1, 'Hello world', 'My first post on here!', '2026-02-10 09:00:00');
INSERT INTO posts (post_id, user_id, title, body, posted_at) VALUES (2, 2, 'SQL tips', 'Foreign keys keep your data consistent.', '2026-02-11 12:15:00');
INSERT INTO posts (post_id, user_id, title, body, posted_at) VALUES (3, 1, 'Weekend hike', 'Saw some great views on the Blue Ridge.', '2026-02-12 18:40:00');
INSERT INTO posts (post_id, user_id, title, body, posted_at) VALUES (4, 3, 'Coffee rankings', 'Ranking every coffee shop near campus.', '2026-02-14 08:05:00');
INSERT INTO posts (post_id, user_id, title, body, posted_at) VALUES (5, 4, 'Learning Python', 'pandas makes CSVs so much easier.', '2026-02-15 20:30:00');
INSERT INTO posts (post_id, user_id, title, body, posted_at) VALUES (6, 5, 'Book club', 'This month we are reading a mystery novel.', '2026-02-17 15:45:00');
INSERT INTO posts (post_id, user_id, title, body, posted_at) VALUES (7, 6, 'Gym progress', 'Finally hit a new personal record.', '2026-02-19 06:50:00');
INSERT INTO posts (post_id, user_id, title, body, posted_at) VALUES (8, 7, 'Recipe share', 'Easy weeknight pasta that takes 20 minutes.', '2026-02-21 19:10:00');
INSERT INTO posts (post_id, user_id, title, body, posted_at) VALUES (9, 8, 'Game night', 'Who is in for board games on Friday?', '2026-02-23 21:00:00');
INSERT INTO posts (post_id, user_id, title, body, posted_at) VALUES (10, 2, 'Joins explained', 'A JOIN combines rows from two related tables.', '2026-02-25 10:25:00');
