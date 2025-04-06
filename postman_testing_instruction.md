## Testing with Postman

### Setting Up Postman

1. **Download and Install Postman**
   - Download Postman from [postman.com](https://www.postman.com/downloads/)
   - Install and open the application

2. **Create a New Collection**
   - Click on "Collections" in the sidebar
   - Click the "+" button to create a new collection
   - Name it "Caller Identification API"

3. **Set Up Environment Variables**
   - Click on "Environments" in the sidebar
   - Click the "+" button to create a new environment
   - Name it "Caller ID Local"
   - Add the following variables:
     - `base_url`: `http://127.0.0.1:8000/api`
     - `token`: Leave this empty (will be filled after login)

4. **Select the Environment**
   - In the top-right corner, select the "Caller ID Local" environment from the dropdown

> **Important Note:** 
- When copying URLs from this document to Postman, make sure to remove the backticks (`) that surround the URLs.

### Authentication Testing

1. **Register a New User**
   - Create a new POST request
   - URL: `{{base_url}}/auth/register/`
   - Headers: `Content-Type: application/json`
   - Body (raw JSON):
     ```json
     {
       "username": "anishfyi",
       "password": "securepassword123",
       "name": "Anish Singh",
       "phone_number": "+917004414932",
       "email": "anishfyi@gmail.com"
     }
     ```
   - Click "Send" to register

2. **Login**
   - Create a new POST request
   - URL: `{{base_url}}/auth/token/`
   - Headers: `Content-Type: application/json`
   - Body (raw JSON):
     ```json
     {
       "username": "anishfyi",
       "password": "securepassword123"
     }
     ```
   - Click "Send" to login
   - From the response, copy the `access` token value

3. **Set the Token**
   - Go to the Authorization tab, set the Bearer Token value to the copied access token.
   - Click "Save" to save the environment.

### Contact Management Testing

1. **Add a New Contact**
   - Create a new POST request
   - URL: `{{base_url}}/contacts/`
   - Headers: 
     - `Content-Type: application/json`
     - `Authorization: Bearer {{token}}`
   - Body (raw JSON):
     ```json
     {
       "name": "John Doe",
       "phone_number": "+919876543210"
     }
     ```
   - Click "Send" to create the contact

2. **Get All Contacts**
   - Create a new GET request
   - URL: `{{base_url}}/contacts/`
   - Headers: `Authorization: Bearer {{token}}`
   - Click "Send" to retrieve all contacts

3. **Import Multiple Contacts**
   - Create a new POST request
   - URL: `{{base_url}}/contacts/import/`
   - Headers: 
     - `Content-Type: application/json`
     - `Authorization: Bearer {{token}}`
   - Body (raw JSON):
     ```json
     {
       "contacts": [
         {
           "name": "Jane Smith",
           "phone_number": "+918765432109"
         },
         {
           "name": "Mike Johnson",
           "phone_number": "+917654321098"
         }
       ]
     }
     ```
   - Click "Send" to import contacts

### Spam Testing

1. **Report a Number as Spam**
   - Create a new POST request
   - URL: `{{base_url}}/spam/report/`
   - Headers: 
     - `Content-Type: application/json`
     - `Authorization: Bearer {{token}}`
   - Body (raw JSON):
     ```json
     {
       "phone_number": "+919999888877"
     }
     ```
   - Click "Send" to report the number

2. **Check Spam Likelihood**
   - Create a new GET request
   - URL: `{{base_url}}/spam/check/+919999888877/`
   - Headers: `Authorization: Bearer {{token}}`
   - Click "Send" to check spam likelihood

### Search Testing

1. **Search by Name**
   - Create a new GET request
   - URL: `{{base_url}}/search/?type=name&q=John`
   - Headers: `Authorization: Bearer {{token}}`
   - Click "Send" to search by name

2. **Search by Phone Number**
   - Create a new GET request
   - URL: `{{base_url}}/search/?type=phone&q=+91765432`
   - Headers: `Authorization: Bearer {{token}}`
   - Click "Send" to search by partial phone number

### Export Contacts

1. **Export as JSON**
   - Create a new GET request
   - URL: `{{base_url}}/contacts/export/?format=json`
   - Headers: `Authorization: Bearer {{token}}`
   - Click "Send" to export contacts as JSON

2. **Export as CSV**
   - Create a new GET request
   - URL: `{{base_url}}/contacts/export/csv`
   - Headers: `Authorization: Bearer {{token}}`
   - Click "Send" to export contacts as CSV

## Sample Data Generation with Custom User (The Script that will populate your database with a decent amount of random, sample data.)

The project includes a custom management command to populate the database with sample data for testing. You can find it at:
`contacts/management/commands/populate_sample_data.py`

You can run this command to generate sample data for testing purposes:

```bash
python manage.py populate_sample_data
```

Optional parameters:
- `--users`: Number of users to create (default: 20)
- `--contacts`: Number of contacts to create (default: 100)
- `--spam-reports`: Number of spam reports to create (default: 30)

Example:
```bash
python manage.py populate_sample_data --users 10 --contacts 50 --spam-reports 15
```