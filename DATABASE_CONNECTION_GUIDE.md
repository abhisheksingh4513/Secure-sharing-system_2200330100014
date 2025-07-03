# 🗄️ Database Connection Guide

## Current Configuration (SQLite)
Your system currently uses SQLite, which is perfect for development and testing.

```
DATABASE_URL=sqlite:///./file_sharing.db
```

## 🔗 SQL Database Connection Options

### 1. PostgreSQL (Recommended for Production)

#### Install Dependencies:
```bash
pip install psycopg2-binary
```

#### Update .env file:
```properties
# PostgreSQL Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/file_sharing_db

# Example with specific details:
DATABASE_URL=postgresql://admin:mypassword@localhost:5432/secure_files
```

#### Connection String Format:
```
postgresql://[username]:[password]@[host]:[port]/[database_name]
```

### 2. MySQL/MariaDB

#### Install Dependencies:
```bash
pip install pymysql
# or
pip install mysqlclient
```

#### Update .env file:
```properties
# MySQL Configuration
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/file_sharing_db

# Example:
DATABASE_URL=mysql+pymysql://root:mypassword@localhost:3306/secure_files
```

#### Connection String Format:
```
mysql+pymysql://[username]:[password]@[host]:[port]/[database_name]
```

### 3. SQL Server

#### Install Dependencies:
```bash
pip install pyodbc
```

#### Update .env file:
```properties
# SQL Server Configuration
DATABASE_URL=mssql+pyodbc://username:password@server:port/database?driver=ODBC+Driver+17+for+SQL+Server

# Example:
DATABASE_URL=mssql+pyodbc://sa:MyPassword123@localhost:1433/SecureFiles?driver=ODBC+Driver+17+for+SQL+Server
```

### 4. Oracle Database

#### Install Dependencies:
```bash
pip install cx_Oracle
```

#### Update .env file:
```properties
# Oracle Configuration
DATABASE_URL=oracle+cx_oracle://username:password@host:port/?service_name=service

# Example:
DATABASE_URL=oracle+cx_oracle://hr:password@localhost:1521/?service_name=xe
```

## 🛠️ Implementation Steps

### Step 1: Update requirements.txt
Add the appropriate database driver to your requirements.txt:

```text
# For PostgreSQL
psycopg2-binary==2.9.10

# For MySQL
pymysql==1.1.0

# For SQL Server
pyodbc==5.1.0

# For Oracle
cx_Oracle==8.3.0
```

### Step 2: Update .env File
Replace the DATABASE_URL with your chosen database connection string.

### Step 3: Database Setup Commands

#### For PostgreSQL:
```sql
-- Connect to PostgreSQL and create database
CREATE DATABASE secure_files;
CREATE USER file_admin WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE secure_files TO file_admin;
```

#### For MySQL:
```sql
-- Connect to MySQL and create database
CREATE DATABASE secure_files CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'file_admin'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON secure_files.* TO 'file_admin'@'localhost';
FLUSH PRIVILEGES;
```

#### For SQL Server:
```sql
-- Connect to SQL Server and create database
CREATE DATABASE SecureFiles;
USE SecureFiles;
```

### Step 4: Initialize Database
After updating the connection string, run:

```bash
python init_db.py
```

## 🔒 Production Database Configuration

### Environment-Specific Settings

#### Development (.env.dev):
```properties
DATABASE_URL=sqlite:///./file_sharing_dev.db
```

#### Testing (.env.test):
```properties
DATABASE_URL=sqlite:///./file_sharing_test.db
```

#### Production (.env.prod):
```properties
DATABASE_URL=postgresql://prod_user:secure_password@db.example.com:5432/file_sharing_prod
```

### Connection Pool Settings
For production databases, you might want to add connection pool settings:

```python
# In database.py, you can add:
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True,
    pool_recycle=3600
)
```

## 🐳 Docker Database Setup

### PostgreSQL with Docker:
```yaml
# docker-compose.yml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: secure_files
      POSTGRES_USER: file_admin
      POSTGRES_PASSWORD: your_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### MySQL with Docker:
```yaml
version: '3.8'
services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: secure_files
      MYSQL_USER: file_admin
      MYSQL_PASSWORD: your_password
      MYSQL_ROOT_PASSWORD: root_password
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

## 🔧 Advanced Configuration

### SSL/TLS Connection (PostgreSQL Example):
```properties
DATABASE_URL=postgresql://username:password@host:5432/database?sslmode=require
```

### Connection with Authentication:
```properties
# With SSL certificate
DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=require&sslcert=client-cert.pem&sslkey=client-key.pem&sslrootcert=ca-cert.pem
```

## 🧪 Testing Database Connection

Create a test script to verify your database connection:

```python
# test_db_connection.py
from app.database import engine, SessionLocal
from sqlalchemy import text

def test_connection():
    try:
        # Test engine connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            
        # Test session
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        print("✅ Database session working!")
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")

if __name__ == "__main__":
    test_connection()
```

## 🚀 Migration Considerations

When switching databases, consider:

1. **Data Types**: Some SQLite types might need adjustment
2. **Constraints**: Database-specific constraint syntax
3. **Indexes**: Optimize for your chosen database
4. **Backup**: Always backup before migration

## 📊 Performance Optimization

### For PostgreSQL:
- Use connection pooling
- Enable query optimization
- Set appropriate `work_mem` and `shared_buffers`

### For MySQL:
- Use InnoDB engine
- Optimize `innodb_buffer_pool_size`
- Enable query cache

### For SQL Server:
- Set appropriate isolation levels
- Use indexed views where beneficial
- Monitor with SQL Server Profiler

Your secure file-sharing system is designed to work with any of these databases with minimal code changes!
