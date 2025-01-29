# Use Node.js for frontend build
FROM node:18 AS frontend-builder
WORKDIR /frontend

# Copy package files first to leverage Docker cache
COPY frontend/package*.json ./

# Install dependencies including axios and babel plugin
RUN npm install && \
    npm install axios @babel/plugin-proposal-private-property-in-object --save-dev

# Copy frontend source
COPY frontend/ ./

# Build frontend
RUN npm run build

# Python backend with frontend files
FROM python:3.11.11
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy backend code
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini .

# Copy built frontend from previous stage
COPY --from=frontend-builder /frontend/build ./frontend/build

# Copy other necessary files
COPY runtime.txt .

# Set environment variables
ENV PORT=8000

# Start the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]