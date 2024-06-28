# Chapter 4 
Spark's structured collection API has three core components
1. Dataframes (Untyped)
2. Datasets (Typed)
3. Sql table & views

DataFrames and Datasets represent immutable, lazily evaluated plans that specify what operations to apply to data residing at a location to generate some output.  
DataFrames are untyped is aslightly inaccurate; they have types, but Spark maintains them completely and only checks whether those types line up to those specified in the schema at runtime. Datasets, on the other hand, check whether types conform to the specification at compile time. Datasets are only available to Java Virtual Machine (JVM)–
based languages (Scala and Java)  

DataFrames are simply Datasets of Type Row. The “Row” type is Spark’s internal representation of its optimized in-memory format for computation. This format makes for highly specialized and efficient computation because rather than using JVM types, which can cause high garbage-collection and object instantiation costs, Spark can operate on its own internal format without incurring any of
those costs. 
### Structured Spark Types
Spark is effectively a programming language of its own. Internally, Spark uses an engine called Catalyst that maintains its own type information through the planning and processing of work. In doing so, this opens up a wide variety of execution optimizations that make significant differences.  
Spark types map directly to the different language APIs. Below are the few types. 

- ByteType()
- ShortType()
- ArrayType()
- StringType()

__Present in__  
`from pyspark.sql.types import *`

### Structured API Execution
__Logical Planning__

The first phase of execution is meant to take user code and convert it into a logical plan which involves below steps
- Converting user code into an unresolved logical plan. This plan is unresolved because although your code might be valid, the tables or columns that it refers to might or might not exist.
- Spark uses the catalog, a repository of all table and DataFrame information, to resolve columns and tables in the analyzer. The analyzer might reject the unresolved logical plan if the required table or column name does not exist in the catalog
- If the analyzer can resolve it, the result is passed through the Catalyst Optimizer, a collection of rules that attempt to optimize the logical plan by pushing down predicates or selections. Packages can extend the Catalyst to include their own rules for domain-specific optimizations.

__Physical Planning__
- After successfully creating an optimized logical plan, Spark then begins the physical planning process
- The physical plan, often called a Spark plan, specifies how the logical plan will executeon the cluster by generating different physical execution strategies and comparing them through
a cost model.
- Physical planning results in a series of RDDs and transformations. This result is why you might have heard Spark referred to as a compiler—it takes queries in DataFrames, Datasets, and SQL and compiles them into RDD transformations for you.

__Execution__  

Upon selecting a physical plan, Spark runs all of this code over RDDs, the lower-level programming interface of Spark. Spark performs further optimizations at runtime, generating native Java bytecode that can remove entire tasks or stages during execution
