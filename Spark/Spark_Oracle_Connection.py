#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Before Doing this plcae ojdbc6.jar in spark Jars folder or on anypath &specify with SPARC_CLASSPATH env variable
#Check jdbc.ajr according to your server version
#If you are recieving No matching authentication protocol exception error check version of server & client are compatible or change config at server side to allow older client also
import findspark
findspark.init()


# In[2]:


from pyspark.sql import SparkSession
spark=SparkSession.builder.appName('Spark_Oracle_Connection').getOrCreate()


# In[3]:


driver='oracle.jdbc.driver.OracleDriver'
url='jdbc:oracle:thin:@localhost:1521/XEPDB1'
user='TEST'
password='TEST'
table='EMPLOYEE'


# In[4]:


# Getting whole table data
df=spark.read.format('jdbc').option('driver',driver).option('url',url).option('dbtable',table).option('user',user).option('password',password).load()


# In[5]:


df.printSchema()


# In[6]:


# Getting data with select query
query='(SELECT E.NAME AS EMPLOYEE_NAME,D.NAME AS DEPARTMENT FROM EMPLOYEE E INNER JOIN DEPARTMENT D ON E.DEPARTMENT_ID=D.ID) EMP_DEP'
df1=spark.read.format('jdbc').option('driver',driver).option('url',url).option('dbtable',query).option('user',user).option('password',password).load()


# In[16]:


df1.printSchema()


# In[7]:


df1.show()


# In[8]:


#Create a new table
df1.write.format('jdbc').option('driver',driver).option('url',url).option('user',user).option('password',password).mode('overwrite').option('createTableOptions','').option('dbtable','EMP_DEP').save()


# In[9]:


#Append in existing table 
df1.write.format('jdbc').option('driver',driver).option('url',url).option('user',user).option('password',password).mode('append').option('dbtable','EMP_DEP').save()


# In[10]:


spark.stop()


# In[ ]:




