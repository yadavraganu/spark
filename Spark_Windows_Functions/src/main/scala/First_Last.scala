import org.apache.log4j.{Level, Logger}
import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types.{DateType, IntegerType, StructField, StructType}

object First_Last {
  def main (array: Array[String]) :Unit = {
    Logger.getLogger("org").setLevel(Level.ERROR)
    val Spark_Config = new SparkConf()
    Spark_Config.set("spark.app.name", "Spark_Windows_Function_First_Last")
    Spark_Config.set("spark.master", "local[*]")
    val spark = SparkSession.builder().config(Spark_Config).getOrCreate()
    val input=List((7782,10,"09-JUN-1981"),
      (7839,10,"17-NOV-1981"),
      (7934,10,"23-JAN-1982"),
      (7369,20,"17-DEC-1980"),
      (7566,20,"02-APR-1981"),
      (7902,20,"03-DEC-1981"),
      (7788,20,"09-DEC-1982"),
      (7876,20,"12-JAN-1983"))
    val schema=StructType(Array(StructField("Emp_Id",IntegerType,false),
      StructField("Dept_Id",IntegerType,false),
      StructField("Hire_Date",DateType,false)))
    val df=spark.createDataFrame(input).toDF("Emp_Id","Dept_Id","Hire_Date").withColumn("Hire_Date",to_date(col("Hire_Date"),"dd-MMM-yyyy"))
    val window_spec=Window.partitionBy("Dept_Id").orderBy(col("Hire_Date").desc)
    val df2 = df.withColumn("First_Value",first("Hire_Date").over(window_spec))
    val df3 = df2.withColumn("Last_Value",last("Hire_Date").over(window_spec))
    df3.show()
  }
}
