from pyspark.sql.session import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType
from pyspark.sql.functions import json_tuple, schema_of_json
import sys
sys.path.append('..')
from config.config_parse import get_config

# Spark Session
spark = SparkSession.builder.master("local[3]").appName('json_function').getOrCreate()

print('=' * 150)
print('Parsing a json string into data frame columns according to given fields')
data = [(1, "{'f1': 'value1', 'f2': 'value2'}"), (2, "{'f1': 'value12'}")]
df = spark.createDataFrame(data, ["key", "json_string"])
df.show(truncate=False)
df = df.select(df.key, json_tuple(df.json_string, 'f1', 'f2')).toDF(*['key', 'f1', 'f2'])
df.show(truncate=False)
print('=' * 150)

print('=' * 150)
print('Parses a JSON string and infers its schema in DDL format.')
data = [(1, "{'f1': 11, 'f2': 'afaf'}")]
df = spark.createDataFrame(data, ["key", "json_string"])
df = df.withColumn("json_schema_ddl", schema_of_json(df.first()[1]))
df.show(truncate=False)
print('=' * 150)
