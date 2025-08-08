# JobTrackerDB - New Chat Session Prompt

## 🎯 Project Overview
JobTrackerDB is a comprehensive job tracking and career management platform with AI-powered resume parsing, address validation, and multi-step profile building capabilities.

## 📋 Current Status Summary

### ✅ **COMPLETED INFRASTRUCTURE**
- **Database**: Complete schema (31+ tables) with Alembic migrations
- **Frontend**: Full 9-step profile builder with address validation UI
- **Backend**: API configuration and models ready
- **Environments**: Dev, Staging, Test, Production databases aligned

### 🔄 **CURRENT FOCUS: Address Validation Backend Integration**

**Status**: Frontend UI is 100% complete and functional with mock data. Backend API implementation needed.

**Key Files**:
- `frontend/src/components/ProfileBuilder/steps/BasicInfoStep.tsx` (Complete UI)
- `frontend/src/components/Map/MapComponent.tsx` (Mapbox integration)
- `backend/app/core/api_config.py` (Geoscape API keys configured)
- `docs/stories/EPC-1.15-address-validation-backend-integration.md` (Backend story)

**Test Addresses**:
- Primary: "4 Milburn Place, St Ives Chase NSW 2075"
- Secondary: "14 Milburn Place, St Ives Chase NSW 2075"
- Coordinates: `-33.70131425995992, 151.16600576829697` (Google Maps verified)

## 🚀 **IMMEDIATE NEXT STEPS**

### Priority 1: Backend API Implementation
1. **Create Geoscape API endpoints**:
   - `GET /api/address/search` (autocomplete)
   - `POST /api/address/validate` (validation)
2. **Implement database integration** with `ProfileAddress` table
3. **Add API usage tracking** in `APIUsageTracking` table
4. **Connect frontend to real APIs** (replace mock data)

### Priority 2: Database Population
1. **Seed country list** in `Country` table
2. **Populate reference data** for industries, skills, etc.
3. **Add API provider configurations**

### Priority 3: Authentication & Profile Saving
1. **Connect profile builder to backend**
2. **Implement user authentication**
3. **Add profile data persistence**

## 📁 **KEY FILES & THEIR PURPOSES**

### Backend Structure
```
backend/
├── alembic.ini                    # Development migration config
├── app/
│   ├── models.py                 # Complete database schema (31+ tables)
│   ├── core/api_config.py       # API configurations (Geoscape keys ready)
│   └── main.py                  # FastAPI application
└── requirements.txt              # Python dependencies
```

### Frontend Structure
```
frontend/src/components/ProfileBuilder/
├── index.tsx                     # Main profile builder component
├── types.ts                      # TypeScript interfaces
├── steps/
│   ├── WelcomeStep.tsx          # Mode selection (Guided vs Independent)
│   ├── ResumeUploadStep.tsx     # AI resume parsing (mock)
│   ├── BasicInfoStep.tsx        # Address validation + personal info ✅ COMPLETE
│   ├── CareerAspirationStep.tsx # Career goals + salary ✅ COMPLETE
│   ├── EducationStep.tsx        # Education + certifications ✅ COMPLETE
│   ├── WorkExperienceStep.tsx   # Professional history ✅ COMPLETE
│   ├── SkillsStep.tsx           # Skills categorization ✅ COMPLETE
│   ├── ProjectsStep.tsx         # Portfolio showcase ✅ COMPLETE
│   └── ReviewStep.tsx           # Profile summary ✅ COMPLETE
└── Map/
    └── MapComponent.tsx         # Mapbox integration ✅ COMPLETE
```

## 🔧 **TECHNICAL DECISIONS MADE**

### Database Architecture
- **Migration System**: Alembic with smart comparison
- **Naming Convention**: Hierarchical (e.g., `ProfileCareerAspiration`)
- **Collation**: `SQL_Latin1_General_CP1_CI_AS` across all environments
- **Environments**: Dev, Staging, Test, Production

### Frontend Architecture
- **Framework**: React + TypeScript + Vite
- **Styling**: Tailwind CSS with responsive design
- **State Management**: Component-level with prop drilling
- **Form Handling**: react-hook-form + Zod validation

### API Integration Strategy
- **Primary**: Geoscape for Australia
- **Backup**: SmartyStreets for US
- **Future**: Regional API providers for global expansion
- **Billing**: APIUsageTracking table for quota management

## 🎯 **SUCCESS CRITERIA FOR THIS SESSION**

1. **Address validation backend APIs implemented and functional**
2. **Frontend successfully connected to real Geoscape API**
3. **Database populated with reference data**
4. **Profile builder saving data to backend**
5. **Authentication system connected**

## 📚 **DOCUMENTATION RESOURCES**

- **Progress Summary**: `PROGRESS_SUMMARY.md` (comprehensive project state)
- **Backend Story**: `docs/stories/EPC-1.15-address-validation-backend-integration.md`
- **API Configuration**: `backend/app/core/api_config.py`
- **Database Schema**: `backend/app/models.py`
- **Test Tools**: `frontend/address-test.html`, `frontend/src/test-address-api.js`

## 🔑 **API KEYS & CONFIGURATION**

### Geoscape API (Already Configured)
```python
# backend/app/core/api_config.py
GEOSCAPE_API_KEY: str = "9x4fpNyrr8VxVqWvPeKnuEWaH9vxgGxS"
GEOSCAPE_CONSUMER_SECRET: str = "8XkTgtu0Sz1D0aG9"
GEOSCAPE_BASE_URL: str = "https://api.geoscape.com.au/v1"
```

### Mapbox API (Already Configured)
```typescript
// frontend/src/components/Map/MapComponent.tsx
const MAPBOX_TOKEN = "pk.eyJ1IjoiYW50aG9ueWtlZXZ5IiwiYSI6ImNtZHR1NXFjejBhdTkybW9qdmJoenZxNWoifQ.eKJynTPhNLEd4TrUYY2aNA"
```

## 🚀 **HOW TO START DEVELOPMENT**

### 1. Start Services
```bash
# Backend (from backend/ directory)
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (from frontend/ directory)
npm install
npm run dev
```

### 2. Database Setup
```bash
# Apply migrations to development
alembic upgrade head

# Apply to staging
alembic -c alembic_staging.ini upgrade head

# Apply to production  
alembic -c alembic_production.ini upgrade head
```

### 3. Current Development Focus
- **Address Validation**: Implement Geoscape API endpoints
- **Backend APIs**: Connect frontend to real APIs
- **Database Seeding**: Populate country lists and reference data

## ⚠️ **KNOWN ISSUES & SOLUTIONS**

### Address Validation
- **Status**: Frontend complete, backend implementation needed
- **Test Files**: `frontend/address-test.html` for systematic testing
- **Solution**: Implement Geoscape API endpoints

### Console Warnings
- **Problem**: `GroupMarkerNotSet` warning
- **Cause**: Chrome WebGL bug (non-critical)
- **Solution**: Already implemented in `MapComponent.tsx`

### Focus Issues
- **Problem**: Address input focus jumping
- **Solution**: Implemented debounced search (500ms)

---

## 🎯 **STARTING INSTRUCTIONS FOR NEW ASSISTANT**

1. **Read the `PROGRESS_SUMMARY.md` file** for complete project context
2. **Review the backend story** `docs/stories/EPC-1.15-address-validation-backend-integration.md`
3. **Start with Priority 1**: Implement Geoscape API endpoints
4. **Use the test files** for systematic testing
5. **Follow the technical decisions** already made (database, frontend, API strategy)
6. **Maintain the existing code quality** and documentation standards

**Key Message**: The frontend is complete and functional. Focus on backend API implementation to connect the UI to real services. 