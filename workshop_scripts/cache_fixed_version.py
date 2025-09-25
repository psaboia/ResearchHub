#!/usr/bin/env python
"""
Cache Bug - Reference Solution

PURPOSE:
Demonstrate the correct cache invalidation implementation.
This is the reference solution participants can compare with their AI-generated fix.

THE FIX:
The key is to invalidate the cache whenever the underlying data changes.
This includes:
1. After downloads (primary fix)
2. After new access requests
3. After dataset updates
"""

import django
import os
import sys

# Add the project directory to the path
sys.path.insert(0, '/code')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.cache import cache
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import FileResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from research.models import Dataset, AuditLog

print("\n" + "=" * 60)
print("📚 REFERENCE SOLUTION: Cache Invalidation Fix")
print("=" * 60)

print("\n🔧 THE CORRECT FIX:")
print("-" * 60)

# Show the fixed download_dataset function
fixed_code = '''
@api_view(['POST'])
@login_required
def download_dataset(request, dataset_id):
    """Fixed version with cache invalidation"""
    dataset = Dataset.objects.get(id=dataset_id)

    file_path = dataset.file_path

    # Log the download
    AuditLog.objects.create(
        user=request.user,
        action='download',
        object_type='Dataset',
        object_id=str(dataset.id),
        ip_address=request.META.get('REMOTE_ADDR'),
    )

    # ✅ FIX: Invalidate the statistics cache after recording download
    cache_key = f"dataset_stats_{dataset_id}"
    cache.delete(cache_key)

    # Also update last_accessed timestamp
    dataset.last_accessed = timezone.now()
    dataset.save(update_fields=['last_accessed'])

    return FileResponse(open(file_path, 'rb'), as_attachment=True)
'''

print(fixed_code)

print("\n📝 KEY POINTS OF THE FIX:")
print("-" * 60)
print("1. Import cache: from django.core.cache import cache")
print("2. Build correct cache key: f'dataset_stats_{dataset_id}'")
print("3. Delete cache after audit log: cache.delete(cache_key)")
print("4. Update last_accessed for completeness")

print("\n🎯 TESTING THE REFERENCE SOLUTION:")
print("-" * 60)

def fixed_download_dataset(request, dataset_id):
    """Fixed version of download_dataset with cache invalidation"""
    dataset = Dataset.objects.get(id=dataset_id)

    # Log the download
    AuditLog.objects.create(
        user=request.user,
        action='download',
        object_type='Dataset',
        object_id=str(dataset.id),
        ip_address=request.META.get('REMOTE_ADDR', '127.0.0.1'),
    )

    # FIX: Invalidate the statistics cache
    cache_key = f"dataset_stats_{dataset_id}"
    cache.delete(cache_key)
    print(f"  ✓ Cache invalidated for key: {cache_key}")

    # Update last_accessed
    dataset.last_accessed = timezone.now()
    dataset.save(update_fields=['last_accessed'])

    # Return a simple response for testing (file might not exist)
    return {'status': 'downloaded', 'cache_invalidated': True}

# Test the fix
try:
    from research.views import get_dataset_statistics
    from rest_framework.test import APIRequestFactory, force_authenticate

    dataset = Dataset.objects.get(name='Research Analytics Dataset')
    user = User.objects.get(username="researcher1")
    factory = APIRequestFactory()

    print(f"\nTesting with dataset: {dataset.name}")

    # Clear cache first
    cache_key = f"dataset_stats_{dataset.id}"
    cache.delete(cache_key)

    # Get initial stats
    request1 = factory.get(f'/api/datasets/{dataset.id}/statistics/')
    force_authenticate(request1, user=user)
    initial_response = get_dataset_statistics(request1, dataset.id)
    initial_downloads = initial_response.data['total_downloads']
    print(f"Initial downloads: {initial_downloads}")

    # Simulate download with fixed function
    class FakeRequest:
        user = user
        META = {'REMOTE_ADDR': '127.0.0.1'}

    print(f"\nSimulating download with fixed function...")
    fixed_download_dataset(FakeRequest(), dataset.id)

    # Check if stats are updated
    request2 = factory.get(f'/api/datasets/{dataset.id}/statistics/')
    force_authenticate(request2, user=user)
    new_response = get_dataset_statistics(request2, dataset.id)
    new_downloads = new_response.data['total_downloads']
    print(f"Downloads after fix: {new_downloads}")

    if new_downloads == initial_downloads + 1:
        print("\n✅ REFERENCE SOLUTION VERIFIED!")
        print("Cache invalidation works correctly")
    else:
        print("\n⚠️ Note: Stats might be cached from earlier tests")

except Dataset.DoesNotExist:
    print("\n⚠️ 'Research Analytics Dataset' not found - run setup_test_data first")
except Exception as e:
    print(f"\n⚠️ Test error: {e}")

print("\n" + "=" * 60)
print("💡 ADDITIONAL CONSIDERATIONS")
print("=" * 60)

print("""
1. COMPLETE SOLUTION should invalidate cache in multiple places:
   - download_dataset (after downloads)
   - approve_access_request (after approvals)
   - upload_dataset (after new uploads)
   - delete_dataset (after deletions)

2. ADVANCED PATTERNS to consider:
   - Cache versioning: Include version in key
   - Cache tags: Group related caches for bulk invalidation
   - Event-driven: Use Django signals for automatic invalidation
   - Time-based: Shorter TTL for frequently changing data

3. PERFORMANCE TRADE-OFFS:
   - Too much invalidation: Loses cache benefits
   - Too little invalidation: Stale data issues
   - Balance: Invalidate only when data actually changes

4. MONITORING in production:
   - Log cache hit/miss ratios
   - Track invalidation frequency
   - Alert on cache-related errors
""")

print("\n📚 DJANGO CACHE QUICK REFERENCE:")
print("-" * 60)
print("cache.get(key)           # Get from cache")
print("cache.set(key, value, timeout)  # Set in cache")
print("cache.delete(key)        # Delete from cache")
print("cache.clear()            # Clear entire cache")
print("cache.get_or_set(key, callable, timeout)  # Get or compute")
print("\n" + "=" * 60)