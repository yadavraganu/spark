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
### Compaction
The consolidation of files is called compaction, or bin-packing. To perform compaction using your own specifications, for example, specifying the number of files to compact the Delta table into, you can use a DataFrame writer with dataChange = false. This indicates that the operation does not change the data; it simply rearranges the data layout
```
# define the path and number of files to repartition
path = "/mnt/datalake/book/chapter05/YellowTaxisDelta"
numberOfFiles = 5
# read the Delta table and repartition it
spark.read \
 .format("delta") \
 .load(path) \
 .repartition(numberOfFiles) \
 .write \
 .option("dataChange", "false") \
 .format("delta") \
 .mode("overwrite") \
 .save(path)
```
### OPTIMIZE
The OPTIMIZE command aims to remove unnecessary files from the transaction log while also producing evenly balanced data files in terms of file size. The smaller files are compacted into new, larger files up to 1 GB. Unlike compaction achieved through the repartition method, there is no need to specify the dataChange option.

OPTIMIZE uses snapshot isolation when performing the command so concurrent operations and downstream streaming consumers remain uninterrupted.

Let’s walk through an example of OPTIMIZE to repartition the existing table into 1,000 files to simulate a scenario where we consistently insert data into a table.
```
%sql
OPTIMIZE taxidb.YellowTaxis
```
After running the OPTIMIZE command on the table, we can see that 1,000 files were removed and 9 files were added.
It is important to note that the 1,000 files that were removed were not physically removed from the underlying storage rather, they were only logically removed from the transaction log. These files will be physically removed from the underlying storage next time you run VACUUM

Optimization using OPTIMIZE is also idempotent, meaning that if it is run twice on the same table or subset of data, the second run has no effect.We can also optimize on specific subsets of data rather than optimizing the entire
table. This can be useful when we are only performing DML operations on a specific partition
```
%sql
OPTIMIZE taxidb.YellowTaxis WHERE PickupMonth = 12
```
### OPTIMIZE Considerations
1. The OPTIMIZE command is effective for tables, or table partitions, that you write data continuously to and thus contain large amounts of small files
2. The OPTIMIZE command is not effective for tables with static data or tables where data is rarely updated because there are few small files to coalesce into larger files
3. The OPTIMIZE command can be a resource-intensive operation that takes time to execute. You can incur costs from your cloud provider while running your compute engine to perform the operation

# ZORDER BY
While OPTIMIZE aims to consolidate files, Z-ordering allows us to read the data in those files more efficiently by optimizing the data layout.Specifically, this technique clusters and colocates related information in the same set of files to allow for faster data retrieval.Z-order indexes can improve the performance of queries that filter on the specified
Z-order columns. Performance is improved because it allows queries to more efficiently locate the relevant rows, and it also allows joins to more efficiently locate rows with matching values. This efficiency can ultimately be attributed to the reduction in the amount of data that needs to be read during queries.
We can apply ZORDER BY with the OPTIMIZE command to consolidate files and effectively order the data in those files.
```
%sql
OPTIMIZE taxidb.tripData ZORDER BY PickupDate

OPTIMIZE taxidb.tripData ZORDER BY PickupDate, VendorId
WHERE PickupMonth = 2022
```
### ZORDER BY Considerations
- You can specify multiple columns for ZORDER BY as a comma-separated list in the command. However, the effectiveness of the locality drops with each additional column
- Similar to OPTIMIZE, you can apply Z-ordering to specific subsets of data, such as partitions, rather than applying it to the entire table
- You cannot use ZORDER BY on fields used for partitioning.
- Z-order clustering can only occur within a partition.
- For unpartitioned tables, files can be combined across the entire table.

Unlike OPTIMIZE, Z-ordering is not idempotent but aims to be an incremental operation. The time it takes for Z-ordering is not guaranteed to reduce over multiple runs. However, if no new data was added to a partition that was just Z-ordered, another Z-ordering of that partition will not have any effect
# Liquid Clustering
While some of the performance tuning techniques mentioned above aim to optimize data layouts and thus improve read and write performance, thereare some shortcomings:
### Partitioning
Partitions run the risk of introducing the small file problem, where data is stored across many different small files, which inevitably results in poor performance. And once a table is partitioned, this partition cannot be changed and can cause challenges for new use cases or new query patterns. While Delta Lake supports partitioning, there are challenges with partition evolution, as partitioning is considered a fixed data layout.
### ZORDER BY
Anytime data is inserted, updated, or deleted on a table, OPTIMIZE ZORDER BY must be run again for optimization. And when ZORDER BY is applied again, the user must remember the columns used in the expression. This is because the columns used in ZORDER BY are not persisted and can cause errors or challenges when attempting to apply it again. Since OPTIMIZE ZORDER BY is not idempotent, this will result in reclustering data when it is run
Many of the shortcomings with partitioning and Z-ordering can be addressed through Delta Lake’s liquid clustering feature. The following scenarios for Delta tables benefit greatly from liquid clustering
- Tables often filtered by high cardinality columns
- Tables with substantial skew in data distribution
- Tables that require large amounts of tuning and maintenance
- Tables with concurrent write requirements
- Tables with partition patterns that change over time
Delta Lake’s liquid clustering feature aims to address limitations found with partitioning and Z-ordering, and revamp both read and write performance through a more dynamic data layout. Ultimately, liquid clustering helps reduce performance tuning overhead while also supporting efficient query access.
### Enabling Liquid Clustering
You must specify liquid clustering using the CLUSTER BY command when you create the table; you cannot add clustering to an existing table (e.g., using ALTER TABLE) that does not have liquid clustering enabled.
It is important to note that only a few operations automatically cluster data on write when writing data to a table with liquid clustering. The following operations support automatically clustering data on write, provided the size of the data being inserted does not exceed 512 GB:
- INSERT INTO
- CREATE TABLE AS SELECT (CTAS) statements
- COPY INTO
- Write appends such as spark.write.format("delta").mode("append")

Since only these specific operations support clustering data on write, you should trigger clustering on a regular basis by running OPTIMIZE. Running this command frequently will ensure that data is properly clustered.
It is also worth noting that liquid clustering is incremental when triggered by OPTIMIZE, meaning that only the necessary data is rewritten to accommodate data that needs to be clustered

### Operations on Clustered Columns
- __Operations on Clustered Columns__ :While you must specify how a table is clustered when it is initially created, you can still change the columns used for clustering on the table using ALTER TABLE and CLUSTER BY.You can specify up to four columns as clustering keys.
```
%sql
ALTER TABLE taxidb.tripDataClustered CLUSTER BY (VendorId, RateCodeId);
```
- __Viewing clustered columns__:
```
%sql
DESCRIBE TABLE taxidb.tripDataClustered;
```
- __Removing clustered columns__:
```
%sql
ALTER TABLE taxidb.tripDataClustered CLUSTER BY NONE;
```
### Liquid Clustering Warnings and Considerations

- You must enable Delta Lake liquid clustering when first creating a table. You cannot alter an existing table to add clustering without clustering being enabled when the table is first created.
- You can only specify columns with statistics collected for clustered columns. Remember, only the first 32 columns in a Delta table have statistics collected bydefault.
- Structured Streaming workloads do not support clustering-on-write.
- Run OPTIMIZE frequently to ensure new data is clustered.
