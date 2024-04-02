# Databricks notebook source
from pyspark.sql.functions import (
    collect_list,
    array_contains,
    array_distinct,
    array_except,
    array_intersect,
    array_join,
    array_min,
    array_max,array_position,array_remove,array_repeat,array_sort,array_union,arrays_overlap,arrays_zip
)

# COMMAND ----------

data = [
    ("x", 4, 1),
    ("x", 6, 2),
    ("z", 7, 3),
    ("a", 3, 4),
    ("z", 5, 2),
    ("x", 7, 3),
    ("x", 9, 7),
    ("z", 1, 8),
    ("z", 4, 9),
    ("z", 7, 4),
    ("a", 8, 5),
    ("a", 5, 2),
    ("a", 3, 8),
    ("x", 2, 7),
    ("z", 1, 9),
]
df = spark.createDataFrame(data,["col1", "col2", "col3"])
df = df.groupBy("col1").agg(collect_list("col2").alias("array_col1"),collect_list("col3").alias("array_col2"))

# COMMAND ----------

# MAGIC %md ### array_contains
# MAGIC - If we need to find a particular element is present in array, we can use array_contains function. This function returns true if the value is present in array and false otherwise

# COMMAND ----------

df = df.withColumn("result", array_contains("array_col2", 3))
display(df)

# COMMAND ----------

# MAGIC %md ###array_distinct
# MAGIC - This function returns only distinct values from an array and removes duplicate values.

# COMMAND ----------

df = df.withColumn("result", array_distinct("array_col2"))
display(df)

# COMMAND ----------

# MAGIC %md ###array_except
# MAGIC - This function returns the elements from first array which are not present in second array. 

# COMMAND ----------

df = df.withColumn("result", array_except("array_col1", "array_col2"))
display(df)

# COMMAND ----------

# MAGIC %md ###array_intersect
# MAGIC - This function returns common elements from both arrays.

# COMMAND ----------

df = df.withColumn("result", array_intersect("array_col1", "array_col2"))
display(df)

# COMMAND ----------

# MAGIC %md ###array_join
# MAGIC - This Function joins all the array elements based on delimiter defined as the second argument.
# MAGIC - if there are any null values then we can replace with third argument (nullReplacement) with any string value.

# COMMAND ----------

df = df.withColumn("result", array_join("array_col2", "_"))
display(df)

# COMMAND ----------

# MAGIC %md ###array_max
# MAGIC - This function returns the maximum value from an array.

# COMMAND ----------

df = df.withColumn("result", array_max("array_col2"))
display(df)

# COMMAND ----------

# MAGIC %md ###array_min
# MAGIC - This function returns the minimum value from an array.

# COMMAND ----------

df = df.withColumn("result", array_min("array_col2"))
display(df)

# COMMAND ----------

# MAGIC %md ###array_position
# MAGIC - This function returns the position of first occurrence of a specified element. If the element is not present it returns 0

# COMMAND ----------

df = df.withColumn("result", array_position("array_col2", 7))
display(df)

# COMMAND ----------

# MAGIC %md ###array_remove
# MAGIC - This function removes all the occurrences of an element from an array.

# COMMAND ----------

df = df.withColumn("result", array_remove("array_col2", 9))
display(df)

# COMMAND ----------

# MAGIC %md ###array_repeat
# MAGIC - This function creates an array that is repeated as specified by second argument.

# COMMAND ----------

df = df.withColumn("result", array_repeat("array_col2", 2))
display(df)

# COMMAND ----------

# MAGIC %md ###array_sort
# MAGIC - This function sorts the elements of an array in ascending order.

# COMMAND ----------

df = df.withColumn("result", array_sort("array_col2"))
display(df)

# COMMAND ----------

# MAGIC %md ###array_union
# MAGIC - This function returns the union of all elements from the input arrays.

# COMMAND ----------

df = df.withColumn("result", array_union("array_col1", "array_col2"))
display(df)

# COMMAND ----------

# MAGIC %md ###arrays_overlap
# MAGIC - This function checks if at least one element is common/overlapping in arrays. It returns true if at least one element is common in both array and false otherwise. It returns null if at least one of the arrays is null.

# COMMAND ----------

df = df.withColumn("result", arrays_overlap("array_col1", "array_col2"))
df.show()

# COMMAND ----------

# MAGIC %md ###arrays_zip
# MAGIC - This function merges the i-th element of an array and returns array<struct>.

# COMMAND ----------

df = df.withColumn("result", arrays_zip("array_col1", "array_col2"))
df.show()

# COMMAND ----------


