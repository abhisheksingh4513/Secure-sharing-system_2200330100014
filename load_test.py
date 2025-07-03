#!/usr/bin/env python3
"""
Load testing script using Locust
To run: locust -f load_test.py
Then open http://localhost:8089/ in your browser
"""

import json
import random
from locust import HttpUser, task, between

class FileServerUser(HttpUser):
    """Simulate users interacting with the file sharing system"""
    
    wait_time = between(1, 5)  # Wait 1-5 seconds between tasks
    
    def on_start(self):
        """Setup before starting tests - authenticate users"""
        # Login as an ops user to upload files
        response = self.client.post(
            "/auth/ops-login",
            json={"username": "admin", "password": "admin123"}
        )
        if response.status_code == 200:
            self.ops_token = response.json()["access_token"]
        else:
            self.ops_token = None
            
        # Create and verify a client user
        username = f"loadtest_user_{random.randint(1000, 9999)}"
        self.username = username
        self.password = "testpassword"
        
        # Register client user
        response = self.client.post(
            "/auth/signup",
            json={
                "username": username,
                "password": self.password,
                "email": f"{username}@example.com",
                "user_type": "client"
            }
        )
        
        if response.status_code == 201:
            # In load testing, we'll manually verify users
            user_id = response.json().get("user_id", 1)  # Fallback to user_id 1 if not returned
            self.client.get(f"/auth/manual-verify/{user_id}")
            
            # Login as the client user
            response = self.client.post(
                "/auth/login",
                json={"username": self.username, "password": self.password}
            )
            if response.status_code == 200:
                self.client_token = response.json()["access_token"]
            else:
                self.client_token = None
        else:
            self.client_token = None

    @task(2)
    def upload_file(self):
        """Test file upload operation (ops user)"""
        if not self.ops_token:
            return
            
        # Generate random file content
        file_content = b"Test file content " + str(random.randint(1, 10000)).encode()
        file_type = random.choice(["docx", "xlsx", "pptx"])
        filename = f"loadtest_{random.randint(1000, 9999)}.{file_type}"
        
        # Set content type based on file extension
        content_types = {
            "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        }
        
        # Upload file
        self.client.post(
            "/files/upload", 
            headers={"Authorization": f"Bearer {self.ops_token}"},
            files={"file": (filename, file_content, content_types[file_type])}
        )

    @task(5)
    def list_files(self):
        """Test file listing operation (client user)"""
        if not self.client_token:
            return
            
        self.client.get(
            "/files/list",
            headers={"Authorization": f"Bearer {self.client_token}"}
        )
        
    @task(3)
    def get_and_download_file(self):
        """Test get download link and download file operations (client user)"""
        if not self.client_token:
            return
            
        # Get file list
        response = self.client.get(
            "/files/list",
            headers={"Authorization": f"Bearer {self.client_token}"}
        )
        
        if response.status_code == 200 and response.json():
            # Get a random file from the list
            files = response.json()
            if len(files) > 0:
                file = random.choice(files)
                file_id = file.get("id")
                
                # Get download link
                response = self.client.get(
                    f"/files/get-download-link/{file_id}",
                    headers={"Authorization": f"Bearer {self.client_token}"}
                )
                
                if response.status_code == 200:
                    download_link = response.json().get("download_link")
                    if download_link:
                        # Extract token and download file
                        token = download_link.split("/")[-1]
                        self.client.get(f"/files/secure-download/{token}")

    @task(1)
    def client_login(self):
        """Test client login operation"""
        self.client.post(
            "/auth/login",
            json={"username": self.username, "password": self.password}
        )
