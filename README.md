# Caller Identification API

A REST API for a mobile app that allows users to identify callers and detect spam numbers, similar to popular caller ID applications.

**Note:** Please refer to `setup_instructions.md` and `postman_testing_instruction.md` files to setup and test the Django app using Postman.

## Tech Stack

- Python 3.8+
- Django 4.2
- Django REST Framework
- JWT for authentication
- SQLite (for development)
- pytest for testing

## Features

- User registration with name and phone number (email optional)
- Authentication required for all operations
- Contact management (CRUD operations)
- Spam detection and reporting
- Mark phone numbers as spam and calculate spam likelihood
- Advanced name and phone number search
- Search for person by name or phone number in global database
- Results ordered by relevance (names starting with query first)
- Privacy controls for personal information
- Privacy restrictions for email display
- Rate limiting for API endpoints
- Data validation and formatting
- Phone number validation in E.164 format

## Project Structure

```
caller_id/
├── caller_id/          # Project settings
├── users/              # User authentication app
│   ├── models.py       # User profile model
│   ├── serializers.py  # User serializers
│   ├── views.py        # Authentication views
│   ├── urls.py         # Auth endpoints
│   └── tests.py        # Authentication tests
├── contacts/           # Contacts and spam detection app
│   ├── models.py       # Contact and spam models
│   ├── serializers.py  # Contact and spam serializers
│   ├── views.py        # Contact and spam views
│   ├── urls.py         # Contact and spam endpoints
│   └── tests.py        # Contact and spam tests
├── manage.py
├── requirements.txt
├── pytest.ini
└── README.md
```

## Feature Highlights

- User registration with name and phone number (email optional)
- Authentication required for all operations
- Mark phone numbers as spam and calculate spam likelihood
- Search for person by name or phone number in global database
- Results ordered by relevance (names starting with query first)
- Privacy restrictions for email display
- Phone number validation in E.164 format
- Rate limiting to prevent abuse:
  - Contact creation: 2 requests per 10 seconds
  - Spam reporting: 1 report per 10 seconds
  - Search operations: 30 requests per minute

## Accessing Sample Data

The application includes a management command to populate the database with sample data for testing purposes.

### Populating Sample Data

Run the following command to populate the database with sample data:

```bash
python manage.py populate_sample_data
```

This command creates:
- Several test users (testuser1, testuser2, etc., plus an admin user 'anishfyi')
- Random contacts for each user
- Some spam reports

### Accessing the Sample Data

1. **Login with a sample user account**:
   ```
   POST /api/auth/token/
   {
     "username": "anishfyi",
     "password": "testpass123"
   }
   ```
   (All sample users have the password "testpass123")

2. **View user accounts**:
   To see all sample users created, run:
   ```
   python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.values_list('username', 'email'))"
   ```

3. **Test searching**:
   After logging in, you can search using:
   - By name: `GET /api/search/?q=john`
   - By phone number: `GET /api/search/?q=+123456` or `GET /api/search/?type=phone&q=123456`

4. **View contacts**:
   To see all contacts for the logged-in user:
   ```
   GET /api/contacts/
   ```

Remember to include the authentication token in your requests:
```
Authorization: Bearer your_access_token
```
