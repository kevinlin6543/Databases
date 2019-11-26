create table sailors(
    sid int PRIMARY KEY,
    sname varchar(30),
    rating int,
    age int
);

create table reserves(
    sid int,
    bid int,
    day date,
    hour int,
	PRIMARY KEY (sid, bid, day)
);

create table boats(
  bid int PRIMARY KEY,
	bname char(20),
	color char(10),
	length int,
	cost int,
	rate int
);

create table repairs(
  bid int,
	cost int
);


insert into sailors values (22,'dusting',7,45);
insert into sailors values (29,'brutus',1,33);
insert into sailors values (31,'lubber',8,55);
insert into sailors values (32,'andy',8,25);
insert into sailors values (58,'rusty',10,35);
insert into sailors values (64,'horatio',7,16);
insert into sailors values (71,'zorba',10,35);
insert into sailors values (74,'horatio',9,25);
insert into sailors values (85,'art',3,25);
insert into sailors values (95,'bob',3,63);
insert into sailors values (23,'emilio',7,45);
insert into sailors values (24,'scruntus',1,33);
insert into sailors values (35,'figaro',8,55);
insert into sailors values (59,'stum',8,25);
insert into sailors values (60,'jit',10,35);
insert into sailors values (61,'ossola',7,16);
insert into sailors values (62,'shaun',10,35);
insert into sailors values (88,'dan',9,25);
insert into sailors values (89,'dye',3,25);
insert into sailors values (90,'vin',3,63);

insert into reserves values (23,104,'1998/10/10', 4);
insert into reserves values (24,104,'1998/10/10', 2);
insert into reserves values (35,104,'1998/8/10', 2);
insert into reserves values (59,105,'1998/7/10', 3);
insert into reserves values (23,105,'1998/11/10', 1);
insert into reserves values (35,105,'1998/11/6', 5);
insert into reserves values (59,106,'1998/11/12', 6);
insert into reserves values (60,106,'1998/9/5', 3);
insert into reserves values (60,106,'1998/9/8', 3);
insert into reserves values (88,107,'1998/9/8', 1);
insert into reserves values (89,108,'1998/10/10', 2);
insert into reserves values (90,109,'1998/10/10', 4);
insert into reserves values (89,109,'1998/8/10', 6);
insert into reserves values (60,109,'1998/7/10', 7);
insert into reserves values (59,109,'1998/11/10', 4);
insert into reserves values (62,110,'1998/11/6', 3);
insert into reserves values (88,110,'1998/11/12', 3);
insert into reserves values (88,110,'1998/9/5', 5);
insert into reserves values (88,111,'1998/9/8', 5);
insert into reserves values (61,112,'1998/9/8', 9);
insert into reserves values (22,101,'1998/10/10', 3);
insert into reserves values (22,102,'1998/10/10', 1);
insert into reserves values (22,103,'1998/8/10', 1);
insert into reserves values (22,104,'1998/7/10', 4);
insert into reserves values (31,102,'1998/11/10', 2);
insert into reserves values (31,103,'1998/11/6', 2);
insert into reserves values (31,104,'1998/11/12', 5);
insert into reserves values (64,101,'1998/9/5', 7);
insert into reserves values (64,102,'1998/9/8', 2);
insert into reserves values (74,103,'1998/9/8', 1);

insert into boats values (101,'Interlake','blue', 45,1800,50);
insert into boats values (102,'Interlake','red', 45,1800,50);
insert into boats values (103,'Clipper','green', 40,950,40);
insert into boats values (104,'Clipper','red', 40,800,40);
insert into boats values (105,'Marine','red', 35,850,35);
insert into boats values (106,'Marine','green', 35,850,35);
insert into boats values (107,'Marine','blue', 35,775,32);
insert into boats values (108,'Driftwood','red', 35,775,32);
insert into boats values (109,'Driftwood','blue', 35,500,32);
insert into boats values (110,'Klapser','red', 30,625,26);
insert into boats values (111,'Sooney','gren', 28,625,22);
insert into boats values (112,'Sooney','red', 28,400,21);

insert into repairs values (101, 200);
insert into repairs values (103, 100);
insert into repairs values (104, 70);
insert into repairs values (111, 30);
insert into repairs values (112, 20);
