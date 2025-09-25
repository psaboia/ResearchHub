# ResearchHub Documentation

## Workshop Materials

### For Participants
- **[QUICKSTART.md](QUICKSTART.md)** - Quick setup guide to get the system running
- **[WORKSHOP_GUIDE.md](WORKSHOP_GUIDE.md)** - Workshop exercises and learning objectives

### For Instructors
- **[INSTRUCTOR_GUIDE_REVISED.md](INSTRUCTOR_GUIDE_REVISED.md)** ⭐ - **Recommended** - Streamlined guide with links to detailed exercises
- **[INSTRUCTOR_GUIDE.md](INSTRUCTOR_GUIDE.md)** - Original complete facilitation guide
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Comprehensive testing documentation for all features and bugs

### Detailed Exercise Guides (For Instructors)
- **[N1_QUERY_DEMONSTRATION.md](N1_QUERY_DEMONSTRATION.md)** - N+1 query problem with Django ORM (~10 min)
- **[CACHE_BUG_DEMONSTRATION.md](CACHE_BUG_DEMONSTRATION.md)** - Cache invalidation issues (~10 min)
- **[SECURITY_BUG_DEMONSTRATION.md](SECURITY_BUG_DEMONSTRATION.md)** - Authorization vulnerability (~12 min)
- **[RACE_CONDITION_DEMONSTRATION.md](RACE_CONDITION_DEMONSTRATION.md)** - Concurrent file upload collisions (~13 min)
- **[DOCUMENTATION_EXERCISE.md](DOCUMENTATION_EXERCISE.md)** - Generating documentation with AI (~25 min)

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
| **INSTRUCTOR_GUIDE_REVISED** ⭐ | Streamlined workshop facilitation with links | Workshop instructors |
| INSTRUCTOR_GUIDE | Original detailed teaching script | Workshop instructors |
| TESTING_GUIDE | Complete testing documentation | Developers & testers |
| N1_QUERY_DEMONSTRATION | Step-by-step N+1 query bug exercise | Instructors |
| CACHE_BUG_DEMONSTRATION | Step-by-step cache invalidation exercise | Instructors |
| SECURITY_BUG_DEMONSTRATION | Step-by-step authorization bug exercise | Instructors |
| RACE_CONDITION_DEMONSTRATION | Step-by-step race condition exercise | Instructors |
| DOCUMENTATION_EXERCISE | Progressive documentation generation | Instructors |

## Workshop Structure

**Week 3: Context-Aware Prompt Engineering**
- Duration: 90 minutes
- Focus: Using AI tools effectively with production code
- Method: Documentation first, then bug fixing
- Goal: Learn how context improves AI responses

### Workshop Flow

```
INSTRUCTOR_GUIDE_REVISED.md (Main Guide)
    │
    ├── Introduction (10 min)
    │
    ├── Setup (10 min) → QUICKSTART.md
    │
    ├── Part 1: Documentation (25 min) → DOCUMENTATION_EXERCISE.md
    │
    ├── Part 2: Bug Fixing (35 min)
    │   ├── Group A → CACHE_BUG_DEMONSTRATION.md
    │   ├── Group B → SECURITY_BUG_DEMONSTRATION.md
    │   └── Group C → RACE_CONDITION_DEMONSTRATION.md
    │
    ├── Part 3: Refinement (15 min) → N1_QUERY_DEMONSTRATION.md
    │
    └── Wrap-up (10 min)
```

### Which Guide Should I Use?

- **Instructors running the workshop**: Start with INSTRUCTOR_GUIDE_REVISED.md
- **Participants**: Use QUICKSTART.md, then follow instructor's guidance
- **Self-study**: Work through each demonstration guide in order