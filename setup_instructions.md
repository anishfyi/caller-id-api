## Setup and Installation

### Prerequisites
- Python 3.8 or higher

### Steps

1. Extract the project files to your desired location
   ```
   Open terminal in this folder caller_identification_anishfyi
   ```

2. Create a virtual environment
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Run migrations
   ```
   python manage.py migrate
   ```

5. Start the development server
   ```
   python manage.py runserver
   ```

The API will be available at http://127.0.0.1:8000/

## Testing

The project includes unit and integration tests using pytest. To run the tests:

```
pytest
```

For more detailed test output:

```
pytest -v
```

## Sample Data Generation

The project includes a management command to generate sample data for testing. To populate the database with sample data:

```
python manage.py populate_sample_data
```

You can customize the amount of data generated:

```
python manage.py populate_sample_data --users 20 --contacts 100 --spam-reports 30
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/login/` - Login to get JWT token
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `GET /api/auth/profile/` - Get user profile

### Contacts
- `GET /api/contacts/` - List all contacts
- `POST /api/contacts/` - Add a new contact
- `GET /api/contacts/<id>/` - Get contact details
- `PUT /api/contacts/<id>/` - Update contact
- `DELETE /api/contacts/<id>/` - Delete contact
- `POST /api/contacts/import/` - Bulk import contacts
- `GET /api/contacts/export/` - Export contacts

### Spam
- `POST /api/spam/report/` - Report a number as spam
- `GET /api/spam/check/<phone_number>/` - Check spam likelihood

### Search
- `GET /api/search/` - Search for contacts by name or phone

