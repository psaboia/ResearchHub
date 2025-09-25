#!/usr/bin/env python
"""
Cache Bug Demonstration Tool

PURPOSE:
Demonstrate why the ResearchHub statistics dashboard shows outdated numbers.

SCENARIO:
During a board meeting, the CEO notices the dashboard shows only 15 downloads,
but the analytics team confirms there are actually 35 in the database.
The statistics cache isn't updating when new downloads occur.

This tool demonstrates the problem by:
- Showing the actual database statistics
- Demonstrating how the cache returns stale data
- Revealing the business impact of incorrect analytics
"""

import django
import os
import sys
import time
from datetime import datetime

# Add the project directory to the path
sys.path.insert(0, '/code')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.cache import cache
from django.contrib.auth.models import User
from research.models import Dataset, AuditLog, ResearchProject
from research.views import get_dataset_statistics
from rest_framework.test import APIRequestFactory, force_authenticate

print("\n" + "=" * 60)
print("📊 DEMONSTRATION: Stale Cache Problem")
print("=" * 60)
print("\n📋 SCENARIO:")
print("  • CEO checks dashboard during board meeting: shows 15 downloads")
print("  • Analytics team checks database: actually has 35 downloads")
print("  • Problem: Cache not updating when new downloads occur")
print("\n" + "-" * 60)

try:
    # Get the cache demo dataset
    dataset = Dataset.objects.get(name='Research Analytics Dataset')
    user = User.objects.get(username="researcher1")

    print("\n🔬 STARTING DEMONSTRATION...")
    print(f"Dataset: {dataset.name}")
    print(f"Dataset ID: {dataset.id}")

    # Clear cache to start fresh
    cache_key = f"dataset_stats_{dataset.id}"
    cache.delete(cache_key)
    print("\n🧹 Cleared any existing cache for clean test")

    # Check actual downloads in database
    initial_downloads = AuditLog.objects.filter(
        object_id=str(dataset.id),
        action='download'
    ).count()

    print(f"\n📊 CURRENT DATABASE STATE:")
    print(f"  Actual downloads in database: {initial_downloads}")

    # Make first API request - this will cache the statistics
    factory = APIRequestFactory()
    request = factory.get(f'/api/datasets/{dataset.id}/statistics/')
    force_authenticate(request, user=user)

    print("\n📱 CEO CHECKS DASHBOARD (First Request):")
    response = get_dataset_statistics(request, dataset.id)
    stats = response.data
    print(f"  Downloads shown on dashboard: {stats['total_downloads']}")
    print(f"  Unique users shown: {stats['unique_users']}")

    # Verify it's cached
    cached = cache.get(cache_key)
    print(f"  ✓ Statistics cached for fast access: {cached is not None}")

    # Simulate the time passing and new activity
    print("\n⏰ SIMULATING NEW ACTIVITY...")
    print("   Conference attendees downloading the dataset:")

    # Create realistic download activity
    conference_users = []
    for i in range(15):  # 15 new users from conference
        conf_user = User.objects.get_or_create(
            username=f'conf_attendee_{i}',
            email=f'attendee{i}@conference.org',
            defaults={'first_name': f'Attendee{i}', 'last_name': 'Conference'}
        )[0]
        conference_users.append(conf_user)

        # Each user downloads the dataset
        AuditLog.objects.create(
            user=conf_user,
            action='download',
            object_type='Dataset',
            object_id=str(dataset.id),
            ip_address=f'192.168.1.{100+i}'
        )

    # Some users download multiple times
    for i in range(5):
        AuditLog.objects.create(
            user=conference_users[i],
            action='download',
            object_type='Dataset',
            object_id=str(dataset.id),
            ip_address=f'192.168.1.{100+i}'
        )

    print(f"   ✓ Added 20 new downloads from 15 conference attendees")

    # Check actual count in database now
    new_downloads = AuditLog.objects.filter(
        object_id=str(dataset.id),
        action='download'
    ).count()

    new_unique = AuditLog.objects.filter(
        object_id=str(dataset.id)
    ).values('user').distinct().count()

    print(f"\n📊 ACTUAL DATABASE STATE (after new activity):")
    print(f"  Real downloads in database: {new_downloads}")
    print(f"  Real unique users: {new_unique}")

    # CEO refreshes dashboard during meeting (uses cached data!)
    print("\n🔄 CEO REFRESHES DASHBOARD:")
    request2 = factory.get(f'/api/datasets/{dataset.id}/statistics/')
    force_authenticate(request2, user=user)
    response2 = get_dataset_statistics(request2, dataset.id)
    stats2 = response2.data

    print(f"  Downloads shown to board: {stats2['total_downloads']} (CACHED!)")
    print(f"  Unique users shown: {stats2['unique_users']} (CACHED!)")

    # Show the problem
    print("\n" + "=" * 60)
    print("🚨 DEMONSTRATION RESULTS")
    print("=" * 60)

    if stats2['total_downloads'] != new_downloads:
        print(f"\n❌ CRITICAL BUG CONFIRMED!")
        print(f"\n📊 DISCREPANCY ANALYSIS:")
        print(f"  Dashboard shows: {stats2['total_downloads']} downloads")
        print(f"  Database has: {new_downloads} downloads")
        print(f"  MISSING: {new_downloads - stats2['total_downloads']} downloads not shown!")
        print(f"  ERROR RATE: {((new_downloads - stats2['total_downloads']) / new_downloads * 100):.1f}% of data hidden")

        print(f"\n👥 USER METRICS:")
        print(f"  Dashboard shows: {stats2['unique_users']} unique users")
        print(f"  Database has: {new_unique} unique users")
        print(f"  MISSING: {new_unique - stats2['unique_users']} users not counted!")

        print("\n💰 BUSINESS IMPACT:")
        print("  • Board sees incorrect metrics during meeting")
        print("  • Recent activity not reflected in dashboard")
        print("  • Decision-making based on stale data")

        print("\n⚠️ ROOT CAUSE:")
        print("  The get_dataset_statistics view caches data for 1 hour")
        print("  But download_dataset NEVER invalidates this cache!")
        print("  Location: research/views.py, lines 137-162")

        print("\n🔧 FIX NEEDED:")
        print("  Add cache invalidation in download_dataset (line 68)")
        print("  Cache key pattern: dataset_stats_{dataset_id}")
    else:
        print("✓ Statistics are up to date (cache may have expired)")

    print("\n💡 NEXT STEP:")
    print("  Open research/views.py in Cursor and fix the cache invalidation")

except Dataset.DoesNotExist:
    print("\n⚠️ ERROR: 'Research Analytics Dataset' not found")
    print("Please run: docker compose exec web python manage.py setup_test_data")
except User.DoesNotExist:
    print("\n⚠️ ERROR: User 'researcher1' not found")
    print("Please run: docker compose exec web python manage.py setup_test_data")
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()