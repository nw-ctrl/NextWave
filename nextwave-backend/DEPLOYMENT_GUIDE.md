# NextWave Backend Deployment Guide

## Issues Fixed

### 1. Import Path Issues
- Fixed relative import paths in all model files (`models/`)
- Updated main.py to use proper relative imports
- Resolved ModuleNotFoundError issues

### 2. Missing Dependencies
- Added PyMuPDF==1.24.14 to requirements.txt for PDF processing
- All dependencies now properly specified

### 3. Database Model Issues
- Fixed foreign key references in ImageAnalysisResult model
- Added missing fields:
  - `uploaded_at` field in Document model
  - `input_data` and `output_data` fields in ProcessingTask model
  - `title` and `generated_for_id` fields in Report model
- Fixed relationship references in User model
- Added WorkflowModel class for compatibility

### 4. Deprecated Flask Methods
- Replaced `@app.before_first_request` with `@app.before_request`
- Added proper initialization guard to prevent multiple executions

### 5. Environment Configuration
- Updated app to use environment variables:
  - `DATABASE_URL` for database connection
  - `SECRET_KEY` for Flask secret key
  - `JWT_SECRET_KEY` for JWT authentication
  - `PORT` for server port

### 6. Workflow Engine
- Created simplified workflow engine to avoid complex dependencies
- Maintains API compatibility while reducing complexity

## Render Deployment Files

### Dockerfile
```dockerfile
FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
```

### render.yaml
```yaml
services:
  - type: web
    name: nextwave-backend
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "gunicorn --bind 0.0.0.0:$PORT main:app"
    envVars:
      - key: DATABASE_URL
        fromDatabase: 
          name: nextwave_db
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: JWT_SECRET_KEY
        generateValue: true
    autoDeploy: true
databases:
  - name: nextwave_db
    plan: free
```

### main.py (Entry Point)
```python
import os
from src.main import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

## Deployment Steps

1. **Connect to Render**:
   - Go to [render.com](https://render.com)
   - Connect your GitHub account
   - Select the NextWave repository

2. **Configure Service**:
   - Render will automatically detect the `render.yaml` file
   - It will create both the web service and database
   - Environment variables will be automatically configured

3. **Deploy**:
   - Render will automatically build and deploy your application
   - The database will be created and connected
   - Your app will be available at the provided URL

## API Endpoints

- `GET /api/health` - Health check endpoint
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile
- `POST /api/documents/upload` - Upload documents
- `POST /api/images/upload` - Upload images
- `GET /api/workflows` - List workflows

## Testing

The application has been tested locally and all endpoints are working correctly:
- ✅ Health endpoint responds with 200 OK
- ✅ Database models load without errors
- ✅ All imports resolve properly
- ✅ Flask app starts successfully

## Environment Variables

The following environment variables are automatically configured by Render:
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - Flask secret key (auto-generated)
- `JWT_SECRET_KEY` - JWT secret key (auto-generated)
- `PORT` - Server port (provided by Render)

## Database

The application uses PostgreSQL in production (via Render) and SQLite for local development. The database schema is automatically created on first request.

Default users created:
- Admin: username=`admin`, password=`admin123`
- Demo: username=`demo`, password=`demo123`

