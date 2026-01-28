import time
import json
import random
from kafka import KafkaProducer
import os

def create_dummy_image():
    # Ensure a dummy image exists if not present
    if not os.path.exists("test_image.jpg"):
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new('RGB', (224, 224), color = (73, 109, 137))
        d = ImageDraw.Draw(img)
        d.text((10,10), "BREAKING NEWS", fill=(255,255,0))
        img.save("test_image.jpg")

def run_producer():
    create_dummy_image()
    
    # Wait for Kafka to be ready (rudimentary check logic could go here)
    print("Connecting to Kafka...")
    # Retrying connection logic is good for docker-compose startup timing
    producer = None
    for _ in range(10):
        try:
            producer = KafkaProducer(
                bootstrap_servers=['localhost:9092'],
                value_serializer=lambda x: json.dumps(x).encode('utf-8')
            )
            break
        except Exception as e:
            print(f"Waiting for Kafka: {e}")
            time.sleep(2)
            
    if not producer:
        print("Could not connect to Kafka provider.")
        return

    print("Producer started. Sending articles...")

    headlines = [
        "Aliens land in New York City",
        "Stock market crashes as tech bubble bursts",
        "Local cat wins mayor election",
        "Scientists discover water on the Sun",
        "New iPhone released with transparent screen"
    ]

    while True:
        headline = random.choice(headlines)
        article = {
            "headline": headline,
            "image_path": "test_image.jpg", # pointing to local file for demo
            "timestamp": time.time()
        }
        
        producer.send('veritas-articles', value=article)
        print(f"Sent: {headline}")
        time.sleep(3) # Simulate 1 article every 3 seconds

if __name__ == "__main__":
    run_producer()
