# Databricks notebook source
# MAGIC %md
# MAGIC #Cleanup

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP DATABASE IF EXISTS cdc_db CASCADE;
# MAGIC CREATE DATABASE cdc_db;

# COMMAND ----------

# MAGIC %md
# MAGIC #Managed Tables

# COMMAND ----------

spark.sql(
    """CREATE OR REPLACE TABLE cdc_db.managed_emp ( Id Integer,
          Name String,
          Salary Double
) USING DELTA
TBLPROPERTIES (delta.enableChangeDataFeed = true)"""
)
spark.sql("INSERT INTO cdc_db.managed_emp VALUES (1,'John',10008)")
display(spark.sql("DESCRIBE EXTENDED cdc_db.managed_emp"))
display(dbutils.fs.ls('dbfs:/user/hive/warehouse/cdc_db.db/managed_emp'))

# COMMAND ----------

# MAGIC %md
# MAGIC #Unmanaged Tables

# COMMAND ----------

spark.sql(
    """CREATE OR REPLACE TABLE cdc_db.unmanaged_emp ( Id Integer,
          Name String,
          Salary Double
) USING DELTA
LOCATION 'dbfs:/user/hive/warehouse/cdc_db.db/unmanaged_emp'"""
)
spark.sql("INSERT INTO cdc_db.unmanaged_emp VALUES (1,'Rock',10008)")
display(spark.sql("DESCRIBE EXTENDED cdc_db.unmanaged_emp"))
display(dbutils.fs.ls('dbfs:/user/hive/warehouse/cdc_db.db/unmanaged_emp'))

# COMMAND ----------

# MAGIC %md 
# MAGIC #Quering CDC Changes

# COMMAND ----------

spark.sql("INSERT INTO cdc_db.managed_emp VALUES (2,'Doe',10008)")
spark.sql(
    """MERGE INTO cdc_db.managed_emp as t USING cdc_db.unmanaged_emp as s on s.id=t.id
           WHEN MATCHED THEN
           UPDATE SET t.name =s.name"""
)

# COMMAND ----------

# MAGIC %md
# MAGIC # Checking Tables Versions

# COMMAND ----------

display(spark.sql("DESCRIBE HISTORY cdc_db.managed_emp"))
display(dbutils.fs.ls('dbfs:/user/hive/warehouse/managed_emp'))

# COMMAND ----------

# MAGIC %md
# MAGIC # Checking CDC data

# COMMAND ----------

display(spark.sql("SELECT * FROM cdc_db.managed_emp"))
display(spark.sql("SELECT * FROM table_changes('cdc_db.managed_emp', 0 , 4)"))
