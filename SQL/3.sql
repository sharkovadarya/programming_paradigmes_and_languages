-- 3.Malaysia capital
select CityName
from 
(
	select City.Name as CityName
	from 
	City inner join 
	(
		select Code from Country as Code
		where Name = 'Malaysia'
	) 
	on City.CountryCode = Code
)
inner join
(
	select City.Name as CapitalName
	from City inner join Capital on City.Id = Capital.CityId
)
on CityName = CapitalName;

