# Databricks notebook source
from pyspark.sql.functions import collect_list
data = [("a", "aa", 1), ("a", "aa", 2), ("b", "bb", 5), ("b", "bb", 3), ("b", "bb", 4)]
df = spark.createDataFrame(data).toDF("col1", "col2", "col3")
display(df)
df = df.groupBy('col1','col2').agg(collect_list('col3').alias('col3'))
display(df)
