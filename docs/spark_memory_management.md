# Reserved Memory
This is the memory reserved by the system, and its size is hardcoded.It's value is 300MB, which means that this 300MB of RAM  
does not participate in Spark memory region size calculations, and its size cannot be changed in any way without Spark recompilation  
or setting `spark.testing.reservedMemory`, which is not recommended as it is a testing parameter not intended to be used in production.  
Be aware, this memory is only called “reserved”, in fact it is not used by Spark in any way, but it sets the limit on what you can allocate  
for Spark usage.Even if you want to give all the Java Heap for Spark to cache your data, you won’t be able to do so as this “reserved”  
part would remain spare (not really spare, it would store lots of Spark internal objects).    
If you don’t give Spark executor at least 1.5 * Reserved Memory = 450MB heap, it will fail with “please use larger heap size” error message.  

# User Memory
This is the memory pool that remains after the allocation of Spark Memory, and it is completely up to you to use it in a way you like.  
You can store your own data structures there that would be used in RDD transformations.The size of this memory pool can be calculated as 
`(“Java Heap” – “Reserved Memory”) * (1.0 – spark.memory.fraction)`  
This is the User Memory and its completely up to you what would be stored in this RAM and  
Spark makes completely no accounting on what you do there and whether you respect this boundary or not. Not respecting this boundary in your code might cause OOM error.
