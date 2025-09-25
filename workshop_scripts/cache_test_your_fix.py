#!/usr/bin/env python
"""
Cache Fix Testing Tool

PURPOSE:
Test if your AI-generated cache invalidation fix actually works.

USAGE:
After you've applied your fix to research/views.py using AI assistance,
run this script to verify the cache invalidation is working correctly.

SUCCESS CRITERIA:
- Statistics should update immediately after new downloads
- No stale data should be shown
- Cache should still work for performance (when no changes)
"""

import django
import os
import sys
import time

# Add the project directory to the path
sys.path.insert(0, '/code')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.cache import cache
from django.contrib.auth.models import User
from research.models import Dataset, AuditLog
from research.views import get_dataset_statistics, download_dataset
from rest_framework.test import APIRequestFactory, force_authenticate
from django.utils import timezone

print("\n" + "=" * 60)
print("🧪 TESTING YOUR CACHE FIX")
print("=" * 60)

def test_cache_invalidation():
    """Test if cache invalidation is working after the fix"""

    try:
        # Get test data
        dataset = Dataset.objects.get(name='Research Analytics Dataset')
        user = User.objects.get(username="researcher1")

        print(f"\n📊 Testing with dataset: {dataset.name}")

        # Clear cache to start fresh
        cache_key = f"dataset_stats_{dataset.id}"
        cache.delete(cache_key)
        print("✓ Cleared cache for clean test")

        # Step 1: Get initial statistics
        factory = APIRequestFactory()
        request = factory.get(f'/api/datasets/{dataset.id}/statistics/')
        force_authenticate(request, user=user)

        initial_response = get_dataset_statistics(request, dataset.id)
        initial_stats = initial_response.data
        initial_downloads = initial_stats['total_downloads']

        print(f"\n📈 Initial State:")
        print(f"  Downloads: {initial_downloads}")
        print(f"  Cached: {cache.get(cache_key) is not None}")

        # Step 2: Simulate a download using the actual download endpoint
        print(f"\n📥 Simulating new download via download_dataset endpoint...")

        # Create download request
        download_request = factory.post(f'/api/datasets/{dataset.id}/download/')
        force_authenticate(download_request, user=user)

        # Call the download function (this should invalidate cache if fixed)
        try:
            download_response = download_dataset(download_request, dataset.id)
            print("  ✓ Download recorded")
        except FileNotFoundError:
            # File might not exist, but audit log should still be created
            print("  ✓ Download recorded (file not found, but that's OK for test)")

        # Step 3: Check if statistics are immediately updated
        print(f"\n🔄 Checking if statistics update immediately...")

        request2 = factory.get(f'/api/datasets/{dataset.id}/statistics/')
        force_authenticate(request2, user=user)

        new_response = get_dataset_statistics(request2, dataset.id)
        new_stats = new_response.data
        new_downloads = new_stats['total_downloads']

        print(f"  Downloads after download: {new_downloads}")

        # Step 4: Verify the fix worked
        print("\n" + "=" * 60)
        print("📋 TEST RESULTS")
        print("=" * 60)

        if new_downloads == initial_downloads + 1:
            print("\n✅ SUCCESS! Cache invalidation is working!")
            print(f"  • Before download: {initial_downloads}")
            print(f"  • After download: {new_downloads}")
            print(f"  • Cache properly invalidated and refreshed")
            print("\n🎉 Your fix correctly invalidates the cache!")
            return True
        else:
            print("\n❌ FAIL! Cache is still stale!")
            print(f"  • Expected: {initial_downloads + 1}")
            print(f"  • Got: {new_downloads}")
            print("\n🔧 Your fix might not be working. Check:")
            print("  1. Did you add cache.delete() in download_dataset?")
            print("  2. Is the cache key correct? Should be: f'dataset_stats_{dataset_id}'")
            print("  3. Did you import cache? from django.core.cache import cache")
            return False

    except Dataset.DoesNotExist:
        print("\n⚠️ ERROR: 'Research Analytics Dataset' not found")
        print("Please run: docker compose exec web python manage.py setup_test_data")
        return False
    except Exception as e:
        print(f"\n❌ ERROR during test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cache_performance():
    """Verify cache still works for performance when no changes"""

    print("\n" + "-" * 60)
    print("⚡ PERFORMANCE TEST: Cache should still work when no changes")
    print("-" * 60)

    try:
        dataset = Dataset.objects.get(name='Research Analytics Dataset')
        user = User.objects.get(username="researcher1")
        factory = APIRequestFactory()

        # Clear cache
        cache_key = f"dataset_stats_{dataset.id}"
        cache.delete(cache_key)

        # First request (should cache)
        request1 = factory.get(f'/api/datasets/{dataset.id}/statistics/')
        force_authenticate(request1, user=user)

        start_time = time.time()
        get_dataset_statistics(request1, dataset.id)
        first_time = (time.time() - start_time) * 1000

        # Second request (should use cache)
        request2 = factory.get(f'/api/datasets/{dataset.id}/statistics/')
        force_authenticate(request2, user=user)

        start_time = time.time()
        get_dataset_statistics(request2, dataset.id)
        second_time = (time.time() - start_time) * 1000

        print(f"\n📊 Performance Results:")
        print(f"  First request (no cache): {first_time:.2f}ms")
        print(f"  Second request (cached): {second_time:.2f}ms")

        if second_time < first_time:
            print(f"  ✅ Cache provides {(first_time/second_time):.1f}x speedup!")
            return True
        else:
            print(f"  ⚠️ Cache might not be working for performance")
            return False

    except Exception as e:
        print(f"❌ Performance test error: {e}")
        return False

# Run tests
print("\n🔬 Running Test Suite...")
print("=" * 60)

test1_passed = test_cache_invalidation()
test2_passed = test_cache_performance()

print("\n" + "=" * 60)
print("🏁 FINAL RESULTS")
print("=" * 60)

if test1_passed and test2_passed:
    print("\n🎉 ALL TESTS PASSED!")
    print("Your cache fix is working perfectly:")
    print("  ✅ Cache invalidates when data changes")
    print("  ✅ Cache still provides performance benefits")
    print("\n👏 Great job fixing the cache bug!")
else:
    print("\n⚠️ SOME TESTS FAILED")
    if not test1_passed:
        print("  ❌ Cache invalidation not working")
    if not test2_passed:
        print("  ❌ Cache performance issue")
    print("\n💡 Review your fix and try again")
    print("Remember to add cache.delete() after the audit log creation!")