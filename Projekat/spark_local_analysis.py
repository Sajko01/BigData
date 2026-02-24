

import sys
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import min, max, avg, stddev, sum as _sum, count, col, expr, countDistinct

# --- Start timer ---
start_time = time.time()

# --- Spark session ---
# spark = SparkSession.builder \
#     .appName("LocalAnalysis") \
#     .master("spark://spark-master:7077") \
#     .getOrCreate()
# spark.sparkContext.setLogLevel("WARN")

# --- Spark session ---             /////////////////////////////////// DRUGA PROMENA 
spark = SparkSession.builder \
    .appName("LocalAnalysis") \
    .master("local[*]") \
    .getOrCreate()
spark.sparkContext.setLogLevel("WARN")

# --- CSV or Parquet path ---
data_file = "college_big.csv"  # promeni po potrebi //PROMENA JEDNA !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# data_file = "hdfs://namenode:9000/user/student/data/college_big.csv"
if data_file.endswith(".csv"):
    df = spark.read.option("header", True).option("inferSchema", True).csv(data_file)
elif data_file.endswith(".parquet"):
    df = spark.read.parquet(data_file)
else:
    raise ValueError("Unsupported file type. Use CSV or Parquet.")

# --- Command line arguments ---
# primer: python spark_local_analysis.py stats stress gender
if len(sys.argv) < 2:
    print("Usage: python spark_local_analysis.py [filter|sort|stats] ...")
    sys.exit(1)

mode = sys.argv[1]

# --------------------
# FILTER mode
# --------------------
if mode == "filter":
    column = sys.argv[2]
    threshold = float(sys.argv[3])
    result = df.filter(col(column) >= threshold)
    print("Count:", result.count())
    result.show(10)

# --------------------
# SORT mode
# --------------------
elif mode == "sort":
    column = sys.argv[2]
    order = sys.argv[3].lower() if len(sys.argv) > 3 else "asc"
    result = df.orderBy(col(column).asc() if order == "asc" else col(column).desc())
    result.show(10)

# --------------------
# STATS mode (grupisana statistika)
# --------------------
elif mode == "stats":
    target_col = sys.argv[2]          # kolona za statistiku (npr. stress)
    group_col = sys.argv[3]           # kolona za grupisanje (npr. gender)

    result = df.groupBy(group_col).agg(
        min(target_col).alias("min"),
        max(target_col).alias("max"),
        avg(target_col).alias("avg"),
        stddev(target_col).alias("stddev"),
        _sum(target_col).alias("sum"),
        count(target_col).alias("count"),
        countDistinct(target_col).alias("distinct_count"),
        expr(f"percentile_approx({target_col}, 0.5)").alias("median"),
        expr(f"percentile_approx({target_col}, array(0.25,0.75))").alias("q1_q3"),
        expr(f"sum(case when {target_col} is null then 1 else 0 end)").alias("null_count")
    )

    result.show(truncate=False)

else:
    print("Unknown mode:", mode)

# --- Execution time ---
print("Execution time:", time.time() - start_time)

spark.stop()


# # Filtriranje
# python spark_local_analysis.py filter stress 3

# # Sortiranje po datumu opadajuće
# python spark_local_analysis.py sort day desc

# # Statistika po grupi (npr. stress po gender)
# python spark_local_analysis.py stats stress gender