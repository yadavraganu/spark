Optimizing the performance of a system, and in the context of Delta tables this involves optimizing how the data is stored and retrieved. Historically, retrieving data is accomplished by either increasing RAM or CPU for faster processing, or reducing the amount of data that needs to be read by skipping nonrelevant data. Delta Lake provides a number of different techniques that can be combined to accelerate data retrieval by efficiently reducing the amount of files and data that needs to be read during operations.
# Data Skipping
Skipping nonrelevant data is ultimately the foundation for most performance tuning features, as it aims to reduce the amount of data that needs to be read. This feature, called data skipping, can be enhanced through a variety of different techniques in Delta Lake.
Delta Lake automatically maintains the minimum and maximum value for up to 32 fields for files, and stores those values as part of the metadata.   
Delta Lake uses these minimum and maximum ranges to skip the files that are out of the range of the querying field values. This is a key aspect that enables data skipping through what is called data skipping statistics  
In order to maximize the effectiveness of data skipping, data can be consolidated, clustered, and colocated using commands such as OPTIMIZE and ZORDER BY  

Delta Lake collects the following data skipping statistics for each data file:
- Number of records
- Minimum values for each of the first 32 columns
- Maximum values for each of the first 32 columns
- Number of null values for each of the first 32 columns

Delta Lake collects these statistics on the first 32 columns defined in your table schema. Please note, each field within nested columns (e.g., StructType) counts as a column. You can configure statistics collection on certain columns by reordering columns in the schema, or you can increase the number of columns to collect statistics on by using __delta.dataSkippingNumIndexedCols__, but adding additional columns also adds additional overhead that can adversely affect write performance  

It may not be effective to collect minimum and maximum values on some columns because collecting statistics on long values like strings or binary can be an expensive operation
