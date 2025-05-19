# 📁 Spark Processor

This folder contains the Apache Spark streaming code for processing real-time traffic data from Kafka.

## What is this for?

- Reads traffic data from the Kafka topic `traffic_data` in real time.
- Processes and transforms the streaming data using Spark Structured Streaming.
- Outputs processed data for further analysis or storage.

## Prerequisites

- Apache Spark installed locally (version 3.x recommended)
- Python 3.7+
- Kafka running locally on `localhost:9092`
- Required Python packages (install via `pip install -r requirements.txt`)

## Files

- **spark_processor.py** — Main Spark streaming script that reads from Kafka and processes traffic data.

## How to run

1. Make sure Kafka broker is running locally on `localhost:9092`.
2. Start your Kafka producer to send traffic data to the `traffic_data` topic.
3. Run the Spark streaming processor locally:

    ```bash
    spark-submit spark_stream_processor.py
    ```

4. The processor will read messages from Kafka, process them, and display output logs on the console.

## Notes

- You can modify the Spark script to write output to files, databases, or other sinks as needed.
- Ensure your environment variables or configs are set correctly if you customize Kafka connection details.
