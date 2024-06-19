# Join Types
There are a variety of different join types available in Spark for you to use:
- __Inner joins__ - Keep rows with keys that exist in the left and right datasets
- __Outer joins__ - Keep rows with keys in either the left or right datasets
- __Left outer joins__ - Keep rows with keys in the left dataset
- __Right outer joins__ - Keep rows with keys in the right dataset
- __Left semi joins__ - Keep the rows in the left, and only the left, dataset where the key appears in the right dataset
- __Left anti joins__ - Keep the rows in the left, and only the left, dataset where they do not appear in the right dataset
- __Natural joins__ - Perform a join by implicitly matching the columns between the two datasets with the same names
- __Cross (or Cartesian) joins__ - Match every row in the left dataset with every row in the right dataset

# Broadcast Join
```
import org.apache.spark.sql.functions.broadcast
val joinExpr = person.col("graduate_program") === graduateProgram.col("id")
person.join(broadcast(graduateProgram), joinExpr)
-------------------------------------------------
large_df.join(small_df.hint("broadcast"), how=”left”, on=”id”)
-------------------------------------------------
In SQL MAPJOIN, BROADCAST, and BROADCASTJOIN all do the same thing and are all supported
SELECT /*+ MAPJOIN(graduateProgram) */ * FROM person JOIN graduateProgram
ON person.graduate_program = graduateProgram.id
```
#### Configuration Properties

- To enable or disable auto-broadcast join, set 
`spark.conf.set("spark.sql.autoBroadcastJoinThreshold", <size_in_bytes> or -1)`.

- Default Size Limit: The default threshold is set at 10MB, meaning tables smaller than this threshold are automatically broadcasted.
