# Databricks notebook source
# MAGIC %md Q1. Split string column with multiple delimiters

# COMMAND ----------

from pyspark.sql.functions import split
from pyspark.sql import Row
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql import SparkSession

spark = SparkSession.builder.master("spark://172.20.0.2:7077").appName('Test').getOrCreate()
data = [Row("1,Alice\t30|New York")]
schema = StructType([StructField("Value", StringType(), True)])
df = spark.createDataFrame(data, schema)
df = df.withColumn("Split_Array", split(df.Value, ",|\t|\|"))
df = (
    df.withColumn("Id", df.Split_Array.getItem(0))
    .withColumn("Name", df.Split_Array.getItem(1))
    .withColumn("Age", df.Split_Array.getItem(2))
    .withColumn("City", df.Split_Array.getItem(3))
)
df = df.select("Value", "Id", "Name", "Age", "City")
df.show()
