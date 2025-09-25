# ResearchHub - Scientific Research Data Management Platform

A Django-based platform for managing research data, facilitating collaboration between institutions, and ensuring data quality and compliance.

## Overview

This platform supports research teams in:
- Uploading and processing experimental datasets
- Managing data access permissions across institutions
- Running automated data quality checks
- Processing data through configurable pipelines
- Tracking data lineage and audit trails

## Tech Stack

- **Backend**: Django 5.2 + Django REST Framework
- **Database**: PostgreSQL
- **Task Queue**: Celery + Redis
- **Data Processing**: pandas, numpy, scipy
- **File Storage**: Local filesystem + AWS S3 (for large files)
- **Containerization**: Docker

## Project Structure

```
ResearchHub/
├── config/                 # Django project settings
├── research/               # Main research app
│   ├── models.py          # Data models
│   ├── views.py           # API endpoints  
│   ├── serializers.py     # DRF serializers
│   └── tasks.py           # Celery tasks
├── authentication/         # Auth and permissions
└── media/                  # Uploaded files
```

## Key Features

### Data Management
- Upload datasets in multiple formats (CSV, Excel, JSON, HDF5, Parquet)
- Automatic file validation and quality checks
- Metadata extraction and indexing
- Version control for datasets

### Collaboration
- Cross-institutional data sharing
- Role-based access control
- Data access request workflow
- Audit logging for compliance

### Processing Pipeline
- Configurable data processing workflows
- Background job processing with Celery
- Statistical analysis tools
- Data quality metrics calculation

## Setup Instructions

1. Create virtual environment:
```bash
uv init
uv add Django djangorestframework psycopg2-binary redis celery pandas numpy scipy boto3
```

2. Configure PostgreSQL database

3. Create `.env` file:
```
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=researchhub
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
REDIS_HOST=localhost
REDIS_PORT=6379
```

4. Run migrations:
```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
```

5. Create superuser:
```bash
uv run python manage.py createsuperuser
```

6. Run development server:
```bash
uv run python manage.py runserver
```

## API Endpoints

### Projects
- `GET /api/projects/` - List research projects
- `GET /api/projects/<id>/dashboard/` - Project dashboard with datasets
- `POST /api/projects/` - Create new project

### Datasets
- `POST /api/datasets/upload/` - Upload new dataset
- `GET /api/datasets/<id>/` - Get dataset details
- `POST /api/datasets/<id>/download/` - Download dataset
- `GET /api/datasets/<id>/statistics/` - Get usage statistics
- `GET /api/datasets/search/?q=<term>` - Search datasets

### Data Processing
- `POST /api/processing/start/` - Start processing job
- `GET /api/processing/<job_id>/status/` - Check job status
- `POST /api/workflow/execute/` - Execute workflow

### Access Management
- `POST /api/access-requests/` - Request dataset access
- `PUT /api/access-requests/<id>/approve/` - Approve access request

## Contributing

Please follow Django best practices and ensure all code is properly tested before submitting pull requests.

## Development Notes

- Use Django Debug Toolbar for query optimization
- Monitor Redis for queue backlog
- Check Celery flower for task monitoring
- Use pgAdmin for database inspection

## Testing

Run tests with:
```bash
uv run python manage.py test
```

## License

Internal use only - Research Institution