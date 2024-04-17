# What is spill & where can we find it in Spark UI if data is spilling ?
A memory spill in Apache Spark is the process of transferring data from RAM to disk, and potentially back again.  
This happens when the dataset exceeds the available memory capacity of an executor during tasks that require more memory than is available

In Apache Spark, you can identify a spill in the Spark Web UI under the Stages tab. The Stages tab displays two values in pairs:  
- __Shuffle spill (memory)__ is the size of the deserialized form of the shuffled data in memory.
- __Shuffle spill (disk)__ is the size of the serialized form of the data on disk.  

If no spill is occurring, these columns/rows will not show up. You can also see the amount of memory data spill in the Query Details under the SQL tab, but the disk data spill might not be visible.
![img.png](images/Spill.png)