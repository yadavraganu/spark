# Databricks notebook source
# MAGIC %md 
# MAGIC #### Drop database if it exists along with child object using CASCADE option & create new database

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP DATABASE IF EXISTS schema_evol CASCADE;
# MAGIC CREATE DATABASE schema_evol;

# COMMAND ----------

# MAGIC %md 
# MAGIC #### Create or replace table & insert data

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE schema_evol.managed_emp (
# MAGIC   Id Integer,
# MAGIC   Name String,
# MAGIC   Salary Double
# MAGIC ) USING DELTA;
# MAGIC INSERT INTO schema_evol.managed_emp values(1, 'X', 1000);
# MAGIC SELECT * FROM schema_evol.managed_emp;

# COMMAND ----------

# MAGIC %md 
# MAGIC #### Add columns in table.We can define comment & column order as well

# COMMAND ----------

# MAGIC %sql
# MAGIC ALTER TABLE schema_evol.managed_emp ADD COLUMNS (Dept String);
# MAGIC ALTER TABLE schema_evol.managed_emp ADD COLUMNS (Dept_Name String FIRST,Hr_Name String AFTER Name);
# MAGIC SELECT * FROM schema_evol.managed_emp;

# COMMAND ----------

# MAGIC %md 
# MAGIC #### Alter existing column to change comment or column position

# COMMAND ----------

# MAGIC %sql
# MAGIC ALTER TABLE schema_evol.managed_emp ALTER COLUMN Dept_Name COMMENT 'Department Name';
# MAGIC ALTER TABLE schema_evol.managed_emp ALTER COLUMN Dept_Name AFTER Dept;
# MAGIC SELECT * FROM schema_evol.managed_emp;

# COMMAND ----------

# MAGIC %md 
# MAGIC #### Completely change/replace the column order for this columns should be existing columns only 

# COMMAND ----------

# MAGIC %sql
# MAGIC ALTER TABLE schema_evol.managed_emp REPLACE COLUMNS (Id integer,Dept string,Dept_Name string,Name string,Hr_Name string,Salary double);
# MAGIC SELECT * FROM schema_evol.managed_emp;

# COMMAND ----------

# MAGIC %md 
# MAGIC #### Renaming columns which requires few table properties to be set first

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE EXTENDED schema_evol.managed_emp;
# MAGIC ALTER TABLE
# MAGIC   schema_evol.managed_emp
# MAGIC SET
# MAGIC   TBLPROPERTIES (
# MAGIC     'delta.minReaderVersion' = '2',
# MAGIC     'delta.minWriterVersion' = '5',
# MAGIC     'delta.columnMapping.mode' = 'name'
# MAGIC   );
# MAGIC ALTER TABLE schema_evol.managed_emp RENAME COLUMN Dept to Department;
# MAGIC SELECT * FROM schema_evol.managed_emp;

# COMMAND ----------

# MAGIC %md
# MAGIC #### By default, overwriting the data in a table does not overwrite the schema. When overwriting a table using mode("overwrite") without replaceWhere, you may still want to overwrite the schema of the data being written. You replace the schema and partitioning of the table by setting the overwriteSchema option to true:

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT OVERWRITE TABLE schema_evol.managed_emp VALUES(1, 'X', 1000)

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT OVERWRITE TABLE schema_evol.managed_emp VALUES(1,NULL,NULL,'X','Y',1000);
# MAGIC SELECT * FROM schema_evol.managed_emp;
