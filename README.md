# Meeting Summarizer

A tool for automatically summarizing meeting transcripts and recordings.

## Setup

### Prerequisites
- Python 3.11+
- Node.js 16+
- PostgreSQL

### Installation
1. Clone the repository
2. Install backend dependencies: `pip install -r requirements.txt`
3. Install frontend dependencies: `cd frontend && npm install`
4. Copy `.env.example` to `.env` and configure your environment variables
5. Run database migrations: `alembic upgrade head`

### Running the Application
1. Start the backend: `uvicorn app.main:app --reload`
2. Start the frontend: `cd frontend && npm start`

## Development

### Backend
- FastAPI for the REST API
- SQLAlchemy for database ORM
- Alembic for database migrations

### Frontend
- React
- Tailwind CSS 