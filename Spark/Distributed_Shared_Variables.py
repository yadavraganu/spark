#!/usr/bin/env python
# coding: utf-8

# In[2]:


import findspark
findspark.init()


# In[20]:


from pyspark.sql import SparkSession
spark=SparkSession.builder.appName('Distributed_Shared_Variables').getOrCreate()
from pyspark import AccumulatorParam


# In[39]:


data='THis is the demo for broadcast variable in spark'.split(' ')
rd=spark.sparkContext.parallelize(data,4)
rd.glom().collect()


# In[40]:


# Broadcast variables are a way you can share an immutable value efficiently around the cluster
#without encapsulating that variable in a function closure
broadcastdata={'THis':1,'broadcast':2,'in':3}
broadcast=spark.sparkContext.broadcast(broadcastdata)


# In[41]:


broadcast.value


# In[42]:


rd.map(lambda word: (word, broadcast.value.get(word, 0))).sortBy(lambda wordPair: wordPair[1]).collect()


# In[43]:


#Accumulators provide a mutable variable that a Spark cluster can safely update on a per-row basis.
accContainsI = spark.sparkContext.accumulator(0)
def ContainsIfunc(row):
    if 'i' in row:
        accContainsI.add(1)
rd.foreach(lambda row:ContainsIfunc(row))
accContainsI.value


# In[49]:


class AddAccumulator(AccumulatorParam):
    def zero(self, v):
        return 0
    def addInPlace(self, acc1, acc2):
        acc1=acc2+acc1
        return acc1
accContainsICustom = spark.sparkContext.accumulator(0,AddAccumulator()) 
def ContainsICustomfunc(row):
    if 'i' in row:
        accContainsICustom.add(1)
rd.foreach(lambda row:ContainsICustomfunc(row))
accContainsICustom.value


# In[50]:


spark.stop()


# In[ ]:




