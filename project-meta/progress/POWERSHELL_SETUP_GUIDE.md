# 🎯 PowerShell Setup Guide for JobTrackerDB

## ✅ Problem Fixed!

I've updated all scripts to be **PowerShell-compatible** and removed all `&&` syntax that was causing errors on your system.

## 🔧 What Was Changed

### 1. **PowerShell-Specific Scripts**
- `start-backend.ps1` - Properly handles Python path and virtual environment
- `install-dependencies.ps1` - PowerShell-compatible dependency installation
- Updated `package.json` to use PowerShell scripts instead of `&&` commands

### 2. **Environment Handling**
- Automatic virtual environment detection and activation
- Proper Python path setting
- PowerShell-compatible command chaining

### 3. **Error Prevention**
- Removed all `&&` syntax that fails in PowerShell
- Used proper PowerShell command separation
- Added proper error handling

## 🚀 How to Use

### **Option 1: npm scripts (Recommended)**
```powershell
# Start both services
npm run dev

# Start only backend
npm run dev:backend

# Start only frontend
npm run dev:frontend
```

### **Option 2: PowerShell scripts directly**
```powershell
# Start development environment
.\dev-setup.ps1 dev

# Install dependencies
.\install-dependencies.ps1

# Start backend only
.\start-backend.ps1
```

### **Option 3: Batch file**
```cmd
start-dev.bat
```

## 📋 Prerequisites

1. **Node.js** (v18 or higher)
2. **Python** (3.8 or higher)
3. **PowerShell** (5.1 or higher)
4. **npm** (comes with Node.js)

## 🔧 Initial Setup

### **First Time Setup:**
```powershell
# Install all dependencies (PowerShell-compatible)
npm run install:all

# Or use the PowerShell script directly
.\install-dependencies.ps1
```

### **Environment Variables:**
```powershell
# Copy backend environment template
Copy-Item backend\env.example backend\.env
# Edit backend\.env with your configuration
```

## 🎯 Service Management

### **Ports Used**
- **Backend**: http://127.0.0.1:8000
- **Frontend**: http://localhost:5173 (or 5174 if 5173 is busy)

### **Auto-reload**
Both services automatically reload when you make changes to files.

### **Stopping Services**
- Press `Ctrl+C` in the terminal to stop all services
- Use `npm run kill:ports` to force-kill processes

## 🔍 Troubleshooting

### **PowerShell Execution Policy**
If you get execution policy errors:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Virtual Environment Issues**
```powershell
# Create virtual environment if missing
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

### **Port Conflicts**
```powershell
# Kill processes on specific ports
npm run kill:ports

# Then restart
npm run dev
```

### **Module Not Found Errors**
```powershell
# Reinstall dependencies
npm run install:all
```

## 📁 Updated Project Structure

```
JobTrackerDB/
├── backend/                    # FastAPI Python backend
│   ├── app/                   # Application code
│   ├── requirements.txt
│   └── .env                   # Environment variables
├── frontend/                  # React TypeScript frontend
│   ├── src/                   # Source code
│   ├── package.json
│   └── vite.config.ts
├── docs/                      # Documentation
├── package.json               # Root package.json with PowerShell scripts
├── start-dev.bat              # Windows batch file
├── dev-setup.ps1              # PowerShell script
├── start-backend.ps1          # PowerShell backend starter
├── install-dependencies.ps1   # PowerShell dependency installer
└── .cursorrules               # Cursor IDE rules
```

## 🛠️ PowerShell-Specific Commands

### **Development**
```powershell
npm run dev                    # Start both services
npm run dev:backend            # Start only backend
npm run dev:frontend           # Start only frontend
```

### **Maintenance**
```powershell
npm run install:all            # Install all dependencies
npm run clean                  # Clean cache
npm run kill:ports             # Kill all processes
```

### **Direct PowerShell Scripts**
```powershell
.\start-backend.ps1            # Start backend with proper setup
.\install-dependencies.ps1     # Install all dependencies
.\dev-setup.ps1 dev           # Start development environment
.\dev-setup.ps1 kill          # Kill all processes
.\dev-setup.ps1 install       # Install dependencies
.\dev-setup.ps1 clean         # Clean cache
```

## 🎯 Benefits for PowerShell Users

### ✅ **No More `&&` Errors**
- All scripts use proper PowerShell syntax
- No command chaining issues
- Proper error handling

### ✅ **Virtual Environment Management**
- Automatic detection and activation
- Proper Python path setting
- Dependency management

### ✅ **Cursor Integration**
- Single terminal session for both services
- All logs visible in Cursor's integrated terminal
- Easy process management

### ✅ **Error Prevention**
- PowerShell-compatible command syntax
- Proper environment variable handling
- Better error messages

## 📊 Current Status

**✅ Both services are running:**
- **Backend**: http://127.0.0.1:8000 ✅
- **Frontend**: http://localhost:5173 ✅

## 🚨 Common PowerShell Issues and Solutions

### **Execution Policy Errors**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Virtual Environment Not Found**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### **Python Path Issues**
The `start-backend.ps1` script automatically sets `$env:PYTHONPATH = "."`

### **Port Already in Use**
```powershell
npm run kill:ports
npm run dev
```

## 📝 Quick Reference

| Command | Action |
|---------|--------|
| `npm run dev` | Start both services |
| `Ctrl+C` | Stop both services |
| `npm run kill:ports` | Force kill all processes |
| `npm run install:all` | Install all dependencies |
| `.\start-backend.ps1` | Start backend with proper setup |

## 🎉 You're All Set!

**Your PowerShell environment is now fully compatible with:**
- ✅ No more `&&` syntax errors
- ✅ Proper virtual environment handling
- ✅ Cursor integration working
- ✅ Both services running successfully
- ✅ Auto-reload on file changes

**No more PowerShell compatibility issues!** 🚀 