#!/usr/bin/env python
# coding: utf-8

# In[36]:


import findspark,os
findspark.init()


# In[37]:


from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import StringType,DateType,StructType,StructField


# In[38]:


spark=SparkSession.builder.appName('Read_Write_Csv').getOrCreate()


# In[39]:


def getFilepath(filename):
    currdir=os.getcwd()
    fullpath=os.path.join(currdir,'data',filename)
    return fullpath
schema=StructType([StructField('show_id',StringType(),True),
StructField('type',StringType(),True),
StructField('title',StringType(),True),
StructField('director',StringType(),True),
StructField('cast',StringType(),True),
StructField('country',StringType(),True),
StructField('date_added',StringType(),True),
StructField('release_year',StringType(),True),
StructField('rating',StringType(),True),
StructField('duration',StringType(),True),
StructField('listed_in',StringType(),True),
StructField('description',StringType(),True)])   


# In[40]:


###Read
df=spark.read.format('csv').option('header','True').schema(schema).load(getFilepath('netflix_titles.csv'))
df.printSchema()


# In[45]:


#String To date
df.withColumn('date_added',to_date(col('date_added'),'MMMM d')).withColumn('release_year',to_date(col('release_year'),'yyyy')).printSchema()


# In[53]:


df1=df.select('show_id','title','type','release_year','date_added','duration')


# In[71]:


df1.write.format('csv').mode('overwrite').option('header','True').option('sep','|').option("path", os.path.join(os.getcwd(),'data','Result')).save()

