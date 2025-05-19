from kafka import KafkaConsumer
import json

# Kafka consumer setup
consumer = KafkaConsumer(
    'traffic-data',                     # topic name
    bootstrap_servers=['localhost:9092'],  # your Kafka broker address
    auto_offset_reset='earliest',      # start reading from the earliest message
    enable_auto_commit=True,
    group_id='traffic-consumers',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Kafka Consumer started, listening to 'traffic-data' topic...")

for message in consumer:
    data = message.value
    print(f"Received message: {data}")
