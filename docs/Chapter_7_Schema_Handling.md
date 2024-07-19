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
Schema evolution allows us to add, remove, or modify columns in an existing Delta table without losing any data.  
Schema evolution is enabled on the table level by using __.option("mergeSchema","true")__ during a write operation.  
You can also enable schema evolution for the entire Spark cluster by setting __spark.databricks.delta.schema.autoMerge.enabled__ to true.

When schema evolution is enabled, the following rules are applied:
- If a column exists in the source DataFrame being written but not in the Delta table, a new column is added to the Delta table with the same name and data
type. All existing rows will have a null value for the new column.
- If a column exists in the Delta table but not in the source DataFrame being written, the column is not changed and retains its existing values. The new records will have a null value for the missing columns in the source DataFrame.
- If a column with the same name but a different data type exists in the Delta table, Delta Lake attempts to convert the data to the new data type. If the conversion fails, an error is thrown.
- If a NullType column is added to the Delta table, all existing rows are set to null for that column

# Explicit Schema Updates
### Adding a Column to a Table
```
%sql
ALTER TABLE delta.`/mnt/datalake/book/chapter07/TaxiRateCode` ADD COLUMN RateCodeTaxPercent INT AFTER RateCodeId
```
We used the AFTER keyword, so the column will be added after the RateCodeId field, and not at the end of the column list, as is the standard practice without the AFTER keyword. Similarly, we can use the FIRST keyword to add the new column at the first position in the column list.
### Adding Comments to a Column
```
%sql
ALTER TABLE taxidb.TaxiRateCode
ALTER COLUMN RateCodeId COMMENT 'This is the id of the Ride'
```
### Changing Column Ordering
```
%sql
ALTER TABLE taxidb.TaxiRateCode ALTER COLUMN RateCodeDesc AFTER RateCodeId
```
By default, Delta Lake collects statistics on only the first 32 columns. Therefore, if there is a specific column that we would like to have included in the statistics, we might want to move that column in the column order.

### Delta Lake Column Mapping
Column mapping allows Delta Lake tables and the underlying Parquet file columns to use different names. This enables Delta Lake schema evolution such as __RENAME COLUMN__ and __DROP COLUMN__ on a Delta Lake table without the need to rewrite the underlying Parquet files.  
You can enable column mapping by setting __delta.columnmapping.mode__ to name
```
%sql
 ALTER TABLE taxidb.TaxiRateCode SET TBLPROPERTIES (
 'delta.minReaderVersion' = '2',
 'delta.minWriterVersion' = '5',
 'delta.columnMapping.mode' = 'name'
 )
```
For each column, you have:
- The name, which is the official Delta Lake column name (e.g., RateCodeId).
- delta.columnMapping.id, which is the ID of the column. This ID will remain stable.
- delta.columnMapping.physicalName, which is the physical name in the Parquet file

### Renaming a Column
You can use ALTER TABLE...RENAME COLUMN to rename a column without rewriting any of the column’s existing data. Note that column mapping needs to be in place for
this to be enabled.  
Assume we want to rename the RateCodeDesc column to a more descriptive RateCodeDescription:
```
%sql
ALTER TABLE taxidb.taxiratecode RENAME COLUMN RateCodeDesc to RateCodeDescription
```
