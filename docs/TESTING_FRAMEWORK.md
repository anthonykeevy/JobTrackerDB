# Testing Framework Documentation

## Overview
This document outlines the comprehensive testing framework for the JobTrackerDB AI resume parsing system. The framework is designed to evaluate and improve the accuracy of AI-powered resume parsing through systematic testing and comparison against baseline datasets.

## Directory Structure
```
tests/
├── backend/
│   ├── ai/
│   │   ├── baseline/           # Baseline dataset creation and management
│   │   │   ├── test_ai_parsing_baseline.py
│   │   │   ├── extract_resume_content.py
│   │   │   ├── create_real_baseline.py
│   │   │   └── test_baseline_usage.py
│   │   ├── prompts/            # Prompt effectiveness testing
│   │   │   ├── compare_prompt_versions.py
│   │   │   └── compare_prompt_effectiveness.py
│   │   └── performance/        # Performance and cost analysis
│   └── integration/            # End-to-end workflow testing
├── frontend/                   # Frontend component testing
└── e2e/                       # End-to-end user journey testing
```

## Testing Categories

### 1. Baseline Dataset Management
**Purpose**: Create and maintain accurate baseline datasets for comparison testing.

**Key Files**:
- `tests/backend/ai/baseline/test_ai_parsing_baseline.py` - Runs AI parsing on real resume
- `tests/backend/ai/baseline/create_real_baseline.py` - Creates manually verified baseline
- `tests/backend/ai/baseline/extract_resume_content.py` - Extracts raw resume content

**Current Status**: ✅ **COMPLETED**
- Manual baseline correction completed on 2025-08-06
- Corrected baseline dataset: `corrected_baseline_dataset_20250806_143321.json`
- All sections verified and corrected based on user feedback

**Baseline Dataset Summary**:
- **Personal Info**: 5 fields (name, email, phone, location, LinkedIn)
- **Work Experience**: 4 entries with corrected locations
- **Education**: 8 entries verified
- **Skills**: 58 skills across 4 categories
- **Certifications**: 2 certifications verified
- **Projects**: Empty (confirmed correct)
- **Summary**: 388 characters, comprehensive professional summary

### 2. Prompt Effectiveness Testing
**Purpose**: Compare different AI prompt versions against the baseline to measure improvements.

**Key Files**:
- `tests/backend/ai/prompts/compare_prompt_versions.py` - Main comparison tool
- `tests/backend/ai/prompts/compare_prompt_effectiveness.py` - Detailed metrics

**Current Status**: 🔄 **READY FOR TESTING**
- Framework is operational
- Corrected baseline is ready for comparison
- Ready to test new prompt versions

### 3. Performance Testing
**Purpose**: Monitor AI usage costs, response times, and token efficiency.

**Key Files**:
- `tests/backend/ai/performance/` - Performance analysis tools

**Current Status**: 📋 **PLANNED**

### 4. Integration Testing
**Purpose**: Test complete workflows from resume upload to profile population.

**Key Files**:
- `tests/backend/integration/` - Integration test suites

**Current Status**: 📋 **PLANNED**

## Getting Started

### Prerequisites
1. Python 3.8+ with required packages
2. Access to OpenAI API
3. Resume file: `Resume/Anthony Keevy Resume 202506.docx`

### Quick Start Commands
```bash
# From backend directory
cd backend

# Run AI parsing baseline test
python ../tests/backend/ai/baseline/test_ai_parsing_baseline.py

# Compare prompt versions
python ../tests/backend/ai/prompts/compare_prompt_versions.py

# Generate baseline correction summary
python baseline_correction_summary.py
```

## Data Management

### Baseline Dataset
The baseline dataset serves as the "ground truth" for comparison testing. It contains manually verified data extracted from the real resume.

**Current Baseline**: `corrected_baseline_dataset_20250806_143321.json`

**Key Corrections Applied**:
1. Added location: 'Sydney, Australia'
2. Added LinkedIn: 'https://www.linkedin.com/in/anthony-keevy-5733286/'
3. Corrected work experience locations to country format (Australia)
4. Verified all other extracted data as accurate
5. Confirmed projects section is empty (correct)

### Performance Metrics
The framework tracks several key metrics:
- **Accuracy**: Percentage of correctly extracted fields
- **Completeness**: Percentage of available fields extracted
- **Token Efficiency**: Cost per extraction
- **Response Quality**: JSON validity and structure

## Configuration

### Environment Variables
```bash
OPENAI_API_KEY=your_api_key_here
DATABASE_URL=your_database_connection_string
```

### Test Configuration
- **Resume File**: `../Resume/Anthony Keevy Resume 202506.docx`
- **Output Directory**: `ai_baseline_results/`
- **Model**: `gpt-3.5-turbo` (optimized for cost and performance)

## Continuous Improvement Workflow

### 1. Baseline Creation ✅ COMPLETED
- [x] Extract content from real resume
- [x] Run AI parsing with current prompt
- [x] Manually correct AI extraction errors
- [x] Create verified baseline dataset

### 2. Prompt Testing 🔄 IN PROGRESS
- [ ] Test new prompt versions
- [ ] Compare against baseline
- [ ] Measure accuracy improvements
- [ ] Document findings

### 3. Performance Optimization 📋 PLANNED
- [ ] Analyze token usage patterns
- [ ] Optimize prompt length
- [ ] Implement cost controls
- [ ] Monitor response times

### 4. Integration Validation 📋 PLANNED
- [ ] Test complete user workflows
- [ ] Validate database persistence
- [ ] Verify frontend integration
- [ ] End-to-end testing

## Maintenance

### Regular Tasks
1. **Weekly**: Review and update baseline dataset
2. **Monthly**: Test new prompt versions
3. **Quarterly**: Performance analysis and optimization

### File Organization
- All test results are stored in `ai_baseline_results/`
- Corrected files are prefixed with `corrected_`
- Timestamps are included in filenames for versioning

## Contributing

### Adding New Tests
1. Create test file in appropriate directory
2. Follow naming convention: `test_*.py`
3. Include comprehensive documentation
4. Add to this documentation

### Reporting Issues
1. Document the issue with specific details
2. Include test data and expected results
3. Provide error messages and stack traces
4. Suggest potential solutions

## Troubleshooting

### Common Issues
1. **Module Import Errors**: Ensure backend directory is in Python path
2. **File Not Found**: Check relative paths from execution directory
3. **API Rate Limits**: Implement retry logic and token optimization
4. **JSON Parsing Errors**: Validate AI response format

### Debug Tools
- `test_active_prompt.py` - Verify current prompt
- `test_truncation.py` - Test resume content truncation
- `test_prompt_size.py` - Analyze prompt token usage

## Additional Resources

### Documentation
- `docs/PROJECT_INDEX.md` - Central navigation
- `docs/PROJECT_COMPLETION_SUMMARY.md` - Project status
- `README.md` - Main project overview

### Key Files
- `backend/app/api/resume.py` - Main AI parsing logic
- `backend/app/services/prompt_service.py` - Prompt management
- `backend/improve_resume_prompt.py` - Prompt versioning

### Current Baseline Dataset
- **File**: `corrected_baseline_dataset_20250806_143321.json`
- **Sections**: 7 (personal_info, work_experience, education, skills, certifications, projects, summary)
- **Total Fields**: 100+ individual data points
- **Status**: Manually verified and corrected

## Version Control

### Baseline Versioning
- Each baseline correction creates a new timestamped file
- Previous versions are retained for comparison
- Version history is documented in this file

### Prompt Versioning
- Prompts are stored in database with version numbers
- Active prompt is tracked for testing
- Version comparison tools available

## Checklist for New Tests

### Before Running Tests
- [ ] Verify resume file exists and is accessible
- [ ] Check OpenAI API key is valid
- [ ] Ensure database connection is working
- [ ] Confirm baseline dataset is up to date

### After Running Tests
- [ ] Review test results for accuracy
- [ ] Document any new findings
- [ ] Update baseline if necessary
- [ ] Commit changes to version control

### Quality Assurance
- [ ] All tests pass without errors
- [ ] Results are consistent across runs
- [ ] Performance metrics are within acceptable ranges
- [ ] Documentation is updated

---

**Last Updated**: 2025-08-06
**Current Status**: Baseline correction completed, ready for prompt effectiveness testing
**Next Milestone**: Prompt version comparison and optimization 