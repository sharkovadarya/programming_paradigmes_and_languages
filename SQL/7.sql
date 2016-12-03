-- 7. countries where most people don't live in cities from database
select Name from
(
	select Country.Name as Name, City.Population as CityPopulation, 
	       Country.Population as CountryPopulation
	from Country inner join City on Country.Code == City.CountryCode
)
group by Name
having sum(CityPopulation) < (CountryPopulation / 2);