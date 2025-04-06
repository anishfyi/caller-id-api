# Setup and Installation

## Prerequisites
- Python 3.8 or higher
- Git (for cloning the repository)

## Setup Options

### Option 1: Clone from GitHub
1. Clone the repository
   ```
   git clone https://github.com/yourusername/caller-id-api.git
   cd caller-id-api
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

4. Set up environment variables
   ```
   # Create a .env file in the project root with the following content:
   DEBUG=True
   SECRET_KEY=django-insecure-2%g9_s-#p&j6hv51_$*phyb2@#8d8!6ae$q8z9$+gla4^o7jmy
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. Run migrations
   ```
   python manage.py migrate
   ```

6. Start the development server
   ```
   python manage.py runserver
   ```

The API will be available at http://127.0.0.1:8000/

### Option 2: Using the provided files
1. Extract the project files to your desired location
   ```
   Open terminal in this folder caller-id-api
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

