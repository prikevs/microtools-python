drop database if exists iiblogs;

CREATE DATABASE iiblogs DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
use iiblogs;

create table blogs
(
 id int unsigned auto_increment primary key,
 name varchar(50) not null,
 address varchar(100) not null
);

