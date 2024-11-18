# Hello, your computer has a virus!

---

## Examples

---

1. First
CREATE table (name, age INDEXED, team);
INSERT table ("Max Verstappen", "27", "ORBR"); 
INSERT table ("Charles Leclerc", "27", "Ferrari"); 
INSERT table ("Carlos Sainz", "30", "Ferrari"); 
INSERT table ("Lewis Hamilton", "39", "Mercedes");
INSERT table ("George Russell", "26", "Mercedes");
INSERT table ("Oscar Piastri", "23", "McLaren");
INSERT table ("Lando Norris", "25", "McLaren");
SELECT FROM table WHERE ((age > "26") AND (age < "28")) OR (team = "McLaren");

---

1. Second
Create studeNts (id, age);
insert into students ("1", "25");
insert into studeNts ("1", "25");
insert into studeNts ("1", "25");
insert into studeNts ("2", "25");
insert into studeNts ("1", "2");
insert into studeNts ("1", "2");
select from students;
select from studeNts;
select from studeNts Where (name = "2");
