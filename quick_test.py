#!/usr/bin/env python3
"""
Quick test to verify the system is working
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoints():
    print("🧪 Testing Fixed Endpoints\n")
    
    # Test 1: Operations user login
    print("1. Testing Ops Login...")
    login_response = requests.post(f"{BASE_URL}/auth/ops-login", json={
        "username": "admin",
        "password": "admin123"
    })
    
    if login_response.status_code == 200:
        ops_token = login_response.json()["access_token"]
        print("✅ Ops login successful")
        
        # Test 2: Check files list endpoint
        print("\n2. Testing File List Endpoint...")
        # First login as client to test list
        client_signup = requests.post(f"{BASE_URL}/auth/signup", json={
            "email": "testuser@example.com",
            "username": "testuser123",
            "password": "password123",
            "user_type": "client"
        })
        
        if client_signup.status_code == 200:
            user_id = client_signup.json()["user_id"]
            
            # Verify user
            verify_response = requests.post(f"{BASE_URL}/auth/manual-verify/{user_id}")
            if verify_response.status_code == 200:
                print("✅ User verification successful")
                
                # Login as client
                client_login = requests.post(f"{BASE_URL}/auth/login", json={
                    "username": "testuser123",
                    "password": "password123"
                })
                
                if client_login.status_code == 200:
                    client_token = client_login.json()["access_token"]
                    print("✅ Client login successful")
                    
                    # Test file list
                    list_response = requests.get(f"{BASE_URL}/files/list", headers={
                        "Authorization": f"Bearer {client_token}"
                    })
                    
                    if list_response.status_code == 200:
                        files = list_response.json()
                        print(f"✅ File list endpoint working - {len(files)} files found")
                        
                        # Test 3: Check download endpoint structure
                        print("\n3. Testing Download Endpoint Structure...")
                        if len(files) > 0:
                            file_id = files[0]["id"]
                            download_response = requests.get(f"{BASE_URL}/files/get-download-link/{file_id}", headers={
                                "Authorization": f"Bearer {client_token}"
                            })
                            
                            if download_response.status_code == 200:
                                download_data = download_response.json()
                                print("✅ Download link generation working")
                                print(f"   Download URL: {download_data['download_link']}")
                                
                                # Test the actual download URL
                                secure_url = f"{BASE_URL}{download_data['download_link']}"
                                secure_response = requests.get(secure_url)
                                print(f"   Secure download status: {secure_response.status_code}")
                                
                                if secure_response.status_code == 200:
                                    print("✅ Secure download working!")
                                else:
                                    print(f"❌ Secure download failed: {secure_response.status_code}")
                            else:
                                print(f"❌ Download link generation failed: {download_response.status_code}")
                        else:
                            print("ℹ️  No files to test download with")
                    else:
                        print(f"❌ File list failed: {list_response.status_code}")
                else:
                    print(f"❌ Client login failed: {client_login.status_code}")
            else:
                print(f"❌ User verification failed: {verify_response.status_code}")
        else:
            print(f"❌ Client signup failed: {client_signup.status_code}")
    else:
        print(f"❌ Ops login failed: {login_response.status_code}")

if __name__ == "__main__":
    test_endpoints()
