# JobTrackerDB Service Management Guide

## 🎯 **Problem Solved**
- **Multiple terminal windows** opening when restarting services
- **Cursor auto-reload** creating new processes instead of reusing existing ones
- **Process cleanup** issues causing port conflicts

## 🛠️ **New Management Commands**

### Quick Commands (from root directory)
```bash
# Check service status
npm run status

# Start services (if not running)
npm run start

# Stop services
npm run stop

# Restart services (recommended)
npm run restart

# Clean up all processes
npm run cleanup
```

### Alternative: Quick Management Script
```bash
# Windows batch file
quick-manage.bat status
quick-manage.bat start
quick-manage.bat restart
quick-manage.bat cleanup
```

### PowerShell Direct Commands
```powershell
# Direct PowerShell commands
powershell -ExecutionPolicy Bypass -File manage-services.ps1 status
powershell -ExecutionPolicy Bypass -File manage-services.ps1 restart
powershell -ExecutionPolicy Bypass -File manage-services.ps1 cleanup
```

## 🔧 **How It Works**

### Service Management Script (`manage-services.ps1`)
- **Status Check**: Monitors Python (backend) and Node.js (frontend) processes
- **Process Cleanup**: Safely terminates all related processes
- **Port Management**: Kills processes on ports 8000, 5173, 5174
- **Smart Restart**: Stops existing services before starting new ones

### Cursor Integration (`.cursorrules`)
- **Prevents auto-reload** of backend files that require manual restart
- **Allows frontend auto-reload** for React development
- **Guides manual restarts** when needed

## 📋 **Best Practices**

### ✅ **Recommended Workflow**
1. **Start services once**: `npm run start`
2. **Check status**: `npm run status`
3. **For backend changes**: `npm run restart`
4. **For cleanup**: `npm run cleanup`

### ❌ **Avoid These**
- Running `npm run dev` multiple times
- Letting Cursor auto-restart backend
- Manually killing processes without cleanup

### 🔄 **When to Restart**
- **Backend changes**: Models, API endpoints, database migrations
- **Environment changes**: `.env` file modifications
- **Package changes**: `requirements.txt` or `package.json` updates

### 🚫 **When NOT to Restart**
- **Frontend changes**: React components, CSS, TypeScript
- **Documentation**: Markdown files, comments
- **Configuration**: Non-critical config files

## 🎯 **Current Status**
- ✅ **Backend**: http://127.0.0.1:8000
- ✅ **Frontend**: http://localhost:5173 (or 5174)
- ✅ **Database**: JobTrackerDB_Dev with new columns
- ✅ **Login**: test@example.com / password123

## 🚨 **Troubleshooting**

### Multiple Processes Running
```bash
npm run cleanup
npm run restart
```

### Port Conflicts
```bash
npm run cleanup
# Wait 5 seconds
npm run start
```

### Cursor Confusion
1. Close all terminal windows in Cursor
2. Run `npm run cleanup`
3. Run `npm run start`
4. Use only one terminal window

## 📊 **Service Status Commands**
```bash
# Check what's running
npm run status

# See all processes
Get-Process | Where-Object {$_.ProcessName -eq 'python' -or $_.ProcessName -eq 'node'}

# Check ports
netstat -an | findstr ":8000\|:5173\|:5174"
```

## 🎉 **Benefits**
- **Single terminal window** for all services
- **Controlled restarts** instead of auto-reload chaos
- **Clean process management** with proper cleanup
- **Better Cursor integration** with clear guidelines
- **Reduced resource usage** from multiple processes
