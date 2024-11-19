# Silver layer

In this layer, the following transformations were applied to the data:

- Missing data removal: Columns containing only null values were dropped (if they exist).
- Data types: 'longitude' and 'latitude' columns were transformed into float columns.
- Standardization: All string columns were converted to lowercase.
- Column deduplication: The 'state' column was removed if its values were identical to the 'state_province' column.

The transformed data was saved in parquet format, partitioned by 'country', 'state_province', and 'city'. Existing matching data was overwritten.