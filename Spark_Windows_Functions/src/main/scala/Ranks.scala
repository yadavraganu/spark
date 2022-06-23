package src.main.scala

import org.apache.log4j.{Level, Logger}
import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions._

object Ranks {
  def main (Args:Array[String]): Unit ={
    Logger.getLogger("org").setLevel(Level.ERROR)
    val SparkConf=new SparkConf()
    SparkConf.set("spark.app.name","Spark_Window_Functions_Ranks")
    SparkConf.set("spark.master","local[*]")
    val spark=SparkSession.builder().config(SparkConf).getOrCreate()
    val input=List((7782,10,"09-JUN-1981"),
      (7839,10,"17-NOV-1981"),
      (7934,10,"23-JAN-2022"),
      (7369,20,"17-DEC-1980"),
      (7566,20,"02-APR-1981"),
      (7902,20,"03-DEC-1981"),
      (7788,20,"09-DEC-1982"),
      (7876,20,"12-JAN-2000"))
    val df=spark.createDataFrame(input).toDF("Emp_Id","Dept_Id","Hire_Date").withColumn("Hire_Date",to_date(col("Hire_Date"),"dd-MMM-yyy"))
    val window_spec=Window.partitionBy("Dept_Id").orderBy(col("Hire_Date").desc)
    val df1=df.withColumn("Recent_Joiner_Rank",rank().over(window_spec))
    df1.show()
  }

}
