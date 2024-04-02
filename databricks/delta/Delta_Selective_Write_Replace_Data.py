# Databricks notebook source
# MAGIC %md
# MAGIC ### Imports

# COMMAND ----------

from pyspark.sql.types import StructField,StructType,IntegerType,StringType
from pyspark.sql.functions import lit

# COMMAND ----------

# MAGIC %md
# MAGIC ### Creating test dataframe & writing partition by Id

# COMMAND ----------

data = [(1,'X'),(2,'Y'),(2,'sadasdasdas'),(3,'Z')]
target = 'dbfs:/Filestore/test_replace'
schema = StructType([StructField('Id',IntegerType()),StructField('Name',StringType())])
df = spark.createDataFrame(data,schema)
df.write.format('delta').partitionBy('Id').mode("overwrite").save(target)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Verify data & file structure

# COMMAND ----------

display(spark.read.load(target))
dbutils.fs.ls(target)

# COMMAND ----------

# MAGIC  %md
# MAGIC ### Using replace where .Dataframe which is being used to write ,should have rows satisfying condition defined in replacewhere clause

# COMMAND ----------

replace_where_df = spark.read.load(target).filter("Id==1 OR Id==3").withColumn('Name',lit('replace_where'))
replace_where_df.write.format("delta").option("replaceWhere", "Id==1 OR Id==3").mode("overwrite").save(target)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Verify data after replace where option

# COMMAND ----------

display(spark.read.load(target))
dbutils.fs.ls(target)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Writing data to only replace ID=2 partition

# COMMAND ----------

data = [(2,'Ydfasf')]
target = 'dbfs:/Filestore/test_replace'
schema = StructType([StructField('Id',IntegerType()),StructField('Name',StringType())])
df = spark.createDataFrame(data,schema)
df.write.format('delta').mode("overwrite").partitionBy('Id').option("partitionOverwriteMode", "dynamic").save(target)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Verify data & file structure after replacing partition dynamically

# COMMAND ----------

display(spark.read.load(target))
dbutils.fs.ls(target)

# COMMAND ----------

# MAGIC %md 
# MAGIC ### Cleanup

# COMMAND ----------

dbutils.fs.rm(target,True)
