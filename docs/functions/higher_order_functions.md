### pyspark.sql.functions.transform
Returns an array of elements after applying a transformation to each element in the input array
```commandline
df = spark.createDataFrame([(1, [1, 2, 3, 4])], ("key", "values"))
df.select(transform("values", lambda x: x * 2).alias("doubled")).show()
+------------+
|     doubled|
+------------+
|[2, 4, 6, 8]|
+------------+
```
### pyspark.sql.functions.filter
Returns an array of elements for which a predicate holds in a given array
```commandline
df = spark.createDataFrame([(1, ["2018-09-20",  "2019-02-03", "2019-07-01", "2020-06-01"])],("key", "values"))

def after_second_quarter(x):
    return month(to_date(x)) > 6
    
df.select(filter("values", after_second_quarter).alias("after_second_quarter")).show(truncate=False)
+------------------------+
|after_second_quarter    |
+------------------------+
|[2018-09-20, 2019-07-01]|
+------------------------+
```
### pyspark.sql.functions.exists
Returns whether a predicate holds for one or more elements in the array
```commandline
df = spark.createDataFrame([(1, [1, 2, 3, 4]), (2, [3, -1, 0])],("key", "values"))
df.select(exists("values", lambda x: x < 0).alias("any_negative")).show()
+------------+
|any_negative|
+------------+
|       false|
|        true|
+------------+
```
### pyspark.sql.functions.reduce
Applies a binary operator to an initial state and all elements in the array, and reduces this to a single state.  
The final state is converted into the final result by applying a finish function.
```commandline
df = spark.createDataFrame([(1, [20.0, 4.0, 2.0, 6.0, 10.0])], ("id", "values"))
df.select(reduce("values", lit(0.0), lambda acc, x: acc + x).alias("sum")).show()
+----+
| sum|
+----+
|42.0|
+----+

def merge(acc, x):
    count = acc.count + 1
    sum = acc.sum + x
    return struct(count.alias("count"), sum.alias("sum"))

df.select(
    reduce(
        "values",
        struct(lit(0).alias("count"), lit(0.0).alias("sum")),
        merge,
        lambda acc: acc.sum / acc.count,
    ).alias("mean")
).show()
+----+
|mean|
+----+
| 8.4|
+----+
```