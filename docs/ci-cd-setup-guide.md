# CI/CD Pipeline Setup Guide for JobTrackerDB

This guide walks you through setting up the complete CI/CD pipeline for JobTrackerDB.

## Prerequisites

- GitHub repository with push access
- Python 3.11+ installed
- Node.js 18+ installed
- MSSQL Server access
- Server access for staging/production deployment

## Step 1: Install Test Dependencies

### Backend Dependencies
```bash
cd backend
pip install -r requirements-test.txt
```

### Frontend Dependencies
```bash
cd frontend
npm install
```

## Step 2: Configure GitHub Secrets

1. Go to your GitHub repository
2. Navigate to Settings > Secrets and variables > Actions
3. Add the following secrets:

### Required Secrets
- `DATABASE_URL`: Your MSSQL connection string
- `GEOSCAPE_API_KEY`: Your Geoscape API key
- `OPENAI_API_KEY`: Your OpenAI API key
- `SECRET_KEY`: A secure random string for JWT tokens

### Optional Secrets (for deployment)
- `STAGING_DB_URL`: Staging database URL
- `PRODUCTION_DB_URL`: Production database URL
- `STAGING_SERVER_SSH_KEY`: SSH key for staging server
- `PRODUCTION_SERVER_SSH_KEY`: SSH key for production server

## Step 3: Test Locally

### Backend Tests
```bash
cd backend
pytest tests/ -v --cov=app
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Linting
```bash
# Backend
cd backend
flake8 app/ --max-line-length=88
black --check app/
isort --check-only app/

# Frontend
cd frontend
npm run lint
```

## Step 4: Configure Environments

### Development Environment
1. Copy `backend/env.example` to `backend/.env`
2. Copy `frontend/env.example` to `frontend/.env`
3. Update the values with your actual configuration

### Staging Environment
1. Set up a staging server
2. Configure the staging database
3. Update deployment scripts with your server details

### Production Environment
1. Set up production servers (blue/green deployment)
2. Configure production database
3. Set up monitoring and alerting

## Step 5: Test the Pipeline

### Manual Trigger
1. Go to Actions tab in GitHub
2. Select "CI/CD Pipeline"
3. Click "Run workflow"
4. Choose environment (staging/production)

### Automatic Trigger
1. Push to `main` branch for production deployment
2. Push to `develop` branch for staging deployment
3. Create pull requests for testing

## Step 6: Monitor and Maintain

### Monitoring
- Check GitHub Actions for pipeline status
- Monitor application health endpoints
- Set up alerts for failures

### Maintenance
- Regularly update dependencies
- Monitor security vulnerabilities
- Review and update secrets

## Troubleshooting

### Common Issues

1. **Tests failing locally but passing in CI**
   - Check environment variables
   - Verify database connection
   - Check file paths

2. **Deployment failing**
   - Verify SSH keys
   - Check server permissions
   - Validate environment variables

3. **Health checks failing**
   - Check database connectivity
   - Verify API keys
   - Review application logs

### Debug Steps

1. **Check GitHub Actions logs**
   - Look for specific error messages
   - Verify secret names match exactly
   - Check environment variable usage

2. **Test locally**
   - Run the same commands locally
   - Check environment setup
   - Verify dependencies

3. **Check server logs**
   - SSH into deployment server
   - Check application logs
   - Verify service status

## Security Considerations

1. **Never commit secrets**
   - Use GitHub secrets for sensitive data
   - Keep `.env` files in `.gitignore`
   - Rotate keys regularly

2. **Limit access**
   - Use least privilege for deployment
   - Monitor access logs
   - Regular security audits

3. **Secure communication**
   - Use HTTPS for all endpoints
   - Validate SSL certificates
   - Implement proper authentication

## Performance Optimization

1. **Caching**
   - Cache dependencies in CI/CD
   - Use build caching
   - Optimize test execution

2. **Parallelization**
   - Run tests in parallel
   - Use matrix builds
   - Optimize deployment steps

3. **Monitoring**
   - Track build times
   - Monitor resource usage
   - Optimize based on metrics 