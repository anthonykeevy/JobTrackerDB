# JobTrackerDB Setup Guide

This guide will help you resolve the registration error and set up the JobTrackerDB application properly.

## Prerequisites

1. **SQL Server** (Local or Azure)
2. **ODBC Driver 17 for SQL Server**
3. **Python 3.8+**
4. **Node.js 16+**

## Quick Fix for Registration Error

The registration error occurs because the database isn't properly configured. Follow these steps:

### 1. Database Setup

**Option A: Local SQL Server**
```bash
# Install SQL Server (if not already installed)
# Download from: https://www.microsoft.com/en-us/sql-server/sql-server-downloads

# Create the database
sqlcmd -S localhost -E -Q "CREATE DATABASE JobTrackerDB"
```

**Option B: Azure SQL Database**
```bash
# Use your Azure SQL connection string
# Format: mssql+pyodbc://username:password@server.database.windows.net/database?driver=ODBC+Driver+17+for+SQL+Server
```

### 2. Environment Configuration

Create a `.env` file in the project root:

```env
# Database Configuration
DATABASE_URL=mssql+pyodbc://localhost/JobTrackerDB?driver=ODBC+Driver+17+for+SQL+Server

# For Azure SQL, use:
# DATABASE_URL=mssql+pyodbc://username:password@server.database.windows.net/JobTrackerDB?driver=ODBC+Driver+17+for+SQL+Server

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Environment
ENVIRONMENT=development
```

### 3. Install Dependencies

```bash
# Activate virtual environment
venv\Scripts\activate

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies
cd ..\frontend
npm install
```

### 4. Initialize Database

```bash
# From the project root
cd backend
python setup_database.py
```

### 5. Start the Application

**Terminal 1 (Backend):**
```bash
cd backend
uvicorn app.main:app --reload
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

## What Was Fixed

The registration error was caused by several issues:

1. **Missing Database Connection**: No `.env` file with database URL
2. **Missing SQL Server Dependencies**: Added `pyodbc` and `pyodbc-azure`
3. **API Endpoint Issues**: Fixed user creation endpoint to handle passwords and create profiles
4. **Missing Password Hashing**: Added secure password hashing
5. **Database Model Mismatch**: Fixed field mappings between frontend and backend

## Troubleshooting

### Common Issues

1. **"ODBC Driver not found"**
   - Install ODBC Driver 17 for SQL Server
   - Download from Microsoft's website

2. **"Database connection failed"**
   - Verify SQL Server is running
   - Check connection string in `.env`
   - Ensure database exists

3. **"Registration still fails"**
   - Check backend logs for specific errors
   - Verify all tables were created successfully
   - Ensure the database setup script ran without errors

### Verification Steps

1. **Check Database Tables:**
   ```sql
   USE JobTrackerDB;
   SELECT * FROM Role;
   SELECT * FROM Profile;
   SELECT * FROM User;
   ```

2. **Test API Endpoint:**
   ```bash
   curl -X POST http://localhost:8000/api/v1/users \
     -H "Content-Type: application/json" \
     -d '{"name":"Test User","email":"test@example.com","password":"password123"}'
   ```

## Next Steps

After successful registration:

1. **Login System**: Implement proper authentication
2. **Profile Management**: Add profile editing features
3. **Job Tracking**: Implement job application tracking
4. **AI Features**: Add resume generation and job matching

## Support

If you continue to experience issues:

1. Check the backend logs for detailed error messages
2. Verify all prerequisites are installed
3. Ensure the database is accessible and properly configured
4. Test the database connection manually

The registration should now work properly with the fixes applied! 