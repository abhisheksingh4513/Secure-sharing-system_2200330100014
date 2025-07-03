#!/usr/bin/env python3
"""
Comprehensive test suite for Secure File Sharing System
Includes unit and integration tests for core functionality
"""

import os
import pytest
import tempfile
import shutil
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Import application components
from app.main import app
from app.database import Base, User, File, get_db, SessionLocal
from app.auth import create_access_token, verify_password, get_password_hash

# Setup test database
TEST_DATABASE_URL = "sqlite:///./test_file_sharing.db"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Setup test client
client = TestClient(app)

# Test data
test_ops_user = {
    "username": "testops",
    "email": "testops@example.com",
    "password": "testpassword",
    "user_type": "ops"
}

test_client_user = {
    "username": "testclient",
    "email": "testclient@example.com",
    "password": "testpassword",
    "user_type": "client"
}

# Test file paths
test_files_dir = os.path.join(os.path.dirname(__file__), "test_files")
test_docx_path = os.path.join(test_files_dir, "test.docx")
test_xlsx_path = os.path.join(test_files_dir, "test.xlsx")
test_pptx_path = os.path.join(test_files_dir, "test.pptx")
test_txt_path = os.path.join(test_files_dir, "test.txt")  # Invalid file type for testing

# Override dependency to use test database
def override_get_db():
    try:
        db = TestSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


# Setup and teardown functions
@pytest.fixture(scope="module")
def test_app():
    # Create test database and tables
    Base.metadata.create_all(bind=engine)
    
    # Create test files directory and sample files
    os.makedirs(test_files_dir, exist_ok=True)
    
    # Create dummy test files of different types
    with open(test_docx_path, "wb") as f:
        f.write(b"test docx content")
    with open(test_xlsx_path, "wb") as f:
        f.write(b"test xlsx content")
    with open(test_pptx_path, "wb") as f:
        f.write(b"test pptx content")
    with open(test_txt_path, "wb") as f:
        f.write(b"test txt content")
    
    # Setup test upload directory
    os.environ["UPLOAD_DIRECTORY"] = "./test_uploads"
    os.makedirs("./test_uploads", exist_ok=True)
    
    yield app  # Testing happens here
    
    # Cleanup
    Base.metadata.drop_all(bind=engine)
    shutil.rmtree(test_files_dir, ignore_errors=True)
    shutil.rmtree("./test_uploads", ignore_errors=True)
    if os.path.exists("./test_file_sharing.db"):
        os.remove("./test_file_sharing.db")


@pytest.fixture(scope="module")
def test_db():
    # Get test database session
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def ops_token(test_app, test_db):
    """Create an operations user and return a valid JWT token"""
    # Create ops test user
    hashed_password = get_password_hash(test_ops_user["password"])
    db_user = User(
        username=test_ops_user["username"],
        email=test_ops_user["email"],
        hashed_password=hashed_password,
        user_type="ops",
        is_active=True,
        is_verified=True
    )
    test_db.add(db_user)
    test_db.commit()
    test_db.refresh(db_user)
    
    # Generate token
    access_token = create_access_token(data={"sub": db_user.username, "user_type": db_user.user_type})
    return access_token


@pytest.fixture(scope="module")
def client_token(test_app, test_db):
    """Create a client user and return a valid JWT token"""
    # Create client test user
    hashed_password = get_password_hash(test_client_user["password"])
    db_user = User(
        username=test_client_user["username"],
        email=test_client_user["email"],
        hashed_password=hashed_password,
        user_type="client",
        is_active=True,
        is_verified=True  # Pre-verified for testing
    )
    test_db.add(db_user)
    test_db.commit()
    test_db.refresh(db_user)
    
    # Generate token
    access_token = create_access_token(data={"sub": db_user.username, "user_type": db_user.user_type})
    return access_token


# Unit Tests
def test_password_hashing():
    """Test password hashing and verification"""
    password = "testpassword"
    hashed = get_password_hash(password)
    
    # Verify hashed password
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)


def test_token_creation():
    """Test JWT token creation and data encoding"""
    data = {"sub": "testuser", "user_type": "ops"}
    token = create_access_token(data=data)
    
    # Verify token is created and is a string
    assert token
    assert isinstance(token, str)
    assert len(token) > 20  # Simple check that it's a reasonably sized token


# Authentication API Tests
def test_ops_login(test_app):
    """Test operations user login endpoint"""
    response = client.post(
        "/auth/ops-login",
        json={"username": test_ops_user["username"], "password": test_ops_user["password"]}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_client_login(test_app):
    """Test client user login endpoint"""
    response = client.post(
        "/auth/login",
        json={"username": test_client_user["username"], "password": test_client_user["password"]}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_failure(test_app):
    """Test login with invalid credentials"""
    response = client.post(
        "/auth/login",
        json={"username": test_client_user["username"], "password": "wrongpassword"}
    )
    assert response.status_code == 401
    

def test_signup_client(test_app):
    """Test client user signup"""
    new_user = {
        "username": "newclient",
        "email": "newclient@example.com",
        "password": "newpassword",
        "user_type": "client"
    }
    
    response = client.post(
        "/auth/signup",
        json=new_user
    )
    assert response.status_code == 201
    data = response.json()
    assert "message" in data
    assert "verification_url" in data or "manual_verification" in data


# File Operations Tests
def test_upload_file_allowed_type(test_app, ops_token):
    """Test file upload with allowed file type"""
    headers = {"Authorization": f"Bearer {ops_token}"}
    
    with open(test_docx_path, "rb") as f:
        files = {"file": ("test.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        response = client.post("/files/upload", headers=headers, files=files)
    
    assert response.status_code == 201
    data = response.json()
    assert data["filename"] == "test.docx"
    assert "file_id" in data


def test_upload_file_forbidden_type(test_app, ops_token):
    """Test file upload with forbidden file type"""
    headers = {"Authorization": f"Bearer {ops_token}"}
    
    with open(test_txt_path, "rb") as f:
        files = {"file": ("test.txt", f, "text/plain")}
        response = client.post("/files/upload", headers=headers, files=files)
    
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]


def test_upload_file_unauthorized(test_app, client_token):
    """Test file upload by unauthorized user (client user)"""
    headers = {"Authorization": f"Bearer {client_token}"}
    
    with open(test_docx_path, "rb") as f:
        files = {"file": ("test.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        response = client.post("/files/upload", headers=headers, files=files)
    
    assert response.status_code == 403
    assert "Not authorized" in response.json()["detail"]


def test_list_files(test_app, ops_token, client_token):
    """Test listing files"""
    # Upload a test file first
    headers_ops = {"Authorization": f"Bearer {ops_token}"}
    with open(test_docx_path, "rb") as f:
        files = {"file": ("test_list.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        client.post("/files/upload", headers=headers_ops, files=files)
    
    # Test client can list files
    headers_client = {"Authorization": f"Bearer {client_token}"}
    response = client.get("/files/list", headers=headers_client)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    
    # Test ops user cannot list files (role-based access control)
    response_ops = client.get("/files/list", headers=headers_ops)
    assert response_ops.status_code == 403


def test_get_download_link(test_app, ops_token, client_token, test_db):
    """Test generating download link for a file"""
    # Upload a test file first
    headers_ops = {"Authorization": f"Bearer {ops_token}"}
    with open(test_docx_path, "rb") as f:
        files = {"file": ("test_download.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        response = client.post("/files/upload", headers=headers_ops, files=files)
    
    file_id = response.json()["file_id"]
    
    # Test client can get download link
    headers_client = {"Authorization": f"Bearer {client_token}"}
    response = client.get(f"/files/get-download-link/{file_id}", headers=headers_client)
    
    assert response.status_code == 200
    data = response.json()
    assert "download_link" in data


def test_secure_download(test_app, ops_token, client_token, test_db):
    """Test secure file download with token"""
    # Upload a test file first
    headers_ops = {"Authorization": f"Bearer {ops_token}"}
    with open(test_docx_path, "rb") as f:
        files = {"file": ("test_secure.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        response = client.post("/files/upload", headers=headers_ops, files=files)
    
    file_id = response.json()["file_id"]
    
    # Get download link
    headers_client = {"Authorization": f"Bearer {client_token}"}
    response = client.get(f"/files/get-download-link/{file_id}", headers=headers_client)
    
    download_link = response.json()["download_link"]
    token = download_link.split("/")[-1]
    
    # Test file download with token
    response = client.get(f"/files/secure-download/{token}")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    
    # Test one-time use - second attempt should fail
    response = client.get(f"/files/secure-download/{token}")
    assert response.status_code == 400
    assert "Invalid or expired token" in response.json()["detail"]


def test_download_nonexistent_file(test_app, client_token):
    """Test attempting to get download link for non-existent file"""
    headers_client = {"Authorization": f"Bearer {client_token}"}
    response = client.get("/files/get-download-link/999999", headers=headers_client)
    
    assert response.status_code == 404
    assert "File not found" in response.json()["detail"]


# Integration Tests - Complete User Flow
def test_complete_user_flow():
    """Test complete user flow from signup to download"""
    # 1. Create a new client user
    new_client = {
        "username": "flowclient",
        "email": "flowclient@example.com",
        "password": "flowpassword",
        "user_type": "client"
    }
    
    signup_response = client.post("/auth/signup", json=new_client)
    assert signup_response.status_code == 201
    
    # 2. Manually verify the client (since we're bypassing email)
    db = TestSessionLocal()
    user = db.query(User).filter(User.username == new_client["username"]).first()
    assert user is not None
    
    verify_response = client.get(f"/auth/manual-verify/{user.id}")
    assert verify_response.status_code == 200
    
    # 3. Login as the client
    login_response = client.post(
        "/auth/login",
        json={"username": new_client["username"], "password": new_client["password"]}
    )
    assert login_response.status_code == 200
    client_token = login_response.json()["access_token"]
    
    # 4. Login as ops user to upload a file
    ops_login_response = client.post(
        "/auth/ops-login",
        json={"username": test_ops_user["username"], "password": test_ops_user["password"]}
    )
    assert ops_login_response.status_code == 200
    ops_token = ops_login_response.json()["access_token"]
    
    # 5. Upload file as ops user
    headers_ops = {"Authorization": f"Bearer {ops_token}"}
    with open(test_pptx_path, "rb") as f:
        files = {"file": ("flow_test.pptx", f, "application/vnd.openxmlformats-officedocument.presentationml.presentation")}
        upload_response = client.post("/files/upload", headers=headers_ops, files=files)
    
    assert upload_response.status_code == 201
    file_id = upload_response.json()["file_id"]
    
    # 6. List files as client
    headers_client = {"Authorization": f"Bearer {client_token}"}
    list_response = client.get("/files/list", headers=headers_client)
    assert list_response.status_code == 200
    files_list = list_response.json()
    assert len(files_list) >= 1
    
    # 7. Get download link
    link_response = client.get(f"/files/get-download-link/{file_id}", headers=headers_client)
    assert link_response.status_code == 200
    download_link = link_response.json()["download_link"]
    token = download_link.split("/")[-1]
    
    # 8. Download file
    download_response = client.get(f"/files/secure-download/{token}")
    assert download_response.status_code == 200
    
    # Cleanup
    db.close()


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])
