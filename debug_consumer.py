from kafka import KafkaConsumer
import json

print("Starting Debug Consumer...")
try:
    consumer = KafkaConsumer(
        'veritas-articles',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest', # Check for ANY messages
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        consumer_timeout_ms=5000 # Stop after 5s if nothing
    )
    print("Connected. Listening...")
    for msg in consumer:
        print(f"Received: {msg.value['headline']}")
except Exception as e:
    print(f"Error: {e}")
