create table if not exists BookLikes(
    id integer primary key autoincrement,
    asin char (100) not null,
    likes integer not null
);
