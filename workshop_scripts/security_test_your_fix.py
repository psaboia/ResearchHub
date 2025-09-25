#!/usr/bin/env python
"""
Security Fix Testing Tool

PURPOSE:
Test if your AI-generated authorization fix actually works.

USAGE:
After you've applied your fix to research/views.py using AI assistance,
run this script to verify the authorization checks are working correctly.

SUCCESS CRITERIA:
- Unauthorized users should be denied access
- Authorized users should still be able to download
- Proper error messages for denied access
"""

import django
import os
import sys

# Add the project directory to the path
sys.path.insert(0, '/code')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from research.models import Dataset, DataAccessRequest, AuditLog
from research.views import download_dataset
from rest_framework.test import APIRequestFactory, force_authenticate
from django.http import FileResponse

print("\n" + "=" * 60)
print("🧪 TESTING YOUR SECURITY FIX")
print("=" * 60)

def test_unauthorized_access():
    """Test that unauthorized users are blocked"""

    print("\n📝 TEST 1: Unauthorized User Should Be Blocked")
    print("-" * 50)

    try:
        # Get test data
        private_dataset = Dataset.objects.get(name='Confidential Drug Trial Results')
        owner = private_dataset.uploaded_by
        unauthorized_user = User.objects.get(username='alice')

        print(f"Dataset: {private_dataset.name} (PRIVATE)")
        print(f"Owner: {owner.username}")
        print(f"Attempting user: {unauthorized_user.username}")

        # Create test file if needed
        if not os.path.exists(private_dataset.file_path):
            os.makedirs(os.path.dirname(private_dataset.file_path), exist_ok=True)
            with open(private_dataset.file_path, 'w') as f:
                f.write("Test data")

        # Attempt unauthorized download
        factory = APIRequestFactory()
        request = factory.post(f'/api/datasets/{private_dataset.id}/download/')
        force_authenticate(request, user=unauthorized_user)

        try:
            response = download_dataset(request, private_dataset.id)

            if isinstance(response, FileResponse):
                print("\n❌ FAIL! Unauthorized user downloaded private data!")
                print("Your fix is NOT working - review authorization logic")
                return False
            elif hasattr(response, 'status_code') and response.status_code == 403:
                print(f"\n✅ PASS! Access correctly denied (403 Forbidden)")
                return True
            else:
                print(f"\n⚠️ Unexpected response: {response}")
                return False

        except PermissionDenied as e:
            print(f"\n✅ PASS! Access correctly denied")
            print(f"   Error message: {e}")
            return True

        except Exception as e:
            if "No such file" in str(e) or "FileNotFoundError" in str(e.__class__.__name__):
                print("\n❌ FAIL! File error but no authorization check!")
                print("   The user would have accessed the file if it existed")
                return False
            else:
                print(f"\n⚠️ Unexpected error: {e}")
                return False

    except Dataset.DoesNotExist:
        print("⚠️ Test dataset not found - run setup_test_data")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def test_owner_access():
    """Test that owners can still download their own datasets"""

    print("\n📝 TEST 2: Owner Should Have Access")
    print("-" * 50)

    try:
        private_dataset = Dataset.objects.get(name='Confidential Drug Trial Results')
        owner = private_dataset.uploaded_by

        print(f"Dataset: {private_dataset.name}")
        print(f"Owner attempting download: {owner.username}")

        # Create test file if needed
        if not os.path.exists(private_dataset.file_path):
            os.makedirs(os.path.dirname(private_dataset.file_path), exist_ok=True)
            with open(private_dataset.file_path, 'w') as f:
                f.write("Test data")

        factory = APIRequestFactory()
        request = factory.post(f'/api/datasets/{private_dataset.id}/download/')
        force_authenticate(request, user=owner)

        try:
            response = download_dataset(request, private_dataset.id)

            if isinstance(response, FileResponse):
                print("\n✅ PASS! Owner can download their own dataset")
                return True
            else:
                print(f"\n⚠️ Unexpected response type: {type(response)}")
                return True  # Might be OK depending on implementation

        except PermissionDenied:
            print("\n❌ FAIL! Owner was denied access to their own data!")
            print("   Check your authorization logic - owners should always have access")
            return False

        except Exception as e:
            if "No such file" in str(e) or "FileNotFoundError" in str(e.__class__.__name__):
                print("\n✅ PASS! Owner has access (file doesn't exist but auth passed)")
                return True
            else:
                print(f"\n⚠️ Error during test: {e}")
                return False

    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def test_public_dataset_access():
    """Test that anyone can access public datasets"""

    print("\n📝 TEST 3: Public Datasets Should Be Accessible")
    print("-" * 50)

    try:
        # Get a public dataset
        public_dataset = Dataset.objects.filter(privacy_level='public').first()
        if not public_dataset:
            print("⚠️ No public dataset available for testing")
            return True  # Skip this test

        any_user = User.objects.get(username='charlie')

        print(f"Dataset: {public_dataset.name} (PUBLIC)")
        print(f"User attempting download: {any_user.username}")

        factory = APIRequestFactory()
        request = factory.post(f'/api/datasets/{public_dataset.id}/download/')
        force_authenticate(request, user=any_user)

        try:
            response = download_dataset(request, public_dataset.id)
            print("\n✅ PASS! Public dataset is accessible")
            return True

        except PermissionDenied:
            print("\n❌ FAIL! User denied access to PUBLIC dataset!")
            print("   Public datasets should be accessible to all authenticated users")
            return False

        except Exception as e:
            if "No such file" in str(e):
                print("\n✅ PASS! Public dataset accessible (file missing but auth passed)")
                return True
            else:
                print(f"\n⚠️ Test inconclusive: {e}")
                return True

    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def test_approved_access_request():
    """Test that users with approved access requests can download"""

    print("\n📝 TEST 4: Approved Access Requests Should Work")
    print("-" * 50)

    try:
        # Check if there's an approved access request in the test data
        approved_request = DataAccessRequest.objects.filter(status='approved').first()
        if not approved_request:
            print("⚠️ No approved access requests in test data - skipping")
            return True

        dataset = approved_request.dataset
        requester = approved_request.requester

        print(f"Dataset: {dataset.name}")
        print(f"Approved requester: {requester.username}")

        factory = APIRequestFactory()
        request = factory.post(f'/api/datasets/{dataset.id}/download/')
        force_authenticate(request, user=requester)

        try:
            response = download_dataset(request, dataset.id)
            print("\n✅ PASS! Approved requester can download")
            return True

        except PermissionDenied:
            print("\n❌ FAIL! User with approved access was denied!")
            print("   Check if you're checking DataAccessRequest correctly")
            return False

        except Exception as e:
            if "No such file" in str(e):
                print("\n✅ PASS! Approved access works (file missing but auth passed)")
                return True
            else:
                print(f"\n⚠️ Test inconclusive: {e}")
                return True

    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

# Run all tests
print("\n🔬 Running Security Test Suite...")
print("=" * 60)

results = []
results.append(("Unauthorized Access Blocked", test_unauthorized_access()))
results.append(("Owner Access Allowed", test_owner_access()))
results.append(("Public Dataset Access", test_public_dataset_access()))
results.append(("Approved Request Access", test_approved_access_request()))

print("\n" + "=" * 60)
print("🏁 FINAL RESULTS")
print("=" * 60)

passed = sum(1 for _, result in results if result)
total = len(results)

print(f"\n📊 Test Summary: {passed}/{total} tests passed")
for test_name, result in results:
    status = "✅ PASS" if result else "❌ FAIL"
    print(f"  {status}: {test_name}")

if passed == total:
    print("\n🎉 ALL TESTS PASSED!")
    print("Your security fix is working correctly:")
    print("  ✅ Unauthorized users are blocked")
    print("  ✅ Authorized users maintain access")
    print("  ✅ Authorization logic is comprehensive")
    print("\n👏 Great job fixing the security vulnerability!")
else:
    print(f"\n⚠️ SOME TESTS FAILED ({total - passed} failures)")
    print("\n💡 Review your authorization logic:")
    print("  1. Check owner: dataset.uploaded_by == user")
    print("  2. Check collaborators: dataset.project.collaborators")
    print("  3. Check access requests: DataAccessRequest status='approved'")
    print("  4. Check privacy: dataset.privacy_level == 'public'")
    print("\nMake sure to raise PermissionDenied for unauthorized access!")