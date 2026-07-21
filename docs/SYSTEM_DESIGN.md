# Syntrix System Design

## High Level Architecture

```
                    Frontend (React)
                           │
                           ▼
                    FastAPI Backend
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   Authentication     Document API       AI Engine
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                     Service Layer
                           │
      ┌──────────────┬──────────────┬──────────────┐
      │              │              │
 PostgreSQL      ChromaDB        Redis
      │              │
      └──────────────┼──────────────┘
                     │
               LangChain RAG
                     │
             Gemini / OpenAI
                     │
              Business Insights
```

---

## Backend Responsibilities

### Authentication

- Register
- Login
- JWT
- Roles

---

### Document Module

- Upload files
- Store metadata
- Versioning

---

### AI Module

- Summaries
- Insights
- Recommendations

---

### RAG Module

- Chunk documents
- Create embeddings
- Semantic Search

---

### ML Module

- Sales prediction
- Revenue forecasting
- Customer churn prediction

---

## Database

- PostgreSQL → Business Data
- ChromaDB → Embeddings

---

## Deployment

- Docker
- GitHub Actions
- Render