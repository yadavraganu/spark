## PySpark JSON Processing Functions
**Common Input DataFrame (`df`) for all examples:**
| id | json\_data\_string |
|----|---------------------------------------------------------------------|
| 1  | `{"name": "Alice", "age": 30, "city": "NY", "tags": ["premium", "active"]}` |
| 2  | `{"name": "Bob", "age": null, "city": "LDN", "tags": []}` |
| 3  | `{"name": "Charlie", "city": "PAR", "preferences": {"theme": "dark"}}` |

-----
### 1\. `from_json(col, schema, options=None)`
  * **Description:** Parses a **JSON string column** into a **structured column** (e.g., `StructType`, `MapType`, or `ArrayType`). It needs a predefined schema to understand the JSON's structure and data types. This is the most common way to get your JSON into a strongly-typed DataFrame.
  * **Input DataFrame:**
    | id | json\_data\_string |
    |----|---------------------------------------------------------------------|
    | 1  | `{"name": "Alice", "age": 30, "city": "NY", "tags": ["premium", "active"]}` |
    | 2  | `{"name": "Bob", "age": null, "city": "LDN", "tags": []}` |
    | 3  | `{"name": "Charlie", "city": "PAR", "preferences": {"theme": "dark"}}` |

  * **Input Schema (Example `user_schema`):**
    ```python
    from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType
    user_schema = StructType([
        StructField("name", StringType(), True),
        StructField("age", IntegerType(), True),
        StructField("city", StringType(), True),
        StructField("tags", ArrayType(StringType()), True),
        StructField("preferences", StructType([StructField("theme", StringType(), True)]), True)
    ])
    ```
  * **Output DataFrame (after `df.withColumn("parsed_data", from_json(col("json_data_string"), user_schema))`)**:
    | id | parsed\_data |
    |----|---------------------------------------------------------------------------------------------------|
    | 1  | `{"name": "Alice", "age": 30, "city": "NY", "tags": ["premium", "active"], "preferences": null}` |
    | 2  | `{"name": "Bob", "age": null, "city": "LDN", "tags": [], "preferences": null}` |
    | 3  | `{"name": "Charlie", "age": null, "city": "PAR", "tags": null, "preferences": {"theme": "dark"}}` |
-----
### 2\. `to_json(col, options=None)`
  * **Description:** Converts a **structured PySpark column** (like a `StructType`, `MapType`, or `ArrayType`) back into a **JSON string**. This is useful for exporting data or re-serializing processed information.
  * **Input DataFrame (Conceptual, assuming `parsed_data` column from `from_json`):**
    | id | parsed\_data |
    |----|---------------------------------------------------------------------------------------------------|
    | 1  | `{"name": "Alice", "age": 30, "city": "NY", "tags": ["premium", "active"], "preferences": null}` |
    | 2  | `{"name": "Bob", "age": null, "city": "LDN", "tags": [], "preferences": null}` |
  * **Output DataFrame (after `df_parsed.withColumn("json_output", to_json(col("parsed_data")))`)**:
    | id | json\_output |
    |----|-------------------------------------------------------------------------------------------------------------|
    | 1  | `{"name":"Alice","age":30,"city":"NY","tags":["premium","active"],"preferences":null}` |
    | 2  | `{"name":"Bob","age":null,"city":"LDN","tags":[],"preferences":null}` |
-----
### 3\. `get_json_object(col, path)`
  * **Description:** Extracts a specific JSON object or **scalar value** from a JSON string using a **JSONPath expression** (e.g., `$.name`, `$.address.street`). The output is ***always*** a `StringType`, regardless of the original JSON type.
  * **Input DataFrame:**
    | id | json\_data\_string |
    |----|---------------------------------------------------------------------|
    | 1  | `{"name": "Alice", "age": 30, "city": "NY", "tags": ["premium", "active"]}` |
    | 2  | `{"name": "Bob", "age": null, "city": "LDN", "tags": []}` |
    | 3  | `{"name": "Charlie", "city": "PAR", "preferences": {"theme": "dark"}}` |
  * **Output DataFrame (after `df.select(get_json_object(col("json_data_string"), "$.name").alias("user_name"), get_json_object(col("json_data_string"), "$.preferences.theme").alias("theme_pref"))`)**:
    | user\_name | theme\_pref |
    |-----------|------------|
    | Alice     | null       |
    | Bob       | null       |
    | Charlie   | dark       |
-----
### 4\. `json_tuple(col, *fields)`
  * **Description:** Extracts multiple ***top-level*** fields from a JSON string column, creating new columns for each. It's similar to `get_json_object` but more concise for several top-level extractions. The output is ***always*** a `StringType`.
  * **Input DataFrame:**
    | id | json\_data\_string |
    |----|---------------------------------------------------------------------|
    | 1  | `{"name": "Alice", "age": 30, "city": "NY", "tags": ["premium", "active"]}` |
    | 2  | `{"name": "Bob", "age": null, "city": "LDN", "tags": []}` |
    | 3  | `{"name": "Charlie", "city": "PAR", "preferences": {"theme": "dark"}}` |
  * **Output DataFrame (after `df.select(json_tuple(col("json_data_string"), "name", "city").alias("user_name", "user_city"))`)**:
    | user\_name | user\_city |
    |-----------|-----------|
    | Alice     | NY        |
    | Bob       | LDN       |
    | Charlie   | PAR       |
-----
### 5\. `schema_of_json(json_string_literal, options=None)`
  * **Description:** Infers the schema (structure and data types) of a JSON string ***literal*** (not a DataFrame column). It returns the schema in DDL (Data Definition Language) format. This is a utility function, primarily for schema discovery.
  * **Input (Conceptual):** A Python string containing JSON.
    ```python
    json_literal = '{"product_id": "P001", "price": 99.99, "available": true}'
    ```
  * **Output (Conceptual, string result from `spark.range(1).select(schema_of_json(lit(json_literal))).collect()[0][0]`):**
    ```
    struct<product_id:string,price:double,available:boolean>
    ```
