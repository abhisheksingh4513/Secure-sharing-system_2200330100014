# 🌐 How to Use the Secure File Sharing System

## 🚀 **Your System is Now Live!**

**Web Interface**: http://localhost:8000  
**API Documentation**: http://localhost:8000/docs

---

## 👥 **User Guide**

### **🔑 For Operations Users (File Uploaders)**

1. **Login as Operations User**:
   - Go to http://localhost:8000
   - Click "Login" tab
   - Select "Operations User" from dropdown
   - **Username**: `admin`
   - **Password**: `admin123`
   - Click "Login"

2. **Upload Files**:
   - Click "Upload Files" tab
   - Drag & drop your file OR click to select
   - Only **.pptx**, **.docx**, **.xlsx** files allowed (Max 50MB)
   - Click "Upload File"
   - You'll see upload progress and success message

### **📥 For Client Users (File Downloaders)**

1. **Sign Up**:
   - Click "Sign Up" tab
   - Enter your email, username, password
   - Click "Sign Up"
   - Click "Verify Email (Demo)" button to activate your account

2. **Login**:
   - Click "Login" tab
   - Select "Client User" from dropdown
   - Enter your username/password
   - Click "Login"

3. **Download Files**:
   - Click "Download Files" tab
   - Click "🔄 Refresh File List" to see available files
   - Click "📥 Download" next to any file
   - File will download with a secure, encrypted URL

---

## 🔒 **Security Features in Action**

### **Secure Download Process**:
1. Client requests download → Gets encrypted token
2. Token is valid for 1 hour only
3. Token can only be used once
4. Only authenticated client users can access

### **File Upload Restrictions**:
- Only Operations users can upload
- File types strictly validated (.pptx, .docx, .xlsx only)
- File size limited to 50MB
- Files stored with secure random names

### **User Access Control**:
- Operations users: Can only upload files
- Client users: Can only download files
- No cross-user type access allowed

---

## 🧪 **Testing the System**

### **Test Scenario 1: Operations User Workflow**
```
1. Login as: admin / admin123
2. Go to Upload Files tab
3. Upload a .docx/.pptx/.xlsx file
4. Verify upload success
```

### **Test Scenario 2: Client User Workflow**
```
1. Sign up new client user
2. Verify email (click demo button)
3. Login with new credentials
4. Go to Download Files tab
5. Download uploaded files
```

### **Test Scenario 3: Security Validation**
```
1. Try uploading .txt file (should fail)
2. Try downloading without login (should fail)
3. Try accessing download URL directly (should work once)
4. Try reusing same download URL (should fail)
```

---

## 🌐 **Sharing Your System**

### **Option 1: Local Network Sharing**
1. Find your local IP address:
   ```bash
   ipconfig
   # Look for IPv4 Address (e.g., 192.168.1.100)
   ```

2. Update the system to accept external connections:
   - Stop the current server (Ctrl+C in terminal)
   - Restart with:
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

3. Share this URL with others on your network:
   ```
   http://YOUR_IP_ADDRESS:8000
   # Example: http://192.168.1.100:8000
   ```

### **Option 2: Internet Sharing (Advanced)**
For internet access, you would need:
- Port forwarding on your router (port 8000)
- Dynamic DNS service
- SSL certificate for HTTPS
- Production database (PostgreSQL)

### **Option 3: Cloud Deployment**
Deploy to platforms like:
- **Heroku**: Free tier available
- **Railway**: Easy deployment
- **DigitalOcean**: VPS hosting
- **AWS/Google Cloud**: Enterprise solutions

---

## 📋 **API Endpoints Summary**

### **Authentication**
- `POST /auth/signup` - Client user registration
- `POST /auth/login` - Client user login
- `POST /auth/ops-login` - Operations user login
- `POST /auth/manual-verify/{user_id}` - Manual email verification

### **File Operations**
- `POST /files/upload` - Upload file (ops users only)
- `GET /files/list` - List all files (client users only)
- `GET /files/download-file/{file_id}` - Get secure download link
- `GET /files/download-file/{token}` - Download file with token

---

## 🔧 **Troubleshooting**

### **Common Issues**:

1. **"API Offline" status**:
   - Make sure the server is running
   - Check if port 8000 is available

2. **Upload fails**:
   - Check file type (.pptx, .docx, .xlsx only)
   - Check file size (max 50MB)
   - Make sure you're logged in as ops user

3. **Download fails**:
   - Make sure you're logged in as client user
   - Check if files exist (refresh file list)

4. **Login fails**:
   - Check credentials
   - For ops user: admin/admin123
   - For client: must be registered and verified

### **Reset System**:
```bash
# Delete database and start fresh
rm file_sharing.db
python init_db.py
```

---

## 🎯 **Next Steps**

Your secure file sharing system is complete and operational! You can:

1. **Use it as-is** for local file sharing
2. **Customize the UI** by editing `index.html`
3. **Add features** like file preview, user management
4. **Deploy to cloud** for internet access
5. **Integrate with email** for real email verification

**🎉 Enjoy your secure file sharing system!**
