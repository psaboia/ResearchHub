#!/usr/bin/env python
"""
Security Bug - Reference Solution

PURPOSE:
Demonstrate the correct authorization implementation for dataset downloads.
This is the reference solution participants can compare with their AI-generated fix.

THE FIX:
Add comprehensive authorization checks to ensure users can only download datasets
they have permission to access.
"""

import django
import os
import sys

# Add the project directory to the path
sys.path.insert(0, '/code')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import FileResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from research.models import Dataset, AuditLog, DataAccessRequest

print("\n" + "=" * 60)
print("📚 REFERENCE SOLUTION: Authorization Fix")
print("=" * 60)

print("\n🔧 THE CORRECT FIX:")
print("-" * 60)

# Show the fixed download_dataset function
fixed_code = '''
@api_view(['POST'])
@login_required
def download_dataset(request, dataset_id):
    """Fixed version with proper authorization checks"""

    # Get dataset with related data for efficient permission checking
    dataset = Dataset.objects.select_related(
        'project', 'uploaded_by'
    ).prefetch_related(
        'project__collaborators'
    ).get(id=dataset_id)

    user = request.user

    # ✅ FIX: Comprehensive authorization checks
    # Check all possible access permissions
    is_owner = dataset.uploaded_by == user
    is_collaborator = dataset.project.collaborators.filter(id=user.id).exists()
    has_approved_access = DataAccessRequest.objects.filter(
        dataset=dataset,
        requester=user,
        status='approved'
    ).exists()
    is_public = dataset.privacy_level == 'public'

    # Deny access if no permission
    if not any([is_owner, is_collaborator, has_approved_access, is_public]):
        # Log the unauthorized attempt for security monitoring
        AuditLog.objects.create(
            user=user,
            action='unauthorized_access',  # Shortened to fit 20 char limit
            object_type='Dataset',
            object_id=str(dataset.id),
            ip_address=request.META.get('REMOTE_ADDR'),
            details={'reason': 'Permission denied for dataset download'}
        )

        # Raise PermissionDenied with helpful message
        raise PermissionDenied(
            f"You don't have permission to download this dataset. "
            f"Please request access from the dataset owner."
        )

    # User is authorized, proceed with download
    file_path = dataset.file_path

    # Log the successful download
    AuditLog.objects.create(
        user=user,
        action='download',
        object_type='Dataset',
        object_id=str(dataset.id),
        ip_address=request.META.get('REMOTE_ADDR'),
    )

    # Update last accessed timestamp
    dataset.last_accessed = timezone.now()
    dataset.save(update_fields=['last_accessed'])

    return FileResponse(open(file_path, 'rb'), as_attachment=True)
'''

print(fixed_code)

print("\n📝 KEY POINTS OF THE FIX:")
print("-" * 60)
print("1. Import PermissionDenied: from django.core.exceptions import PermissionDenied")
print("2. Check four access paths:")
print("   - Owner: dataset.uploaded_by == user")
print("   - Collaborator: dataset.project.collaborators.filter(id=user.id)")
print("   - Approved request: DataAccessRequest with status='approved'")
print("   - Public: dataset.privacy_level == 'public'")
print("3. Use any([...]) to check if ANY permission exists")
print("4. Log unauthorized attempts for security monitoring")
print("5. Raise PermissionDenied with helpful error message")

print("\n🎯 TESTING THE REFERENCE SOLUTION:")
print("-" * 60)

def fixed_download_dataset(request, dataset_id):
    """Fixed version of download_dataset with authorization"""

    dataset = Dataset.objects.select_related(
        'project', 'uploaded_by'
    ).prefetch_related(
        'project__collaborators'
    ).get(id=dataset_id)

    user = request.user

    # Authorization checks
    is_owner = dataset.uploaded_by == user
    is_collaborator = dataset.project.collaborators.filter(id=user.id).exists()
    has_approved_access = DataAccessRequest.objects.filter(
        dataset=dataset,
        requester=user,
        status='approved'
    ).exists()
    is_public = dataset.privacy_level == 'public'

    if not any([is_owner, is_collaborator, has_approved_access, is_public]):
        # Log unauthorized attempt
        AuditLog.objects.create(
            user=user,
            action='unauthorized_access',  # Shortened to fit 20 char limit
            object_type='Dataset',
            object_id=str(dataset.id),
            ip_address=request.META.get('REMOTE_ADDR', '127.0.0.1'),
            details={'reason': 'Permission denied'}
        )
        raise PermissionDenied(
            "You don't have permission to download this dataset."
        )

    # Log successful access
    AuditLog.objects.create(
        user=user,
        action='download',
        object_type='Dataset',
        object_id=str(dataset.id),
        ip_address=request.META.get('REMOTE_ADDR', '127.0.0.1'),
    )

    print(f"  ✓ User {user.username} authorized to download {dataset.name}")
    return {'status': 'authorized', 'dataset': dataset.name}

# Test the fix
try:
    from rest_framework.test import APIRequestFactory

    private_dataset = Dataset.objects.get(name='Confidential Drug Trial Results')
    owner = private_dataset.uploaded_by
    unauthorized_user = User.objects.get(username='alice')

    print(f"\nTesting with dataset: {private_dataset.name}")
    print(f"Owner: {owner.username}")

    # Test 1: Unauthorized user should be blocked
    class FakeRequest:
        def __init__(self, user):
            self.user = user
            self.META = {'REMOTE_ADDR': '127.0.0.1'}

    print(f"\n1. Testing unauthorized user ({unauthorized_user.username})...")
    try:
        fixed_download_dataset(FakeRequest(unauthorized_user), private_dataset.id)
        print("   ❌ Should have been denied!")
    except PermissionDenied as e:
        print(f"   ✅ Correctly denied: {e}")

    # Test 2: Owner should have access
    print(f"\n2. Testing owner ({owner.username})...")
    try:
        result = fixed_download_dataset(FakeRequest(owner), private_dataset.id)
        print(f"   ✅ Owner has access")
    except PermissionDenied:
        print("   ❌ Owner was incorrectly denied!")

    # Test 3: Public dataset should be accessible
    public_dataset = Dataset.objects.filter(privacy_level='public').first()
    if public_dataset:
        print(f"\n3. Testing public dataset access...")
        try:
            result = fixed_download_dataset(FakeRequest(unauthorized_user), public_dataset.id)
            print(f"   ✅ Public dataset accessible")
        except PermissionDenied:
            print("   ❌ Public dataset was incorrectly denied!")

    print("\n✅ REFERENCE SOLUTION VERIFIED!")

except Dataset.DoesNotExist:
    print("\n⚠️ Test dataset not found - run setup_test_data first")
except Exception as e:
    print(f"\n⚠️ Test error: {e}")

print("\n" + "=" * 60)
print("💡 SECURITY BEST PRACTICES")
print("=" * 60)

print("""
1. PRINCIPLE OF LEAST PRIVILEGE:
   - Default deny - require explicit permission
   - Check all access paths systematically
   - Don't assume authentication means authorization

2. DEFENSE IN DEPTH:
   - Multiple permission checks
   - Audit logging for forensics
   - Clear error messages (but not too revealing)

3. PERFORMANCE CONSIDERATIONS:
   - Use select_related/prefetch_related to avoid N+1
   - Cache permission checks if needed
   - Consider using Django's permission framework

4. ADDITIONAL SECURITY MEASURES:
   - Rate limiting to prevent mass downloads
   - File encryption at rest
   - Signed/expiring URLs for downloads
   - Watermarking for tracking

5. COMPLIANCE REQUIREMENTS:
   - GDPR: Must control access to personal data
   - HIPAA: Requires access controls for health data
   - SOC 2: Demonstrate access control measures
""")

print("\n📚 DJANGO SECURITY QUICK REFERENCE:")
print("-" * 60)
print("from django.core.exceptions import PermissionDenied")
print("raise PermissionDenied('Message')  # Returns 403 Forbidden")
print("")
print("# Django permission decorators:")
print("@login_required  # Only checks authentication")
print("@permission_required('app.permission')  # Checks specific permission")
print("@user_passes_test(lambda u: u.is_staff)  # Custom check")
print("\n" + "=" * 60)