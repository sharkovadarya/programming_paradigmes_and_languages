-- 6. top 20 biggest percentage cities
select City.Name, City.Population, Country.Population
from City inner join Country on City.CountryCode = Country.Code
order by (100.0 * City.Population / Country.Population) desc, City.Name desc
limit 20;