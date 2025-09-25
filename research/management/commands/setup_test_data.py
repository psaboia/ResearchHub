from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from research.models import Institution, ResearchProject, Dataset, DataAccessRequest, DataProcessingJob, AuditLog
from datetime import datetime, timedelta
from django.utils import timezone
import uuid


class Command(BaseCommand):
    help = 'Creates test data for the ResearchHub platform'

    def handle(self, *args, **options):
        self.stdout.write('Setting up test data...')

        # Clear existing data for clean slate
        self.stdout.write('Clearing existing data...')
        DataAccessRequest.objects.all().delete()
        DataProcessingJob.objects.all().delete()
        Dataset.objects.all().delete()
        ResearchProject.objects.all().delete()
        Institution.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        # Create institutions
        mit = Institution.objects.create(
            name='MIT',
            country='USA',
            address='77 Massachusetts Ave, Cambridge, MA 02139'
        )

        stanford = Institution.objects.create(
            name='Stanford University',
            country='USA',
            address='450 Serra Mall, Stanford, CA 94305'
        )

        oxford = Institution.objects.create(
            name='University of Oxford',
            country='UK',
            address='Wellington Square, Oxford OX1 2JD'
        )

        test_university = Institution.objects.create(
            name='Test University',
            country='USA',
            address='123 Research Ave'
        )

        self.stdout.write(self.style.SUCCESS('Created 4 institutions'))

        # Create users
        alice = User.objects.create_user(
            username='alice',
            email='alice@mit.edu',
            password='testpass123',
            first_name='Alice',
            last_name='Smith'
        )

        bob = User.objects.create_user(
            username='bob',
            email='bob@stanford.edu',
            password='testpass123',
            first_name='Bob',
            last_name='Johnson'
        )

        charlie = User.objects.create_user(
            username='charlie',
            email='charlie@oxford.edu',
            password='testpass123',
            first_name='Charlie',
            last_name='Brown'
        )

        researcher1 = User.objects.create_user(
            username='researcher1',
            email='researcher1@example.com',
            password='testpass123',
            first_name='Research',
            last_name='User'
        )

        user_2 = User.objects.create_user(
            username='user_2',
            email='user2@example.com',
            password='testpass123'
        )

        user_3 = User.objects.create_user(
            username='user_3',
            email='user3@example.com',
            password='testpass123'
        )

        # Create admin user
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@researchhub.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()

        self.stdout.write(self.style.SUCCESS('Created 7 users (including admin)'))
        
        # Create research projects
        project1 = ResearchProject.objects.create(
            title='Climate Change Impact on Ocean Ecosystems',
            description='Studying the effects of climate change on marine biodiversity and ecosystem functions',
            institution=mit,
            principal_investigator=alice,
            status='active',
            start_date=timezone.now().date() - timedelta(days=180),
            budget=750000.00
        )
        project1.collaborators.add(bob)
        
        project2 = ResearchProject.objects.create(
            title='AI-Powered Drug Discovery',
            description='Using machine learning to accelerate pharmaceutical research',
            institution=stanford,
            principal_investigator=bob,
            status='active',
            start_date=timezone.now().date() - timedelta(days=90),
            budget=1200000.00
        )
        project2.collaborators.add(charlie)
        
        project3 = ResearchProject.objects.create(
            title='Quantum Computing Applications',
            description='Exploring practical applications of quantum computing in cryptography',
            institution=oxford,
            principal_investigator=charlie,
            status='draft',
            start_date=timezone.now().date() + timedelta(days=30),
            budget=500000.00
        )
        
        self.stdout.write(self.style.SUCCESS('Created 3 research projects'))

        # Create Multi-Dataset Research Project
        collaboration_project = ResearchProject.objects.create(
            title='Multi-Dataset Research Collaboration',
            description='Large-scale collaborative project analyzing multiple research datasets across institutions',
            institution=test_university,
            principal_investigator=researcher1,
            status='active',
            start_date=timezone.now().date() - timedelta(days=30),
            budget=500000.00
        )
        collaboration_project.collaborators.add(user_2, user_3)

        self.stdout.write(self.style.SUCCESS('Created collaboration project'))

        # Create datasets for collaboration project
        for i in range(1, 11):
            dataset = Dataset.objects.create(
                project=collaboration_project,
                name=f'Research Dataset {i:02d}',
                description=f'Research dataset {i} from collaborative study',
                file_type='csv',
                file_size=1000000 * i,
                file_path=f'/media/datasets/collaboration/data_{i:02d}.csv',
                privacy_level='private' if i % 2 == 0 else 'public',
                uploaded_by=researcher1,
                row_count=10000 * i,
                column_count=20,
                is_processed=True,
                metadata={'study_phase': 'data_collection', 'dataset_index': i}
            )

            # Add processing jobs for each dataset
            for j in range(3):
                DataProcessingJob.objects.create(
                    dataset=dataset,
                    job_type='quality_check' if j == 0 else 'analysis',
                    status='completed',
                    created_by=researcher1,
                    completed_at=timezone.now() - timedelta(hours=j),
                    parameters={'step': j}
                )

            # Add approved access requests
            for k in range(2):
                requester = user_2 if k == 0 else user_3
                DataAccessRequest.objects.create(
                    dataset=dataset,
                    requester=requester,
                    requester_institution=test_university,
                    status='approved',
                    reason='Research collaboration',
                    approved_by=researcher1,
                    approval_date=timezone.now() - timedelta(days=k+1)
                )

        self.stdout.write(self.style.SUCCESS('Created 10 datasets with related data for collaboration project'))

        # Create additional datasets
        dataset1 = Dataset.objects.create(
            project=project1,
            name='Ocean Temperature Measurements 2023',
            description='Temperature data from 50 ocean monitoring stations',
            file_type='csv',
            file_size=15728640,  # 15MB
            file_path='/media/datasets/ocean_temp_2023.csv',
            privacy_level='public',
            uploaded_by=alice,
            row_count=50000,
            column_count=25,
            is_processed=True,
            metadata={'source': 'NOAA', 'sensors': 50, 'frequency': 'hourly'}
        )

        # Private dataset
        private_dataset = Dataset.objects.create(
            project=project2,
            name='Confidential Drug Trial Results',
            description='PRIVATE: Clinical trial data - restricted access',
            file_type='excel',
            file_size=8388608,  # 8MB
            file_path='/media/datasets/private/drug_trial.xlsx',
            privacy_level='private',
            uploaded_by=bob,
            row_count=5000,
            column_count=30,
            is_processed=True,
            metadata={'confidential': True, 'trial_phase': 3}
        )

        # Create sample file
        import os
        os.makedirs('/media/datasets/private', exist_ok=True)
        with open('/media/datasets/private/drug_trial.xlsx', 'wb') as f:
            f.write(b'Mock Excel file with confidential drug trial data')

        # Analytics dataset
        analytics_dataset = Dataset.objects.create(
            project=project1,
            name='Research Analytics Dataset',
            description='Dataset for research analytics and reporting dashboard',
            file_type='csv',
            file_size=5242880,  # 5MB
            file_path='/media/datasets/analytics_data.csv',
            privacy_level='public',
            uploaded_by=alice,
            row_count=15000,
            column_count=10,
            is_processed=True,
            metadata={'analytics_type': 'dashboard_metrics'}
        )

        self.stdout.write(self.style.SUCCESS('Created additional datasets'))

        # Create some initial audit logs for analytics dataset
        for i in range(15):
            AuditLog.objects.create(
                user=alice if i % 3 == 0 else (bob if i % 3 == 1 else charlie),
                action='download',
                object_type='Dataset',
                object_id=str(analytics_dataset.id),
                ip_address=f'192.168.1.{10 + i}',
                timestamp=timezone.now() - timedelta(hours=12 - i)  # Spread over last 12 hours
            )

        self.stdout.write(self.style.SUCCESS('Created initial audit logs'))

        # Create data access requests
        DataAccessRequest.objects.create(
            dataset=private_dataset,
            requester=alice,
            requester_institution=mit,
            status='pending',
            reason='Need clinical trial data for comparative analysis',
            notes='Collaborative research opportunity'
        )
        
        DataAccessRequest.objects.create(
            dataset=dataset1,
            requester=charlie,
            requester_institution=oxford,
            status='approved',
            reason='Comparing Atlantic and Pacific ocean temperature patterns',
            approved_by=alice,
            approval_date=timezone.now(),
            expiry_date=timezone.now() + timedelta(days=365)
        )
        
        self.stdout.write(self.style.SUCCESS('Created sample data access requests'))

        # Summary of created data
        self.stdout.write(self.style.SUCCESS(
            '\n' + '='*60 +
            '\nTEST DATA SETUP COMPLETE!\n' +
            '='*60 +
            '\n\nCredentials:' +
            '\n  Admin: admin / admin123' +
            '\n  Test users: researcher1, alice, bob, charlie (password: testpass123)' +
            '\n\nTotal Created:' +
            f'\n  Users: {User.objects.count()}' +
            f'\n  Projects: {ResearchProject.objects.count()}' +
            f'\n  Datasets: {Dataset.objects.count()}' +
            f'\n  Processing Jobs: {DataProcessingJob.objects.count()}' +
            f'\n  Access Requests: {DataAccessRequest.objects.count()}\n' +
            '='*60
        ))