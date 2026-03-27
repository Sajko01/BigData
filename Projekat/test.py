from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()
df = spark.read.parquet("college_big.parquet")
print("Ukupan broj redova:", df.count())
df.show(5)