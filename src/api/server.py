from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from kafka import KafkaConsumer
import json
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VeritasAPI")

app = FastAPI()

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws/analysis")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket connection accepted")
    
    # Create a consumer for this client
    # We use a group_id of None (or random) to ensure every client gets a copy of the messages
    # if we wanted broadcast. Or same group_id for load balancing.
    # For a dashboard, we usually want broadcast, so random group_id or no group_id.
    consumer = KafkaConsumer(
        'veritas-results',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='latest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    ) # No group_id = independent consumer

    try:
        while True:
            # Poll Kafka (blocking call wrapped in logic)
            # Since kafka-python is blocking, we use a short timeout and sleep to yield control
            # so the event loop (ping/pong) stays alive.
            msg_pack = consumer.poll(timeout_ms=100) 
            
            for tp, messages in msg_pack.items():
                for message in messages:
                    data = message.value
                    logger.info(f"Sending update: {data['headline'][:20]}...")
                    await websocket.send_json(data)
            
            await asyncio.sleep(0.1)
            
    except Exception as e:
        logger.error(f"WebSocket Error: {e}")
    finally:
        consumer.close()
        logger.info("WebSocket connection closed")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "veritas-api"}
