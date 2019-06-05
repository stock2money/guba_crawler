CREATE DATABASE if not EXISTS mydb;
use mydb;


create table if not exists comment(
    code varchar(20) not NULL,
	time varchar(30) not null,
    title varchar(200) not null,
    href varchar(100) not null,
    detail text not null,
    author varchar(50) not null,
    emotion int,
    primary key(code, author, title)
) charset=utf8;

create table if not exists news(
	time varchar(30) not null,
    title varchar(200) not null,
    href varchar(100) not null,
    detail text not null,
    primary key(time, title)
) charset=utf8;