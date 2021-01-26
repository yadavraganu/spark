#!/usr/bin/env python
# coding: utf-8

# In[2]:


from pyspark.sql import SparkSession


# In[6]:


spark=SparkSession.builder.appName('Spark_RDDs_Functions_Part_2').getOrCreate()


# In[7]:


myCollection = "Spark The Definitive Guide : Big Data Processing Made Simple".split(" ")
words = spark.sparkContext.parallelize(myCollection, 2)


# In[9]:


words.map(lambda word: (word.lower(), 1)).glom().collect()


# In[13]:


#keyBy The preceding example demonstrated a simple way to create a key. However, you can also use
#the keyBy function to achieve the same result by specifying a function that creates the key from
#your current value
keyword = words.keyBy(lambda word: word.lower()[0])
keyword.glom().collect()


# In[14]:


#mapValues
keyword.mapValues(lambda word: word.upper()).collect()


# In[15]:


#flatMapValues
keyword.flatMapValues(lambda word: word.upper()).collect()


# In[16]:


#Keys & Values
keyword.keys().collect()
keyword.values().collect()


# In[17]:


#LookUp
keyword.lookup("s")


# In[25]:


import random
distinctChars = words.flatMap(lambda word: list(word.lower())).distinct().collect()
sampleMap = dict(map(lambda c: (c, random.random()), distinctChars))
print(sampleMap)
words.map(lambda word: (word.lower()[0], word)).sampleByKey(True, sampleMap, 6).collect()


# In[ ]:




