# JobTrackerDB Testing Framework

## Overview

The JobTrackerDB Testing Framework provides a comprehensive, organized approach to testing all components of the application. This framework ensures consistent testing practices, proper file organization, and accurate baseline data for AI prompt evaluation.

## 📁 Directory Structure

```
tests/
├── backend/                    # Backend-specific tests
│   ├── ai/                    # AI/Resume parsing tests
│   │   ├── baseline/          # Baseline data extraction
│   │   ├── performance/       # Performance testing
│   │   └── prompts/           # Prompt management tests
│   ├── api/                   # API endpoint tests
│   ├── database/              # Database tests
│   └── integration/           # Backend integration tests
├── frontend/                  # Frontend-specific tests
│   ├── components/            # Component tests
│   ├── pages/                 # Page tests
│   └── integration/           # Frontend integration tests
├── general/                   # General testing
│   ├── performance/           # Performance tests
│   ├── security/              # Security tests
│   └── e2e/                  # End-to-end tests
└── data/                      # Test data and exports
    ├── resumes/               # Sample resumes
    ├── baseline/              # Baseline datasets
    └── exports/               # Test exports
```

## 🧪 Testing Categories

### Backend Tests
- **AI Tests**: Resume parsing, prompt management, performance evaluation
- **API Tests**: Endpoint functionality, request/response validation
- **Database Tests**: Data persistence, migrations, stored procedures
- **Integration Tests**: Component interaction, workflow testing

### Frontend Tests
- **Component Tests**: Individual React component functionality
- **Page Tests**: Full page rendering and interaction
- **Integration Tests**: Component integration, routing

### General Tests
- **Performance Tests**: Load testing, response time analysis
- **Security Tests**: Authentication, authorization, data protection
- **E2E Tests**: Complete user workflow testing

### Data Management
- **Resumes**: Sample resume files for testing
- **Baseline**: Ground truth datasets for AI testing
- **Exports**: Test result exports and reports

## 🚀 Getting Started

### Running Baseline Extraction
```bash
cd tests/backend/ai/baseline
python extract_resume_baseline.py
```

### Running Performance Tests
```bash
cd tests/backend/ai/performance
python test_resume_parser_performance.py
```

### Running API Tests
```bash
cd tests/backend/api
python test_api_endpoints.py
```

## 📊 Test Data Management

### Baseline Data
The baseline data is extracted from a comprehensive test resume and serves as the "ground truth" for evaluating AI prompt effectiveness. Files include:

- `baseline_resume_content.txt`: Raw resume text
- `baseline_personal_info.csv`: Personal information fields
- `baseline_work_experience.csv`: Work experience entries
- `baseline_education.csv`: Education records
- `baseline_skills.csv`: Skills by category
- `baseline_certifications.csv`: Certification records
- `baseline_projects.csv`: Project information
- `baseline_summary.csv`: Professional summary
- `baseline_dataset.json`: Complete structured dataset

### Performance Metrics
Tests generate detailed performance metrics including:
- Extraction accuracy by subject area
- Completeness scores
- Processing time
- Token usage and costs
- Quality assessments

## 🔧 Configuration

### Environment Setup
Ensure the backend environment is properly configured:
```bash
cd backend
pip install -r requirements.txt
```

### Database Connection
Tests require access to the development database (`JobTrackerDB_Dev`).

## 📈 Continuous Improvement

### Prompt Testing Workflow
1. **Extract Baseline**: Run baseline extractor to create ground truth
2. **Manual Verification**: Review and correct CSV files
3. **Update Baseline**: Incorporate corrections into JSON dataset
4. **Test Prompts**: Run performance tests against baseline
5. **Compare Results**: Analyze improvements and regressions
6. **Iterate**: Refine prompts based on results

### Performance Tracking
- Track accuracy improvements over time
- Monitor cost efficiency
- Document prompt version changes
- Maintain historical test results

## 🛠️ Maintenance

### File Organization
- Keep test files in appropriate directories
- Use descriptive naming conventions
- Maintain clear separation of concerns
- Document test purposes and expected outcomes

### Data Management
- Version control baseline datasets
- Archive historical test results
- Clean up temporary files regularly
- Maintain data quality standards

## 📝 Contributing

When adding new tests:
1. Place files in appropriate directories
2. Follow existing naming conventions
3. Include comprehensive documentation
4. Add to this README if needed
5. Update test runners if applicable

## 🔍 Troubleshooting

### Common Issues
- **Path Issues**: Ensure Python path includes backend directory
- **Database Connection**: Verify database is running and accessible
- **Dependencies**: Check all required packages are installed
- **Permissions**: Ensure write access to test directories

### Debug Mode
Enable detailed logging for troubleshooting:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📚 Additional Resources

- [Backend Testing Guide](../backend/README.md)
- [API Documentation](../docs/api.md)
- [Database Schema](../docs/schema.md)
- [Performance Testing Guide](../docs/performance.md)

## 🎯 Key Files

### Baseline Dataset Files
Located in `tests/backend/ai/baseline/`:
- `extract_resume_baseline.py` - Baseline data extractor
- `baseline_dataset.json` - Complete structured dataset
- `baseline_*.csv` - Individual subject area files

### Performance Testing Files
Located in `tests/backend/ai/performance/`:
- `test_resume_parser_performance.py` - Performance evaluation framework

### Prompt Management Files
Located in `tests/backend/ai/prompts/`:
- `test_prompt_management.py` - Prompt management tests
- `compare_prompt_versions.py` - Version comparison tools
- `improve_resume_prompt.py` - Prompt improvement utilities

## 📊 Current Baseline Dataset Summary

- **Personal Info**: 5 fields
- **Work Experience**: 2 entries
- **Education**: 2 entries
- **Skills**: 30 skills in 2 categories
- **Certifications**: 2 entries
- **Projects**: 2 entries

## 🔄 Version Control

All test files and baseline data should be committed to version control:
```bash
git add tests/
git commit -m "Add comprehensive testing framework and baseline dataset"
```

## 📋 Checklist for New Tests

- [ ] Place test file in appropriate directory
- [ ] Follow naming conventions
- [ ] Include proper documentation
- [ ] Add to relevant test runners
- [ ] Update this documentation if needed
- [ ] Test the new test file
- [ ] Commit to version control 