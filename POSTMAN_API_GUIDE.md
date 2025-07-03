# 🔐 Secure File Sharing System - API Documentation

## 📖 Overview
This is a complete Postman collection for testing the Secure File Sharing System API. The system implements role-based access control with two user types: Operations Users (can upload files) and Client Users (can download files).

## 🚀 Quick Start

### 1. Import to Postman
1. Open Postman
2. Click "Import" button
3. Select `Secure_File_Sharing_API.postman_collection.json`
4. Import the environment file: `Secure_File_Sharing.postman_environment.json`
5. Select the "Secure File Sharing Environment" from the environment dropdown

### 2. Start the Server
```bash
cd "c:\Users\Abhishek Singh\OneDrive\Pictures\Desktop\New folder\ez-lab-assignmet"
python run.py
```

### 3. Run the Collection
- **Option A**: Run individual requests in the suggested order
- **Option B**: Use Postman's Collection Runner to run all tests automatically

## 📋 API Endpoints

### 🔐 Authentication Endpoints

#### 1. Operations User Login
- **Method**: `POST`
- **URL**: `/auth/ops-login`
- **Purpose**: Login for Operations users who can upload files
- **Body**:
```json
{
    "username": "admin",
    "password": "admin123"
}
```
- **Response**: JWT token stored in `ops_token` variable

#### 2. Client User Signup
- **Method**: `POST`
- **URL**: `/auth/signup`
- **Purpose**: Register new client users
- **Body**:
```json
{
    "email": "client@example.com",
    "username": "testclient",
    "password": "password123",
    "user_type": "client"
}
```
- **Response**: User ID and verification URL

#### 3. Manual Email Verification
- **Method**: `POST`
- **URL**: `/auth/manual-verify/{user_id}`
- **Purpose**: Verify email (demo endpoint)
- **Note**: In production, users would click email link

#### 4. Client User Login
- **Method**: `POST`
- **URL**: `/auth/login`
- **Purpose**: Login for Client users who can download files
- **Body**:
```json
{
    "username": "testclient",
    "password": "password123"
}
```
- **Response**: JWT token stored in `client_token` variable

### 📁 File Operation Endpoints

#### 5. File Upload (Operations Only)
- **Method**: `POST`
- **URL**: `/files/upload`
- **Headers**: `Authorization: Bearer {{ops_token}}`
- **Body**: Form-data with file field
- **Allowed Types**: `.pptx`, `.docx`, `.xlsx`
- **Max Size**: 50MB
- **Response**: File information with ID

#### 6. List Files (Client Only)
- **Method**: `GET`
- **URL**: `/files/list`
- **Headers**: `Authorization: Bearer {{client_token}}`
- **Purpose**: List all uploaded files
- **Response**: Array of file objects

#### 7. Get Secure Download Link (Client Only)
- **Method**: `GET`
- **URL**: `/files/get-download-link/{file_id}`
- **Headers**: `Authorization: Bearer {{client_token}}`
- **Purpose**: Generate encrypted, time-limited download URL
- **Response**:
```json
{
    "download_link": "/files/secure-download/encrypted_token",
    "message": "success"
}
```

#### 8. Download File with Secure Token
- **Method**: `GET`
- **URL**: `{{download_link}}` (full URL from previous response)
- **Purpose**: Download file using one-time token
- **Response**: File content (binary)
- **Note**: Token expires after use

## 🛡️ Security Tests

The collection includes comprehensive security tests:

1. **Role Separation**: Client users cannot upload, Ops users cannot download
2. **File Type Validation**: Only allowed file types (.pptx, .docx, .xlsx)
3. **Authentication Required**: All endpoints require valid tokens
4. **One-Time Use**: Download tokens expire after use
5. **Time-Limited**: Download tokens have expiration time

## 🔄 Suggested Test Flow

### Complete System Test (Run in Order):
1. **Operations User Login** → Get ops token
2. **Client User Signup** → Register client
3. **Manual Email Verification** → Verify email
4. **Client User Login** → Get client token
5. **Upload File** → Upload using ops token
6. **List Files** → List using client token
7. **Get Download Link** → Generate secure URL
8. **Download File** → Download using secure token
9. **Try Download Again** → Should fail (one-time use)

### Security Tests:
- Try upload as client user (should fail)
- Try list files as ops user (should fail)
- Try invalid file type upload (should fail)
- Try access without authentication (should fail)

## 📊 Test Results

After running the collection, you should see:
- ✅ **8 Successful Requests** (main flow)
- ✅ **4 Security Failures** (expected failures proving security)
- ✅ **All Tests Passing** (assertions validate responses)

## 🔧 Environment Variables

The collection uses these environment variables:
- `base_url`: API server URL (http://localhost:8000)
- `ops_token`: Operations user JWT token
- `client_token`: Client user JWT token
- `user_id`: Created user ID for verification
- `file_id`: Uploaded file ID
- `download_link`: Generated secure download URL

## 📝 Example Responses

### Successful Login Response:
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "user_type": "client"
}
```

### File Upload Response:
```json
{
    "id": 1,
    "filename": "uuid-filename.docx",
    "original_filename": "test_document.docx",
    "file_size": 1024,
    "file_type": "docx",
    "upload_date": "2025-07-02T10:00:00Z",
    "message": "File uploaded successfully"
}
```

### Download Link Response:
```json
{
    "download_link": "/files/secure-download/encrypted_token_here",
    "message": "success"
}
```

## 🚨 Common Issues & Solutions

### 1. Server Not Running
**Error**: Connection refused
**Solution**: Start server with `python run.py`

### 2. Authentication Failed
**Error**: 401 Unauthorized
**Solution**: Run login requests first to get tokens

### 3. File Upload Failed
**Error**: 400 Bad Request
**Solution**: Ensure file type is .pptx, .docx, or .xlsx

### 4. Download Link Expired
**Error**: 404 Not Found
**Solution**: Generate new download link (tokens are one-time use)

## 🎯 Success Criteria

Your API is working correctly if:
- ✅ Operations users can login and upload files
- ✅ Client users can signup, verify, login, and download files
- ✅ Role-based access is enforced (no cross-access)
- ✅ Only allowed file types are accepted
- ✅ Download tokens are one-time use
- ✅ Secure encrypted URLs are generated
- ✅ Authentication is required for all operations

## 🔍 API Documentation

For interactive API documentation, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📞 Support

If you encounter any issues:
1. Check that the server is running on http://localhost:8000
2. Verify that the database is initialized (`python init_db.py`)
3. Ensure all dependencies are installed (`pip install -r requirements.txt`)
4. Check the console output for error messages

---

**🎉 Your secure file-sharing system is ready for testing!**
