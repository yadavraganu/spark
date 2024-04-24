# Databricks notebook source
data = [
    (1, "A", 1000, "IT"),
    (2, "B", 1500, "IT"),
    (3, "C", 2500, "IT"),
    (4, "D", 3000, "HR"),
    (5, "E", 2000, "HR"),
    (6, "F", 1000, "HR"),
    (7, "G", 4000, "Sales"),
    (8, "H", 4000, "Sales"),
    (9, "I", 1000, "Sales"),
    (10, "J", 2000, "Sales"),
]
df = spark.createDataFrame(data).toDF('Id','Name','Salary','Dept')
display(df)

# COMMAND ----------

from pyspark.sql import Window
from pyspark.sql.functions import col,dense_rank

wdw = Window.partitionBy('Dept').orderBy(col('Salary').desc())
df = df.withColumn('Rank',dense_rank().over(wdw)).filter("Rank = 1").drop('Rank')
display(df)
