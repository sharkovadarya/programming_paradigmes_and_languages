-- 1. top 5 countries with largest area ordered by descending
select Name 
from Country
order by SurfaceArea desc, Name
limit 5;