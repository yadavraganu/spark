### Data Serialization
Serialization plays an important role in the performance of any distributed application.
Formats that are slow to serialize objects into, or consume a large number of bytes, will greatly slow down the computation.
Often, this will be the first thing you should tune to optimize a Spark application.
Spark aims to strike a balance between convenience (allowing you to work with any Java type in your operations) and performance.
It provides two serialization libraries:

- __Java serialization:__ By default, Spark serializes objects using Java’s ObjectOutputStream framework, and can work with any class you create that implements java.io.Serializable.
You can also control the performance of your serialization more closely by extending java.io.Externalizable.Java serialization is flexible but often quite slow, and leads to large serialized formats for many classes.

- __Kryo serialization:__ Spark can also use the Kryo library (version 4) to serialize objects more quickly.Kryo is significantly faster and more compact than Java serialization (often as much as 10x), but does not support all Serializable types and requires you to register the classes you’ll use in the program in advance for best performance.
You can switch to using Kryo by initializing your job with a SparkConf and calling 
conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
This setting configures the serializer used for not only shuffling data between worker nodes but also when serializing RDDs to disk.
The only reason Kryo is not the default is because of the custom registration requirement, but we recommend trying it in any network-intensive application.
Since Spark 2.0.0, we internally use Kryo serializer when shuffling RDDs with simple types, arrays of simple types, or string type.


In this example, we first define a custom class called Person.
We then initialize a Spark configuration and set the spark.serializer property to org.apache.spark.serializer.KryoSerializer.
This tells Spark to use Kryo serialization to serialize and deserialize data.
We then register the Person class with Kryo. This is necessary because Kryo does not support all Serializable types by default.
Next, we create an RDD of Person objects and save it to disk using Kryo serialization. 
We then load the RDD from disk using Kryo serialization and print the loaded RDD.
Kryo serialization is significantly faster and more compact than Java serialization.
However, it does not support all Serializable types and requires you to register the classes you will use in the program in advance for best performance.

```
class Person(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

conf = SparkConf()
conf.setAppName("kyroExample")
conf.setMaster("local[*]")
conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
conf.set("spark.kryo.registrationRequired", "true")
conf.registerKryoClasses([Person])
sc = SparkContext(conf=conf)
people = sc.parallelize([Person("John", 30), Person("Mary", 25)])
people.saveAsObjectFile("people.kryo")
loadedPeople = sc.objectFile("people.kryo")
for person in loadedPeople.collect():
    print(person.name, person.age) <code>
```