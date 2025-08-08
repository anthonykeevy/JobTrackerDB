# JobTrackerDB Development Guide

## 🚀 Quick Start with Cursor

### Option 1: Using npm scripts (Recommended)
```bash
# Start both services concurrently
npm run dev

# Start only backend
npm run dev:backend

# Start only frontend  
npm run dev:frontend
```

### Option 2: Using the batch file
```bash
# Double-click or run from terminal
start-dev.bat
```

### Option 3: Using PowerShell script
```powershell
# Start development environment
.\dev-setup.ps1 dev

# Kill all processes
.\dev-setup.ps1 kill

# Install dependencies
.\dev-setup.ps1 install

# Clean cache
.\dev-setup.ps1 clean
```

## 📋 Prerequisites

1. **Node.js** (v18 or higher)
2. **Python** (3.8 or higher)
3. **npm** (comes with Node.js)
4. **pip** (Python package manager)

## 🔧 Initial Setup

1. **Install all dependencies:**
   ```bash
   npm run install:all
   ```

2. **Set up environment variables:**
   ```bash
   # Copy backend environment template
   copy backend\env.example backend\.env
   # Edit backend\.env with your configuration
   ```

## 🎯 Service Management

### Ports Used
- **Backend**: http://127.0.0.1:8000
- **Frontend**: http://localhost:5173

### Auto-reload
Both services automatically reload when you make changes to files.

### Stopping Services
- Press `Ctrl+C` in the terminal to stop all services
- Use `npm run kill:ports` to force-kill processes

## 🔍 Troubleshooting

### Port Conflicts
If you get "port already in use" errors:
```bash
npm run kill:ports
# Then restart with
npm run dev
```

### Module Not Found Errors
```bash
# Reinstall dependencies
npm run install:all
```

### Cache Issues
```bash
# Clean all cache
npm run clean
```

### Python Environment Issues
```bash
# Ensure you're in the correct Python environment
cd backend
pip install -r requirements.txt
```

## 📁 Project Structure

```
JobTrackerDB/
├── backend/           # FastAPI Python backend
│   ├── app/          # Application code
│   ├── requirements.txt
│   └── .env          # Environment variables
├── frontend/         # React TypeScript frontend
│   ├── src/          # Source code
│   ├── package.json
│   └── vite.config.ts
├── docs/             # Documentation
├── package.json      # Root package.json with scripts
├── start-dev.bat     # Windows batch file
├── dev-setup.ps1     # PowerShell script
└── .cursorrules      # Cursor IDE rules
```

## 🛠️ Development Workflow

1. **Start development environment:**
   ```bash
   npm run dev
   ```

2. **Make changes to your code**

3. **Services auto-reload automatically**

4. **Stop services:**
   - Press `Ctrl+C` in terminal

## 🔧 Cursor Integration

### Why This Setup Works Better with Cursor

1. **Single Terminal Session**: Both services run in the same terminal session that Cursor can monitor
2. **Concurrent Execution**: Uses `concurrently` to run both services simultaneously
3. **Process Management**: Cursor can see and control both processes from one terminal
4. **Auto-reload**: Both services reload automatically on file changes
5. **Error Visibility**: All errors and logs appear in Cursor's integrated terminal

### Benefits Over Separate PowerShell Sessions

- ✅ Cursor can monitor both services
- ✅ Single terminal for all output
- ✅ Easy to stop both services with `Ctrl+C`
- ✅ Better error handling and logging
- ✅ Consistent development experience

## 🚨 Common Issues and Solutions

### "Module not found" errors
```bash
npm run install:all
```

### Services not starting
```bash
npm run kill:ports
npm run dev
```

### Frontend not connecting to backend
- Check that backend is running on port 8000
- Verify CORS settings in backend
- Check network tab in browser dev tools

### Database connection issues
- Verify database server is running
- Check connection string in `backend/.env`
- Ensure database exists and is accessible

## 📝 Useful Commands

```bash
# Development
npm run dev              # Start both services
npm run dev:backend      # Start only backend
npm run dev:frontend     # Start only frontend

# Maintenance
npm run install:all      # Install all dependencies
npm run clean            # Clean cache
npm run kill:ports       # Kill all processes
npm run build            # Build frontend for production
npm run test             # Run frontend tests
npm run lint             # Run frontend linting
```

## 🎉 You're Ready!

With this setup, Cursor can now properly monitor and manage both your backend and frontend services from a single integrated terminal. The services will auto-reload on changes, and you'll have full visibility into both processes. 