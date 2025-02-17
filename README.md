# HackRx_Breakbot

### Overview
HackRx_Breakbot is an AI-powered chatbot that answers insurance-related queries, books appointments via API calls, and maintains chat memory for improved interactions. It utilizes Retrieval-Augmented Generation (RAG) with reranking for accurate responses.

### Tech Stack
- **Backend:** FastAPI, Pinecone, Cohere, Groq
- **Frontend:** React.js
- **LLM:** Groq LLaMA with RAG and reranking

### Features
- **Insurance Query Resolution**: Answers user queries based on uploaded insurance documents.
- **Appointment Booking**: Uses external API calls to book appointments.
- **Chat Memory**: Retains previous conversations for better contextual responses.
- **RAG with Reranking**: Retrieves relevant information and re-ranks responses for accuracy.
- **Admin UI**: Allows uploading PDFs to update the knowledge base.

### Installation

#### Prerequisites
- Python 3.10+
- Node.js 16+
- pip and virtualenv

#### Backend Setup
```bash
git clone https://github.com/your-repo/HackRx_Breakbot.git
cd HackRx_Breakbot/backend
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Frontend
```bash
cd ../frontend
npm install
npm run dev
```