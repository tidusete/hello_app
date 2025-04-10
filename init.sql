-- init.sql
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    date_of_birth DATE NOT NULL
);