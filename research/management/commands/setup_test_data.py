from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from research.models import Institution, ResearchProject, Dataset, DataAccessRequest
from datetime import datetime, timedelta
from django.utils import timezone
import uuid


class Command(BaseCommand):
    help = 'Creates test data for the ResearchHub platform'

    def handle(self, *args, **options):
        self.stdout.write('Setting up test data...')
        
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
        
        self.stdout.write(self.style.SUCCESS('Created 3 institutions'))
        
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
        
        # Create admin user
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@researchhub.com',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        
        self.stdout.write(self.style.SUCCESS('Created 4 users (including admin)'))
        
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
        project2.collaborators.add(alice, charlie)
        
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
        
        # Create datasets
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
        
        dataset2 = Dataset.objects.create(
            project=project1,
            name='Marine Species Distribution',
            description='Species observation data from research vessels',
            file_type='excel',
            file_size=8388608,  # 8MB
            file_path='/media/datasets/species_dist.xlsx',
            privacy_level='restricted',
            uploaded_by=alice,
            row_count=12000,
            column_count=15,
            is_processed=True,
            metadata={'species_count': 234, 'locations': 45}
        )
        
        dataset3 = Dataset.objects.create(
            project=project2,
            name='Drug Compound Analysis Results',
            description='ML predictions for drug compound effectiveness',
            file_type='json',
            file_size=104857600,  # 100MB
            file_path='/media/datasets/drug_compounds.json',
            privacy_level='private',
            uploaded_by=bob,
            row_count=75000,
            column_count=50,
            is_processed=False,
            processing_status='pending',
            metadata={'compounds': 75000, 'features': 50, 'ml_model': 'XGBoost'}
        )
        
        self.stdout.write(self.style.SUCCESS('Created 3 datasets'))
        
        # Create data access requests
        DataAccessRequest.objects.create(
            dataset=dataset2,
            requester=bob,
            requester_institution=stanford,
            status='pending',
            reason='Need marine species data for comparative analysis with Pacific Ocean data',
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
        
        self.stdout.write(self.style.SUCCESS('Created 2 data access requests'))
        
        self.stdout.write(self.style.SUCCESS(
            '\nTest data setup complete!\n'
            'Admin credentials: admin / admin123\n'
            'Test users: alice, bob, charlie (password: testpass123)'
        ))