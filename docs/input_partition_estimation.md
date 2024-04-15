While reading the file based data spark considers below parameter for calculating the partition size & input partition count.  

- __spark.default.parallelism__ (default: Total No. of CPU cores)
- __spark.sql.files.maxPartitionBytes__ (default: 128 MB) - The maximum number of bytes to pack into a single partition when reading files.  
This configuration is effective only when using file-based sources such as Parquet, JSON and ORC.
- __spark.sql.files.openCostInBytes__ (default: 4 MB) -The estimated cost to open a file, measured by the number of bytes could be scanned in the same time.  
This is used when putting multiple files into a partition. It is better to over-estimated, then the partitions with small files will be faster than partitions with bigger files (which is scheduled first).  
This configuration is effective only when using file-based sources such as Parquet, JSON and ORC.

Calculation :

```
Total_File_size =  Sum of all the file sizes over disk  
Total_cost_for_file_opening = Number_of_files * spark.sql.files.openCostInBytes  
Total_size = Total_File_size + Total_cost_for_file_opening  
Per_core_size = Total_size/spark.default.parallelism  
Max_bytes_per_split = min(spark.sql.files.maxPartitionBytes, max(spark.sql.files.openCostInBytes,Per_core_size))
Num_of_partitions = Total_size / Max_bytes_per_split 
```