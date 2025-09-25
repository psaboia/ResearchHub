#!/usr/bin/env python
"""
Security Vulnerability Demonstration Tool

PURPOSE:
Demonstrate how any authenticated user can download private datasets they shouldn't access.

SCENARIO:
A security audit reveals that researchers from competing institutions can download
your private research data just by logging in. This includes confidential drug trials
and patient data worth millions in research value.

This tool demonstrates the vulnerability by:
- Showing an unauthorized user accessing private data
- Revealing the missing authorization checks
- Highlighting the compliance violations
"""

import django
import os
import sys

# Add the project directory to the path
sys.path.insert(0, '/code')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from research.models import Dataset, DataAccessRequest, AuditLog
from research.views import download_dataset
from rest_framework.test import APIRequestFactory, force_authenticate
from django.http import FileResponse

print("\n" + "=" * 60)
print("🔒 DEMONSTRATION: Authorization Vulnerability")
print("=" * 60)
print("\n📋 SCENARIO:")
print("  • Security audit finds any logged-in user can access private data")
print("  • Confidential drug trial data worth $10M+ at risk")
print("  • Problem: Authentication exists but authorization missing")
print("\n" + "-" * 60)

try:
    # Get the private dataset (created by setup_test_data)
    private_dataset = Dataset.objects.get(name='Confidential Drug Trial Results')
    owner = private_dataset.uploaded_by

    # Get an unauthorized user (alice has no access to bob's private data)
    unauthorized_user = User.objects.get(username='alice')

    print("\n🎯 TARGET DATASET:")
    print(f"  Name: {private_dataset.name}")
    print(f"  Privacy Level: {private_dataset.privacy_level.upper()}")
    print(f"  Owner: {owner.username}")
    print(f"  Project: {private_dataset.project.title}")
    print(f"  Description: {private_dataset.description}")

    print(f"\n👤 ATTEMPTING USER:")
    print(f"  Username: {unauthorized_user.username}")
    print(f"  Institution: MIT (different from owner)")

    # Check all legitimate access paths
    print("\n🔍 CHECKING LEGITIMATE ACCESS:")

    # 1. Is the user the owner?
    is_owner = private_dataset.uploaded_by == unauthorized_user
    print(f"  ✓ Is dataset owner? {is_owner}")

    # 2. Is the user a project collaborator?
    is_collaborator = private_dataset.project.collaborators.filter(
        id=unauthorized_user.id
    ).exists()
    print(f"  ✓ Is project collaborator? {is_collaborator}")

    # 3. Does the user have an approved access request?
    has_approved_access = DataAccessRequest.objects.filter(
        dataset=private_dataset,
        requester=unauthorized_user,
        status='approved'
    ).exists()
    print(f"  ✓ Has approved access request? {has_approved_access}")

    # 4. Is the dataset public?
    is_public = private_dataset.privacy_level == 'public'
    print(f"  ✓ Is dataset public? {is_public}")

    should_have_access = any([is_owner, is_collaborator, has_approved_access, is_public])
    print(f"\n📊 VERDICT: User SHOULD have access? {'YES' if should_have_access else 'NO'}")

    # Now attempt the unauthorized download
    print("\n" + "=" * 60)
    print("🚨 ATTEMPTING UNAUTHORIZED DOWNLOAD...")
    print("=" * 60)

    # Create a fake file if it doesn't exist (for demo purposes)
    if not os.path.exists(private_dataset.file_path):
        os.makedirs(os.path.dirname(private_dataset.file_path), exist_ok=True)
        with open(private_dataset.file_path, 'w') as f:
            f.write("CONFIDENTIAL: Phase 3 Clinical Trial Results\n")
            f.write("Drug: EXP-2024-CANCER\n")
            f.write("Patient Data: 500 subjects\n")
            f.write("Efficacy: 87% response rate\n")
            f.write("Market Value: $10-15 Million\n")

    # Simulate the download attempt
    factory = APIRequestFactory()
    request = factory.post(f'/api/datasets/{private_dataset.id}/download/')
    force_authenticate(request, user=unauthorized_user)

    # Count downloads before attempt
    downloads_before = AuditLog.objects.filter(
        object_id=str(private_dataset.id),
        action='download'
    ).count()

    try:
        response = download_dataset(request, private_dataset.id)

        if isinstance(response, FileResponse):
            # Check if download was logged
            downloads_after = AuditLog.objects.filter(
                object_id=str(private_dataset.id),
                action='download'
            ).count()

            print("\n❌❌❌ CRITICAL SECURITY BREACH CONFIRMED! ❌❌❌")
            print("\n🔓 UNAUTHORIZED ACCESS SUCCESSFUL:")
            print(f"  Attacker: {unauthorized_user.username} (from competing institution)")
            print(f"  Downloaded: {private_dataset.name}")
            print(f"  Owner: {owner.username}")
            print(f"  Privacy: {private_dataset.privacy_level.upper()}")
            print(f"  Download logged: {'Yes' if downloads_after > downloads_before else 'No'}")

            print("\n💰 POTENTIAL DAMAGE:")
            print("  • Competitor accessed proprietary research")
            print("  • $10M+ research value compromised")
            print("  • HIPAA violation - patient data exposed")
            print("  • Legal liability for data breach")

            print("\n⚠️ VULNERABILITY DETAILS:")
            print("  Location: research/views.py, lines 53-70")
            print("  Problem: @login_required only checks authentication")
            print("  Missing: Authorization checks for data access")

        else:
            print("\n✅ Access was properly denied")
            print("The security vulnerability has been fixed!")

    except PermissionDenied as e:
        print("\n✅ ACCESS DENIED (Good - vulnerability is fixed)")
        print(f"  Reason: {e}")

    except Exception as e:
        # File might not exist, but that's OK for the demo
        if "No such file" in str(e) or "FileNotFoundError" in str(e.__class__.__name__):
            print("\n❌❌❌ CRITICAL SECURITY BREACH CONFIRMED! ❌❌❌")
            print("\n🔓 UNAUTHORIZED ACCESS SUCCESSFUL (file missing but access granted):")
            print(f"  Attacker: {unauthorized_user.username}")
            print(f"  Would have downloaded: {private_dataset.name}")
            print("\n💰 The authorization check is missing!")
        else:
            print(f"\n⚠️ Unexpected error: {e}")

    print("\n" + "=" * 60)
    print("🔧 FIX NEEDED:")
    print("=" * 60)
    print("Add authorization checks in download_dataset to verify:")
    print("  1. User is the dataset owner, OR")
    print("  2. User is a project collaborator, OR")
    print("  3. User has an approved access request, OR")
    print("  4. Dataset is public")
    print("\nUse PermissionDenied exception for unauthorized access")

    print("\n💡 NEXT STEP:")
    print("Open research/views.py in Cursor and add authorization checks")

except Dataset.DoesNotExist:
    print("\n⚠️ ERROR: 'Confidential Drug Trial Results' dataset not found")
    print("Please run: docker compose exec web python manage.py setup_test_data")
except User.DoesNotExist as e:
    print(f"\n⚠️ ERROR: Required user not found: {e}")
    print("Please run: docker compose exec web python manage.py setup_test_data")
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

# Import at top to check if available
try:
    from django.core.exceptions import PermissionDenied
except ImportError:
    pass