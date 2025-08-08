#!/usr/bin/env python3
"""
Test Baseline Usage

This script demonstrates how to use the real baseline dataset
for testing AI prompt effectiveness.
"""

import sys
import os
import json
from pathlib import Path

def load_baseline(baseline_file: str) -> dict:
    """Load the baseline dataset"""
    with open(baseline_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def test_baseline_structure(baseline_data: dict):
    """Test the structure of the baseline data"""
    print("BASELINE STRUCTURE TEST")
    print("=" * 50)
    
    # Check personal info
    personal_info = baseline_data.get('personal_info', {})
    print(f"Personal Info: {len(personal_info)} fields")
    for field, value in personal_info.items():
        print(f"  {field}: {value}")
    
    # Check work experience
    work_experience = baseline_data.get('work_experience', [])
    print(f"\nWork Experience: {len(work_experience)} entries")
    for i, exp in enumerate(work_experience[:3]):  # Show first 3
        print(f"  {i+1}. {exp.get('position', '')} at {exp.get('company', '')}")
    
    # Check education
    education = baseline_data.get('education', [])
    print(f"\nEducation: {len(education)} entries")
    for edu in education:
        print(f"  - {edu.get('degree', '')} from {edu.get('institution', '')}")
    
    # Check skills
    skills = baseline_data.get('skills', [])
    total_skills = sum(len(group.get('skills', [])) for group in skills)
    print(f"\nSkills: {total_skills} skills in {len(skills)} categories")
    for group in skills:
        category = group.get('category', '')
        skill_count = len(group.get('skills', []))
        print(f"  - {category}: {skill_count} skills")
    
    # Check certifications
    certifications = baseline_data.get('certifications', [])
    print(f"\nCertifications: {len(certifications)} entries")
    for cert in certifications:
        print(f"  - {cert.get('name', '')} ({cert.get('issuer', '')})")
    
    # Check projects
    projects = baseline_data.get('projects', [])
    print(f"\nProjects: {len(projects)} entries")
    for project in projects:
        print(f"  - {project.get('name', '')}")
    
    # Check summary
    summary = baseline_data.get('summary', '')
    print(f"\nSummary: {len(summary)} characters")
    print(f"  Preview: {summary[:100]}...")

def demonstrate_comparison_logic(baseline_data: dict):
    """Demonstrate how comparison logic would work"""
    print("\n\nCOMPARISON LOGIC DEMONSTRATION")
    print("=" * 50)
    
    # Simulate AI extraction result (this would come from actual AI parsing)
    ai_result = {
        "personal_info": {
            "name": "Anthony Keevy",  # Correct
            "email": "anthonykeevy@gmail.com",  # Correct
            "phone": "0414785260",  # Correct
            "location": "Australia",  # Correct
            "linkedin": "LinkedIn"  # Correct
        },
        "work_experience": [
            {
                "company": "Inchcape Global",
                "position": "Data Lead and Product Manager",
                "location": "Digital Parts",
                "start_date": "Nov 2022",
                "end_date": "May 2025",
                "description": "Defined and led the enterprise data vision...",
                "achievements": [
                    "Reduced product categorization effort by 80% through the design and deployment of a machine learning classification model"
                ],
                "technologies": ["SAP Commerce Cloud", "Machine Learning", "Data Pipelines"]
            }
        ],
        "education": [
            {
                "institution": "UNSW",
                "degree": "Accounting",
                "field_of_study": "Accounting",
                "graduation_date": "2004",
                "gpa": ""
            }
        ],
        "skills": [
            {
                "category": "Strategic Leadership & Management",
                "skills": ["Team Leadership", "Project Management", "Agile", "Waterfall"]
            }
        ],
        "certifications": [
            {
                "name": "T-SQL05 Writing & Queries in SQL Server 2005",
                "issuer": "New Horizons",
                "date_earned": "2008",
                "expiry_date": ""
            }
        ],
        "projects": [
            {
                "name": "Machine Learning Classification Model",
                "description": "Designed and deployed a machine learning classification model for product categorization",
                "achievements": [
                    "Reduced product categorization effort by 80%",
                    "Improved accuracy and reduced manual intervention"
                ],
                "technologies": ["Machine Learning", "Python", "Data Science"],
                "url": ""
            }
        ],
        "summary": "Results-driven Data & Product Lead with extensive experience spearheading strategic IT transformation..."
    }
    
    # Calculate accuracy for personal info
    baseline_personal = baseline_data.get('personal_info', {})
    ai_personal = ai_result.get('personal_info', {})
    
    correct_fields = 0
    total_fields = len(baseline_personal)
    
    for field, expected_value in baseline_personal.items():
        ai_value = ai_personal.get(field, '')
        if ai_value == expected_value:
            correct_fields += 1
    
    personal_accuracy = (correct_fields / total_fields * 100) if total_fields > 0 else 0
    
    print(f"Personal Info Accuracy: {personal_accuracy:.2f}%")
    print(f"  Correct: {correct_fields}/{total_fields} fields")
    
    # Calculate accuracy for work experience
    baseline_work = baseline_data.get('work_experience', [])
    ai_work = ai_result.get('work_experience', [])
    
    print(f"\nWork Experience: {len(ai_work)} extracted vs {len(baseline_work)} expected")
    
    # Calculate accuracy for skills
    baseline_skills = baseline_data.get('skills', [])
    ai_skills = ai_result.get('skills', [])
    
    total_baseline_skills = sum(len(group.get('skills', [])) for group in baseline_skills)
    total_ai_skills = sum(len(group.get('skills', [])) for group in ai_skills)
    
    print(f"Skills: {total_ai_skills} extracted vs {total_baseline_skills} expected")
    
    # Overall assessment
    print(f"\nOVERALL ASSESSMENT:")
    print(f"  Personal Info: {personal_accuracy:.2f}% accuracy")
    print(f"  Work Experience: {len(ai_work)}/{len(baseline_work)} entries extracted")
    print(f"  Skills: {total_ai_skills}/{total_baseline_skills} skills extracted")
    print(f"  Education: {len(ai_result.get('education', []))}/{len(baseline_data.get('education', []))} entries")
    print(f"  Certifications: {len(ai_result.get('certifications', []))}/{len(baseline_data.get('certifications', []))} entries")
    print(f"  Projects: {len(ai_result.get('projects', []))}/{len(baseline_data.get('projects', []))} entries")

def main():
    """Main function"""
    print("BASELINE USAGE TEST")
    print("=" * 50)
    
    try:
        # Find the most recent baseline file
        baseline_dir = Path("real_baseline_results")
        if not baseline_dir.exists():
            print("Error: Baseline results directory not found. Please run create_real_baseline.py first.")
            return False
        
        baseline_files = list(baseline_dir.glob("real_baseline_dataset_*.json"))
        if not baseline_files:
            print("Error: No baseline dataset files found. Please run create_real_baseline.py first.")
            return False
        
        # Use the most recent baseline file
        latest_baseline = max(baseline_files, key=lambda x: x.stat().st_mtime)
        print(f"Using baseline file: {latest_baseline}")
        
        # Load baseline data
        baseline_data = load_baseline(latest_baseline)
        
        # Test baseline structure
        test_baseline_structure(baseline_data)
        
        # Demonstrate comparison logic
        demonstrate_comparison_logic(baseline_data)
        
        print("\n\nNEXT STEPS:")
        print("1. Use this baseline with the AI parsing test framework")
        print("2. Run actual AI parsing against your resume")
        print("3. Compare AI results against this baseline")
        print("4. Measure accuracy and completeness by subject area")
        print("5. Iterate on prompts to improve extraction quality")
        
        return True
        
    except Exception as e:
        print(f"Error testing baseline usage: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 