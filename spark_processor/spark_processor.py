# spark_processor/spark_stream_processor.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, IntegerType, FloatType

# Define schema matching the Kafka message
schema = StructType() \
    .add("timestamp", StringType()) \
    .add("vehicle_count", IntegerType()) \
    .add("location", StringType()) \
    .add("avg_speed", FloatType()) \
    .add("congestion_level", StringType())

# Create Spark session
spark = SparkSession.builder \
    .appName("TrafficDataProcessor") \
    .getOrCreate()

# Read from Kafka
df_raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "traffic_data") \
    .option("startingOffsets", "earliest") \
    .load()

# Parse Kafka value (JSON string)
df_parsed = df_raw.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Print live data to console (you can later write to PostgreSQL or dashboard)
query = df_parsed.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", False) \
    .start()

query.awaitTermination()
