### Broadcasting
A join() is a common operation in which two data sets are combined based on one or more common keys.
Rows from two different data sets can be merged into a single data set by matching values in the specified columns.
Because data shuffling across multiple nodes is required, a join() can be a costly operation in terms of network latency.  

In scenarios in which a small data set is being joined with a larger data set, Spark offers an optimization technique called broadcasting.
If one of the data sets is small enough to fit into the memory of each worker node, it can be sent to all nodes, reducing the need for costly shuffle operations.
The join() operation simply happens locally on each node.   

In the following example, the small DataFrame df2 is broadcast across all of the worker nodes, and the join() operation with the large DataFrame df1 is performed locally on each node:  

```
from pyspark.sql.functions import broadcast
df1.join(broadcast(df2), 'id')
```
df2 must be small enough to fit into the memory of each worker node; a DataFrame that is too large will cause out-of-memory errors.  

#### Configuration Properties

- To enable or disable auto-broadcast join, set 
`spark.conf.set("spark.sql.autoBroadcastJoinThreshold", <size_in_bytes> or -1)`.

- Default Size Limit: The default threshold is set at 10MB, meaning tables smaller than this threshold are automatically broadcasted.