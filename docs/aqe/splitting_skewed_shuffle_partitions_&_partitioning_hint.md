# Using Partitioning hints
Partitioning hints allow you to suggest a partitioning strategy that Databricks should follow.  
COALESCE, REPARTITION, and REPARTITION_BY_RANGE hints are supported and are equivalent to coalesce, repartition,  
and repartitionByRange Dataset APIs, respectively. These hints give you a way to tune performance and control the  
number of output files. When multiple partitioning hints are specified, multiple nodes are inserted into the logical plan,  
but the leftmost hint is picked by the optimizer.

- __Coalesce -__ Reduce the number of partitions to the specified number of partitions.  
 A partition number is the only parameter of the COALESCE hint.

- __Repartition -__ Repartition to the specified number of partitions by using the specified partitioning expressions.  
 The REPARTITION hint parameters are a partition number, column names, or both.

- __Repartition by range -__ Repartition to the specified number of partitions by using the specified partitioning expressions.  
 Column names is a required parameter for the REPARTITION_BY_RANGE hint, and a partition number is optional.

- __Rebalance -__ The REBALANCE hint can be used to rebalance the query result output partitions, so that every partition is of  
 a reasonable size (not too small and not too big). It can take column names as parameters, and try its best to partition the  
 query result by these columns. This is a best-effort: if there are skews, Spark will split the skewed partitions, to make these  
 partitions not too big. This hint is useful when you need to write the result of this query to a table, to avoid too small/big files.  
 This hint is ignored if AQE is not enabled.
 
  Below parameters work for same :  
  ##### spark.sql.adaptive.rebalancePartitionsSmallPartitionFactor	
  Default Value : 0.2    
  A partition will be merged during splitting if its size is smaller than this factor multiply spark.sql.adaptive.advisoryPartitionSizeInBytes.
  
  ##### spark.sql.adaptive.optimizeSkewsInRebalancePartitions.enabled	
  Default Value : true  
  When true and spark.sql.adaptive.enabled is true, Spark will optimize the skewed shuffle partitions in RebalancePartitions  
  and split them to smaller ones according to the target size (specified by spark.sql.adaptive.advisoryPartitionSizeInBytes),  
  to avoid data skew.

Examples : 
```
> SELECT /*+ COALESCE(3) */ * FROM t;

> SELECT /*+ REPARTITION(3) */ * FROM t;

> SELECT /*+ REPARTITION(c) */ * FROM t;

> SELECT /*+ REPARTITION(3, c) */ * FROM t;

> SELECT /*+ REPARTITION_BY_RANGE(c) */ * FROM t;

> SELECT /*+ REPARTITION_BY_RANGE(3, c) */ * FROM t;

> SELECT /*+ REBALANCE */ * FROM t;

> SELECT /*+ REBALANCE(c) */ * FROM t;
```