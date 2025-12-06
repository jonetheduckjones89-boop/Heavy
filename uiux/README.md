# MedCore AI - Medical Document Automation Backend

A production-ready FastAPI backend for automated medical document processing with AI-powered classification, extraction, and action generation.

## 🏗️ Architecture

- **FastAPI** - Modern async web framework
- **PostgreSQL** - Relational database for structured data
- **Redis** - Message broker and caching
- **Celery** - Distributed task queue for background processing
- **SQLModel** - Type-safe ORM with Pydantic integration
- **OpenAI API** - LLM-powered document analysis

## 📋 Features

- ✅ Document upload and storage
- ✅ Async document processing pipeline
- ✅ AI-powered document classification
- ✅ Medical field extraction (patient info, medications, diagnoses, labs)
- ✅ Automated action generation
- ✅ Clinical summarization
- ✅ WebSocket support for real-time updates
- ✅ RESTful API with automatic documentation

## 🚀 Quick Start (Docker)

### Prerequisites
- Docker & Docker Compose
- (Optional) OpenAI API key for AI features

### Setup

1. **Clone and navigate to the project:**
   ```bash
   cd /Users/bexruzbek/Desktop/uiux
   ```

2. **Copy environment file:**
   ```bash
   cp .env.example .env
   ```

3. **Edit `.env` and configure:**
   - Set `SECRET_KEY` to a secure random string
   - Add `OPENAI_API_KEY` if using AI features
   - Adjust other settings as needed

4. **Start all services:**
   ```bash
   docker-compose up --build
   ```

5. **Initialize database (first time only):**
   ```bash
   docker-compose exec api python scripts/init_db.py
   ```

6. **Access the application:**
   - API: http://localhost:8000
   - Interactive API docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## 📡 API Endpoints

### Documents
- `POST /api/documents/upload` - Upload a document (PDF, DOCX, TXT)
- `GET /api/documents/{document_id}` - Get document status and results

### Patients
- `GET /api/patients` - List all patients

### Health
- `GET /api/health/ready` - Health check endpoint

### WebSocket
- `WS /ws/{room}` - Real-time updates

## 🧪 Testing the API

### Upload a document:
```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -F "file=@/path/to/medical-document.pdf" \
  -F "patient_id=optional-patient-id"
```

### Check document status:
```bash
curl "http://localhost:8000/api/documents/{document_id}"
```

## 🔧 Development Setup (Local)

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Redis 7+

### Installation

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your local database and Redis URLs
   ```

4. **Initialize database:**
   ```bash
   python scripts/init_db.py
   ```

5. **Run the API server:**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Run Celery worker (in separate terminal):**
   ```bash
   celery -A app.tasks.celery_app worker --loglevel=info -Q documents
   ```

## 📁 Project Structure

```
uiux/
├── app/
│   ├── api/
│   │   └── routes/          # API endpoints
│   │       ├── documents.py # Document upload & retrieval
│   │       ├── patients.py  # Patient management
│   │       └── health.py    # Health checks
│   ├── core/
│   │   └── config.py        # Configuration & settings
│   ├── services/
│   │   ├── ai_agent.py      # AI/LLM integration
│   │   ├── document_processor.py  # Text extraction
│   │   ├── storage.py       # File storage
│   │   ├── email_service.py # Email notifications
│   │   ├── calendar_service.py  # Meeting scheduling
│   │   └── connectors.py    # External integrations
│   ├── tasks/
│   │   ├── celery_app.py    # Celery configuration
│   │   └── workers.py       # Background tasks
│   ├── db.py                # Database setup
│   ├── models.py            # SQLModel schemas
│   ├── schemas.py           # Pydantic schemas
│   ├── crud.py              # Database operations
│   ├── websockets.py        # WebSocket manager
│   └── main.py              # FastAPI application
├── scripts/
│   └── init_db.py           # Database initialization
├── .env.example             # Environment template
├── requirements.txt         # Python dependencies
├── docker-compose.yml       # Docker orchestration
├── Dockerfile               # Container definition
└── README.md                # This file
```

## 🔐 Security Notes

**For Production:**
- ✅ Change `SECRET_KEY` to a strong random value
- ✅ Restrict CORS origins in `app/main.py`
- ✅ Use environment-specific `.env` files
- ✅ Enable HTTPS/TLS
- ✅ Implement authentication (JWT/OAuth)
- ✅ Use managed database services
- ✅ Store secrets in a vault (AWS Secrets Manager, HashiCorp Vault)
- ✅ Replace local storage with S3 or similar object storage
- ✅ Add rate limiting and input validation

## 🚢 Deployment

### Docker Deployment
The application is containerized and ready for deployment to:
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances
- Kubernetes clusters

### Environment Variables
Ensure all required environment variables are set in your deployment platform.

### Database Migrations
For production, use Alembic for database migrations:
```bash
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## 🤝 Contributing

1. Follow the existing code structure
2. Add type hints to all functions
3. Write docstrings for complex logic
4. Test endpoints before committing

## 📝 License

This project is for internal use. All rights reserved.

## 🆘 Troubleshooting

### Database connection errors
- Verify PostgreSQL is running
- Check `DATABASE_URL` in `.env`
- Ensure database exists: `createdb medcore`

### Celery worker not processing
- Verify Redis is running
- Check `REDIS_URL` in `.env`
- Ensure worker is running with correct queue name

### AI features not working
- Add valid `OPENAI_API_KEY` to `.env`
- Check API quota and billing
- Review logs for API errors

## 📧 Support

For issues or questions, contact the development team.
