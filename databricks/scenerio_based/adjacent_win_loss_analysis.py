# Databricks notebook source
from pyspark.sql.functions import row_number,to_date,col,abs,min ,max
from pyspark.sql import Window
from pyspark.sql.types import DateType

# COMMAND ----------

data = [("01-06-2020","Won"),("02-06-2020","Won"),("03-06-2020","Won"),("04-06-2020","Loss"),("05-06-2020","Loss"),("06-06-2020","Loss"),("07-06-2020","Won")]
df = spark.createDataFrame(data).toDF('Date','Status').withColumn('Date',to_date('Date','dd-MM-yyyy'))
display(df)

# COMMAND ----------

wdw1 = Window.orderBy(col('Date').asc())
wdw2 = Window.partitionBy('Status').orderBy(col('Date').asc())
df = df.withColumn("OverAllRank",row_number().over(wdw1)).withColumn("WithInGroupRank",row_number().over(wdw2)).withColumn("SeqGroups",abs(col('WithInGroupRank')-col('OverAllRank')))
df = df.groupBy('Status','SeqGroups').agg(min('Date').alias('StartDate'),max('Date').alias('EndDate')).drop('SeqGroups')
display(df)
