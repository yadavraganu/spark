## Converting sort-merge join to shuffled hash join
AQE converts sort-merge join to shuffled hash join when all post-shuffle partitions are smaller than a threshold,  
the max threshold can see the config spark.sql.adaptive.maxShuffledHashJoinLocalMapThreshold.

### spark.sql.adaptive.maxShuffledHashJoinLocalMapThreshold	
Default Value: 0	
Configures the maximum size in bytes per partition that can be allowed to build a local hash map. If this value is not  
smaller than spark.sql.adaptive.advisoryPartitionSizeInBytes and all the partition sizes are not larger than this config,  
join selection prefers to use shuffled hash join instead of sort merge join regardless of the value of  
spark.sql.join.preferSortMergeJoin.