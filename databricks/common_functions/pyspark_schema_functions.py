# Databricks notebook source
# MAGIC %md ### Importing

# COMMAND ----------

from pyspark.sql import Row
from pyspark.sql.types import StringType, IntegerType, StructType, StructField ,ArrayType, MapType
from pyspark.sql.functions import to_json
import pyspark.sql.types as T

# COMMAND ----------

# MAGIC %md ### Adding data & schema with Struct as well as DDL string

# COMMAND ----------

data = [
    Row("James", "", "Smith", "36636", "M", 3000),
    Row("Michael", "Rose", "", "40288", "M", 4000),
    Row("Robert", "", "Williams", "42114", "M", 4000),
    Row("Maria", "Anne", "Jones", "39192", "F", 4000),
    Row("Jen", "Mary", "Brown", "", "F", -1),
]
schema = StructType(
    [
        StructField("First Name", StringType(), False),
        StructField("Middle Name", StringType(), True),
        StructField("Last Name", StringType(), True),
        StructField("Id", StringType(), False),
        StructField("Gender", StringType(), False),
        StructField("Salary", IntegerType(), False),
    ]
)
ddl_schema = '`First Name` STRING NOT NULL,`Middle Name` STRING,`Last Name` STRING,Id STRING NOT NULL,Gender STRING NOT NULL,Salary INT NOT NULL'
df=spark.createDataFrame(data,ddl_schema)

# COMMAND ----------

# MAGIC %md #### Printing Schema

# COMMAND ----------

df.schema
df.printSchema()

# COMMAND ----------

# MAGIC %md ### Adding data with Neseted data structures & schema with Struct as well as DDL string

# COMMAND ----------

data = [
    Row(Row("James", "", "Smith"),["Cricket", "Movies"],{"hair": "black", "eye": "brown"}),
    Row(Row("Michael", "Rose", ""), ["Tennis"], {"hair": "brown", "eye": "black"}),
    Row(Row("Robert", "", "Williams"),["Cooking", "Football"],{"hair": "red", "eye": "gray"}),
    Row(Row("Maria", "Anne", "Jones"), None, {"hair": "blond", "eye": "red"}),
    Row(Row("Jen", "Mary", "Brown"), ["Blogging"], {"white": "black", "eye": "black"}),
]
schema = schema = StructType(
    [
        StructField(
            "Name",
            StructType(
                [
                    StructField("First Name", StringType(), False),
                    StructField("Middle Name", StringType(), True),
                    StructField("Last Name", StringType(), True),
                ]
            ),
            False,
        ),
        StructField("Hobbies", ArrayType(StringType()), True),
        StructField("Properties", MapType(StringType(), StringType()), False),
    ]
)
ddl_schema = 'Name STRUCT<`First Name`: STRING, `Middle Name`: STRING, `Last Name`: STRING> NOT NULL,Hobbies ARRAY<STRING>,Properties MAP<STRING, STRING> NOT NULL'
df=spark.createDataFrame(data,schema)

# COMMAND ----------

# MAGIC %md #### Print schema

# COMMAND ----------

df.schema
df.printSchema()

# COMMAND ----------

# MAGIC %md ### Getting schema string from struct type schema

# COMMAND ----------

df._jdf.schema().toDDL()

# COMMAND ----------

# MAGIC %md ### Getting struct schema from DDL string

# COMMAND ----------

ddlString = '`First Name` STRING NOT NULL,`Middle Name` STRING,`Last Name` STRING,Id STRING NOT NULL,Gender STRING NOT NULL,Salary INT NOT NULL'
print(T._parse_datatype_string(ddlString))
