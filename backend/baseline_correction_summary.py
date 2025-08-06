#!/usr/bin/env python3
"""
Baseline Correction Summary
Documents the manual baseline correction process and prepares for next testing phase.
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime

def generate_baseline_summary():
    """Generate a comprehensive summary of the baseline correction process"""
    
    print("📋 BASELINE CORRECTION SUMMARY")
    print("=" * 50)
    
    # Load the corrected baseline
    baseline_files = list(Path("ai_baseline_results").glob("corrected_baseline_dataset_*.json"))
    if not baseline_files:
        print("❌ No corrected baseline files found")
        return
    
    latest_baseline = max(baseline_files, key=lambda x: x.stat().st_mtime)
    
    with open(latest_baseline, 'r') as f:
        baseline_data = json.load(f)
    
    print(f"✅ Corrected Baseline: {latest_baseline.name}")
    print(f"📅 Generated: {datetime.fromtimestamp(latest_baseline.stat().st_mtime)}")
    print()
    
    # Personal Info Summary
    print("👤 PERSONAL INFO")
    print("-" * 20)
    personal_info = baseline_data['personal_info']
    for field, value in personal_info.items():
        print(f"   {field}: {value}")
    print()
    
    # Work Experience Summary
    print("💼 WORK EXPERIENCE")
    print("-" * 20)
    work_exp = baseline_data['work_experience']
    print(f"   Total entries: {len(work_exp)}")
    for i, exp in enumerate(work_exp, 1):
        print(f"   {i}. {exp['position']} at {exp['company']}")
        print(f"      Location: {exp.get('location', 'N/A')}")
        print(f"      Period: {exp['start_date']} - {exp['end_date']}")
        print(f"      Technologies: {', '.join(exp['technologies'])}")
        print()
    
    # Education Summary
    print("🎓 EDUCATION")
    print("-" * 20)
    education = baseline_data['education']
    print(f"   Total entries: {len(education)}")
    for i, edu in enumerate(education, 1):
        print(f"   {i}. {edu['degree']} from {edu['institution']}")
        print(f"      Graduation: {edu['graduation_date']}")
        print()
    
    # Skills Summary
    print("🛠️ SKILLS")
    print("-" * 20)
    skills = baseline_data['skills']
    categories = {}
    for skill_group in skills:
        category = skill_group['category']
        if category not in categories:
            categories[category] = []
        categories[category].extend(skill_group['skills'])
    
    total_skills = sum(len(skills) for skills in categories.values())
    print(f"   Total skills: {total_skills}")
    for category, skill_list in categories.items():
        print(f"   {category}: {len(skill_list)} skills")
    print()
    
    # Certifications Summary
    print("🏆 CERTIFICATIONS")
    print("-" * 20)
    certifications = baseline_data['certifications']
    print(f"   Total certifications: {len(certifications)}")
    for cert in certifications:
        print(f"   • {cert['name']} from {cert['issuer']}")
    print()
    
    # Projects Summary
    print("📁 PROJECTS")
    print("-" * 20)
    projects = baseline_data['projects']
    if projects:
        print(f"   Total projects: {len(projects)}")
        for project in projects:
            print(f"   • {project['name']}")
    else:
        print("   No projects listed in resume")
    print()
    
    # Summary
    print("📝 SUMMARY")
    print("-" * 20)
    summary = baseline_data['summary']
    print(f"   Length: {len(summary)} characters")
    print(f"   Preview: {summary[:100]}...")
    print()
    
    # Key Corrections Made
    print("🔧 KEY CORRECTIONS MADE")
    print("-" * 20)
    print("   1. Added location: 'Sydney, Australia'")
    print("   2. Added LinkedIn: 'https://www.linkedin.com/in/anthony-keevy-5733286/'")
    print("   3. Corrected work experience locations to country format (Australia)")
    print("   4. Verified all other extracted data as accurate")
    print("   5. Confirmed projects section is empty (correct)")
    print()
    
    # Next Steps
    print("🚀 NEXT STEPS")
    print("-" * 20)
    print("   1. Use this corrected baseline for prompt effectiveness testing")
    print("   2. Run compare_prompt_versions.py against this baseline")
    print("   3. Test new prompt versions for improvements")
    print("   4. Measure accuracy and completeness metrics")
    print("   5. Iterate on prompt engineering based on results")
    print()
    
    # File Locations
    print("📁 FILES CREATED")
    print("-" * 20)
    corrected_files = [
        "corrected_personal_info.csv",
        "corrected_work_experience.csv", 
        "corrected_education.csv",
        "corrected_skills.csv",
        "corrected_certifications.csv",
        "corrected_projects.csv",
        "corrected_summary.csv",
        latest_baseline.name
    ]
    
    for file in corrected_files:
        file_path = Path("ai_baseline_results") / file
        if file_path.exists():
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} (missing)")
    print()
    
    print("✅ Baseline correction process completed successfully!")
    print("📊 This corrected baseline is now ready for prompt effectiveness testing.")

def main():
    """Run the baseline summary"""
    if not Path("ai_baseline_results").exists():
        print("❌ Error: ai_baseline_results directory not found. Run from backend directory.")
        return
    
    generate_baseline_summary()

if __name__ == "__main__":
    main() 