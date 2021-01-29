#!/usr/bin/env python
# coding: utf-8

# In[2]:


import findspark,os
findspark.init()


# In[3]:


from pyspark.sql import SparkSession
from pyspark.sql.functions import input_file_name
spark=SparkSession.builder.appName('Read_Write_Json_Spark').getOrCreate()


# In[4]:


def getFilePath(File):
    cwd=os.getcwd()
    filepath=os.path.join(cwd,'data',File)
    return filepath


# In[5]:


df=spark.read.format('json').option('inferSchema',True).load(getFilePath('*-summary.json'))


# In[10]:


df1=df.withColumn('FILE_NAME',input_file_name()).coalesce(1)


# In[11]:


df1.write.format('json').mode('overwrite').option('path',getFilePath('JsonResult')).save()

