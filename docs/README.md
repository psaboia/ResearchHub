# ResearchHub Documentation

## Workshop Materials

### For Participants
- **[QUICKSTART.md](QUICKSTART.md)** - Quick setup guide to get the system running
- **[WORKSHOP_GUIDE.md](WORKSHOP_GUIDE.md)** - Workshop exercises and learning objectives

### For Instructors  
- **[INSTRUCTOR_GUIDE.md](INSTRUCTOR_GUIDE.md)** - Complete facilitation guide with step-by-step instructions
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Comprehensive testing documentation for all features and bugs

## Quick Links

### Essential Setup Commands
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
- **Test Users**: alice, bob, charlie (password: testpass123)

### Key URLs
- Django Admin: http://localhost:8000/admin/
- API Root: http://localhost:8000/api/

## Document Overview

| Document | Purpose | Audience |
|----------|---------|----------|
| QUICKSTART | Get system running quickly | Everyone |
| WORKSHOP_GUIDE | Exercise instructions and prompt examples | Workshop participants |
| INSTRUCTOR_GUIDE | Detailed teaching script with demonstrations | Workshop instructors |
| TESTING_GUIDE | Complete testing documentation | Developers & testers |

## Workshop Structure

**Week 3: Context-Aware Prompt Engineering**
- Duration: 90 minutes
- Focus: Using AI tools effectively with production code
- Method: Documentation first, then bug fixing
- Goal: Learn how context improves AI responses