# Secure File Sharing System

A secure file-sharing system built with FastAPI that supports two types of users: Operations Users and Client Users. This system implements role-based access control, secure file uploads/downloads, and email verification.

## Features

- **Role-based Access Control**: Operations users can upload files, Client users can download files
- **Secure File Upload**: Only supports .pptx, .docx, and .xlsx files with size validation
- **Email Verification**: Client users must verify their email before accessing the system
- **Secure Download Links**: Encrypted, time-limited, one-time use download URLs
- **File Management**: Complete file listing and management system
- **API Documentation**: Comprehensive Swagger UI and Postman collection for testing

## Project Structure

```
ez-lab-assignmet/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database models and configuration
│   ├── schemas.py           # Pydantic models for data validation
│   ├── auth.py              # Authentication and security utilities
│   ├── file_utils.py        # File handling utilities
│   ├── email_service.py     # Email service for verification
│   └── routers/
│       ├── __init__.py
│       ├── auth.py          # Authentication endpoints
│       └── files.py         # File operation endpoints
├── uploads/                 # File upload directory (created automatically)
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables configuration
├── init_db.py               # Database initialization script
├── run.py                   # Application runner
├── test_system.py           # System test script
├── Secure_File_Sharing_API.postman_collection.json   # Postman collection
├── Secure_File_Sharing.postman_environment.json      # Postman environment
├── POSTMAN_API_GUIDE.md     # Detailed Postman API documentation
├── STEP_BY_STEP_POSTMAN_GUIDE.md # Step-by-step Postman testing guide
├── DATABASE_CONNECTION_GUIDE.md  # Database connection guide
└── README.md                # This file
```

## Complete Setup Guide for New Users

### 1. Clone the Repository

```bash
# Clone the repository to your local machine
git clone https://github.com/yourusername/secure-file-sharing.git
# Or download and extract the ZIP file

# Navigate to the project directory
cd secure-file-sharing
```

### 2. Set Up Python Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

# Your command prompt should now show (venv) at the beginning
```

### 3. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# If you want to use a different database (optional)
# Uncomment and install the appropriate database driver in requirements.txt
# For PostgreSQL: pip install psycopg2-binary
# For MySQL: pip install pymysql
# For SQL Server: pip install pyodbc
```

### 4. Configure Environment Variables

1. Open the `.env` file in the root directory
2. Update the following settings:

```properties
# Security (IMPORTANT: Change this in production)
SECRET_KEY=your-super-secret-key-here-change-this-in-production

# Database Configuration
# SQLite is configured by default (no action needed for development)
# For production, uncomment and configure one of the other database options

# Email Configuration (Required for email verification)
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_FROM=your-email@gmail.com
```

### 5. Initialize the Database & Create Admin User

```bash
# Run the initialization script
python init_db.py

# This creates the database tables and a default admin user:
# Username: admin
# Password: admin123
# Email: admin@fileserver.com
```

### 6. Create Upload Directory (if it doesn't exist)

```bash
# Create the uploads directory
mkdir uploads
```

### 7. Run the Application

```bash
# Start the FastAPI server
python run.py

# The server will start at http://localhost:8000
# API documentation is available at http://localhost:8000/docs
```

## Testing with Postman

The project includes a complete Postman collection and environment for testing all API endpoints. This is the recommended method for new users to test and understand the system.

### Setting Up Postman

1. Download and install [Postman](https://www.postman.com/downloads/)
2. Import the collection:
   - Open Postman
   - Click "Import" button
   - Select `Secure_File_Sharing_API.postman_collection.json` from the project directory
3. Import the environment:
   - Click "Import" button again
   - Select `Secure_File_Sharing.postman_environment.json` from the project directory
4. Select the "Secure File Sharing Environment" from the environment dropdown in the top-right corner

### Running the Tests

The collection is designed to be run in sequence to test the complete workflow:

1. **Authentication**:
   - **Login as Operations User**: Use the default admin credentials
   - **Create Client User**: Register a new client user
   - **Manually Verify Client**: Since email verification is optional in testing
   - **Login as Client User**: Login with the newly created client user

2. **File Operations**:
   - **Upload File (as Operations User)**: Test file upload restrictions
   - **List Files (as Client User)**: View available files
   - **Generate Download Link**: Create secure, one-time download URL
   - **Download File**: Use the secure link to download the file

The collection includes pre-request scripts and test scripts that automatically:
- Store authentication tokens
- Pass data between requests
- Validate responses
- Generate dynamic test data

For detailed instructions, refer to `STEP_BY_STEP_POSTMAN_GUIDE.md` in the project directory.

## API Endpoints Reference

### Authentication

#### 1. Client User Signup
- **POST** `/auth/signup`
- **Body**: 
  ```json
  {
    "email": "client@example.com",
    "username": "client1",
    "password": "password123",
    "user_type": "client"
  }
  ```

#### 2. Email Verification
- **GET** `/auth/verify-email?token={verification_token}`
- For testing: **GET** `/auth/manual-verify/{user_id}`

#### 3. Client User Login
- **POST** `/auth/login`
- **Body**:
  ```json
  {
    "username": "client1",
    "password": "password123"
  }
  ```

#### 4. Operations User Login
- **POST** `/auth/ops-login`
- **Body**:
  ```json
  {
    "username": "admin",
    "password": "admin123"
  }
  ```

### File Operations

#### 5. Upload File (Operations Users Only)
- **POST** `/files/upload`
- **Headers**: `Authorization: Bearer {access_token}`
- **Body**: Form data with file
- **Allowed file types**: .pptx, .docx, .xlsx
- **Max file size**: 50MB

#### 6. List Files (Client Users Only)
- **GET** `/files/list`
- **Headers**: `Authorization: Bearer {access_token}`

#### 7. Get Download Link (Client Users Only)
- **GET** `/files/get-download-link/{file_id}`
- **Headers**: `Authorization: Bearer {access_token}`

#### 8. Download File (Secure One-Time Download)
- **GET** `/files/secure-download/{token}`

## Security Features

The system implements multiple layers of security:

1. **JWT Authentication**: Secure token-based authentication with expiration
2. **Password Hashing**: Bcrypt password hashing with salt
3. **Email Verification**: Mandatory email verification for client users
4. **File Type Validation**: Only allows specific file types (.pptx, .docx, .xlsx)
5. **File Size Limits**: Maximum 50MB file size
6. **Secure Download URLs**: Time-limited, one-time use download tokens
7. **Role-based Access Control**: Strict separation between operations and client user permissions
8. **Input Validation**: Pydantic models for request validation
9. **Exception Handling**: Comprehensive error handling and logging

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check your .env DATABASE_URL setting
   - Ensure the database driver is installed
   - See `DATABASE_CONNECTION_GUIDE.md` for detailed instructions

2. **Email Verification Problems**
   - Check SMTP settings in .env
   - For Gmail, use App Password instead of regular password
   - For testing, use the manual verification endpoint

3. **File Upload Issues**
   - Ensure the uploads directory exists and is writable
   - Check file type (only .pptx, .docx, .xlsx allowed)
   - Check file size (max 50MB)

4. **Permission Denied Errors**
   - Verify user roles (operations vs client)
   - Check that JWT token is valid and not expired
   - Ensure client users are verified before accessing files

### Running Tests

The project includes a test script that validates core functionality:

```bash
# Run the system test script
python test_system.py
```

This will test authentication flows, file operations, and access control.

## API Documentation

Once the application is running, you can access:

- **Interactive Swagger UI**: http://localhost:8000/docs
  - Test endpoints directly in the browser
  - See request/response schemas
  - Authenticate with the "Authorize" button

- **ReDoc Documentation**: http://localhost:8000/redoc
  - Clean, organized API reference

## Command-Line Testing (Alternative to Postman)

If you prefer using curl commands for testing:

### 1. Operations User Login
```bash
curl -X POST "http://localhost:8000/auth/ops-login" ^
     -H "Content-Type: application/json" ^
     -d "{\"username\": \"admin\", \"password\": \"admin123\"}"
```

### 2. File Upload (with ops token)
```bash
curl -X POST "http://localhost:8000/files/upload" ^
     -H "Authorization: Bearer YOUR_OPS_TOKEN" ^
     -F "file=@test.xlsx"
```

### 3. Client Signup
```bash
curl -X POST "http://localhost:8000/auth/signup" ^
     -H "Content-Type: application/json" ^
     -d "{\"email\": \"client@test.com\", \"username\": \"testclient\", \"password\": \"password123\", \"user_type\": \"client\"}"
```

### 4. Manual Verification (for testing)
```bash
curl -X GET "http://localhost:8000/auth/manual-verify/1" 
```

### 5. Client Login
```bash
curl -X POST "http://localhost:8000/auth/login" ^
     -H "Content-Type: application/json" ^
     -d "{\"username\": \"testclient\", \"password\": \"password123\"}"
```

### 6. List Files (with client token)
```bash
curl -X GET "http://localhost:8000/files/list" ^
     -H "Authorization: Bearer YOUR_CLIENT_TOKEN"
```

### 7. Get Download Link
```bash
curl -X GET "http://localhost:8000/files/get-download-link/1" ^
     -H "Authorization: Bearer YOUR_CLIENT_TOKEN"
```

## Environment Variables Reference

| Variable | Description | Default | Required? |
|----------|-------------|---------|-----------|
| SECRET_KEY | JWT secret key for token signing | random string | Yes |
| ALGORITHM | JWT algorithm | HS256 | Yes |
| ACCESS_TOKEN_EXPIRE_MINUTES | JWT token expiration time | 30 | Yes |
| DATABASE_URL | Database connection string | sqlite:///./file_sharing.db | Yes |
| UPLOAD_DIRECTORY | File upload directory | ./uploads | Yes |
| MAX_FILE_SIZE | Maximum file size in bytes | 50000000 | Yes |
| ALLOWED_EXTENSIONS | Allowed file extensions | pptx,docx,xlsx | Yes |
| SMTP_SERVER | Email SMTP server | smtp.gmail.com | For email verification |
| SMTP_PORT | Email SMTP port | 587 | For email verification |
| EMAIL_USERNAME | Email username | None | For email verification |
| EMAIL_PASSWORD | Email password | None | For email verification |
| EMAIL_FROM | Sender email address | None | For email verification |

## Production Deployment Checklist

When moving to production, make these important changes:

1. **Security Hardening**
   - Generate a strong unique SECRET_KEY (use `openssl rand -hex 32`)
   - Use HTTPS with a valid SSL certificate
   - Configure CORS to specific domains

2. **Database Configuration**
   - Use PostgreSQL or MySQL instead of SQLite
   - Set up proper database credentials
   - Configure regular database backups

3. **Email Setup**
   - Configure SMTP with a reliable email provider
   - Set up email monitoring and delivery tracking

4. **File Storage**
   - Consider cloud storage (AWS S3, Azure Blob Storage)
   - Implement file encryption at rest

5. **Deployment Options**
   - Docker containerization
   - Deploy behind reverse proxy (Nginx/Apache)
   - Set up load balancing for high availability

6. **Monitoring & Logging**
   - Set up centralized logging
   - Implement request tracing
   - Configure performance monitoring
   - Set up alerts for security events

For more deployment details, refer to the FastAPI documentation on deployment: https://fastapi.tiangolo.com/deployment/

## Additional Documentation

This project includes several detailed guides to help you:

1. **POSTMAN_API_GUIDE.md**: Detailed overview of the API endpoints and testing with Postman
2. **STEP_BY_STEP_POSTMAN_GUIDE.md**: Walkthrough for testing the complete system flow
3. **DATABASE_CONNECTION_GUIDE.md**: How to configure different database backends
4. **USAGE_GUIDE.md**: Day-to-day usage instructions
5. **FIXES_APPLIED.md**: History of bug fixes and improvements
6. **PROJECT_SUMMARY.md**: High-level overview of the project architecture

## License

This project is licensed under the MIT License.

---

For questions or support, please create an issue in the project repository.

Last updated: July 2023
