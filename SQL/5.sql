-- 5. government form with maximum surface area
select GovernmentForm, max(TotalArea) from
(
	select GovernmentForm, sum(SurfaceArea) as TotalArea
	from Country
	group by GovernmentForm
);