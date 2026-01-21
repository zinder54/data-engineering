'''Created a database with tables - FactBilling, DimCustomer,DimMonth, 
Below is querying this data using rollup, cube and grouping sets. this is witin postgresSQL'''

'''grouping sets query'''
-- select year,category, sum(billedamount) as totalbilledamount
-- from "FactBilling"
-- left join "DimCustomer"
-- on "FactBilling".customerid = "DimCustomer".customerid
-- left join "DimMonth"
-- on "FactBilling".monthid="DimMonth".monthid
-- group by grouping sets(year,category);
'''rollup query'''
-- select year,category, sum(billedamount) as totalbilledamount
-- from "FactBilling"
-- left join "DimCustomer"
-- on "FactBilling".customerid = "DimCustomer".customerid
-- left join "DimMonth"
-- on "FactBilling".monthid="DimMonth".monthid
-- group by rollup(year,category)
-- order by year, category;
'''cube query'''
-- select year,category, sum(billedamount) as totalbilledamount
-- from "FactBilling"
-- left join "DimCustomer"
-- on "FactBilling".customerid = "DimCustomer".customerid
-- left join "DimMonth"
-- on "FactBilling".monthid="DimMonth".monthid
-- group by cube(year,category)
-- order by year, category;
'''creating a materialised view for the data grouped by country and year'''
-- CREATE MATERIALIZED VIEW countrystats (country, year, totalbilledamount) AS
-- (select country, year, sum(billedamount)
-- from "FactBilling"
-- left join "DimCustomer"
-- on "FactBilling".customerid = "DimCustomer".customerid
-- left join "DimMonth"
-- on "FactBilling".monthid="DimMonth".monthid
-- group by country,year);
'''querying the view to see the data'''
-- SELECT * FROM countrystats

'''These are the same but querying different columns and are self led with hints'''
'''grouping sets'''
SELECT year, quartername, sum(billedamount) AS totalbilledamount
from "FactBilling"
left join "DimCustomer"
on "FactBilling".customerid = "DimCustomer".customerid
left join "DimMonth"
on "FactBilling".monthid = "DimMonth".monthid
group by grouping sets(year,quartername)

'''rollup'''
SELECT country,category, sum(billedamount) AS totalbilledamount
from "FactBilling"
left join "DimCustomer"
on "FactBilling".customerid = "DimCustomer".customerid
left join "DimMonth"
on "FactBilling".monthid = "DimMonth".monthid
group by rollup(country,category)
order by country, category

'''cube'''
SELECT year,country, category, sum(billedamount) AS totalbilledamount
from "FactBilling"
left join "DimCustomer"
on "FactBilling".customerid = "DimCustomer".customerid
left join "DimMonth"
on "FactBilling".monthid = "DimMonth".monthid
group by cube(year,country, category)

'''creating the materialised view for the columns, this is then refreshed and queried using a SELECT * query'''
create MATERIALIZED VIEW average_billamount (year, quarter, category, country, average_bill_amount) AS
(SELECT year, quarter, category, country, avg(billedamount) as average_bill_amount
from "FactBilling"
left join "DimCustomer"
on "FactBilling".customerid = "DimCustomer".customerid
left join "DimMonth"
on "FactBilling".monthid="DimMonth".monthid
group by (year, quarter, category, country))