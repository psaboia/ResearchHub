#!/usr/bin/env python
"""
Step 7: Performance Comparison Summary
This script runs both versions and shows the performance difference.
"""

import django
import os
import sys

# Add the project directory to the path
sys.path.insert(0, '/code')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection, reset_queries
from django.db.models import Count, Q, Prefetch
from research.models import ResearchProject, DataAccessRequest

def run_problematic_version(project):
    """Run the version with N+1 queries."""
    datasets = project.datasets.all()

    dataset_info = []
    for dataset in datasets:
        info = {
            'name': dataset.name,
            'uploaded_by': dataset.uploaded_by.username,  # N+1
            'processing_jobs': dataset.processing_jobs.count(),  # N+1
            'access_requests': dataset.access_requests.filter(status='approved').count(),  # N+1
        }
        dataset_info.append(info)

    return dataset_info

def run_optimized_version(project_id):
    """Run the optimized version."""
    project = ResearchProject.objects.select_related(
        'institution',
        'principal_investigator'
    ).get(id=project_id)

    approved_requests = Prefetch(
        'access_requests',
        queryset=DataAccessRequest.objects.filter(status='approved'),
        to_attr='approved_access_requests'
    )

    datasets = project.datasets.select_related(
        'uploaded_by',
    ).prefetch_related(
        'processing_jobs',
        approved_requests,
    ).annotate(
        processing_count=Count('processing_jobs'),
        approved_requests_count=Count('access_requests', filter=Q(access_requests__status='approved'))
    )

    dataset_info = []
    for dataset in datasets:
        info = {
            'name': dataset.name,
            'uploaded_by': dataset.uploaded_by.username,
            'processing_jobs': dataset.processing_count,
            'access_requests': dataset.approved_requests_count,
        }
        dataset_info.append(info)

    return dataset_info

print("=" * 60)
print("PERFORMANCE COMPARISON: N+1 Problem vs Optimized")
print("=" * 60)

try:
    project = ResearchProject.objects.get(title="Multi-Dataset Research Collaboration")

    # Test problematic version
    print("\n📊 PROBLEMATIC VERSION (with N+1 queries)")
    print("-" * 40)
    reset_queries()
    result1 = run_problematic_version(project)
    queries_bad = len(connection.queries)
    print(f"Queries executed: {queries_bad}")
    print(f"Datasets processed: {len(result1)}")

    # Test optimized version
    print("\n✅ OPTIMIZED VERSION (with select/prefetch_related)")
    print("-" * 40)
    reset_queries()
    result2 = run_optimized_version(project.id)
    queries_good = len(connection.queries)
    print(f"Queries executed: {queries_good}")
    print(f"Datasets processed: {len(result2)}")

    # Show comparison
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"""
For a project with {len(result1)} datasets:

BEFORE OPTIMIZATION:
- Queries: {queries_bad} queries
- Pattern: 2 + N*3 (where N = number of datasets)
- Time complexity: O(N)

AFTER OPTIMIZATION:
- Queries: {queries_good} queries
- Pattern: Fixed number regardless of datasets
- Time complexity: O(1)

IMPROVEMENT: ~{queries_bad/max(queries_good, 1):.1f}x reduction in database queries!

Key Techniques Used:
1. select_related() - For ForeignKey relationships (joins)
2. prefetch_related() - For reverse ForeignKey and ManyToMany
3. annotate() with Count() - For aggregations
4. Prefetch() objects - For filtered prefetching
    """)

except ResearchProject.DoesNotExist:
    print("ERROR: 'Multi-Dataset Research Collaboration' not found. Please run setup_test_data first.")