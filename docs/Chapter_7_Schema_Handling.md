# Schema Validation
Every DataFrame that you create in Apache Spark will have a schema. The best way to look at a schema is as a blueprint or structure that defines the shape of your data. This includes the name of each column, its data type, whether or not the column can be NULL, and any metadata associated with each column  
Delta Lake will store the schema of a Delta Table as a schemaString in the metaData action of the transaction log entries. Table’s schema is saved in JSON format inside the transaction log when we view the transaction log file

# Schema on Write
Schema validation rejects writes to a table that does not match a table’s schema. Delta Lake performs schema validation on write, so it will check the schema of the data that is being written to the table. If the schema is compatible, the validation will pass and the write will succeed; if the schema of the data is not compatible, Delta Lake will cancel the transaction and no data is written.  
Note that this operation will always be atomic, so you will never have a condition where only a part of the data is written to the table. 

To determine whether a write to a table is compatible, Delta Lake uses the following rules:  
The source DataFrame to be written:  
- Cannot contain any columns that are not present is the target table’s schema
- It is allowed that the new data does not contain every column in the table, as long as the missing columns are marked as nullable in the target table’s schema.
- If a missing column was not marked as nullable in the target schema, the transaction will fail
- Cannot have column data types that differ from the column data types in the target table
- Cannot contain column names that differ only by case
    - Spark can be used in case-sensitive or case-insensitive (default) mode.
    - Parquet, on the other hand, is case-sensitive when storing and returning column information.
    - Delta Lake is case preserving but insensitive when storing the schema.
    To simlify above complexity, Delta Lake will not allow column names that only differ in case

# Schema Evolution
