from kafka import KafkaProducer
import json
import time
import pandas as pd

# Load your traffic data CSV
df = pd.read_csv("traffic_sample_data_clean.csv")

# Convert each row to JSON and send as Kafka message
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = 'traffic-data'

for _, row in df.iterrows():
    message = row.to_dict()
    producer.send(topic, value=message)
    print(f"Sent: {message}")
    time.sleep(1)  # Adjust delay to simulate real-time streaming

producer.flush()
producer.close()
