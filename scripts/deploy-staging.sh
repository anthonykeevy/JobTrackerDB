#!/bin/bash

# JobTrackerDB Staging Deployment Script
# This script deploys the application to the staging environment

set -e  # Exit on any error

echo "🚀 Starting staging deployment..."

# Configuration
STAGING_SERVER="your-staging-server.com"
STAGING_PATH="/var/www/jobtrackerdb-staging"
BACKUP_PATH="/var/backups/jobtrackerdb"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to log with colors
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required environment variables are set
if [ -z "$STAGING_DB_URL" ]; then
    log_error "STAGING_DB_URL environment variable is not set"
    exit 1
fi

if [ -z "$GEOSCAPE_API_KEY" ]; then
    log_error "GEOSCAPE_API_KEY environment variable is not set"
    exit 1
fi

# Create backup
log_info "Creating backup of current deployment..."
ssh user@$STAGING_SERVER "mkdir -p $BACKUP_PATH && tar -czf $BACKUP_PATH/backup-$(date +%Y%m%d-%H%M%S).tar.gz -C $STAGING_PATH ."

# Deploy backend
log_info "Deploying backend..."
scp backend/backend-package.tar.gz user@$STAGING_SERVER:$STAGING_PATH/
ssh user@$STAGING_SERVER "cd $STAGING_PATH && tar -xzf backend-package.tar.gz"

# Deploy frontend
log_info "Deploying frontend..."
scp -r frontend/dist/* user@$STAGING_SERVER:$STAGING_PATH/static/

# Run database migrations
log_info "Running database migrations..."
ssh user@$STAGING_SERVER "cd $STAGING_PATH && source venv/bin/activate && alembic upgrade head"

# Restart services
log_info "Restarting services..."
ssh user@$STAGING_SERVER "sudo systemctl restart jobtrackerdb-api"
ssh user@$STAGING_SERVER "sudo systemctl restart nginx"

# Health check
log_info "Performing health check..."
sleep 10
HEALTH_CHECK=$(curl -s -o /dev/null -w "%{http_code}" https://staging.jobtrackerdb.com/health)

if [ "$HEALTH_CHECK" = "200" ]; then
    log_info "✅ Health check passed"
else
    log_error "❌ Health check failed (HTTP $HEALTH_CHECK)"
    log_warn "Rolling back to previous version..."
    ssh user@$STAGING_SERVER "cd $STAGING_PATH && tar -xzf $BACKUP_PATH/backup-$(ls -t $BACKUP_PATH | head -1)"
    ssh user@$STAGING_SERVER "sudo systemctl restart jobtrackerdb-api"
    exit 1
fi

log_info "🎉 Staging deployment completed successfully!" 