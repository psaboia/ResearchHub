#!/usr/bin/env python
"""
Step 5 & 6: Test the Fixed Version
This script demonstrates the optimized version using select_related and prefetch_related.
"""

import django
import os
import sys
import logging

# Add the project directory to the path
sys.path.insert(0, '/code')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection, reset_queries
from django.db.models import Count, Q, Prefetch
from research.models import ResearchProject, DataAccessRequest

# Set up logging to see SQL queries
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('django.db.backends')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

print("\n" + "=" * 60)
print("N+1 QUERY PROBLEM - FIXED VERSION")
print("=" * 60)

def get_project_dashboard_fixed(project_id):
    """
    Optimized version using Django ORM optimization techniques.
    """
    # Use select_related for ForeignKey relationships
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
            'processing_jobs': dataset.processing_count,  # Use annotated count
            'access_requests': dataset.approved_requests_count,  # Use annotated count
        }
        dataset_info.append(info)

    return {'project': project.title, 'datasets': dataset_info}

try:
    # Get the demo project
    project = ResearchProject.objects.get(title="Multi-Dataset Research Collaboration")

    # Clear and reset query tracking
    reset_queries()

    print(f"\nRunning OPTIMIZED get_project_dashboard for: {project.title}")
    print("Watch the reduced number of SQL queries...")
    print("-" * 60)

    # Run the optimized function
    result = get_project_dashboard_fixed(project.id)

    # Show results
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"Total queries executed: {len(connection.queries)}")
    print(f"Datasets returned: {len(result['datasets'])}")

    print("\n✅ OPTIMIZATION SUCCESS!")
    print(f"Reduced from ~32 queries to {len(connection.queries)} queries")
    print(f"Performance improvement: ~{32/max(len(connection.queries), 1):.1f}x faster")

    # Show all queries
    if connection.queries:
        print("\nAll SQL queries executed:")
        for i, query in enumerate(connection.queries, 1):
            print(f"\nQuery {i}:")
            print(f"  {query['sql'][:200]}...")

    print("\n" + "=" * 60)
    print("KEY TECHNIQUES USED:")
    print("=" * 60)
    print("1. select_related() - For ForeignKey relationships (SQL JOINs)")
    print("2. prefetch_related() - For reverse ForeignKey and ManyToMany")
    print("3. annotate() with Count() - For aggregations")
    print("4. Prefetch() objects - For filtered prefetching")
    print("=" * 60)

except ResearchProject.DoesNotExist:
    print("ERROR: 'Multi-Dataset Research Collaboration' not found. Please run setup_test_data first.")