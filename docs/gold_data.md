# Gold layer

In this layer, the following transformations were applied to the data:

- Aggregation: The data was grouped by 'state_province' and 'brewery_type', and the count of breweries in each group was calculated.
- Filtering: Rows where the brewery count was zero were removed.

The aggregated data was saved in parquet format.
The table below brings details about the aggregated data:

| column name | type | description |
|-------------|------|-------------|
| state_province | STRING | state/province of the brewery
| brewery_type | STRING | size of the brewery
| brewery_count | INT | quantity of breweries per type and location