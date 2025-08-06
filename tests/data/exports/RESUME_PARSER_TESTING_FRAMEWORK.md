# Resume Parser Testing & Evaluation Framework

## Overview

This framework provides a comprehensive system for testing, evaluating, and improving the AI-powered resume parser. It tracks performance metrics by subject area (BasicInfo, Experience, Education, etc.) and enables targeted prompt improvements.

## Key Features

### 🎯 **Subject Area Performance Tracking**
- **Personal Information**: Name, email, phone, location
- **Work Experience**: Company, position, dates, achievements, technologies
- **Education**: Institution, degree, field of study, graduation date, GPA
- **Skills**: Technical and soft skills categorization
- **Certifications**: Name, issuer, dates
- **Projects**: Name, description, technologies, URLs

### 📊 **Performance Metrics**
- **Accuracy**: How well extracted data matches expected data
- **Completeness**: Percentage of expected fields extracted
- **Quality Score**: Combined accuracy and completeness
- **Cost Tracking**: Token usage and API costs
- **Processing Time**: Performance efficiency

### 🔧 **Improvement Tools**
- **Performance Testing**: Test current prompt performance
- **Improvement Analysis**: Identify weak areas and suggest enhancements
- **Version Comparison**: Compare different prompt versions
- **Prompt Management**: Create, activate, and manage prompt versions

## Usage Guide

### 1. **Test Current Performance**

```bash
python test_resume_parser_performance.py
```

**Output Example:**
```
📊 TEST RESULTS - Prompt Version: 1.1
Overall Accuracy: 95.8%
Overall Completeness: 100.0%

📋 SUBJECT AREA BREAKDOWN:
PERSONAL_INFO: 100.0% accuracy, 100.0% completeness
WORK_EXPERIENCE: 100.0% accuracy, 100.0% completeness
EDUCATION: 75.0% accuracy, 100.0% completeness
SKILLS: 100.0% accuracy, 100.0% completeness
CERTIFICATIONS: 100.0% accuracy, 100.0% completeness
PROJECTS: 100.0% accuracy, 100.0% completeness
```

### 2. **Analyze and Improve Prompts**

```bash
python improve_resume_prompt.py
```

**Output Example:**
```
📊 RESUME PARSER IMPROVEMENT REPORT
============================================================

🎯 OVERALL PERFORMANCE:
  Accuracy: 95.8%
  Completeness: 100.0%

⚠️  WEAKEST AREAS:
  • EDUCATION: 87.5% quality score

🚀 IMPROVEMENT PRIORITIES:
  • EDUCATION: 87.5% (needs improvement)

📋 DETAILED ANALYSIS:
EDUCATION:
  Current Accuracy: 75.0%
  Issues: GPA mismatch in education 1, GPA mismatch in education 2
  Suggested Improvements:
    • Add instructions for GPA extraction and formatting
    • Include examples of different degree formats
```

### 3. **Compare Prompt Versions**

```bash
python compare_prompt_versions.py
```

**Output Example:**
```
📊 PROMPT VERSION COMPARISON REPORT
============================================================

🔄 VERSION COMPARISON:
  Baseline: v1.0
  New Version: v1.1

🎯 OVERALL PERFORMANCE CHANGES:
  Accuracy Change: +0.0%
  Completeness Change: +0.0%

📋 SUBJECT AREA CHANGES:
EDUCATION:
  Accuracy: +0.0%
  Completeness: +0.0%
  Quality Score: +0.0%

💡 RECOMMENDATIONS:
  1. 🤔 Mixed results: Further testing recommended
```

### 4. **Manage Prompt Versions**

```bash
python activate_prompt.py
```

**Output Example:**
```
📋 Available Resume Parser Prompts:
==================================================
1. Resume Parser v1.0 (Improved) v1.1 - ✅ ACTIVE
2. Resume Parser v1.0 v1.0 - ⏸️ INACTIVE

🔄 Activating improved prompt: Resume Parser v1.0 (Improved) v1.1
✅ Activated: Resume Parser v1.0 (Improved) v1.1
```

## Benefits of This Framework

### 🎯 **Targeted Improvements**
- Identify specific subject areas that need improvement
- Focus development efforts on weak areas
- Avoid unnecessary changes to well-performing areas

### 💰 **Cost Efficiency**
- Track API costs per prompt version
- Compare cost vs. performance improvements
- Optimize for both accuracy and cost

### 📈 **Continuous Improvement**
- Version control for prompts
- Performance tracking over time
- Data-driven prompt optimization

### 🔍 **Detailed Analysis**
- Subject area breakdown
- Specific issues identification
- Improvement suggestions

## Current Performance

Based on recent testing:

| Subject Area | Accuracy | Completeness | Quality Score | Status |
|--------------|----------|--------------|---------------|---------|
| Personal Info | 100.0% | 100.0% | 100.0% | ✅ Excellent |
| Work Experience | 100.0% | 100.0% | 100.0% | ✅ Excellent |
| Education | 75.0% | 100.0% | 87.5% | ⚠️ Needs Improvement |
| Skills | 100.0% | 100.0% | 100.0% | ✅ Excellent |
| Certifications | 100.0% | 100.0% | 100.0% | ✅ Excellent |
| Projects | 100.0% | 100.0% | 100.0% | ✅ Excellent |

**Overall Performance: 95.8% accuracy, 100% completeness**

## Next Steps

1. **Focus on Education**: The GPA extraction issue needs targeted improvement
2. **Test with Real Resumes**: Use actual user resumes for more realistic testing
3. **Expand Test Cases**: Add more diverse resume formats and content
4. **Cost Optimization**: Monitor and optimize for cost efficiency
5. **Automated Testing**: Set up automated performance monitoring

## Files in the Framework

- `test_resume_parser_performance.py` - Main performance testing tool
- `improve_resume_prompt.py` - Analysis and improvement tool
- `compare_prompt_versions.py` - Version comparison tool
- `activate_prompt.py` - Prompt version management
- `check_prompts.py` - Database prompt status checker

## Database Tables

- `PromptManagement` - Stores prompt versions and metadata
- `APIUsageTracking` - Tracks AI API usage and costs

This framework enables systematic, data-driven improvement of the resume parser while keeping costs low through targeted optimizations. 