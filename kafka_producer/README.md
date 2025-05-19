# 📁 Kafka Producer

Contains the Python script that simulates traffic data streaming into Kafka topics.

This producer reads CSV data and sends it as messages to Kafka in real time.
## Files

- **kafka_producer.py** : Kafka producer script that reads data from CSV and sends to Kafka topic.

## Prerequisites

- Python 3.x
- Kafka running locally at `localhost:9092`
- Python packages: `kafka-python`, `pandas`

Install required packages using:

```bash
pip install kafka-python pandas

How to Run
python kafka_producer.py.

