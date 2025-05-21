# Step 1: Setup PySpark (only needed in Colab or new environments)
import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
os.environ["SPARK_HOME"] = "/content/spark-3.3.2-bin-hadoop3"

import findspark
findspark.init()

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

# Step 2: Start Spark session
spark = SparkSession.builder.appName("SpeedProcessing").getOrCreate()

# Step 3: Create and transform data
data = [(35,), (55,), (65,), (75,), (45,)]
df = spark.createDataFrame(data, ["speed_kmph"])
df = df.withColumn("speed_kmph_corrected", col("speed_kmph") + 5)
df = df.withColumn("is_overspeeding", when(col("speed_kmph") > 60, "Yes").otherwise("No"))

# Show result
df.show()

# Step 4: Convert to Pandas and export CSV
df_pd = df.toPandas()
csv_file = "speed_data.csv"
df_pd.to_csv(csv_file, index=False)
print(f"CSV saved to: {csv_file}")

# Step 5: Load CSV into SQLite
import sqlite3
import pandas as pd

conn = sqlite3.connect("traffic_data.db")
df_pd.to_sql("speed_data", conn, if_exists="replace", index=False)
print("Data written to SQLite database: traffic_data.db")

# Step 6: Run a simple SQL query
query = "SELECT * FROM speed_data WHERE is_overspeeding = 'Yes';"
df_result = pd.read_sql_query(query, conn)
print("\nOverspeeding vehicles:")
print(df_result)

conn.close()
