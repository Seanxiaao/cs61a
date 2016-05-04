.read sp16data.sql
.read fa15data.sql

-- Q2
CREATE TABLE obedience AS
  select seven as obedience, hilfinger as hilfinger from students;

-- Q3
CREATE TABLE smallest_int AS
  select time as time, smallest as smallest from students where smallest > 12 order by smallest limit 20;

-- Q4
CREATE TABLE greatstudents AS
  select a.date as date, a.number as number, a.pet as pet, a.color,b.color from students as a, fa15students as b where a.date = b.date and a.number = b.number and a.pet = b.pet;
-- Q5
CREATE TABLE matchmaker AS
  select a.pet as pet, a.song as song, a.color, b.color from students as a, students as b where a.pet = b.pet and a.song = b.song and a.time < b.time;

-- Q6
CREATE TABLE fa15favnum AS
  SELECT number,count(*) as count from fa15students group by number order by count desc limit 1;

CREATE TABLE fa15favpets AS
  SELECT pet, count(*) as count from fa15students group by pet order by count desc limit 10;

CREATE TABLE sp16favpets AS
  SELECT pet, count(*) as count from students group by pet order by count desc limit 10;

CREATE TABLE sp16dragon AS
  SELECT pet, count(*) as count from students where pet = 'dragon';

CREATE TABLE sp16alldragons AS
  SELECT pet, count(*) as count from students where pet like 'dragon';
  
CREATE TABLE obedienceimage AS
  SELECT seven, hilfinger, count(*) as count from students where seven = '7' group by hilfinger;

-- Q7
CREATE TABLE pairs AS
  WITH
    nums(n) as (
      SELECT 0 UNION
      SELECT n + 1 FROM nums WHERE n < 42
    )
  SELECT a.n AS x, b.n AS y FROM nums AS a, nums AS b WHERE a.n <= b.n;
