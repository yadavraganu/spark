# Databricks notebook source
# MAGIC %md Q2. Find missing number

# COMMAND ----------

from pyspark.sql import Row
from pyspark.sql.types import StructType, StructField, IntegerType

data = [Row(1), Row(4), Row(3)]
schema = StructType([StructField("Value", IntegerType(), True)])
df_1 = spark.createDataFrame(data, schema)
df_2 = spark.range(0, 5).toDF('Value')

missing_number = df_2.join(df_1, df_2.Value == df_1.Value, how='left_anti')
display(df_1)
display(df_2)
display(missing_number)
