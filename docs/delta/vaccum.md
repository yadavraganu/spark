# Use of Vaccum
You can remove data files no longer referenced by a Delta table that are older than the retention threshold by running  
the VACUUM command on the table.Below are few point to consider while running vaccum

- It is used for deleting unused data files reduces cloud storage costs.
- It removed file old files & which have retention threshold beyond time set by below property
``` 
delta.deletedFileRetentionDuration = "interval <interval>": 
Determines the threshold VACUUM uses to remove data  
files no longer referenced in the current table version. The default is interval 7 days.
```
- Data files removed by VACUUM might contain records that have been modified or deleted.Permanently removing these  
  files from cloud storage ensures these records are no longer accessible.
- VACUUM removes all files from directories not managed by Delta Lake, ignoring directories beginning with _ or .
- If you are storing additional metadata like Structured Streaming checkpoints within a Delta table directory,   
  use a directory name such as _checkpoints.
- Data for change data feed is managed by Delta Lake in the _change_data directory and removed with VACUUM
- Bloom filter indexes use the _delta_index directory managed by Delta Lake. VACUUM cleans up files in this directory
- The ability to query table versions older than the retention period is lost after running VACUUM.
- Log files are deleted automatically and asynchronously after checkpoint operations and are not governed by VACUUM.
- While the default retention period of log files is 30 days, running VACUUM on a table removes the data files  
  necessary for time travel.
- When disk caching is enabled, a cluster might contain data from Parquet files that have been deleted with VACUUM.  
  Therefore, it may be possible to query the data of previous table versions whose files have been deleted.  
  Restarting the cluster will remove the cached data.

```
VACUUM eventsTable   -- vacuum files not required by versions older than the default retention period

VACUUM '/data/events' -- vacuum files in path-based table

VACUUM delta.`/data/events/`

VACUUM delta.`/data/events/` RETAIN 100 HOURS  -- vacuum files not required by versions more than 100 hours old

VACUUM eventsTable DRY RUN    -- do dry run to get the list of files to be deleted
-------------------------------------------------------------------------------------------
from delta.tables import DeltaTable

spark.conf.set('spark.databricks.delta.retentionDurationCheck.enabled',False)

table = DeltaTable.forPath(spark,'dbfs:/FileStore/delta_tables_performance/YellowTaxi')

table.vacuum(0)
```

# How frequently should you run vacuum?

Databricks recommends regularly running VACUUM on all tables to reduce excess cloud data storage costs.The default  
retention threshold for vacuum is 7 days. Setting a higher threshold gives you access to a greater history for your table,  
but increases the number of data files stored and, as a result, incurs greater storage costs from your cloud provider.

# Why can’t you vacuum a Delta table with a low retention threshold?

Delta Lake has a safety check to prevent you from running a dangerous VACUUM command. If you are certain that there  
are no operations being performed on this table that take longer than the retention interval you plan to specify,  
you can turn off this safety check by setting the Spark configuration property  
`spark.databricks.delta.retentionDurationCheck.enabled` to false.