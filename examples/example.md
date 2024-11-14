CREATE table (name, age INDEXED, team);
INSERT table ("Max Verstappen", "27", "ORBR"); 
INSERT table ("Charles Leclerc", "27", "Ferrari"); 
INSERT table ("Carlos Sainz", "30", "Ferrari"); 
INSERT table ("Lewis Hamilton", "39", "Mercedes");
INSERT table ("George Russell", "26", "Mercedes");
INSERT table ("Oscar Piastri", "23", "McLaren");
INSERT table ("Lando Norris", "25", "McLaren");
SELECT FROM table WHERE ((age > "26") AND (age < "28")) OR (team = "McLaren");