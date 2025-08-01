# JobTrackerDB - Setup and Startup Instructions

## Prerequisites

Before starting, ensure you have the following installed:
- **Python 3.8+**
- **Node.js 16+**
- **SQL Server** (Local or Azure)
- **ODBC Driver 17 for SQL Server**

## Quick Start Guide

### 1. Clone and Navigate to Project
```bash
cd JobTrackerDB
```

### 2. Set Up Python Virtual Environment

**Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

**macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 3. Install Backend Dependencies
```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Return to project root
cd ..
```

### 4. Install Frontend Dependencies
```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Return to project root
cd ..
```

### 5. Configure Environment

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

### 6. Initialize Database
```bash
# Navigate to backend directory
cd backend

# Run database setup script
python setup_database.py

# Return to project root
cd ..
```

### 7. Start the Application

**Terminal 1 - Start Backend Server:**
```bash
# Activate virtual environment (if not already active)
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Navigate to backend directory
cd backend

# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Start Frontend Development Server:**
```bash
# Navigate to frontend directory
cd frontend

# Start React development server
npm run dev
```

### 8. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Development Workflow

### Starting Services Daily
1. Open two terminal windows
2. In Terminal 1: Activate venv and start backend
3. In Terminal 2: Start frontend
4. Access the application at http://localhost:5173

### Stopping Services
- **Backend**: Press `Ctrl+C` in the backend terminal
- **Frontend**: Press `Ctrl+C` in the frontend terminal

## Troubleshooting

### Common Issues

1. **"ODBC Driver not found"**
   - Install ODBC Driver 17 for SQL Server from Microsoft's website

2. **"Database connection failed"**
   - Verify SQL Server is running
   - Check connection string in `.env`
   - Ensure database exists

3. **"Port already in use"**
   - Backend: Change port in uvicorn command or kill process on port 8000
   - Frontend: Change port in package.json or kill process on port 5173

4. **"Module not found"**
   - Ensure virtual environment is activated
   - Reinstall dependencies: `pip install -r requirements.txt`

### Verification Commands

**Check if services are running:**
```bash
# Check backend
curl http://localhost:8000/docs

# Check frontend
curl http://localhost:5173
```

**Check database connection:**
```bash
# From backend directory
python -c "from mcp.db.session import engine; print('Database connected!')"
```

## Project Structure

```
JobTrackerDB/
├── backend/           # FastAPI backend
│   ├── app/          # Main application
│   ├── mcp/          # Database models and endpoints
│   └── requirements.txt
├── frontend/         # React frontend
│   ├── src/          # Source code
│   └── package.json
└── docs/             # Documentation
```

## Support

For detailed setup instructions and troubleshooting, see `SETUP.md` in the project root.

## Environment Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | SQL Server connection string | Required |
| HOST | Backend server host | 0.0.0.0 |
| PORT | Backend server port | 8000 |
| ENVIRONMENT | Application environment | development |

## 1. Schema Review Process

You're correct that we need to design the complete schema based on your project requirements. Let me help you with this systematic approach:

### Schema Design Process
```
<code_block_to_apply_changes_from>
```

**Current State Analysis:**
- Your `setup_database.py` has basic tables (User, Profile, Role)
- These are likely just for testing connectivity
- We need to expand this based on your full feature set

### What We Need to Review:
1. **Career Profile System** (Epic 1)
2. **Job Discovery & Logging** (Epic 2) 
3. **Fit Score Analysis** (Epic 3)
4. **Resume Tailoring** (Epic 4)
5. **Job Search Artifacts** (Epic 6)
6. **Dashboard Analytics** (Epic 9)
7. **Export & File Management** (Epic 10)
8. **Notification System** (Epic 11)

## 2. Alembic Environment Process - High Level Overview

Let me break down the Alembic process and environment separation:

### Environment Separation Strategy

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   DEVELOPMENT   │    │    STAGING      │    │   PRODUCTION    │
│                 │    │                 │    │                 │
│ Database:       │    │ Database:       │    │ Database:       │
│ JobTrackerDB_Dev│    │ JobTrackerDB_Stg│    │ JobTrackerDB_Prod│
│                 │    │                 │    │                 │
│ Alembic Config: │    │ Alembic Config: │    │ Alembic Config: │
│ dev.ini         │    │ staging.ini     │    │ prod.ini        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Alembic Workflow Process

```
┌─────────────────────────────────────────────────────────────────┐
│                    ALEMBIC DEVELOPMENT WORKFLOW                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 1. MODEL CHANGES                                                │
│    ┌─────────────┐                                             │
│    │ Update      │                                             │
│    │ SQLAlchemy  │                                             │
│    │ Models      │                                             │
│    └─────────────┘                                             │
│           │                                                     │
│           ▼                                                     │
│                                                                 │
│ 2. GENERATE MIGRATION                                          │
│    ┌─────────────┐                                             │
│    │ alembic     │ → Creates migration file                    │
│    │ revision    │   (e.g., 003_add_job_tracking.py)          │
│    │ --autogenerate│                                           │
│    └─────────────┘                                             │
│           │                                                     │
│           ▼                                                     │
│                                                                 │
│ 3. REVIEW & EDIT                                                │
│    ┌─────────────┐                                             │
│    │ Review      │ → Check generated SQL                       │
│    │ Migration   │ → Add custom logic if needed                │
│    │ File        │ → Test migration locally                    │
│    └─────────────┘                                             │
│           │                                                     │
│           ▼                                                     │
│                                                                 │
│ 4. APPLY TO DEVELOPMENT                                        │
│    ┌─────────────┐                                             │
│    │ alembic     │ → Updates dev database                      │
│    │ upgrade     │ → Tests the migration                       │
│    │ head        │                                             │
│    └─────────────┘                                             │
│           │                                                     │
│           ▼                                                     │
│                                                                 │
│ 5. TEST & VALIDATE                                             │
│    ┌─────────────┐                                             │
│    │ Run Tests   │ → Unit tests, integration tests            │
│    │ Manual      │ → Manual testing of new features           │
│    │ Testing     │                                             │
│    └─────────────┘                                             │
│           │                                                     │
│           ▼                                                     │
│                                                                 │
│ 6. DEPLOY TO STAGING                                           │
│    ┌─────────────┐                                             │
│    │ alembic     │ → Apply to staging database                 │
│    │ upgrade     │ → Use staging.ini config                   │
│    │ head        │                                             │
│    └─────────────┘                                             │
│           │                                                     │
│           ▼                                                     │
│                                                                 │
│ 7. PRODUCTION DEPLOYMENT                                       │
│    ┌─────────────┐                                             │
│    │ alembic     │ → Apply to production database              │
│    │ upgrade     │ → Use prod.ini config                      │
│    │ head        │ → Backup before applying                   │
│    └─────────────┘                                             │
└─────────────────────────────────────────────────────────────────┘
```

### Environment Configuration Files

```ini
# alembic.ini (Development)
[alembic]
sqlalchemy.url = mssql+pyodbc://localhost/JobTrackerDB_Dev?driver=ODBC+Driver+17+for+SQL+Server

# staging.ini
[alembic]
sqlalchemy.url = mssql+pyodbc://staging-server/JobTrackerDB_Stg?driver=ODBC+Driver+17+for+SQL+Server

# production.ini
[alembic]
sqlalchemy.url = mssql+pyodbc://prod-server/JobTrackerDB_Prod?driver=ODBC+Driver+17+for+SQL+Server
```

### Key Commands You'll Use:

```bash
# Development
alembic -c alembic.ini revision --autogenerate -m "Add job tracking"
alembic -c alembic.ini upgrade head

# Staging
alembic -c staging.ini upgrade head

# Production
alembic -c production.ini upgrade head

# Rollback (if needed)
alembic -c alembic.ini downgrade -1
```

## Recommended Next Steps

### Step 1: Schema Review (Priority 1)
1. **Review your PRD and Epics** to identify all data entities
2. **Create a comprehensive data model** covering all features
3. **Design relationships** between entities
4. **Validate the schema** against your user stories

### Step 2: Alembic Setup (Priority 2)
1. **Install and configure Alembic** with environment separation
2. **Create initial migration** with the complete schema
3. **Set up environment configurations** (dev/staging/prod)
4. **Test the migration process**

Would you like me to help you with **Step 1 - Schema Review** first? I can analyze your PRD and epics to help design the complete database schema before we implement Alembic.
