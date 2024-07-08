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
# Partitioning
In an effort to further reduce the amount of data that needs to be read during operations (i.e., data skipping) and to increase performance on large tables, Delta Lake partitioning allows you to organize a Delta table by dividing the data into smaller chunks called partitions.

![image](https://github.com/yadavraganu/spark/assets/77580939/b6e854d4-bb0d-49c5-8f6a-6162533af0d2)

1. A Delta table with no partitions is organized into a single directory.
2. A Delta table partitioned on a single column has a directory created for each of the partition values.
3. A Delta table partitioned on multiple columns has a directory created for each partition value, and then subdirectories are created for each of the additional columns defined for the partition

In Delta Lake, partitions run the risk of decreasing performance in many cases, as opposed to not partitioning a Delta table. This is because partitions can create the small file problem
Delta Lake also makes it easy to update only specified partitions using replaceWhere
```
# import month from SQL functions
from pyspark.sql.functions import lit
from pyspark.sql.types import LongType
# use replaceWhere to update a specified partition
spark.read.format("delta").load(destination_path).where("PickupMonth == '12' and PaymentType == '3' ").withColumn("PaymentType", lit(4).cast(LongType())).write.format("delta").option("replaceWhere", "PickupMonth = '12'").mode("overwrite").save(destination_path)
```
While using .where() for reading data can be very effective, you can also use .where() in combination with performance tuning commands, such as compaction, OPTIMIZE, and ZORDER BY, to perform those operations only on a specified partition(s)
### Partitioning Warnings and Considerations
1. Select your partition column(s) carefully. If the cardinality of a column is very high, do not use that column for partitioning. High cardinality columns are great for Z-ordering, but not partitioning, because it can lead to the same small file problem
2. You can partition by a column if you expect data in that partition to be at least 1 GB. Tables with fewer, larger partitions tend to outperform tables with many smaller partitions, otherwise you run into the small file problem
# Compact Files
When performing DML operations on a Delta table, often new data is written in many small files across partitions. Due to the additional volume of file metadata and the total number of data files that need to be read, queries and operation speed can be reduced
