#!/bin/bash

# JobTrackerDB Production Deployment Script
# This script deploys the application to the production environment

set -e  # Exit on any error

echo "🚀 Starting production deployment..."

# Configuration
PRODUCTION_SERVER="your-production-server.com"
PRODUCTION_PATH="/var/www/jobtrackerdb"
BACKUP_PATH="/var/backups/jobtrackerdb"
BLUE_PATH="/var/www/jobtrackerdb-blue"
GREEN_PATH="/var/www/jobtrackerdb-green"

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
if [ -z "$PRODUCTION_DB_URL" ]; then
    log_error "PRODUCTION_DB_URL environment variable is not set"
    exit 1
fi

if [ -z "$GEOSCAPE_API_KEY" ]; then
    log_error "GEOSCAPE_API_KEY environment variable is not set"
    exit 1
fi

# Determine current active environment
CURRENT_ENV=$(ssh user@$PRODUCTION_SERVER "readlink -f $PRODUCTION_PATH" | grep -o "blue\|green" || echo "blue")
if [ "$CURRENT_ENV" = "blue" ]; then
    ACTIVE_PATH=$BLUE_PATH
    INACTIVE_PATH=$GREEN_PATH
    NEW_ENV="green"
else
    ACTIVE_PATH=$GREEN_PATH
    INACTIVE_PATH=$BLUE_PATH
    NEW_ENV="blue"
fi

log_info "Current active environment: $CURRENT_ENV"
log_info "Deploying to: $NEW_ENV"

# Create backup of current deployment
log_info "Creating backup of current deployment..."
ssh user@$PRODUCTION_SERVER "mkdir -p $BACKUP_PATH && tar -czf $BACKUP_PATH/backup-$(date +%Y%m%d-%H%M%S).tar.gz -C $ACTIVE_PATH ."

# Deploy to inactive environment
log_info "Deploying to inactive environment ($NEW_ENV)..."
ssh user@$PRODUCTION_SERVER "mkdir -p $INACTIVE_PATH"

# Deploy backend
log_info "Deploying backend..."
scp backend/backend-package.tar.gz user@$PRODUCTION_SERVER:$INACTIVE_PATH/
ssh user@$PRODUCTION_SERVER "cd $INACTIVE_PATH && tar -xzf backend-package.tar.gz"

# Deploy frontend
log_info "Deploying frontend..."
scp -r frontend/dist/* user@$PRODUCTION_SERVER:$INACTIVE_PATH/static/

# Run database migrations
log_info "Running database migrations..."
ssh user@$PRODUCTION_SERVER "cd $INACTIVE_PATH && source venv/bin/activate && alembic upgrade head"

# Test the new deployment
log_info "Testing new deployment..."
ssh user@$PRODUCTION_SERVER "cd $INACTIVE_PATH && source venv/bin/activate && python -m pytest tests/ -v"

# Switch traffic to new environment
log_info "Switching traffic to new environment..."
ssh user@$PRODUCTION_SERVER "ln -sfn $INACTIVE_PATH $PRODUCTION_PATH"

# Restart services
log_info "Restarting services..."
ssh user@$PRODUCTION_SERVER "sudo systemctl restart jobtrackerdb-api"
ssh user@$PRODUCTION_SERVER "sudo systemctl restart nginx"

# Health check
log_info "Performing health check..."
sleep 15
HEALTH_CHECK=$(curl -s -o /dev/null -w "%{http_code}" https://jobtrackerdb.com/health)

if [ "$HEALTH_CHECK" = "200" ]; then
    log_info "✅ Health check passed"
    
    # Run smoke tests
    log_info "Running smoke tests..."
    SMOKE_TEST_RESULT=$(curl -s -o /dev/null -w "%{http_code}" https://jobtrackerdb.com/api/address/validate)
    
    if [ "$SMOKE_TEST_RESULT" = "405" ] || [ "$SMOKE_TEST_RESULT" = "404" ]; then
        log_info "✅ Smoke tests passed"
    else
        log_warn "⚠️ Smoke tests returned unexpected status: $SMOKE_TEST_RESULT"
    fi
    
else
    log_error "❌ Health check failed (HTTP $HEALTH_CHECK)"
    log_warn "Rolling back to previous version..."
    ssh user@$PRODUCTION_SERVER "ln -sfn $ACTIVE_PATH $PRODUCTION_PATH"
    ssh user@$PRODUCTION_SERVER "sudo systemctl restart jobtrackerdb-api"
    exit 1
fi

# Monitor for 5 minutes
log_info "Monitoring deployment for 5 minutes..."
for i in {1..30}; do
    sleep 10
    CURRENT_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" https://jobtrackerdb.com/health)
    if [ "$CURRENT_HEALTH" != "200" ]; then
        log_error "❌ Health check failed during monitoring (HTTP $CURRENT_HEALTH)"
        log_warn "Rolling back to previous version..."
        ssh user@$PRODUCTION_SERVER "ln -sfn $ACTIVE_PATH $PRODUCTION_PATH"
        ssh user@$PRODUCTION_SERVER "sudo systemctl restart jobtrackerdb-api"
        exit 1
    fi
    echo -n "."
done

log_info "✅ Production deployment completed successfully!"
log_info "New active environment: $NEW_ENV"

# Cleanup old backups (keep last 10)
log_info "Cleaning up old backups..."
ssh user@$PRODUCTION_SERVER "cd $BACKUP_PATH && ls -t | tail -n +11 | xargs -r rm" 