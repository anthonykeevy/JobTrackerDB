# Environment Setup Guide for JobTrackerDB

## Overview

This guide explains how to set up environment variables for JobTrackerDB, respecting the `.gitignore` restrictions that protect sensitive data.

## Why .env Files Are Protected

The `.env` files are intentionally blocked by `globalignore` to prevent:
- Accidental commits of API keys
- Exposure of database credentials
- Leakage of sensitive configuration

## Setup Process

### Step 1: Create Local Environment Files

**Backend Setup:**
```bash
cd backend
cp env.example .env
```

**Frontend Setup:**
```bash
cd frontend
cp env.example .env
```

### Step 2: Configure Local Environment

Edit the `.env` files with your actual values:

**Backend (.env):**
```bash
# Database Configuration
DATABASE_URL=mssql+pyodbc://your_username:your_password@your_server:1433/JobTrackerDB?driver=ODBC+Driver+17+for+SQL+Server

# API Keys
GEOSCAPE_API_KEY=your_actual_geoscape_key
OPENAI_API_KEY=your_actual_openai_key

# Application Settings
DEBUG=True
SECRET_KEY=your_secure_random_string
ENVIRONMENT=development
```

**Frontend (.env):**
```bash
# API Configuration
VITE_API_URL=http://localhost:8000

# Map Configuration
VITE_MAPBOX_ACCESS_TOKEN=your_actual_mapbox_token
```

### Step 3: GitHub Secrets for CI/CD

For the CI/CD pipeline, add these secrets in GitHub:

1. Go to your repository
2. Settings > Secrets and variables > Actions
3. Add each secret:

**Required Secrets:**
- `DATABASE_URL`: Your MSSQL connection string
- `GEOSCAPE_API_KEY`: Your Geoscape API key
- `OPENAI_API_KEY`: Your OpenAI API key
- `SECRET_KEY`: Secure random string for JWT

**Optional Secrets:**
- `VITE_API_URL`: Frontend API URL for builds
- `STAGING_DB_URL`: Staging database URL
- `PRODUCTION_DB_URL`: Production database URL

## Environment-Specific Configuration

### Development Environment
- Use local `.env` files
- Connect to local MSSQL instance
- Use development API keys

### Staging Environment
- Use GitHub secrets: `STAGING_DB_URL`, `STAGING_API_KEYS`
- Deploy to staging server
- Use staging database

### Production Environment
- Use GitHub secrets: `PRODUCTION_DB_URL`, `PRODUCTION_API_KEYS`
- Deploy to production servers
- Use production database

## Security Best Practices

1. **Never commit .env files** - They're protected by globalignore
2. **Use different keys per environment** - Development, staging, production
3. **Rotate keys regularly** - Update API keys periodically
4. **Use strong secrets** - Generate secure random strings
5. **Monitor usage** - Track API key usage and costs

## Troubleshooting

### Common Issues

1. **"Module not found" errors**
   - Ensure you're in the correct directory
   - Check that `.env` files exist
   - Verify environment variable names

2. **Database connection errors**
   - Check MSSQL server is running
   - Verify connection string format
   - Test with SQL Server Management Studio

3. **API key errors**
   - Verify keys are valid
   - Check API quotas and limits
   - Test with API documentation

### Debug Steps

1. **Test environment variables:**
```bash
# Backend
cd backend
python -c "import os; print('DATABASE_URL:', 'SET' if os.getenv('DATABASE_URL') else 'NOT SET')"

# Frontend
cd frontend
node -e "console.log('VITE_API_URL:', process.env.VITE_API_URL || 'NOT SET')"
```

2. **Test database connection:**
```bash
cd backend
python -c "from sqlalchemy import create_engine; import os; engine = create_engine(os.getenv('DATABASE_URL')); print('Database connection:', 'SUCCESS' if engine.connect() else 'FAILED')"
```

3. **Test API connections:**
```bash
cd backend
python -c "import os; print('GEOSCAPE_API_KEY:', 'SET' if os.getenv('GEOSCAPE_API_KEY') else 'NOT SET')"
```

## CI/CD Integration

The CI/CD pipeline automatically uses GitHub secrets:

```yaml
# From the workflow file
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
  GEOSCAPE_API_KEY: ${{ secrets.GEOSCAPE_API_KEY }}
  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

This ensures:
- ✅ Secure secret management
- ✅ Environment-specific configuration
- ✅ No hardcoded secrets in code
- ✅ Automatic deployment configuration 