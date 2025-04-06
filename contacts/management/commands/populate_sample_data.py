from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import UserProfile
from contacts.models import Contact, SpamReport
import random
from faker import Faker
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Populates the database with sample data for testing'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=20, help='Number of users to create')
        parser.add_argument('--contacts', type=int, default=100, help='Number of contacts to create')
        parser.add_argument('--spam-reports', type=int, default=30, help='Number of spam reports to create')

    def handle(self, *args, **options):
        fake = Faker()
        num_users = options['users']
        num_contacts = options['contacts']
        num_spam_reports = options['spam_reports']

        # Create users
        self.stdout.write(f'Creating {num_users} users...')
        created_users = []
        
        for i in range(num_users):
            username = f'testuser{i+1}'
            first_name = "Anish"
            last_name = fake.last_name()
            email = f'{username}@example.com'
            
            try:
                # Create user
                user = User.objects.create_user(
                    username=username,
                    password='password123',
                    first_name=first_name,
                    last_name=last_name,
                    email=email
                )
                
                # Create user profile with unique phone number
                phone_number = f'+1{random.randint(2000000000, 9999999999)}'
                
                # Make sure phone number is unique
                while UserProfile.objects.filter(phone_number=phone_number).exists():
                    phone_number = f'+1{random.randint(2000000000, 9999999999)}'
                
                UserProfile.objects.filter(user=user).update(phone_number=phone_number)
                created_users.append(user)
                
                self.stdout.write(f'  Created user: {username} ({first_name} {last_name}) with phone: {phone_number}')
            
            except Exception as e:
                self.stderr.write(f'Error creating user {username}: {str(e)}')
        
        # Create contacts
        if created_users:
            self.stdout.write(f'Creating {num_contacts} contacts...')
            
            for i in range(num_contacts):
                owner = random.choice(created_users)
                name = fake.name()
                phone_number = f'+1{random.randint(2000000000, 9999999999)}'
                
                try:
                    Contact.objects.create(
                        owner=owner,
                        name=name,
                        phone_number=phone_number
                    )
                    self.stdout.write(f'  Created contact: {name} with phone: {phone_number} (owner: {owner.username})')
                
                except Exception as e:
                    self.stderr.write(f'Error creating contact for {owner.username}: {str(e)}')
        
        # Create spam reports
        if created_users:
            self.stdout.write(f'Creating {num_spam_reports} spam reports...')
            
            for i in range(num_spam_reports):
                reporter = random.choice(created_users)
                
                # Sometimes report an existing contact's number
                if random.random() < 0.3 and Contact.objects.exists():
                    random_contact = Contact.objects.order_by('?').first()
                    phone_number = random_contact.phone_number
                    name = random_contact.name
                else:
                    phone_number = f'+1{random.randint(2000000000, 9999999999)}'
                    name = "Unknown"
                
                try:
                    SpamReport.objects.create(
                        reporter=reporter,
                        phone_number=phone_number
                    )
                    self.stdout.write(f'  Created spam report for number: {phone_number} (reporter: {reporter.username})')
                
                except Exception as e:
                    self.stderr.write(f'Error creating spam report for {phone_number}: {str(e)}')
        
        self.stdout.write(self.style.SUCCESS(f'''
Sample data generation complete!
Created:
- {len(created_users)} users
- {Contact.objects.count()} contacts
- {SpamReport.objects.count()} spam reports
        ''')) 