import sys
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    min, max, avg, stddev,
    sum as _sum, count,
    col, expr, countDistinct
)

# ===============================
# START TIMER
# ===============================

start_time = time.time()

# ===============================
# SPARK SESSION (LOCAL)
# ===============================

spark = SparkSession.builder \
    .appName("LocalParquetAnalysis") \
    .master("local[*]") \
    .config("spark.sql.shuffle.partitions", "8") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# ===============================
# PARQUET PUTANJA (LOKALNO)
# ===============================

# data_file = "D:\0BIGDATA\Novo\college_clean.parquet"   # ← tvoj parquet fajl
data_file = r"D:\0BIGDATA\Novo\college_clean.parquet"

df = spark.read.parquet(data_file)

# ===============================
# ARGUMENTI
# ===============================

if len(sys.argv) < 2:
    print("Usage: python spark_local_analysis.py [filter|sort|stats] ...")
    sys.exit(1)

mode = sys.argv[1]

# ===============================
# FILTER
# ===============================

if mode == "filter":
    column = sys.argv[2]
    threshold = float(sys.argv[3])

    result = df.filter(col(column) >= threshold)

    print("Count:", result.count())
    result.show(10)

# ===============================
# SORT
# ===============================

elif mode == "sort":
    column = sys.argv[2]
    order = sys.argv[3].lower() if len(sys.argv) > 3 else "asc"

    result = df.orderBy(
        col(column).asc() if order == "asc"
        else col(column).desc()
    )

    result.show(10)

# ===============================
# STATS
# ===============================

elif mode == "stats":
    target_col = sys.argv[2]
    group_col = sys.argv[3]

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

# ===============================
# EXECUTION TIME
# ===============================

print("Execution time:", time.time() - start_time)

spark.stop()