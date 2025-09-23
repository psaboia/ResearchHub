# ResearchHub - First Time Setup Guide

## Prerequisites
- Docker and Docker Compose installed
- Git installed
- Port 8000, 5432, and 6379 available

## Step-by-Step First Time Setup

### 1. Clone the Repository
```bash
git clone https://github.com/psaboia/ResearchHub.git
cd ResearchHub
```

### 2. Start All Services
```bash
docker-compose up -d
```
Wait ~10 seconds for services to start

### 3. Create Database Tables
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### 4. Load Test Data
```bash
docker-compose exec web python manage.py setup_test_data
```

### 5. Access the Application
Open your browser and go to: http://localhost:8000/admin/

Login with:
- Username: `admin`
- Password: `admin123`

## That's it! 🎉

The system is now running with:
- 3 research institutions
- 4 users (admin + 3 researchers)
- 3 research projects
- 3 datasets
- 2 data access requests

## Quick Test Commands

### Test the API (optional)
```bash
# Test the dashboard endpoint (has N+1 bug)
curl http://localhost:8000/api/projects/
```

### View Logs
```bash
docker-compose logs -f web
```

### Stop Everything
```bash
docker-compose down
```

### Restart Later
```bash
docker-compose up -d
# No need to run migrations again, data is preserved
```

## Alternative: Local Setup (without Docker)

If you prefer to run locally:

```bash
# 1. Clone repository
git clone https://github.com/psaboia/ResearchHub.git
cd ResearchHub

# 2. Install dependencies
uv init
uv add Django djangorestframework psycopg2-binary redis celery pandas numpy scipy boto3 python-decouple

# 3. Create .env file
cp .env.example .env

# 4. Start PostgreSQL and Redis (using Docker)
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres --name postgres postgres:14
docker run -d -p 6379:6379 --name redis redis:7

# 5. Create database
docker exec postgres psql -U postgres -c "CREATE DATABASE researchhub;"

# 6. Run migrations
uv run python manage.py makemigrations
uv run python manage.py migrate

# 7. Create test data
uv run python manage.py setup_test_data

# 8. Start server
uv run python manage.py runserver
```

## Troubleshooting

### Port 8000 already in use?
```bash
# Find and kill the process
lsof -i :8000
kill -9 <PID>
```

### Reset everything?
```bash
docker-compose down -v  # Remove volumes too
docker-compose up -d
# Then repeat steps 3-4
```

### Can't access http://localhost:8000?
```bash
# Check if containers are running
docker-compose ps

# Check web container logs
docker-compose logs web
```