## Architecture Diagram
Parquet is referred as columnar format in many books but internally it is like an hybrid format ( Combination of Row and Columnar ).
A Parquet file consists of a header followed by one or more blocks, terminated by a footer. The header contains only a 4-byte magic number, PAR1, that identifies the file as being in Parquet format, and all the file metadata is stored in the footer. The footer’s metadata includes the format version, the schema, any extra key-value pairs, and metadata for every block in the file. The final two fields in the footer are a 4-byte field encoding the length of the footer metadata, and the magic number again (PAR1).    
![image](https://github.com/yadavraganu/spark/assets/77580939/f531121a-3dc8-4769-8928-8e18fe963c4b)
![image](https://github.com/yadavraganu/spark/assets/77580939/dabfacaa-3f1d-4fd8-a4f2-d55a4ef54dee)

Each block in a Parquet file stores one or more row groups, which is made up of column chunks containing the column data for those rows. The data for each column chunk is written in pages. Each page contains values from the same column, making a page a very good candidate for compression since the values are likely to be similar. The first level of compression is achieved through how the values are encoded. There are different encoding techniques ( Simple encoding, Run-Length encoding, Dictionary encoding, Bit Packing, Delta encoding.

Parquet file properties are set at write time. The properties listed below are appropriate if you are creating Parquet files from Map Reduce, Crunch, Pig, or Hive.  
![image](https://github.com/yadavraganu/spark/assets/77580939/6cc388c3-2249-42c7-b4d8-d14f00009fdc)  
A page is the smallest unit of storage in a Parquet file, so retrieving an arbitrary row requires that the page containing the row be decompressed and decoded. Thus, for single-row lookups, it is more efficient to have smaller pages, so there are fewer values to read through before reaching the target value.

There are three types of metadata: file metadata, column (chunk) metadata and page header metadata.  
![image](https://github.com/yadavraganu/spark/assets/77580939/29e7e646-3106-4c3b-9e88-9be575325f5c)  

## Pros of Parquet:

- __Columnar Storage:__ Unlike row-based files, Parquet is columnar-oriented. This means it stores data by columns, which allows for more efficient disk I/O and compression. It reduces the amount of data transferred from disk to memory, leading to faster query performance.
- __Schema Evolution:__ Parquet supports complex nested data structures, and allows for schema evolution. This means that as the schema of your data evolves, Parquet can adapt to those changes.
- __Compression:__ Parquet has good compression and encoding schemes. It reduces the disk storage space and improves performance, especially for columnar data retrieval, which is a common case in data analytics.

## Cons of Parquet:

- __Write-heavy Workloads:__ Since Parquet performs column-wise compression and encoding, the cost of writing data can be high for write-heavy workloads.
- __Small Data Sets:__ Parquet may not be the best choice for small datasets because the advantages of its columnar storage model aren’t as pronounced.

