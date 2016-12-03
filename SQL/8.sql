-- 8. countries where capital doesn't have the largest population
select Country.Name, Population, SurfaceArea 
from
(
	select max_cities.CountryName as Name
	from 
	(
		select Country.Name as CountryName, City.Name as MaxCity
		from Country inner join City on Country.Code == City.CountryCode		
		group by Country.Name
		having max(City.Population) = City.Population
	) max_cities

	left join 

	(
		select Country.Name as CountryName, City.Name as MaxCity
		from Country inner join (City inner join Capital on City.Id = Capital.CityId) on Country.Code == City.CountryCode
	) capitals

	on max_cities.MaxCity = capitals.MaxCity
	where capitals.CountryName is null	
) MaxNotCapital

inner join Country on MaxNotCapital.Name = Country.Name
order by 1.0 * Population / SurfaceArea desc, Country.Name;