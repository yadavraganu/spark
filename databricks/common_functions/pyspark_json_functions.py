# Databricks notebook source
# MAGIC %md ###pyspark.sql.functions.json_tuple(col, *fields)
# MAGIC - Parses a json string into data frame columns according to given fields

# COMMAND ----------

from pyspark.sql.functions import json_tuple
data = [("1", """{"f1": "value1", "f2": "value2"}"""), ("2", """{"f1": "value12"}""")]
df = spark.createDataFrame(data, ["key", "json_string"])
display(df)
df = df.select(df.key, json_tuple(df.json_string, 'f1', 'f2')).toDF(*['key', 'f1', 'f2'])
display(df)

# COMMAND ----------

# MAGIC %md ###pyspark.sql.functions.schema_of_json(json, options={})
# MAGIC - Parses a JSON string and infers its schema in DDL format.

# COMMAND ----------

from pyspark.sql.types import StringType
from pyspark.sql.functions import schema_of_json
data = [(1,"""{"f1": 11, "f2": "afaf"}""")]
df = spark.createDataFrame(data,["key","json_string"])
df = df.withColumn("json_schema_ddl",schema_of_json(df.first()[1]))
display(df)

# COMMAND ----------

# MAGIC %md ###pyspark.sql.functions.to_json(col, options={})
# MAGIC - Converts a column containing a StructType, ArrayType or a MapType into a JSON string. Throws an exception, in the case of an unsupported type.

# COMMAND ----------

from pyspark.sql import Row
from pyspark.sql.types import *
from pyspark.sql.functions import to_json
# Struct to json
data = [(1, Row(age=2, name='Alice'))]
df1 = spark.createDataFrame(data, ("key", "value"))
print(df1.select(to_json(df1.value).alias("json")).collect())
# Array of Struct to json
data = [(1, [Row(age=2, name='Alice'), Row(age=3, name='Bob')])]
df2 = spark.createDataFrame(data, ("key", "value"))
print(df2.select(to_json(df2.value).alias("json")).collect())
# Map to json
data = [(1, {"name": "Alice"})]
df3 = spark.createDataFrame(data, ("key", "value"))
print(df3.select(to_json(df3.value).alias("json")).collect())
# Array of map to json
data = [(1, [{"name": "Alice"}, {"name": "Bob"}])]
df4 = spark.createDataFrame(data, ("key", "value"))
print(df4.select(to_json(df4.value).alias("json")).collect())
# Array of String to json
data = [(1, ["Alice", "Bob"])]
df5 = spark.createDataFrame(data, ("key", "value"))
print(df5.select(to_json(df5.value).alias("json")).collect())

# COMMAND ----------

# MAGIC %md ###pyspark.sql.functions.get_json_object(col, path)
# MAGIC - Extracts json object from a json string based on json path specified, and returns json string of the extracted json object. It will return null if the input json string is invalid.

# COMMAND ----------

from pyspark.sql.functions import get_json_object
data = [("1", '''{"f1": "value1", "f2": "value2"}'''), ("2", '''{"f1": "value12"}''')]
df = spark.createDataFrame(data, ("key", "json_string"))
df.select(df.key, get_json_object(df.json_string, '$.f1').alias("c0"), \
                  get_json_object(df.json_string, '$.f2').alias("c1") ).collect()

# COMMAND ----------

# MAGIC %md ###pyspark.sql.functions.from_json(col, schema, options={})
# MAGIC - Parses a column containing a JSON string into a MapType with StringType as keys type, StructType or ArrayType with the specified schema. Returns null, in the case of an unparseable string

# COMMAND ----------

from pyspark.sql.types import *
from pyspark.sql.functions import from_json, schema_of_json, lit
data = [(1, '''{"a": 1}''')]
schema = StructType([StructField("a", IntegerType())])
df = spark.createDataFrame(data, ("key", "value"))
print(df.select(from_json(df.value, schema).alias("json")).collect())
print(df.select(from_json(df.value, "a INT").alias("json")).collect())
print(df.select(from_json(df.value, "MAP<STRING,INT>").alias("json")).collect())

data = [(1, '''[{"a": 1}]''')]
schema = ArrayType(StructType([StructField("a", IntegerType())]))
df = spark.createDataFrame(data, ("key", "value"))
print(df.select(from_json(df.value, schema).alias("json")).collect())
schema = schema_of_json(lit('''{"a": 0}'''))
print(df.select(from_json(df.value, schema).alias("json")).collect())

data = [(1, '''[1, 2, 3]''')]
schema = ArrayType(IntegerType())
df = spark.createDataFrame(data, ("key", "value"))
print(df.select(from_json(df.value, schema).alias("json")).collect())
