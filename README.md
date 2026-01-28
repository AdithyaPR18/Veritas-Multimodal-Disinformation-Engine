# Veritas: Real Time Multimodal Disinformation Engine

**Veritas** is a high-performance, event-driven pipeline designed to detect disinformation in real-time. It processes multimodal news articles (Text + Image) using a deep learning model to assign an authenticity score. If the model is uncertain, it triggers a secondary OCR (Optical Character Recognition) check to verify semantic consistency between the headline and the image text.

## 🚀 Key Features

*   **Real-Time Event Stream**: Built on Apache Kafka for high-throughput data ingestion.
*   **Multimodal AI**: Custom PyTorch model fusing BERT (Text) and ResNet50 (Vision).
*   **Live Mission Control**: A "Minority Report" style dashboard built with Next.js, Framer Motion, and WebSockets.
*   **Adaptive Verification**: Automatically triggers expensive OCR checks only when model confidence is low (Uncertainty Sampling).


## 📦 Tech Stack

-   **Frontend**: Next.js 14, Tailwind CSS, Framer Motion, Lucide Icons.
-   **Backend API**: FastAPI, Uvicorn, WebSockets.
-   **AI Engine**: PyTorch, HuggingFace Transformers, EasyOCR, Kafka-Python.
-   **Infrastructure**: Docker, Zookeeper, Kafka.

## 🏁 Quick Start

### 1. Start Infrastructure
```bash
docker compose up -d
```

### 2. Start the AI Engine
```bash
# Terminal 1: The Producer (Simulates News)
python3 src/pipeline/producer.py

# Terminal 2: The Consumer (AI Analysis)
python3 src/pipeline/consumer.py
```

### 3. Start the Real-Time API
```bash
# Terminal 3: WebSocket Server
uvicorn src.api.server:app --reload
```

### 4. Launch the Dashboard
```bash
# Terminal 4: Frontend
cd web
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the live analysis feed.

## 📷 Screenshots
<img width="1468" height="741" alt="image" src="https://github.com/user-attachments/assets/af317f4d-337a-4ef6-a068-9b03f4453f5d" />


## 📄 License
MIT
