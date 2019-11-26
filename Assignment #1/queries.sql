-- Databases Course Assignment #1 Queries
-- By: Kevin Lin

-- Select, for each boat, the sailor who made the highest number of reservations for that boat.
SELECT t.bid, t.sid, MAX(count1)
FROM (
    SELECT r.bid as bid, r.sid as sid, COUNT(r.bid) as count1
    FROM reserves as r, sailors as s
    WHERE r.sid = s.sid
    GROUP BY r.bid, r.sid
    ORDER BY count1 DESC) as t
GROUP BY t.bid
ORDER BY t.bid;

-- List, for every boat, the number of times it has been reserved, excluding those boats that have never been reserved (list the id and the name).
SELECT b.*, COUNT(b.bid) as reservations
FROM boats as b
RIGHT JOIN reserves as r
ON r.bid = b.bid
WHERE b.bid IS NOT NULL
GROUP BY b.bid;


-- List those sailors who have reserved every red boat (list the id and the name).
SELECT s.*, b.bid
FROM sailors as s, reserves as r, boats as b
WHERE s.sid = r.sid AND b.bid = r.bid AND b.color = 'red'
GROUP BY s.sid
HAVING COUNT(DISTINCT s.sid, b.bid) = (
    SELECT COUNT(b.bid)
    FROM boats as b
    WHERE b.color = 'red'
    );

-- List those sailors who have reserved only red boats.
SELECT s.*
FROM sailors as s,reserves as r, boats as b
WHERE r.sid = s.sid AND b.bid = r.bid
GROUP BY s.sid
HAVING (s.sid, COUNT(s.sid)) IN (
    SELECT s.sid, COUNT(s.sid)
    FROM sailors as s,reserves as r, boats as b
    WHERE r.sid = s.sid AND b.bid = r.bid AND b.color = 'red'
    GROUP BY s.sid);

-- For which boat are there the most reservations?
SELECT b.*, COUNT(r.bid) as count
FROM reserves as r, boats as b
WHERE r.bid = b.bid
GROUP BY b.bid
ORDER BY count DESC
LIMIT 1;


-- Select all sailors who have never reserved a red boat.
SELECT s.*
FROM sailors as s
LEFT JOIN (
    reserves as r
        INNER JOIN boats as b
        ON r.bid = b.bid AND b.color = 'red')
    ON s.sid = r.sid
WHERE b.color is NULL;


-- Find the average age of sailors with a rating of 10.
SELECT AVG(age) as Average_age from sailors
WHERE rating = 10
GROUP BY age;