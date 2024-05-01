Optimize is used to coalesce small files into larger ones in delta tables.
```
OPTIMIZE delta.`/data/events`
OPTIMIZE events

from delta.tables import *
deltaTable = DeltaTable.forPath(spark, "/data/events")
deltaTable.optimize().executeCompaction()
```
If you have a large amount of data and only want to optimize a subset of it, you can specify an optional  
partition predicate using WHERE:
```
OPTIMIZE events WHERE date >= '2022-11-18'

from delta.tables import *
deltaTable = DeltaTable.forName(spark, "events")
deltaTable.optimize().where("date='2021-11-18'").executeCompaction()
```
Notes :
- Bin-packing optimization is idempotent, meaning that if it is run twice on the same dataset, the second run has no effect.
- Bin-packing aims to produce evenly balanced data files with respect to their size on disk, but not necessarily the
  number of tuples per file. However, the two measures are most often correlated.
- Readers of Delta tables use snapshot isolation, which means that they are not interrupted when OPTIMIZE  
  removes unnecessary files from the transaction log. OPTIMIZE makes no data related changes to the table,  
  so a read before and after an OPTIMIZE has the same results. Performing OPTIMIZE on a table that is a streaming  
  source does not affect any current or future streams that treat this table as a source. OPTIMIZE returns the file  
  statistics (min, max, total, and so on) for the files removed and the files added by the operation.  
  Optimize stats also contains the Z-Ordering statistics, the number of batches, and partitions optimized.

# How often should I run OPTIMIZE?
When you choose how often to run OPTIMIZE, there is a trade-off between performance and cost. For better end-user  
query performance, run OPTIMIZE more often. This will incur a higher cost because of the increased resource usage.  
To optimize cost, run it less often.

# What’s the best instance type to run OPTIMIZE (bin-packing and Z-Ordering) on?
Both operations are CPU intensive operations doing large amounts of Parquet decoding and encoding.
Databricks recommends Compute optimized instance types. OPTIMIZE also benefits from attached SSDs.

# Auto Compaction/Optimize
Auto compaction combines small files within Delta table partitions to automatically reduce small file problems.  
Auto compaction occurs after a write to a table has succeeded and runs synchronously on the cluster that has  
performed the write. Auto compaction only compacts files that haven’t been compacted previously.  

- You can control the output file size by setting the Spark configuration 
`spark.databricks.delta.autoCompact.maxFileSize`
- Auto compaction is only triggered for partitions or tables that have at least a certain number of small files.
  You can optionally change the minimum number of files required to trigger auto compaction by setting 
  `spark.databricks.delta.autoCompact.minNumFiles`
- Auto compaction can be enabled at the table or session level using the following settings:
```
Table property: delta.autoOptimize.autoCompact
SparkSession setting: spark.databricks.delta.autoCompact.enabled
  
Below are possible values ->
  
auto (recommended) :Tunes target file size while respecting other autotuning functionality.
Requires Databricks Runtime 10.4 LTS or above.
legacy : Alias for true. Requires Databricks Runtime 10.4 LTS or above. 
true : Use 128 MB as the target file size. No dynamic sizing
false : Turns off auto compaction. Can be set at the session level to override auto compaction
for all Delta tables modified in the workload.
```
# Optimized writes
Optimized writes improve file size as data is written and benefit subsequent reads on the table.
Optimized writes are most effective for partitioned tables, as they reduce the number of small files written to each  
partition. Writing fewer large files is more efficient than writing many small files, but you might still see an  
increase in write latency because data is shuffled before being written.

Optimized writes can be enabled at the table or session level using the following settings:
```
Table setting: delta.autoOptimize.optimizeWrite
SparkSession setting: spark.databricks.delta.optimizeWrite.enabled

Below are possible values ->

true: Use 128 MB as the target file size.
false:Turns off optimized writes. It Can be set at the session level to override auto compaction for all Delta tables  
modified in the workload.
```