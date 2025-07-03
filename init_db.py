#!/usr/bin/env python3
"""
Database initialization script
Creates an operations user for initial system setup
"""

from app.database import SessionLocal, User
from app.auth import get_password_hash

def create_ops_user():
    """Create a default operations user"""
    db = SessionLocal()
    
    try:
        # Check if ops user already exists
        existing_user = db.query(User).filter(User.username == "admin").first()
        
        if existing_user:
            print("Operations user already exists!")
            return
        
        # Create ops user
        ops_user = User(
            email="admin@fileserver.com",
            username="admin",
            hashed_password=get_password_hash("admin123"),
            user_type="ops",
            is_active=True,
            is_verified=True  # Ops users are pre-verified
        )
        
        db.add(ops_user)
        db.commit()
        print("Operations user created successfully!")
        print("Username: admin")
        print("Password: admin123")
        print("Email: admin@fileserver.com")
        
    except Exception as e:
        print(f"Error creating ops user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_ops_user()
