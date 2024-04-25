# Databricks notebook source
from pyspark.sql.functions import explode
data = [
    ({"dept_id": 101, "emp_id": [10101, 10102, 10103]}),
    ({"dept_id": 102, "emp_id": [10201, 10202]}),
]
df = spark.createDataFrame(data)
display(df)
df = df.withColumn('emp_id',explode('emp_id'))
display(df)
