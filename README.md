# Multi-Tenant RAG Chatbot

A production-ready Retrieval-Augmented Generation (RAG) chatbot application. This project features a **FastAPI** backend integrated with **PostgreSQL (pgvector)** for semantic search and a **React** frontend chat widget.

## 🚀 Features

-   **RAG Architecture**: Ingests PDF documents, generates semantic embeddings via OpenAI, and retrieves relevant context for LLM responses.
-   **Hybrid Search**: Combines vector similarity (`pgvector`) with keyword-based search for improved accuracy.
-   **Multi-Tenancy**: Support for isolated data and configurations per `tenant_id`.
-   **Persistent Session Memory**: Chat history is maintained across sessions using a combination of database storage and frontend `localStorage`.
-   **PDF Ingestion Pipeline**: Automated text extraction, chunking, and embedding storage for uploaded documents.
-   **Embeddable UI**: A clean, modern React chat widget with citation support for source documents.
-   **CI/CD Ready**: Automated deployment configuration for Azure Static Web Apps.

## 🛠️ Tech Stack

### Backend
-   **Framework**: FastAPI
-   **Database**: PostgreSQL with `pgvector` extension
-   **ORM**: SQLAlchemy
-   **AI**: OpenAI API (GPT-3.5/4 & Embeddings)
-   **Containerization**: Docker & Docker Compose

### Frontend
-   **Library**: React 18
-   **Build Tool**: Create React App / Webpack
-   **Deployment**: Azure Static Web Apps

## 📂 Project Structure

```text
sanjay-labs/
├── chatbot/
│   ├── backend/            # FastAPI application
│   │   ├── services/       # Chat, Retrieval, and Ingestion logic
│   │   ├── main.py         # API entry point & routing
│   │   ├── models.py       # DB Schema (Documents, History)
│   │   └── db.py           # SQLAlchemy & pgvector config
│   ├── frontend/           # React application
│   │   ├── src/
│   │   │   ├── ChatBot.js  # Main Chat UI component
│   │   │   └── SourceCitation.js # RAG source display
│   │   └── package.json
└── .github/workflows/      # Azure Deployment CI/CD
```

## ⚙️ Setup & Installation

### Prerequisites
-   Python 3.10+
-   Node.js (v16+)
-   PostgreSQL with `pgvector`
-   OpenAI API Key

### Backend Configuration
1.  Navigate to `/chatbot/backend`.
2.  Create a `.env` file:
    ```env
    OPENAI_API_KEY=your_openai_key
    OPENAI_MODEL=gpt-3.5-turbo
    DB_USER=your_user
    DB_PASSWORD=your_password
    DB_HOST=your_host
    DB_PORT=5432
    DB_NAME=your_db
    ```
3.  Install dependencies: `pip install -r requirements.txt`
4.  Run server: `uvicorn main:app --reload --port 5000`

### Frontend Configuration
1.  Navigate to `/chatbot/frontend`.
2.  Install dependencies: `npm install`
3.  Update the API endpoint in `ChatBot.js` if deploying to a different environment.
4.  Start development: `npm start`

## 🐳 Docker Deployment

The project includes Docker support for both the backend and any required services (like Redis or PostgreSQL).

```bash
docker compose up --build -d
```

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/ask` | Submit a query to the RAG chatbot |
| `POST` | `/upload-pdf` | Upload and index a document |
| `GET` | `/documents` | List all ingested source files |
| `DELETE` | `/documents/{name}`| Remove a specific document and its embeddings |
| `GET` | `/chat-history` | Fetch history for a specific session |