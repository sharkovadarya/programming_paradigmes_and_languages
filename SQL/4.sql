-- 4. country name and number of cities with population >= 1e6
select Name, count(Cities) as million_count from
(
	select Country.Name as Name, City.Name as Cities
	from Country left join City on City.CountryCode == Country.Code 
	                               and City.Population >= 1000000
)
group by Name
order by million_count desc, Name;