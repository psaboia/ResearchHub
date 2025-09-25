# ResearchHub Testing Guide

## Quick Start Options

### Option 1: Using Docker Compose (Easiest)

```bash
# Start all services
docker-compose up

# In another terminal, run migrations and create test data
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py setup_test_data
```

Access the application at http://localhost:8000

### Option 2: Local Setup with PostgreSQL and Redis

1. **Start PostgreSQL and Redis:**
```bash
# macOS with Homebrew
brew services start postgresql
brew services start redis

# Or use Docker for just the databases
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres:14
docker run -d -p 6379:6379 redis:7
```

2. **Create database:**
```bash
psql -U postgres -c "CREATE DATABASE researchhub;"
```

3. **Set up the application:**
```bash
# Create .env file
cp .env.example .env

# Run migrations
uv run python manage.py migrate

# Create test data
uv run python manage.py setup_test_data

# Start the server
uv run python manage.py runserver
```

### Option 3: SQLite for Quick Testing (No PostgreSQL needed)

```bash
# Temporarily modify settings.py to use SQLite
# Change DATABASES setting to:
# 'ENGINE': 'django.db.backends.sqlite3',
# 'NAME': BASE_DIR / 'db.sqlite3',

uv run python manage.py migrate
uv run python manage.py setup_test_data
uv run python manage.py runserver
```

## Test Credentials

After running `setup_test_data`:

- **Admin**: admin / admin123
- **Test Users**:
  - alice / testpass123 (MIT)
  - bob / testpass123 (Stanford)
  - charlie / testpass123 (Oxford)

## Testing the Application

### 1. Test Project Dashboard
```bash
# View project dashboard with datasets
curl http://localhost:8000/api/projects/<project-id>/dashboard/
```

### 2. Test Dataset Download
```bash
# Download a dataset (requires proper permissions)
curl -X POST http://localhost:8000/api/datasets/<dataset-id>/download/
```

### 3. Test File Upload
```bash
# Upload a dataset file
curl -X POST -F "file=@test.csv" -F "project_id=<id>" http://localhost:8000/api/datasets/upload/
```

### 4. Test Dataset Statistics
```bash
# Get dataset usage statistics
curl http://localhost:8000/api/datasets/<id>/statistics/
```

### 5. Test Dataset Search
```bash
# Search for datasets
curl http://localhost:8000/api/datasets/search/?q=research
```

```

## Using Django Admin

1. Access admin at: http://localhost:8000/admin/
2. Login with: admin / admin123
3. You can create/edit/delete all models

## Using Django Shell

```bash
uv run python manage.py shell

# Test the models
from research.models import *
from django.contrib.auth.models import User

# Get all projects
projects = ResearchProject.objects.all()

# Get all datasets
for dataset in Dataset.objects.all():
    print(dataset.uploaded_by.username)

# Test the complex functions
from research.views import calculate_data_quality_metrics
metrics = calculate_data_quality_metrics(dataset_id)
```

## Testing with Celery

If you want to test background tasks:

```bash
# Start Celery worker
uv run celery -A config worker -l info

# Start Celery beat (for scheduled tasks)
uv run celery -A config beat -l info
```

## API Testing with HTTPie or cURL

```bash
# Install HTTPie for better API testing
pip install httpie

# Test endpoints
http GET localhost:8000/api/projects/
http POST localhost:8000/api/datasets/upload/ file@test.csv project_id=<id>
http GET localhost:8000/api/datasets/search/ q==ocean
```

## Monitoring

### Database Queries
Add to settings.py for development:
```python
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    },
}
```

### Redis Monitoring
```bash
redis-cli MONITOR
```

### PostgreSQL Monitoring
```sql
-- Connect to database
psql -U postgres -d researchhub

-- Show running queries
SELECT pid, age(clock_timestamp(), query_start), usename, query 
FROM pg_stat_activity 
WHERE query != '<IDLE>' AND query NOT ILIKE '%pg_stat_activity%' 
ORDER BY query_start desc;
```

## Troubleshooting

### Port Already in Use
```bash
# Find and kill process using port 8000
lsof -i :8000
kill -9 <PID>
```

### Database Connection Issues
```bash
# Check PostgreSQL is running
pg_isready

# Check Redis is running
redis-cli ping
```

### Migration Issues
```bash
# Reset database
uv run python manage.py flush --no-input
uv run python manage.py migrate
uv run python manage.py setup_test_data
```