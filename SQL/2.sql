-- 2. select country with biggest rate based on latest available data
select Name, Rate
from Country inner join LiteracyRate on Country.Code = LiteracyRate.CountryCode
group by Name
having max(Year) = Year
order by Rate desc
limit 1;