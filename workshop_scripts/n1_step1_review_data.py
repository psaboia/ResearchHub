#!/usr/bin/env python
"""
Step 1: Review the Data Structure
This script shows the test data created for the N+1 query demonstration.
"""

import django
import os
import sys

# Add the project directory to the path
sys.path.insert(0, '/code')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from research.models import ResearchProject, Dataset, DataProcessingJob, DataAccessRequest

print("=" * 60)
print("N+1 QUERY DEMO - DATA STRUCTURE REVIEW")
print("=" * 60)

# Get our demo project
try:
    user = User.objects.get(username="researcher1")
    project = ResearchProject.objects.get(title="Multi-Dataset Research Collaboration")

    print(f"\nProject: {project.title}")
    print(f"Owner: {project.principal_investigator.username}")
    print(f"Datasets: {project.datasets.count()}")

    # Examine the data relationships
    sample_dataset = project.datasets.first()
    if sample_dataset:
        print(f"\nSample Dataset: {sample_dataset.name}")
        print(f"  - Uploaded by: {sample_dataset.uploaded_by.username}")
        print(f"  - Processing jobs: {sample_dataset.processing_jobs.count()}")
        print(f"  - Access requests: {sample_dataset.access_requests.count()}")
        print(f"  - Approved requests: {sample_dataset.access_requests.filter(status='approved').count()}")

    print("\n⚠️  KEY INSIGHT:")
    print("When we loop through all 10 datasets and access these relationships,")
    print("each relationship access triggers a separate database query.")
    print("This is the N+1 problem: 1 query for datasets + N queries per relationship!")
    print("=" * 60)

except User.DoesNotExist:
    print("ERROR: User 'researcher1' not found. Please run setup_test_data first.")
except ResearchProject.DoesNotExist:
    print("ERROR: 'Multi-Dataset Research Collaboration' not found. Please run setup_test_data first.")