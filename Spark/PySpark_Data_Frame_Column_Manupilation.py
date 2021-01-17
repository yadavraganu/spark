#!/usr/bin/env python
# coding: utf-8

# In[71]:


#Required Imports
from pyspark.sql import SparkSession
import os
from pyspark.sql.functions import *
from pyspark.sql.types import IntegerType


# In[72]:


# create Spark Session
spark = SparkSession.builder.appName('Column_Manupilation').getOrCreate()


# In[73]:


# Function to laod data & return data  frame
def load_data(file):
    current_dir=os.getcwd()
    full_path=os.path.join(current_dir,'data',file)
    data=spark.read.format('csv').load(full_path,inferSchema=True,header=True)
    return data
data=load_data('netflix_titles.csv')


# In[74]:


# Renaming title to TITLE ,adding a Upper Type column which have Upper case of type & printing the updated schema
data.withColumnRenamed('title','TITLE').withColumn('Upper Type',upper(col('type'))).printSchema()


# In[75]:


# Reverting the add column,rename changes 
data.withColumnRenamed('title','TITLE').withColumn('Upper Type',upper(col('type'))).drop('Upper Type').withColumnRenamed('TITLE','title').printSchema()


# In[76]:


# adding a Constant columns to the dataframe
data.withColumn('Constant',lit(7.89)).select('title','Type','Constant').show()


# In[77]:


# casting Constant column to integer
data.withColumn('Constant',lit(7.89).cast(IntegerType())).select('title','Type','Constant').show()


# In[ ]:




