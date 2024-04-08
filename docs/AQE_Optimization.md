# Adaptive Query Execution
Adaptive Query Execution (AQE) is an optimization technique in Spark SQL that makes use of the runtime statistics to choose the most efficient query execution plan, which is enabled by default since Apache Spark 3.2.0.  
Spark SQL can turn on and off AQE by `spark.sql.adaptive.enabled` as an umbrella configuration.  
As of Spark 3.0, there are three major features in AQE: including  
- Coalescing post-shuffle partitions
- Converting sort-merge join to broadcast join
- Skew join optimization

## Coalescing post-shuffle partitions
### spark.sql.adaptive.advisoryPartitionSizeInBytes:
Default Value : 64 MB  
The advisory size in bytes of the shuffle partition during adaptive optimization (when spark.sql.adaptive.enabled is true).  
It takes effect when Spark coalesces small shuffle partitions or splits skewed shuffle partition.

### spark.sql.adaptive.coalescePartitions.initialPartitionNum	
Default Value : none  
The initial number of shuffle partitions before coalescing.If not set,it equals to spark.sql.shuffle.partitions.  
This configuration only has an effect when spark.sql.adaptive.enabled and spark.sql.adaptive.coalescePartitions.enabled are both enabled.

### spark.sql.adaptive.coalescePartitions.minPartitionSize	
Default Value : 1MB  
The minimum size of shuffle partitions after coalescing.  
Its value can be at most 20% of spark.sql.adaptive.advisoryPartitionSizeInBytes.  
This is useful when the target size is ignored during partition coalescing, which is the default case.

### spark.sql.adaptive.coalescePartitions.minPartitionNum
Default value: 2x no. of cluster cores
The minimum number of partitions after coalescing. Not recommended, because setting explicitly overrides spark.sql.adaptive.coalescePartitions.minPartitionSize.

### spark.sql.adaptive.coalescePartitions.parallelismFirst	
Default Value : true  
When true, Spark ignores the target size specified by spark.sql.adaptive.advisoryPartitionSizeInBytes (default 64MB) when coalescing contiguous shuffle partitions  
and only respect the minimum partition size specified by spark.sql.adaptive.coalescePartitions.minPartitionSize (default 1MB),  
to maximize the parallelism. This is to avoid performance regression when enabling adaptive query execution.  
It's recommended to set this config to false and respect the target size specified by spark.sql.adaptive.advisoryPartitionSizeInBytes.

### spark.sql.adaptive.coalescePartitions.enabled
Default Value : true  
When true and spark.sql.adaptive.enabled is true, Spark will coalesce contiguous shuffle partitions according to the target size  
(specified by spark.sql.adaptive.advisoryPartitionSizeInBytes), to avoid too many small tasks.

## Spliting skewed shuffle partitions 

### spark.sql.adaptive.rebalancePartitionsSmallPartitionFactor	
Default Value : 0.2  
A partition will be merged during splitting if its size is smaller than this factor multiply spark.sql.adaptive.advisoryPartitionSizeInBytes.

### spark.sql.adaptive.optimizeSkewsInRebalancePartitions.enabled	
Default Value : true	
When true and spark.sql.adaptive.enabled is true, Spark will optimize the skewed shuffle partitions in RebalancePartitions  
and split them to smaller ones according to the target size (specified by spark.sql.adaptive.advisoryPartitionSizeInBytes),  
to avoid data skew.

## Converting sort-merge join to broadcast join
AQE converts sort-merge join to broadcast hash join when the runtime statistics of any join side is smaller than the adaptive broadcast hash join threshold.  
This is not as efficient as planning a broadcast hash join in the first place, but it’s better than keep doing the sort-merge join, as we can save the sorting of both the join sides, and read shuffle files locally to save network traffic(if spark.sql.adaptive.localShuffleReader.enabled is true)  

### spark.sql.adaptive.autoBroadcastJoinThreshold
Default Value: none	
Configures the maximum size in bytes for a table that will be broadcast to all worker nodes when performing a join.  
By setting this value to -1, broadcasting can be disabled. The default value is the same as spark.sql.autoBroadcastJoinThreshold. Note that,  
this config is used only in adaptive framework.

### spark.sql.adaptive.localShuffleReader.enabled
Default Value : true  
When true and spark.sql.adaptive.enabled is true, Spark tries to use local shuffle reader to read the shuffle data when the shuffle partitioning is not needed.  
For example, after converting sort-merge join to broadcast-hash join.

## Converting sort-merge join to shuffled hash join
AQE converts sort-merge join to shuffled hash join when all post shuffle partitions are smaller than a threshold,  
the max threshold can see the config spark.sql.adaptive.maxShuffledHashJoinLocalMapThreshold.

### spark.sql.adaptive.maxShuffledHashJoinLocalMapThreshold	
Default Value : 0	
Configures the maximum size in bytes per partition that can be allowed to build local hash map. If this value is not smaller than spark.sql.adaptive.advisoryPartitionSizeInBytes and all the partition sizes are not larger than this config,  
join selection prefers to use shuffled hash join instead of sort merge join regardless of the value of spark.sql.join.preferSortMergeJoin.