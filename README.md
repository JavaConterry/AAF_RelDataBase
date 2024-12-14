# Examples

---

1. First
CREATE drivers (name, age INDEXED, team);  
INSERT drivers ("Max Verstappen", "27", "ORBR");  
INSERT drivers ("Charles Leclerc", "27", "Ferrari");  
INSERT drivers ("Carlos Sainz", "30", "Ferrari");  
INSERT drivers ("Lewis Hamilton", "39", "Mercedes");  
INSERT drivers ("George Russell", "26", "Mercedes");  
INSERT drivers ("Oscar Piastri", "23", "McLaren");  
INSERT drivers ("Lando Norris", "25", "McLaren");  
SELECT FROM drivers WHERE ((age > "26") AND (age < "28")) OR (team = "McLaren");  

---

2. Second
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
