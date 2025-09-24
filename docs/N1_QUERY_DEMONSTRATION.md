# Complete Step-by-Step N+1 Query Demonstration

## Step 1: Setup Database Logging and Create Test Data

```bash
# First, ensure Docker is running and enter the Django shell
docker-compose exec web python manage.py shell
```

```python
# In the Django shell, set up logging to see SQL queries
import logging
import django
django.setup()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('django.db.backends')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

# Import necessary models
from django.contrib.auth.models import User
from research.models import Institution, ResearchProject, Dataset, DataProcessingJob, DataAccessRequest
from datetime import date, datetime
import uuid

# Create test data if not exists
institution, _ = Institution.objects.get_or_create(
    name="Test University",
    defaults={"country": "USA", "address": "123 Research Ave"}
)

# Create a user with profile (Note: The profile relationship is missing - this is part of the bug!)
user, _ = User.objects.get_or_create(username="researcher1")

# Create a project with multiple datasets
project, _ = ResearchProject.objects.get_or_create(
    title="N+1 Test Project",
    defaults={
        "description": "Project to demonstrate N+1 queries",
        "institution": institution,
        "principal_investigator": user,
        "start_date": date.today(),
        "status": "active"
    }
)

# Create 10 datasets with processing jobs and access requests
for i in range(10):
    dataset, created = Dataset.objects.get_or_create(
        name=f"Test Dataset {i+1}",
        project=project,
        defaults={
            "description": f"Dataset {i+1} for testing",
            "file_type": "csv",
            "file_size": 1000000,
            "file_path": f"/data/test_{i+1}.csv",
            "uploaded_by": user,
            "privacy_level": "private"
        }
    )

    if created:
        # Add 3 processing jobs per dataset
        for j in range(3):
            DataProcessingJob.objects.create(
                dataset=dataset,
                job_type="quality_check",
                status="completed",
                created_by=user
            )

        # Add 2 approved access requests per dataset
        for k in range(2):
            requester, _ = User.objects.get_or_create(username=f"user_{k+2}")
            DataAccessRequest.objects.get_or_create(
                dataset=dataset,
                requester=requester,
                defaults={
                    "requester_institution": institution,
                    "status": "approved",
                    "reason": "Research purposes"
                }
            )

print(f"Created project '{project.title}' with {project.datasets.count()} datasets")
```

## Step 2: Demonstrate the N+1 Problem

**Note:** The original view has a bug - it tries to access `user.profile.institution` but the profile relationship doesn't exist. We'll demonstrate the N+1 problem by commenting out that line.

```python
# Clear the console and reset query tracking
from django.db import connection, reset_queries
reset_queries()

# Now call the problematic view function
from research.views import get_project_dashboard
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

# Create a fake request
factory = APIRequestFactory()
request = factory.get(f'/api/projects/{project.id}/dashboard/')
force_authenticate(request, user=user)

# Execute the view and count queries
print("\n" + "="*60)
print("BEFORE FIX - Executing get_project_dashboard view:")
print("="*60)

try:
    response = get_project_dashboard(request, project.id)
except AttributeError as e:
    print(f"ERROR: {e}")
    print("The view tries to access 'profile' which doesn't exist!")
    print(f"Queries executed before error: {len(connection.queries)}")

# To see the full N+1 problem, temporarily comment out line 43 in views.py
# Or use this modified version that skips the profile access:

def get_project_dashboard_demo(project_id):
    from research.models import ResearchProject
    project = ResearchProject.objects.get(id=project_id)
    datasets = project.datasets.all()

    dataset_info = []
    for dataset in datasets:
        info = {
            'id': str(dataset.id),
            'name': dataset.name,
            'uploaded_by': dataset.uploaded_by.username,  # N+1: query per user
            # 'institution': dataset.uploaded_by.profile.institution.name,  # Skip - no profile
            'processing_jobs': dataset.processing_jobs.count(),  # N+1: query per dataset
            'access_requests': dataset.access_requests.filter(status='approved').count(),  # N+1
        }
        dataset_info.append(info)

    return {'project': project.title, 'datasets': dataset_info}

# Run the demo version
reset_queries()
result = get_project_dashboard_demo(project.id)
print(f"\nTotal queries executed: {len(connection.queries)}")
print("\nFirst 5 queries:")
for i, query in enumerate(connection.queries[:5], 1):
    print(f"\nQuery {i}: {query['sql'][:100]}...")

print("\n... and many more similar queries for each dataset!")
```

**Expected Output:**
```
Total queries executed: 32
(1 for project + 1 for datasets + 10 for users + 10 for processing_jobs count + 10 for access_requests)
```

## Step 3: Show the Problem in Code

```bash
# Exit Django shell
exit()
```

Now let's examine the problematic code:

```bash
# Show the problematic view
docker-compose exec web python -c "
import ast
with open('research/views.py', 'r') as f:
    lines = f.readlines()
    print(''.join(lines[30:50]))
"
```

**The Problem Explained:**
```
Line 42: dataset.uploaded_by.username - Triggers 1 query per dataset (10 queries)
Line 43: dataset.uploaded_by.profile.institution.name - FAILS! No profile relationship exists
Line 44: dataset.processing_jobs.count() - Triggers 1 query per dataset (10 queries)
Line 45: dataset.access_requests.filter(status='approved').count() - Triggers 1 query per dataset (10 queries)

Total: 32 queries for 10 datasets (should be only 3-4 with proper optimization)
```

## Step 4: Apply the Fix

Create a fixed version of the view:

```python
# Create a fixed version file
docker-compose exec web python -c "
fixed_code = '''from django.db.models import Count, Q, Prefetch
from rest_framework.decorators import api_view
from rest_framework.response import Response
from research.models import ResearchProject, DataAccessRequest

@api_view(['GET'])
def get_project_dashboard_fixed(request, project_id):
    # Use select_related for ForeignKey relationships
    # Use prefetch_related for reverse ForeignKey and ManyToMany
    project = ResearchProject.objects.select_related(
        'institution',
        'principal_investigator'
    ).get(id=project_id)

    # Prefetch access requests with specific filtering
    approved_requests = Prefetch(
        'access_requests',
        queryset=DataAccessRequest.objects.filter(status='approved'),
        to_attr='approved_access_requests'
    )

    # Optimize dataset query with all related data
    datasets = project.datasets.select_related(
        'uploaded_by',  # Get user in one query
    ).prefetch_related(
        'processing_jobs',  # Get all processing jobs
        approved_requests,  # Get filtered access requests
    ).annotate(
        processing_count=Count('processing_jobs'),
        approved_requests_count=Count('access_requests', filter=Q(access_requests__status='approved'))
    )

    dataset_info = []
    for dataset in datasets:
        info = {
            'id': str(dataset.id),
            'name': dataset.name,
            'uploaded_by': dataset.uploaded_by.username,
            # Note: Profile doesn't exist in the models, so removing institution reference
            # In real fix, would need to add UserProfile model or use Institution differently
            'processing_jobs': dataset.processing_count,  # Use annotated count
            'access_requests': dataset.approved_requests_count,  # Use annotated count
        }
        dataset_info.append(info)

    return Response({'project': project.title, 'datasets': dataset_info})
'''

with open('research/views_fixed.py', 'w') as f:
    f.write(fixed_code)
print('Fixed view saved to research/views_fixed.py')
"
```

## Step 5: Test the Fixed Version

```bash
docker-compose exec web python manage.py shell
```

```python
# Import and setup logging again
import logging
import django
django.setup()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('django.db.backends')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

from django.db import connection, reset_queries
from django.contrib.auth.models import User
from research.models import ResearchProject
from rest_framework.test import APIRequestFactory, force_authenticate

# Import the fixed version
import sys
sys.path.insert(0, '/app')
from research.views_fixed import get_project_dashboard_fixed

# Get test data
user = User.objects.get(username="researcher1")
project = ResearchProject.objects.get(title="N+1 Test Project")

# Create request
factory = APIRequestFactory()
request = factory.get(f'/api/projects/{project.id}/dashboard/')
force_authenticate(request, user=user)

# Clear queries and run fixed version
reset_queries()

print("\n" + "="*60)
print("AFTER FIX - Executing get_project_dashboard_fixed view:")
print("="*60)

response = get_project_dashboard_fixed(request, project.id)

print(f"\nTotal queries executed: {len(connection.queries)}")
print("\nAll queries:")
for i, query in enumerate(connection.queries, 1):
    print(f"\nQuery {i}: {query['sql'][:150]}...")

print(f"\nResponse data sample: {response.data['datasets'][0] if response.data['datasets'] else 'No data'}")
```

**Expected Output:**
```
Total queries executed: 4-5
(1 for project with relations + 1 for datasets with users + 1 for processing_jobs + 1 for access_requests)
```

## Step 6: Performance Comparison Summary

```python
print("\n" + "="*60)
print("PERFORMANCE COMPARISON SUMMARY")
print("="*60)
print(f"""
For a project with 10 datasets:

BEFORE OPTIMIZATION:
- Queries: 32 queries (without the broken profile access)
- Pattern: 2 + N*3 (where N = number of datasets)
- Time complexity: O(N)

AFTER OPTIMIZATION:
- Queries: 4-5 queries
- Pattern: Fixed number regardless of datasets
- Time complexity: O(1)

IMPROVEMENT: ~8x reduction in database queries!

Key Techniques Used:
1. select_related() - For ForeignKey relationships (joins)
2. prefetch_related() - For reverse ForeignKey and ManyToMany
3. annotate() with Count() - For aggregations
4. Prefetch() objects - For filtered prefetching
""")
```

## Instructor Notes for Demonstration

### 1. Start Simple
First show the bad prompt "Fix the bug" and let AI give generic advice

### 2. Add Context Gradually:
- "Fix the performance issue in get_project_dashboard"
- "Fix the N+1 query problem in get_project_dashboard"
- "Fix the N+1 query problem in get_project_dashboard using Django's select_related and prefetch_related"

### 3. Best Prompt Example:
```
"Analyze the get_project_dashboard view for N+1 query problems:
1. The view is at research/views.py lines 31-49
2. Each dataset access triggers queries for: uploaded_by, profile.institution, processing_jobs.count(), access_requests filtering
3. Fix using:
   - select_related() for ForeignKey fields
   - prefetch_related() for reverse relationships
   - Count annotations for aggregations
4. The models are in research/models.py
5. Show the complete optimized code"
```

### 4. Common Issues to Address:
- The `profile` relationship doesn't exist (intentional bug in the original code!)
- The view will fail when trying to access `dataset.uploaded_by.profile.institution.name`
- Need to use Prefetch objects for filtered relationships
- Difference between select_related (SQL JOIN) and prefetch_related (separate query)

### 5. Important Notes for Instructors:
- The original view in `research/views.py` line 43 will throw an AttributeError
- This is intentional to show how N+1 problems often hide behind other bugs
- Have participants comment out line 43 or use the demo function provided
- With 10 datasets, you'll see ~32 queries instead of 4-5 optimal queries

## Teaching Points to Emphasize

### Poor Context Example
**Prompt:** "Fix the bug"
**Result:** Generic suggestions, no specific solution

### Better Context Example
**Prompt:** "Fix the performance issue in the dashboard view"
**Result:** May suggest caching or indexing, still missing the real issue

### Good Context Example
**Prompt:** "Fix the N+1 query problem in get_project_dashboard view at lines 31-49. The issue is with accessing related objects in the loop."
**Result:** Will identify the N+1 problem and suggest select_related/prefetch_related

### Excellent Context Example
**Prompt:**
```
Analyze the get_project_dashboard view for N+1 query problems:
- File: research/views.py, lines 31-49
- Problem: Each dataset in the loop accesses uploaded_by.username, uploaded_by.profile.institution.name, processing_jobs.count(), and filters access_requests
- Models are defined in research/models.py
- Use Django ORM optimization: select_related for ForeignKeys, prefetch_related for reverse relationships
- Show the complete fixed code with proper imports
```
**Result:** Complete, working solution with all optimizations