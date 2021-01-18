#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pyspark.sql import SparkSession


# In[4]:


Spark=SparkSession.builder.appName('DataFrame_Join').getOrCreate()


# In[13]:


person = Spark.createDataFrame([
(0, "Bill Chambers", 0, [100]),
(1, "Matei Zaharia", 1, [500, 250, 100]),
(2, "Michael Armbrust", 1, [250, 100])])\
.toDF("id", "name", "graduate_program", "spark_status")
sparkStatus = spark.createDataFrame([
(500, "Vice President"),
(250, "PMC Member"),
(100, "Contributor")])\
.toDF("id", "status")
graduateProgram = spark.createDataFrame([
(0, "Masters", "School of Information", "UC Berkeley"),
(2, "Masters", "EECS", "UC Berkeley"),
(1, "Ph.D.", "EECS", "UC Berkeley")])\
.toDF("id", "degree", "department", "school")


# In[17]:


#Inner Join
joinExpression = person["graduate_program"] == graduateProgram['id']
wrongJoinExpression = person["name"] == graduateProgram["school"]
person.join(graduateProgram, joinExpression).show()
jointype='inner'
person.join(graduateProgram, joinExpression,jointype).show()


# In[18]:


jointype='outer'
person.join(graduateProgram, joinExpression,jointype).show()


# In[21]:


jointype='left_outer'
graduateProgram.join(person, joinExpression,jointype).show()


# In[24]:


joinType='right_outer'
person.join(graduateProgram, joinExpression, joinType).show()


# In[25]:


joinType='left_semi'
person.join(graduateProgram, joinExpression, joinType).show()


# In[27]:


joinType='left_anti'
graduateProgram.join(person, joinExpression, joinType).show()


# In[31]:


joinType='cross' #works like inner if condition specified
graduateProgram.join(person,joinExpression,joinType).show()


# In[32]:


#You should use cross-joins only if you are absolutely, 100 percent sure that this is the join you need.
#There is a reason why you need to be explicit when defining a cross-join in Spark. They’re dangerous!
#Advanced users can set the session-level configuration spark.sql.crossJoin.enable to true in
#order to allow cross-joins without warnings or without Spark trying to perform another join for you.
person.crossJoin(graduateProgram).show()


# In[33]:


#Even though this might seem like a challenge, it’s actually not. Any expression is a valid join
#expression, assuming that it returns a Boolean:
from pyspark.sql.functions import expr
person.withColumnRenamed("id", "personId").join(sparkStatus, expr("array_contains(spark_status, id)")).show()


# In[40]:


#Handling Duplicate Column Names
gradProgramDupe = graduateProgram.withColumnRenamed("id", "graduate_program")
joinExpr=gradProgramDupe["graduate_program"]==person["graduate_program"]
person.join(gradProgramDupe, joinExpr).show()
person.join(gradProgramDupe, joinExpr).select("graduate_program").show() # Error for ambigious column


# In[42]:


#When you have two keys that have the same name, probably the easiest fix is to change the join
#expression from a Boolean expression to a string or sequence. This automatically removes one of
#the columns for you during the join:
person.join(gradProgramDupe,"graduate_program").select("graduate_program")show()


# In[50]:


#Another approach is to drop the offending column after the join. When doing this, we need to
#refer to the column via the original source DataFrame. We can do this if the join uses the same
#key names or if the source DataFrames have columns that simply have the same name:
from pyspark.sql.functions import col
person.join(gradProgramDupe, joinExpr).drop(gradProgramDupe["graduate_program"]).show()


# In[51]:


#We can avoid this issue altogether if we rename one of our columns before the join:
gradProgram3 = graduateProgram.withColumnRenamed("id", "grad_id")
joinExpr = person["graduate_program"]== gradProgram3["grad_id"]
person.join(gradProgram3, joinExpr).show()


# In[ ]:




