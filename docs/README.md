# ResearchHub Documentation

## Getting Started

### Quick Setup

```bash
git clone https://github.com/psaboia/ResearchHub.git
cd ResearchHub
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py setup_test_data
```

### Access Credentials

- **Admin**: admin / admin123
- **Test Users**: alice, bob, charlie (password: testpass123)
- **Research User**: researcher1 / testpass123

### Key URLs

- Django Admin: http://localhost:8000/admin/
- API Root: http://localhost:8000/api/

## Available Documentation

| Document | Purpose |
|----------|---------|
| [QUICKSTART.md](QUICKSTART.md) | Quick setup guide |
| [User Guide](https://github.com/psaboia/ResearchHub/wiki/RSE-Up%E2%80%90Skilling-Training%E2%80%90Week3) | Workshop exercises and learning objectives |
| [TESTING_GUIDE.md](TESTING_GUIDE.md) | Testing documentation |

## System Overview

ResearchHub is a Django-based platform for managing research data, projects, and collaboration between institutions. The platform provides:

- User authentication and authorization
- Research project management
- Dataset upload and processing
- Data access request workflows
- Audit logging and analytics

## Development Setup

For local development without Docker:

```bash
# Create virtual environment
uv venv

# Install dependencies
uv pip install -r requirements.txt

# Set up database
uv run python manage.py migrate
uv run python manage.py setup_test_data

# Start development server
uv run python manage.py runserver
```