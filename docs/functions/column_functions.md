### pyspark.sql.Column.alias
Returns this column aliased with a new name.
```commandline
df = spark.createDataFrame([(2, "Alice"), (5, "Bob")], ["age", "name"])
df.select(df.age.alias("age2")).collect()
df.select(df.age.alias("age3", metadata={'max': 99})).schema['age3'].metadata['max']
```
### pyspark.sql.Column.cast
Cast the column into type dataType  
Alias: pyspark.sql.Column.astype
```
from pyspark.sql.types import StringType
df = spark.createDataFrame([(2, "Alice"), (5, "Bob")], ["age", "name"])
df.select(df.age.cast("string").alias('ages')).collect()
df.select(df.age.cast(StringType()).alias('ages')).collect()
```
### pyspark.sql.Column.between
True if the current column is between the lower bound and upper bound, inclusive.
```commandline
df = spark.createDataFrame([(2, "Alice"), (5, "Bob")], ["age", "name"])
df.select(df.name, df.age.between(2, 4)).show()
+-----+---------------------------+
| name|((age >= 2) AND (age <= 4))|
+-----+---------------------------+
|Alice|                       true|
|  Bob|                      false|
+-----+---------------------------+
```