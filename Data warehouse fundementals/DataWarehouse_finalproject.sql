'''this is the final project for the course data warehouse fundementals
 this is self lead and fully my work, these are copies of what i used within postgres platform to create
 tables, import csv data and query that data'''

--  create DimStation
CREATE TABLE DimStation (
	stationid int not null primary key,
	city varchar(20) not null
)

-- create DimDate table 
CREATE TABLE DimDate (
    dateid int PRIMARY KEY,          
    full_date date NOT NULL,
    year int NOT NULL,
    quarter int NOT NULL,
    quarter_name char(2) NOT NULL,
    month int NOT NULL,
    month_name varchar(11) NOT NULL,
    day int NOT NULL,
    weekday int NOT NULL,
    weekday_name varchar(11) NOT NULL
);

-- create DimTruck table
CREATE TABLE DimTruck (
    truckid int not null primary key,
	truck_type varchar(7) not null
)

--  create the facts table
CREATE TABLE FactTrips (
	tripid int not null,
	dateid int not null,
	stationid int not null,
	truckid int not null,
	waste_collected NUMERIC(5,2) not null,

	constraint fk_fact_dateid
    foreign key (dateid)
    references DimDate (dateid),
	
	constraint fk_fact_stationid
	foreign key (stationid)
	references DimStation(stationid),

	constraint fk_fact_truckid
	foreign key (truckid)
	references DimTruck(truckid)
)

-- IMPORTING DATA
'''tried using the below, as i have different col names than the source csv, but as i am in pgadmin
this hasnt worked so used the import function on the table to load the data into each table'''
COPY dim_station (
    station_id,
    city
)
FROM '/var/lib/pgadmin/dim_station.csv'
DELIMITER ','
CSV HEADER;

'''querying the data using grouping sets, rollup and cube. then creating a materialised view'''

--grouping sets
SELECT
    s.stationid,
    t.truck_type,
    SUM(f.amount) AS total_waste
FROM MyFactTrips f
JOIN DimStation s ON f.stationid = s.stationid
JOIN DimTruck t ON f.truckid = t.truckid
GROUP BY GROUPING SETS (s.stationid,t.truck_type,total_waste)

--rollup
SELECT s.stationid,s.city, d.year, SUM(waste_collected) as total_waste,
    GROUPING(s.stationid) AS station_id,
    GROUPING(d.year) AS g_year,
    GROUPING(s.city) AS g_city
From FactTrips f
JOIN DimStation s ON f.stationid = s.stationid
JOIN DimDate d ON f.dateid = d.dateid
GROUP BY ROLLUP (
(s.stationid,s.city, d.year)
) LIMIT 5

--cube
SELECT
    s.city,s.stationid,d.year,
    AVG(f.waste_collected) AS avg_waste,
    GROUPING(s.stationid) AS g_station,
    GROUPING(s.city) AS g_city,
	GROUPING(d.year) AS g_year
FROM FactTrips f
JOIN DimStation s ON f.stationid = s.stationid
JOIN DimDate d ON f.dateid = d.dateid
GROUP BY CUBE (
    (s.stationid, s.city,d.year))

--materialised view 
CREATE MATERIALIZED VIEW max_waste_stats (city, stationid, trucktype, max_waste_collected) AS 
(SELECT s.city,s.stationid,t.trcuk_type, MAX(waste_collected) AS max_waste
FROM FactTrips f
JOIN DimStation s ON f.stationid = s.stationid
JOIN DimTruck t ON f.truckid = t.truckid
GROUP BY (s.city,s.stationid,t.trcuk_type))