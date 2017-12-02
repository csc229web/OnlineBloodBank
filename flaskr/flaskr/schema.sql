drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  'text' text not null
);
drop table if exists donor_login;
create table donor_login (
  donor_id integer primary key autoincrement,
  donor_username text not null,
  donor_password text not null
);