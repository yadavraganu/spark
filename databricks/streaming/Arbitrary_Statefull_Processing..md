Arbitrary statefull stream processing can be done in pyspark using __applyInPandasWithState__ which takes below parameters  

__func :__
A Python native function to be called on every group. 
It should take parameters (key, Iterator[pandas.DataFrame], state) and return Iterator[pandas.DataFrame]. 
Note that the type of the key is tuple and the type of the state is pyspark.sql.streaming.state.GroupState.

__outputStructType :__
The type of the output records. The value can be either a pyspark.sql.types.DataType object or a DDL-formatted type string.

__stateStructType :__
The type of the user-defined state. The value can be either a pyspark.sql.types.DataType object or a DDL-formatted type string.

__outputMode :__
The output mode of the function.

__timeoutConfstr :__
Timeout configuration for groups that do not receive data for a while.
Valid values are defined in pyspark.sql.streaming.state.GroupStateTimeout.


```
import pandas as pd
from pyspark.sql.types import StructType,StructField,IntegerType,StringType
from pyspark.sql.streaming.state import GroupStateTimeout
from pyspark.sql.functions import col

input_path = 'dbfs:/FileStore/arbitrary_streamfull_processing/input_data/'
schema_path = 'dbfs:/FileStore/arbitrary_streamfull_processing/schema/'

spark.conf.set('spark.sql.shuffle.partitions',2)
df = (
    spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", schema_path)
    .load(input_path)
).withColumn('price',col('price').cast('Integer'))

op_schema = StructType([StructField('user',StringType()),StructField('status',StringType()),StructField('sum',IntegerType())])
state_schema = StructType([StructField('sum',IntegerType()),StructField('status',StringType())])

def arbitrary_statefull_processing(key,data_iter,state):
    for data in data_iter:
        sm = sum(data[data['session_status'] != 'InActive' ]['price'])
        status = 'InActive' if any(data[data['session_status'] == 'InActive'].count()>0) else 'Active'
        if state.exists:
            old_state = state.get
            sm = old_state[0] + sm
        state.update((sm,status))
        if status == 'InActive':
            state.remove()
        yield pd.DataFrame({"user":[key[0]],"status":[status],"sum":[sm]})

df = df.groupBy('user').applyInPandasWithState(func = arbitrary_statefull_processing,outputStructType=op_schema,stateStructType=state_schema,outputMode='append',timeoutConf=GroupStateTimeout.NoTimeout)
display(df)
```
