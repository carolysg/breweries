# PostgreSQL

The data in PostgreSQL mirrors the aggregated data from the gold layer, which contains information on breweries grouped by 'state_province' and 'brewery_type', along with the corresponding count of breweries. This data was persisted in PostgreSQL to facilitate easier analysis and querying through SQL.

Persisting the data in PostgreSQL allows users to run efficient queries for insights, perform more complex analysis, and integrate with various analytical tools.

To query the data in PostgreSQL, you can use SQL commands. For example:

```
SELECT * 
FROM breweries
WHERE state_province = 'arizona' 
AND brewery_type = 'micro';
```