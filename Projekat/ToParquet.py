# from pyspark.sql import SparkSession
# import sys
# import time

# # --- Setup Spark ---
# spark = SparkSession.builder \
#     .appName("CSV to Parquet Converter") \
#     .master("local[*]") \
#     .getOrCreate()

# # --- Putanje ---
# # Možeš koristiti lokalnu putanju ili HDFS putanju
# input_csv = "college_big.csv"
# output_parquet = "college_big.parquet"

# print(f"Započinjem učitavanje: {input_csv} ...")
# start_time = time.time()

# try:
#     # 1. Učitaj CSV sa prepoznavanjem šeme
#     df = spark.read.option("header", True) \
#                    .option("inferSchema", True) \
#                    .csv(input_csv)

#     print(f"Učitano {df.count()} redova.")

#     # 2. Snimi kao Parquet
#     # .mode("overwrite") briše stari folder ako postoji
#     df.write.mode("overwrite").parquet(output_parquet)

#     end_time = time.time()
#     print("-----------------------------------------")
#     print(f"USPEH! Konverzija završena za: {end_time - start_time:.2f} sekundi")
#     print(f"Parquet folder: {output_parquet}")
#     print("-----------------------------------------")

# except Exception as e:
#     print(f"GREŠKA tokom konverzije: {e}")

# spark.stop()
from pyspark.sql import SparkSession
import time

spark = SparkSession.builder \
    .appName("CSV to Parquet Converter") \
    .master("local[*]") \
    .config("spark.sql.shuffle.partitions", "4") \
    .getOrCreate()

input_csv = "college_big.csv"
output_parquet = "college_big.parquet"

print(f"Započinjem učitavanje: {input_csv} ...")
start_time = time.time()

try:
    df = spark.read.option("header", True) \
                   .option("inferSchema", True) \
                   .csv(input_csv)

    print("CSV uspešno učitan.")

    # optimizacija
    df = df.repartition(4)

    df.write.mode("overwrite").parquet(output_parquet)

    end_time = time.time()
    print("-----------------------------------------")
    print(f"USPEH! Završeno za: {end_time - start_time:.2f} sekundi")
    print(f"Parquet folder: {output_parquet}")
    print("-----------------------------------------")

except Exception as e:
    print(f"GREŠKA: {e}")

spark.stop()