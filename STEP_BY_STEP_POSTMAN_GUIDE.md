# 🚀 Step-by-Step Postman Testing Guide

## 📋 Pre-requisites
1. **Postman installed** (download from https://www.postman.com/downloads/)
2. **Server running** on http://localhost:8000
3. **Collection files** ready to import

---

## 🔧 Step 1: Setup Postman Environment

### 1.1 Import the Collection
1. **Open Postman**
2. **Click "Import"** button (top left)
3. **Select "Upload Files"**
4. **Choose** `Secure_File_Sharing_API.postman_collection.json`
5. **Click "Import"**

### 1.2 Import the Environment
1. **Click "Import"** again
2. **Select "Upload Files"**
3. **Choose** `Secure_File_Sharing.postman_environment.json`
4. **Click "Import"**

### 1.3 Select Environment
1. **Click environment dropdown** (top right corner)
2. **Select "Secure File Sharing Environment"**
3. **Verify** `base_url` is set to `http://localhost:8000`

---

## 🏃‍♂️ Step 2: Start Your Server

### 2.1 Open Terminal/Command Prompt
```bash
cd "c:\Users\Abhishek Singh\OneDrive\Pictures\Desktop\New folder\ez-lab-assignmet"
python run.py
```

### 2.2 Verify Server is Running
- **Look for**: "API Documentation available at: http://localhost:8000/docs"
- **Test in browser**: Visit http://localhost:8000/docs

---

## 🔐 Step 3: Test Authentication Endpoints

### 3.1 Operations User Login
1. **Find** "Authentication" folder in collection
2. **Click** "Operations User Login"
3. **Check URL**: Should be `{{base_url}}/auth/ops-login`
4. **Check Method**: Should be `POST`
5. **Check Body**: 
   ```json
   {
       "username": "admin",
       "password": "admin123"
   }
   ```
6. **Click "Send"**
7. **Expected Response**: Status 200 with access token
8. **Verify**: Check that `ops_token` variable is automatically set

### 3.2 Client User Signup
1. **Click** "Client User Signup"
2. **Check URL**: `{{base_url}}/auth/signup`
3. **Check Body**:
   ```json
   {
       "email": "client@example.com",
       "username": "testclient",
       "password": "password123",
       "user_type": "client"
   }
   ```
4. **Click "Send"**
5. **Expected Response**: Status 200 with user_id and verification_url
6. **Verify**: Check that `user_id` is set in environment

### 3.3 Manual Email Verification
1. **Click** "Manual Email Verification (Demo)"
2. **Check URL**: `{{base_url}}/auth/manual-verify/{{user_id}}`
3. **Check Method**: POST
4. **Click "Send"**
5. **Expected Response**: Status 200 - Email verified

### 3.4 Client User Login
1. **Click** "Client User Login"
2. **Check URL**: `{{base_url}}/auth/login`
3. **Check Body**:
   ```json
   {
       "username": "testclient",
       "password": "password123"
   }
   ```
4. **Click "Send"**
5. **Expected Response**: Status 200 with client access token
6. **Verify**: Check that `client_token` is set

---

## 📁 Step 4: Test File Operations

### 4.1 Upload File (Operations User)
1. **Find** "File Operations" folder
2. **Click** "Upload File (Operations Only)"
3. **Check URL**: `{{base_url}}/files/upload`
4. **Check Headers**: `Authorization: Bearer {{ops_token}}`
5. **Check Body Type**: Select "form-data"
6. **Add File**:
   - **Key**: `file`
   - **Type**: File
   - **Value**: Select `test_document_for_postman.docx` (or any .docx/.pptx/.xlsx file)
7. **Click "Send"**
8. **Expected Response**: Status 200 with file details
9. **Verify**: `file_id` is automatically stored

### 4.2 List Files (Client User)
1. **Click** "List All Files (Client Only)"
2. **Check URL**: `{{base_url}}/files/list`
3. **Check Headers**: `Authorization: Bearer {{client_token}}`
4. **Click "Send"**
5. **Expected Response**: Status 200 with array of files
6. **Verify**: You can see the uploaded file in the list

### 4.3 Get Secure Download Link
1. **Click** "Get Secure Download Link (Client Only)"
2. **Check URL**: `{{base_url}}/files/get-download-link/{{file_id}}`
3. **Check Headers**: `Authorization: Bearer {{client_token}}`
4. **Click "Send"**
5. **Expected Response**: Status 200 with download_link
   ```json
   {
       "download_link": "/files/secure-download/encrypted_token",
       "message": "success"
   }
   ```
6. **Verify**: `download_link` is stored in environment

### 4.4 Download File with Secure Token
1. **Click** "Download File with Secure Token"
2. **Check URL**: `{{base_url}}{{download_link}}`
3. **Click "Send"**
4. **Expected Response**: Status 200 with file content (binary)
5. **Check**: Response should show file size and download successful

### 4.5 Test One-Time Use (Should Fail)
1. **Click** "Test Download Again (Should Fail - One-time Use)"
2. **Check URL**: Same as above
3. **Click "Send"**
4. **Expected Response**: Status 404 - "Invalid or expired download link"

---

## 🛡️ Step 5: Test Security Features

### 5.1 Try Upload as Client (Should Fail)
1. **Find** "Security Tests" folder
2. **Click** "Try Upload as Client (Should Fail)"
3. **Check Headers**: Uses `{{client_token}}` (client token)
4. **Click "Send"**
5. **Expected Response**: Status 403 - Forbidden

### 5.2 Try List Files as Ops User (Should Fail)
1. **Click** "Try List Files as Ops User (Should Fail)"
2. **Check Headers**: Uses `{{ops_token}}` (ops token)
3. **Click "Send"**
4. **Expected Response**: Status 403 - Forbidden

### 5.3 Try Invalid File Type
1. **Click** "Try Invalid File Type Upload"
2. **Upload a .txt file** instead of allowed types
3. **Click "Send"**
4. **Expected Response**: Status 400 - File type not allowed

### 5.4 Try Access Without Authentication
1. **Click** "Try Access Without Authentication"
2. **Check**: No Authorization header
3. **Click "Send"**
4. **Expected Response**: Status 401 - Unauthorized

---

## 🔍 Step 6: Verify System Health

### 6.1 API Health Check
1. **Find** "System Health" folder
2. **Click** "API Health Check"
3. **Check URL**: `{{base_url}}/`
4. **Click "Send"**
5. **Expected Response**: Status 200

### 6.2 API Documentation
1. **Click** "API Documentation"
2. **Check URL**: `{{base_url}}/docs`
3. **Click "Send"**
4. **Expected Response**: HTML page with Swagger UI

---

## 📊 Step 7: Use Collection Runner (Automated Testing)

### 7.1 Run Entire Collection
1. **Right-click** on collection name
2. **Select "Run collection"**
3. **Click "Run Secure File Sharing System API"**
4. **Watch** all tests execute automatically

### 7.2 Expected Results
- ✅ **12 requests** should run
- ✅ **8 successful** (main functionality)
- ✅ **4 expected failures** (security tests)
- ✅ **All assertions** should pass

---

## 🔧 Step 8: Manual Testing Each Endpoint

If you prefer manual testing without collection:

### 8.1 Create New Request
1. **Click "New"** → "HTTP Request"
2. **Set Method**: GET/POST as needed
3. **Enter URL**: http://localhost:8000/endpoint
4. **Add Headers** (if needed):
   - `Content-Type: application/json`
   - `Authorization: Bearer your_token_here`
5. **Add Body** (for POST requests):
   - Select "raw" and "JSON"
   - Enter JSON data

### 8.2 Example Manual Test - Login
1. **Method**: POST
2. **URL**: `http://localhost:8000/auth/ops-login`
3. **Headers**: `Content-Type: application/json`
4. **Body**:
   ```json
   {
       "username": "admin",
       "password": "admin123"
   }
   ```
5. **Click Send**

---

## 🎯 Expected Results Summary

After completing all steps, you should have:

1. ✅ **Successfully logged in** as both user types
2. ✅ **Uploaded a file** as operations user
3. ✅ **Listed files** as client user
4. ✅ **Generated secure download link**
5. ✅ **Downloaded file** using secure token
6. ✅ **Verified one-time use** (second download fails)
7. ✅ **Confirmed role-based security** (cross-access fails)
8. ✅ **Validated file type restrictions**

---

## 🚨 Troubleshooting

### Server Not Responding
- **Check**: Is `python run.py` running?
- **Check**: Is port 8000 available?
- **Try**: Visit http://localhost:8000/docs in browser

### Authentication Issues
- **Check**: Did login request succeed?
- **Check**: Is token stored in environment variables?
- **Try**: Re-run login requests

### File Upload Issues
- **Check**: Is file type .docx, .pptx, or .xlsx?
- **Check**: Is file size under 50MB?
- **Check**: Are you using ops_token (not client_token)?

### Download Issues
- **Check**: Did you get download link first?
- **Check**: Is download link properly stored?
- **Try**: Generate new download link (tokens are one-time use)

---

**🎉 Your API testing is complete! All endpoints should work as expected.**
