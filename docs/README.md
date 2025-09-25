# ResearchHub Documentation

## Overview

ResearchHub is a Django-based platform for managing research data, facilitating collaboration between institutions, and ensuring data quality and compliance.

## Getting Started

### Quick Setup
```bash
git clone https://github.com/psaboia/ResearchHub.git
cd ResearchHub
docker-compose up -d
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py setup_test_data
```

### Access Credentials
- **Admin**: admin / admin123
- **Test Users**: alice, bob, charlie, researcher1 (password: testpass123)

### Key URLs
- Django Admin: http://localhost:8000/admin/
- API Root: http://localhost:8000/api/

## Available Guides

- **[QUICKSTART.md](QUICKSTART.md)** - Quick setup guide to get the system running
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Testing documentation for all features

## System Features

- Research project management
- Dataset upload and processing
- Data access control and permissions
- Cross-institutional collaboration
- Audit logging and compliance tracking