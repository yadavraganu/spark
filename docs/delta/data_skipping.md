Data skipping information is collected automatically when you write data into a Delta table. Delta Lake on Databricks  
takes advantage of this information (minimum and maximum values, null counts, and total records per file) at query  
time to provide faster queries.  

You must have statistics collected for columns that are used in ZORDER statements.    
By default, Delta Lake collects statistics on the first 32 columns defined in your table schema. For this collection,    
each field in a nested column is considered an individual column. You can modify this behavior by setting one of  
the following table properties 

__delta.dataSkippingNumIndexedCols:__  
Increase or decrease the number of columns on which Delta collects statistics. Depends on column order.  
__delta.dataSkippingStatsColumns:__  
Specify a list of column names for which Delta Lake collects statistics. Supersedes dataSkippingNumIndexedCols.  

Table properties can be set at table creation or with ALTER TABLE statements.  
Updating this property does not automatically recompute statistics for existing data.    
Rather, it impacts the behavior of future statistics collection when adding or updating data in the table.  

Delta Lake does not leverage statistics for columns not included in the current list of statistics columns.  
You can manually trigger the re-computation of statistics for a Delta table using the following command: 

`ANALYZE TABLE table_name COMPUTE DELTA STATISTICS`

Z-ordering is a technique to colocate related information in the same set of files. This co-locality is automatically  
used by Delta Lake on Databricks data-skipping algorithms. This behavior dramatically reduces the amount of data that  
Delta Lake on Databricks needs to read. To Z-order data, you specify the columns to order on in the ZORDER BY clause

If you expect a column to be commonly used in query predicates and if that column has high cardinality  
(that is, a large number of distinct values), then use ZORDER BY.  

You can specify multiple columns for ZORDER BY as a comma-separated list. However, the effectiveness of the locality  
drops with each extra column. Z-ordering on columns that do not have statistics collected on them would be ineffective  
and a waste of resources. This is because data skipping requires column-local stats such as min, max, and count.  
You can configure statistics collection on certain columns by reordering columns in the schema, or you can increase 
the number of columns to collect statistics on.