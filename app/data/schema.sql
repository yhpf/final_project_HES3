DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
    uid serial NOT NULL PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

INSERT INTO users (username, password) VALUES ( 'Test1', 'losen1' );
INSERT INTO users (username, password) VALUES ( 'Test2', 'losen2' );

