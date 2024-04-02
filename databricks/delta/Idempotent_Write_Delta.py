# Databricks notebook source
# MAGIC %md
# MAGIC ##Imports

# COMMAND ----------

from pyspark.sql.types import StructType,StructField,IntegerType,StringType
workdir = 'dbfs:/Filestore/test/'
dbutils.fs.rm(workdir,True)
target_path = f"{workdir}/target"

# COMMAND ----------

# MAGIC %md
# MAGIC ## Data Prep

# COMMAND ----------

data = [(1,'X'),(2,'Y'),(3,'Z')]
schema = StructType([StructField('Id',IntegerType()),StructField('Name',StringType())])
df = spark.createDataFrame(data,schema)
display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Write data with 
# MAGIC - AppId = Idempotent_App
# MAGIC - Version = 1  
# MAGIC Data will be written successfully

# COMMAND ----------

txnVersion='1'
txnAppId='Idempotent_App'
df.write.format("delta").mode("append").option("txnVersion", txnVersion).option(
    "txnAppId", txnAppId
).save(target_path)
dbutils.fs.ls(target_path)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Write data with 
# MAGIC - AppId = Idempotent_App
# MAGIC - Version = 1  
# MAGIC Data write will be skipped since AppId & Version are same  successfully

# COMMAND ----------

txnVersion='1'
txnAppId='Idempotent_App'
df.write.format("delta").mode("append").option("txnVersion", txnVersion).option(
    "txnAppId", txnAppId
).save(target_path)
dbutils.fs.ls(target_path)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Write data with 
# MAGIC - AppId = Idempotent_App
# MAGIC - Version = 2  
# MAGIC Data write will be written since Version is 2 greater than previous version

# COMMAND ----------

txnVersion='2'
txnAppId='Idempotent_App'
df.write.format("delta").mode("append").option("txnVersion", txnVersion).option(
    "txnAppId", txnAppId
).save(target_path)
dbutils.fs.ls(target_path)

# COMMAND ----------

display(spark.read.format('delta').load(target_path))

# COMMAND ----------

display(spark.sql(f"DESCRIBE HISTORY delta.`{target_path}`"))
