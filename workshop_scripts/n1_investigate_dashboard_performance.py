#!/usr/bin/env python
"""
Dashboard Performance Investigation Tool

PURPOSE:
Diagnose why the ResearchHub dashboard is slow by analyzing database queries.

SCENARIO:
Users report the dashboard takes 5+ seconds to load when displaying project data.
The DevOps team noticed database CPU usage spikes whenever the dashboard is accessed.
This started after the platform grew from 10 to 100+ datasets per project.

This tool helps you investigate by:
- Measuring actual response time
- Counting database queries
- Identifying performance bottlenecks
- Showing impact at scale
"""

import django
import os
import sys
import logging
import time

# Add the project directory to the path
sys.path.insert(0, '/code')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection, reset_queries
from django.contrib.auth.models import User
from research.models import ResearchProject
from research.views import get_project_dashboard
from rest_framework.test import APIRequestFactory, force_authenticate

# Set up logging to see SQL queries
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('django.db.backends')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

print("\n" + "=" * 60)
print("🔍 PERFORMANCE INVESTIGATION: Dashboard Slowdown")
print("=" * 60)
print("\n📋 SCENARIO:")
print("  • Users report dashboard takes 5+ seconds to load")
print("  • Database CPU usage spikes during dashboard access")
print("  • Problem started after growing to 100+ datasets per project")
print("\n" + "-" * 60)

try:
    # Get test data
    user = User.objects.get(username="researcher1")
    project = ResearchProject.objects.get(title="Multi-Dataset Research Collaboration")

    print("\n🔬 STARTING INVESTIGATION...")
    print(f"Testing dashboard for project: {project.title}")
    print(f"Number of datasets: {project.datasets.count()}")

    # Create a fake request
    factory = APIRequestFactory()
    request = factory.get(f'/api/projects/{project.id}/dashboard/')
    force_authenticate(request, user=user)

    # Clear and reset query tracking
    reset_queries()

    print("\n⏱️  Measuring dashboard load time...")
    print("Calling get_project_dashboard from research/views.py")
    print("-" * 60)

    # Measure execution time
    start_time = time.time()

    # Call the actual view function
    response = get_project_dashboard(request, project.id)

    # Calculate elapsed time
    elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds

    # Show results
    print("\n" + "=" * 60)
    print("🚨 INVESTIGATION RESULTS")
    print("=" * 60)

    num_queries = len(connection.queries)
    num_datasets = len(response.data['datasets'])

    print(f"\n📊 PERFORMANCE METRICS:")
    print(f"  • Execution time: {elapsed_time:.2f}ms")
    print(f"  • Total queries executed: {num_queries}")
    print(f"  • Datasets returned: {num_datasets}")
    print(f"  • Queries per dataset: {(num_queries - 2) / num_datasets:.1f}")

    # Show breakdown
    print("\n🔍 QUERY BREAKDOWN:")
    print("  1 query: Fetch project")
    print("  1 query: Fetch datasets")
    print(f" {num_datasets} queries: Fetch uploaded_by user for each dataset")
    print(f" {num_datasets} queries: Count processing_jobs for each dataset")
    print(f" {num_datasets} queries: Count approved access_requests for each dataset")
    print("-" * 60)
    print(f"Total: {num_queries} queries (should be only 4-5 with optimization!)")

    # Calculate impact at scale
    print("\n📈 IMPACT AT SCALE:")
    print(f"  Current ({num_datasets} datasets): {num_queries} queries, ~{elapsed_time:.0f}ms")
    print(f"  With 100 datasets: ~{2 + (100 * 3)} queries, ~{elapsed_time * 10:.0f}ms (~{elapsed_time * 10 / 1000:.1f} seconds)")
    print(f"  With 1000 datasets: ~{2 + (1000 * 3)} queries, ~{elapsed_time * 100:.0f}ms (~{elapsed_time * 100 / 1000:.1f} seconds) ⏰ TIMEOUT!")

    # Cost analysis
    avg_query_time = elapsed_time / num_queries
    print("\n💰 DATABASE COST IMPACT:")
    print(f"  • Average time per query: {avg_query_time:.2f}ms")
    print(f"  • Database connections held: {elapsed_time:.0f}ms per request")
    print(f"  • At 100 requests/minute: {num_queries * 100} queries/minute to database")
    print(f"  • At peak load (1000 req/min): {num_queries * 1000} queries/minute 🔥")

    print("\n⚠️  PROBLEM IDENTIFIED: N+1 QUERY PATTERN")
    print("The view makes a separate query for EACH dataset's relationships!")
    print("This is why users are experiencing slow load times.")

    # Show sample data
    if response.data['datasets']:
        print("\nSample dataset from response:")
        sample = response.data['datasets'][0]
        for key, value in sample.items():
            print(f"  {key}: {value}")

    # Show first few queries
    if connection.queries:
        print("\nFirst 3 SQL queries executed:")
        for i, query in enumerate(connection.queries[:3], 1):
            print(f"\nQuery {i}:")
            print(f"  {query['sql'][:150]}...")

except User.DoesNotExist:
    print("ERROR: User 'researcher1' not found. Please run setup_test_data first.")
except ResearchProject.DoesNotExist:
    print("ERROR: 'Multi-Dataset Research Collaboration' not found. Please run setup_test_data first.")
except Exception as e:
    print(f"ERROR: {e}")
    print("Make sure the view is working correctly.")