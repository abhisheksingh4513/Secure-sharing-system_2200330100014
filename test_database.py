#!/usr/bin/env python3
"""
Database Connection Test Script
Test different database connections for the secure file-sharing system
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from decouple import config

def test_database_connection():
    """Test the current database connection"""
    
    print("🔗 Testing Database Connection...")
    print("=" * 50)
    
    # Get database URL from environment
    database_url = config("DATABASE_URL", default="sqlite:///./file_sharing.db")
    print(f"Database URL: {database_url}")
    
    try:
        # Create engine
        if database_url.startswith("sqlite"):
            engine = create_engine(database_url, connect_args={"check_same_thread": False})
        else:
            engine = create_engine(database_url)
        
        # Test connection
        with engine.connect() as connection:
            # Execute a simple query
            result = connection.execute(text("SELECT 1 as test"))
            test_value = result.fetchone()[0]
            
            if test_value == 1:
                print("✅ Database connection successful!")
                
                # Get database info
                if database_url.startswith("postgresql"):
                    db_info = connection.execute(text("SELECT version()")).fetchone()[0]
                    print(f"📊 Database Info: {db_info}")
                elif database_url.startswith("mysql"):
                    db_info = connection.execute(text("SELECT @@version")).fetchone()[0]
                    print(f"📊 Database Version: {db_info}")
                elif database_url.startswith("sqlite"):
                    db_info = connection.execute(text("SELECT sqlite_version()")).fetchone()[0]
                    print(f"📊 SQLite Version: {db_info}")
                elif database_url.startswith("mssql"):
                    db_info = connection.execute(text("SELECT @@version")).fetchone()[0]
                    print(f"📊 SQL Server Version: {db_info[:100]}...")
                
                return True
                
    except ImportError as e:
        print(f"❌ Database driver not installed: {e}")
        print("\n💡 Install the required driver:")
        if "psycopg2" in str(e):
            print("   pip install psycopg2-binary")
        elif "pymysql" in str(e):
            print("   pip install pymysql")
        elif "pyodbc" in str(e):
            print("   pip install pyodbc")
        elif "cx_Oracle" in str(e):
            print("   pip install cx_Oracle")
        return False
        
    except SQLAlchemyError as e:
        print(f"❌ Database connection failed: {e}")
        print("\n💡 Common solutions:")
        print("   1. Check if database server is running")
        print("   2. Verify connection credentials")
        print("   3. Ensure database exists")
        print("   4. Check network connectivity")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_application_database():
    """Test the application's database setup"""
    
    print("\n🏗️ Testing Application Database Setup...")
    print("=" * 50)
    
    try:
        # Import application database components
        from app.database import engine, SessionLocal, Base, User
        
        # Test session creation
        db = SessionLocal()
        
        # Test query execution
        users_count = db.query(User).count()
        print(f"✅ Application database accessible!")
        print(f"📊 Users in database: {users_count}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Application database test failed: {e}")
        return False

def show_database_examples():
    """Show database connection string examples"""
    
    print("\n📚 Database Connection Examples:")
    print("=" * 50)
    
    examples = {
        "SQLite (Current)": "sqlite:///./file_sharing.db",
        "PostgreSQL": "postgresql://username:password@localhost:5432/secure_files",
        "MySQL": "mysql+pymysql://username:password@localhost:3306/secure_files",
        "SQL Server": "mssql+pyodbc://username:password@server:port/database?driver=ODBC+Driver+17+for+SQL+Server",
        "Oracle": "oracle+cx_oracle://username:password@host:port/?service_name=service"
    }
    
    for db_type, connection_string in examples.items():
        print(f"\n{db_type}:")
        print(f"  {connection_string}")

def main():
    """Main test function"""
    
    print("🔐 Secure File Sharing System - Database Connection Test")
    print("=" * 60)
    
    # Test current database connection
    connection_success = test_database_connection()
    
    if connection_success:
        # Test application database
        app_success = test_application_database()
        
        if app_success:
            print("\n🎉 All database tests passed!")
            print("Your secure file-sharing system is ready to use!")
        else:
            print("\n⚠️ Database connection works, but application setup needs attention.")
            print("Run: python init_db.py")
    else:
        print("\n❌ Database connection failed.")
        show_database_examples()
        print("\n💡 Update your .env file with the correct DATABASE_URL")

if __name__ == "__main__":
    main()
