# Cursor Development Guide for JobTrackerDB

## Overview
This guide provides the optimal workflow for developing with Cursor while maintaining separate control over backend and frontend services.

## Service Control Commands

### Backend Service
```bash
# Start backend (stable mode - no auto-reload)
npm run start:backend

# Stop backend
npm run stop:backend

# Restart backend
npm run restart:backend

# Check backend status
npm run status:backend
```

### Frontend Service
```bash
# Start frontend
npm run start:frontend

# Stop frontend
npm run stop:frontend

# Restart frontend
npm run restart:frontend

# Check frontend status
npm run status:frontend
```

### Combined Services (Legacy)
```bash
# Start both services together (not recommended for Cursor development)
npm run dev:stable

# Stop all services
npm run cleanup
```

## Recommended Cursor Workflow

### 1. Initial Setup
```bash
# Start backend first (stable mode)
npm run start:backend

# Wait for backend to be ready, then start frontend
npm run start:frontend
```

### 2. Development Workflow
- **Backend Changes**: Use `npm run restart:backend` when you make backend code changes
- **Frontend Changes**: Frontend auto-reloads, no restart needed
- **Database Changes**: Use `npm run restart:backend` after database migrations

### 3. Monitoring
- **Backend Status**: `npm run status:backend`
- **Frontend Status**: `npm run status:frontend`
- **Both Services**: Run both status commands

### 4. Troubleshooting
- **Backend Issues**: `npm run restart:backend`
- **Frontend Issues**: `npm run restart:frontend`
- **Port Conflicts**: `npm run cleanup` then restart individual services

## Service URLs

### Backend
- **API**: http://127.0.0.1:8000
- **Documentation**: http://127.0.0.1:8000/docs
- **Health Check**: http://127.0.0.1:8000/health

### Frontend
- **Application**: http://localhost:5173
- **Alternative**: http://localhost:5174

## Why Separate Control?

### Benefits for Cursor Development
1. **Independent Monitoring**: Cursor can monitor each service separately
2. **Targeted Restarts**: Restart only the service you're working on
3. **Better Visibility**: Clear status for each service
4. **Reduced Conflicts**: No cascade failures between services
5. **Faster Development**: No waiting for both services to restart

### When to Use Each Command
- **`npm run start:backend`**: Starting development session
- **`npm run restart:backend`**: After backend code changes
- **`npm run status:backend`**: Checking if backend is healthy
- **`npm run stop:backend`**: Before making major changes
- **`npm run start:frontend`**: Starting frontend development
- **`npm run status:frontend`**: Checking frontend health

## Common Scenarios

### Scenario 1: Backend Code Changes
```bash
# Make your backend changes
# Then restart backend
npm run restart:backend
# Frontend continues running
```

### Scenario 2: Database Changes
```bash
# Run database migrations
# Then restart backend
npm run restart:backend
# Frontend continues running
```

### Scenario 3: Frontend Issues
```bash
# Check frontend status
npm run status:frontend
# If needed, restart frontend
npm run restart:frontend
# Backend continues running
```

### Scenario 4: Complete Reset
```bash
# Stop all services
npm run cleanup
# Start backend first
npm run start:backend
# Then start frontend
npm run start:frontend
```

## Tips for Cursor

1. **Use Terminal Tabs**: Keep backend and frontend in separate terminal tabs
2. **Monitor Status**: Regularly check service status during development
3. **Restart Strategically**: Only restart the service you're working on
4. **Keep Services Running**: Don't stop services unless necessary
5. **Use Health Checks**: Test API endpoints to verify backend health

## Troubleshooting

### Backend Won't Start
```bash
# Check if port 8000 is in use
netstat -ano | findstr ":8000"
# Kill any conflicting processes
npm run cleanup
# Start backend again
npm run start:backend
```

### Frontend Won't Start
```bash
# Check if ports 5173/5174 are in use
netstat -ano | findstr ":5173\|:5174"
# Kill any conflicting processes
npm run cleanup
# Start frontend again
npm run start:frontend
```

### Services Not Responding
```bash
# Check both service statuses
npm run status:backend
npm run status:frontend
# Restart problematic service
npm run restart:backend  # or restart:frontend
```

This approach gives Cursor maximum visibility and control over the development environment while maintaining stability.
