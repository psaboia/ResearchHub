#!/usr/bin/env python
"""
Setup Verification Script

PURPOSE:
Verify that the ResearchHub workshop environment is properly configured
with all necessary data for the exercises.
"""

import django
import os
import sys

# Add the project directory to the path
sys.path.insert(0, '/code')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from research.models import ResearchProject, Dataset, Institution, DataProcessingJob, DataAccessRequest

print("\n" + "=" * 60)
print("🔍 RESEARCHHUB WORKSHOP SETUP VERIFICATION")
print("=" * 60)

# Check counts
users = User.objects.count()
projects = ResearchProject.objects.count()
datasets = Dataset.objects.count()
institutions = Institution.objects.count()
jobs = DataProcessingJob.objects.count()
requests = DataAccessRequest.objects.count()

print("\n📊 DATABASE CONTENTS:")
print(f"  • Users: {users}")
print(f"  • Projects: {projects}")
print(f"  • Datasets: {datasets}")
print(f"  • Institutions: {institutions}")
print(f"  • Processing Jobs: {jobs}")
print(f"  • Access Requests: {requests}")

# Verify critical data exists
print("\n✅ CHECKING CRITICAL DATA:")

# Check for key users
try:
    admin = User.objects.get(username='admin')
    print("  ✓ Admin user exists")
except User.DoesNotExist:
    print("  ✗ Admin user NOT FOUND - Run setup_test_data!")

try:
    researcher1 = User.objects.get(username='researcher1')
    print("  ✓ Workshop user 'researcher1' exists")
except User.DoesNotExist:
    print("  ✗ Workshop user 'researcher1' NOT FOUND - Run setup_test_data!")

# Check for N+1 demo project
try:
    n1_project = ResearchProject.objects.get(title='Multi-Dataset Research Collaboration')
    print(f"  ✓ N+1 Demo Project exists with {n1_project.datasets.count()} datasets")
except ResearchProject.DoesNotExist:
    print("  ✗ N+1 Demo Project NOT FOUND - Run setup_test_data!")

# Check for other demo data
try:
    cache_dataset = Dataset.objects.get(name='Research Analytics Dataset')
    print("  ✓ Research Analytics Dataset exists")
except Dataset.DoesNotExist:
    print("  ✗ Research Analytics Dataset NOT FOUND")

try:
    private_dataset = Dataset.objects.get(name='Confidential Drug Trial Results')
    print("  ✓ Security Demo Dataset exists")
except Dataset.DoesNotExist:
    print("  ✗ Security Demo Dataset NOT FOUND")

# Final status
print("\n" + "=" * 60)
if users >= 7 and projects >= 4 and datasets >= 13:
    print("✅ SETUP COMPLETE - Ready for workshop!")
    print("\n📋 Quick Reference:")
    print("  • Admin login: admin / admin123")
    print("  • Workshop user: researcher1 / testpass123")
    print("  • Test users: alice, bob, charlie / testpass123")
else:
    print("⚠️  SETUP INCOMPLETE - Please run:")
    print("  docker compose exec web python manage.py setup_test_data")

print("=" * 60 + "\n")