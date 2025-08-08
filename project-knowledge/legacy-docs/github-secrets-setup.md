# GitHub Secrets Setup for JobTrackerDB CI/CD

This document outlines the required GitHub secrets for the CI/CD pipeline to function properly.

## Required Secrets

### Database Secrets
- `DATABASE_URL`: Connection string for the database
- `STAGING_DB_URL`: Staging environment database URL
- `PRODUCTION_DB_URL`: Production environment database URL

### API Keys
- `GEOSCAPE_API_KEY`: Geoscape API key for address validation
- `OPENAI_API_KEY`: OpenAI API key for AI features
- `SMARTY_STREETS_API_KEY`: SmartyStreets API key (backup address validation)

### Application Secrets
- `SECRET_KEY`: Application secret key for JWT tokens
- `VITE_API_URL`: Frontend API URL for builds

### Deployment Secrets
- `STAGING_SERVER_SSH_KEY`: SSH private key for staging server access
- `PRODUCTION_SERVER_SSH_KEY`: SSH private key for production server access
- `STAGING_SERVER_HOST`: Staging server hostname
- `PRODUCTION_SERVER_HOST`: Production server hostname

### Monitoring Secrets
- `SENTRY_DSN`: Sentry DSN for error tracking
- `SLACK_WEBHOOK_URL`: Slack webhook for notifications

## How to Set Up Secrets

1. Go to your GitHub repository
2. Navigate to Settings > Secrets and variables > Actions
3. Click "New repository secret"
4. Add each secret with the exact name listed above

## Environment-Specific Secrets

### Staging Environment
- `STAGING_DB_URL`
- `STAGING_SERVER_SSH_KEY`
- `STAGING_SERVER_HOST`

### Production Environment
- `PRODUCTION_DB_URL`
- `PRODUCTION_SERVER_SSH_KEY`
- `PRODUCTION_SERVER_HOST`

## Security Best Practices

1. **Never commit secrets to the repository**
2. **Use different keys for different environments**
3. **Rotate keys regularly**
4. **Use least privilege principle**
5. **Monitor secret usage**

## Testing Secrets

You can test if secrets are properly configured by running:

```bash
# Test database connection
python -c "import os; print('DATABASE_URL:', 'SET' if os.getenv('DATABASE_URL') else 'NOT SET')"

# Test API keys
python -c "import os; print('GEOSCAPE_API_KEY:', 'SET' if os.getenv('GEOSCAPE_API_KEY') else 'NOT SET')"
```

## Troubleshooting

### Common Issues

1. **Secret not found**: Ensure the secret name matches exactly
2. **Permission denied**: Check SSH key permissions
3. **Database connection failed**: Verify connection string format
4. **API calls failing**: Check API key validity

### Debug Steps

1. Check GitHub Actions logs for secret-related errors
2. Verify secret names match exactly
3. Test secrets locally before pushing
4. Check environment-specific secret configuration 