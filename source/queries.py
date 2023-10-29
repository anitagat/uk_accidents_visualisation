query1 = """
select * from accidents limit 100
"""

query2 = """
select * from vehicles limit 100
"""

query3 = """
select count(*) from accidents where Date between '2017-01-01' and '2017-12-31'
"""

query4 = """
select accident_count, district from
(select accidents.'Local_Authority_(District)' as district, count(accidents.'Accident_Index') as accident_count from accidents
where accidents.Date between '2005-01-01' and '2017-12-31'
group by accidents.'Local_Authority_(District)') as subquery 
order by accident_count desc 
limit 5
"""

query5 = """
select accident_count, make from
(select accidents.Date, vehicles.make, count(accidents.'Accident_Index') as accident_count
from accidents 
inner join vehicles on accidents.Accident_Index = vehicles.Accident_Index
where Date between '2005-01-01' and '2005-12-31'
group by vehicles.make) as subquery
order by accident_count desc
limit 5"""

query6 = """ 
select avg(casualties), year from

(
    select substr(accidents.Date, 1,4) as year, Number_of_Casualties as casualties 
    from accidents
)

group by year
order by year
"""

query7 = """
select count(accident_no) as accident_count, year from
(select substr(accidents.Date, 1,4) as year, accidents.Accident_Index as accident_no
from accidents)
group by year
order by year"""

query8 = """
select accidents.'Local_Authority_(District)' as district, accidents.'Accident_Index' as accident_count, accidents.'Year' as year, accidents.'Longitude' as longitude, accidents.'Latitude' as latitude from accidents
where Year = '2017'
"""

query9 = """
select accidents.Accident_Severity, accidents.Urban_or_Rural_Area, vehicles.Age_Band_of_Driver, vehicles.Age_of_Vehicle, vehicles.'Engine_Capacity_.CC.', vehicles.Sex_of_Driver from accidents
inner join vehicles on accidents.Accident_Index = vehicles.Accident_Index
limit 100000
"""