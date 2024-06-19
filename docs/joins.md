# Broadcast Join


```
import org.apache.spark.sql.functions.broadcast
val joinExpr = person.col("graduate_program") === graduateProgram.col("id")
person.join(broadcast(graduateProgram), joinExpr)
```
```
large_df.join(small_df.hint("broadcast"), how=”left”, on=”id”)
```
```
-- In SQL MAPJOIN, BROADCAST, and BROADCASTJOIN all do the same thing and are all supported
SELECT /*+ MAPJOIN(graduateProgram) */ * FROM person JOIN graduateProgram
ON person.graduate_program = graduateProgram.id

```
