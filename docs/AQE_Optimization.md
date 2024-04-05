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