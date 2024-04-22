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
- Bin-packing aims to produce evenly-balanced data files with respect to their size on disk, but not necessarily  
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