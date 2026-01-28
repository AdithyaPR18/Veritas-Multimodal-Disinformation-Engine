# Veritas: Real-Time Multimodal Disinformation Engine

![React](https://img.shields.io/badge/前端-Next.js_14-blue)
![Python](https://img.shields.io/badge/Backend-FastAPI-green)
![AI](https://img.shields.io/badge/AI-PyTorch_&_Transformers-orange)
![Infra](https://img.shields.io/badge/Infra-Docker_&_Kafka-blueviolet)

**Veritas** is a high-performance, event-driven pipeline designed to detect disinformation in real-time. It processes multimodal news articles (Text + Image) using a deep learning model to assign an authenticity score. If the model is uncertain, it triggers a secondary OCR (Optical Character Recognition) check to verify semantic consistency between the headline and the image text.

## 🚀 Key Features

*   **Real-Time Event Stream**: Built on Apache Kafka for high-throughput data ingestion.
*   **Multimodal AI**: Custom PyTorch model fusing BERT (Text) and ResNet50 (Vision).
*   **Live Mission Control**: A "Minority Report" style dashboard built with Next.js, Framer Motion, and WebSockets.
*   **Adaptive Verification**: Automatically triggers expensive OCR checks only when model confidence is low (Uncertainty Sampling).

## 🛠 Architecture

```mermaid
graph LR
    A[Producer (News Source)] -->|JSON Articles| B(Kafka Topic: veritas-articles)
    B --> C[Consumer (AI Engine)]
    C -->|Inference| D{Confidence Score}
    D -->|High/Low| E[Result Stream]
    D -->|Uncertain (0.4-0.6)| F[OCR Module]
    F --> E
    E -->|JSON Results| G(Kafka Topic: veritas-results)
    G --> H[FastAPI WebSocket Server]
    H -->|ws://| I[Next.js Dashboard]
```

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
*(Add screenshots of your dashboard here)*

## 📄 License
MIT
