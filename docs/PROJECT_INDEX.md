# JobTrackerDB Project Index

## 📋 Quick Navigation

### Core Documentation
- [README.md](../README.md) - Main project overview and setup
- [TESTING_FRAMEWORK.md](TESTING_FRAMEWORK.md) - Comprehensive testing guide
- [PROJECT_INDEX.md](PROJECT_INDEX.md) - This navigation index

### Key Directories
- [backend/](../backend/) - FastAPI backend application
- [frontend/](../frontend/) - React frontend application
- [tests/](../tests/) - Comprehensive testing framework
- [docs/](.) - Project documentation
- [scripts/](../scripts/) - Utility scripts

## 🏗️ Architecture Overview

### Backend Structure
```
backend/
├── app/                       # Main FastAPI application
│   ├── api/                  # API route handlers
│   ├── models/               # SQLAlchemy models
│   ├── services/             # Business logic services
│   └── main.py              # Application entry point
├── mcp/                      # Model Context Protocol service
└── requirements.txt          # Python dependencies
```

### Testing Framework Structure
```
tests/
├── backend/                  # Backend-specific tests
│   ├── ai/                  # AI/Resume parsing tests
│   │   ├── baseline/        # Baseline data extraction
│   │   ├── performance/     # Performance testing
│   │   └── prompts/         # Prompt management tests
│   ├── api/                 # API endpoint tests
│   ├── database/            # Database tests
│   └── integration/         # Backend integration tests
├── frontend/                # Frontend-specific tests
├── general/                 # General testing
└── data/                    # Test data and exports
```

## 🧪 Testing Framework Index

### Baseline Dataset Files
Located in `tests/backend/ai/baseline/`:
- `extract_resume_baseline.py` - Baseline data extractor
- `baseline_dataset.json` - Complete structured dataset
- `baseline_personal_info.csv` - Personal information fields
- `baseline_work_experience.csv` - Work experience entries
- `baseline_education.csv` - Education records
- `baseline_skills.csv` - Skills by category
- `baseline_certifications.csv` - Certification records
- `baseline_projects.csv` - Project information
- `baseline_summary.csv` - Professional summary
- `baseline_resume_content.txt` - Raw resume text

### Performance Testing Files
Located in `tests/backend/ai/performance/`:
- `test_resume_parser_performance.py` - Performance evaluation framework

### Prompt Management Files
Located in `tests/backend/ai/prompts/`:
- `test_prompt_management.py` - Prompt management tests
- `compare_prompt_versions.py` - Version comparison tools
- `improve_resume_prompt.py` - Prompt improvement utilities

### API Testing Files
Located in `tests/backend/api/`:
- `test_resume_upload.py` - Resume upload testing
- `test_address_api.py` - Address validation testing
- `test_geoscape_api.py` - Geoscape API testing

### Database Testing Files
Located in `tests/backend/database/`:
- `check_resume_data_saved.py` - Data persistence verification
- `schema_comparison.py` - Database schema validation

## 🔧 Key Features Index

### AI-Powered Resume Parsing
- **Location**: `backend/app/api/resume.py`
- **Features**: 
  - Intelligent data extraction
  - Cost tracking and monitoring
  - Prompt management
  - Performance evaluation

### Profile Management
- **Location**: `frontend/src/components/ProfileBuilder/`
- **Features**:
  - Multi-section profile builder
  - Auto-save functionality
  - Address validation
  - Gamification system

### Database Management
- **Location**: `backend/app/models.py`
- **Features**:
  - Hierarchical table structure
  - Stored procedures
  - Environment segregation
  - Audit logging

## 📊 Baseline Dataset Summary

### Current Dataset Statistics
- **Personal Info**: 5 fields
- **Work Experience**: 2 entries
- **Education**: 2 entries
- **Skills**: 30 skills in 2 categories
- **Certifications**: 2 entries
- **Projects**: 2 entries

### Dataset Files
1. **baseline_dataset.json** - Complete structured dataset
2. **baseline_personal_info.csv** - Personal information fields
3. **baseline_work_experience.csv** - Work experience entries
4. **baseline_education.csv** - Education records
5. **baseline_skills.csv** - Skills by category
6. **baseline_certifications.csv** - Certification records
7. **baseline_projects.csv** - Project information
8. **baseline_summary.csv** - Professional summary
9. **baseline_resume_content.txt** - Raw resume text

## 🚀 Quick Start Commands

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Database Setup
```bash
cd backend
python setup_database.py
```

### Testing Framework
```bash
# Baseline extraction
cd tests/backend/ai/baseline
python extract_resume_baseline.py

# Performance testing
cd tests/backend/ai/performance
python test_resume_parser_performance.py

# API testing
cd tests/backend/api
python test_api_endpoints.py
```

## 📚 Documentation Index

### Core Documentation
- [README.md](../README.md) - Main project overview
- [TESTING_FRAMEWORK.md](TESTING_FRAMEWORK.md) - Testing guide
- [PROJECT_INDEX.md](PROJECT_INDEX.md) - This navigation index

### Planned Documentation
- [api.md](api.md) - API documentation
- [schema.md](schema.md) - Database schema
- [performance.md](performance.md) - Performance guidelines

## 🔄 Development Workflow

### Adding New Tests
1. Place test files in appropriate `tests/` subdirectories
2. Follow existing naming conventions
3. Include comprehensive documentation
4. Update test runners if applicable
5. Commit to version control

### AI Prompt Management
1. Store prompts in database with version control
2. Test against baseline dataset
3. Measure accuracy improvements
4. Track cost efficiency
5. Document changes and results

### File Organization
- Keep test files in appropriate directories
- Use descriptive naming conventions
- Maintain clear separation of concerns
- Document test purposes and expected outcomes

## 📈 Performance Monitoring

### AI Usage Tracking
- **Location**: `backend/app/api/resume.py`
- **Features**: Cost tracking, token usage, performance metrics

### Database Performance
- **Location**: `backend/mcp/`
- **Features**: Query optimization, response time monitoring

### Test Performance
- **Location**: `tests/backend/ai/performance/`
- **Features**: Accuracy measurement, completeness scoring

## 🔒 Security Features

### Authentication
- **Location**: `backend/app/api/`
- **Features**: OAuth via database stored procedures

### Environment Segregation
- **Location**: `backend/app/models.py`
- **Features**: Dev/Staging/Production database separation

### Audit Logging
- **Location**: `backend/app/services/`
- **Features**: Comprehensive activity tracking

## 📋 Project Status

### ✅ Completed Features
- [x] Comprehensive testing framework organization
- [x] Baseline dataset creation
- [x] AI resume parsing implementation
- [x] Profile builder with auto-save
- [x] Address validation integration
- [x] Database structure with proper naming
- [x] Cost tracking and monitoring

### 🔄 In Progress
- [ ] Frontend component testing
- [ ] End-to-end testing
- [ ] Performance optimization
- [ ] Security testing

### 📋 Planned Features
- [ ] Advanced AI prompt optimization
- [ ] Enhanced gamification features
- [ ] Mobile responsiveness
- [ ] Advanced analytics dashboard

## 🎯 Key Metrics

### Testing Framework
- **Test Categories**: 4 main categories (AI, API, Database, Integration)
- **Baseline Dataset**: 9 comprehensive files
- **Performance Metrics**: Accuracy, completeness, cost tracking

### Project Structure
- **Organized Files**: All test files properly categorized
- **Documentation**: Comprehensive guides and indexes
- **Version Control**: Ready for GitHub sync

---

**Last Updated**: August 2025  
**Version**: 1.0.0  
**Testing Framework**: Comprehensive baseline dataset and organized structure 