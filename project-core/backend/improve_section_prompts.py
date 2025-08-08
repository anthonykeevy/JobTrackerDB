#!/usr/bin/env python3
"""
Improve Section Prompts
Creates improved prompts for sections that didn't achieve 100% accuracy in the baseline.
"""

import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.')
sys.path.insert(0, backend_path)

from app.services.prompt_service import PromptService
from mcp.db.session import get_db

def create_improved_personal_info_prompt():
    """Create an improved prompt specifically for personal information extraction"""
    
    db = next(get_db())
    prompt_service = PromptService(db)
    
    improved_prompt_data = {
        "PromptName": "Resume Parser v1.5 (Enhanced Personal Info)",
        "PromptType": "resume_parse",
        "PromptVersion": "1.5",
        "SystemPrompt": """You are a resume parser specializing in personal information extraction. Extract ALL personal details including location and social media profiles. Always return valid JSON only.""",
        "UserPrompt": """Extract personal information from this resume and return it as JSON:

{resume_text}

Return this exact JSON structure with ALL available personal information:
{{
    "personal_info": {{
        "name": "Full Name",
        "email": "email@example.com", 
        "phone": "phone number",
        "location": "city, state/country (extract from resume or infer from context)",
        "linkedin": "full LinkedIn URL if available",
        "website": "personal website if available",
        "github": "GitHub profile if available"
    }},
    "summary": "Professional summary",
    "work_experience": [
        {{
            "company": "Company Name",
            "position": "Job Title", 
            "location": "city, state/country (NOT department/division)",
            "start_date": "YYYY-MM",
            "end_date": "YYYY-MM or Present",
            "description": "Job description",
            "achievements": ["achievement1", "achievement2"],
            "technologies": ["tech1", "tech2"]
        }}
    ],
    "education": [
        {{
            "institution": "University/College Name",
            "degree": "Degree Name",
            "field_of_study": "Field of Study",
            "graduation_date": "YYYY-MM",
            "gpa": "GPA if available"
        }}
    ],
    "skills": [
        {{
            "category": "Technical/Soft/Other",
            "skills": ["skill1", "skill2", "skill3"]
        }}
    ],
    "certifications": [
        {{
            "name": "Certification Name",
            "issuer": "Issuing Organization",
            "date_earned": "YYYY-MM",
            "expiry_date": "YYYY-MM if applicable"
        }}
    ],
    "projects": [
        {{
            "name": "Project Name",
            "description": "Project description",
            "technologies": ["tech1", "tech2"],
            "url": "project URL if available"
        }}
    ]
}}

CRITICAL INSTRUCTIONS:
1. ALWAYS extract location from resume or infer from context (company locations, etc.)
2. ALWAYS look for LinkedIn and other social media profiles
3. For work experience locations, use city/state/country format, NOT department names
4. If location is not explicitly stated, infer from company context (e.g., "Inchcape Australia" = Australia)
5. Return ONLY valid JSON, no other text.""",
        "Description": "Enhanced personal information extraction with location and social media focus",
        "ExpectedOutput": "Complete personal information including location and social profiles",
        "ValidationRules": "Must extract location and social profiles if available",
        "IsActive": False,  # Don't activate yet, we'll test first
        "IsDefault": False,
        "PerformanceMetrics": "Personal info accuracy and completeness"
    }
    
    try:
        prompt_service.create_prompt(improved_prompt_data)
        print("✅ Enhanced Personal Info prompt created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating enhanced personal info prompt: {e}")
        return False

def create_improved_work_experience_prompt():
    """Create an improved prompt specifically for work experience location extraction"""
    
    db = next(get_db())
    prompt_service = PromptService(db)
    
    improved_prompt_data = {
        "PromptName": "Resume Parser v1.6 (Enhanced Work Experience)",
        "PromptType": "resume_parse",
        "PromptVersion": "1.6",
        "SystemPrompt": """You are a resume parser specializing in work experience extraction with accurate location identification. Extract work experience with proper location formatting.""",
        "UserPrompt": """Extract work experience from this resume and return it as JSON:

{resume_text}

Return this exact JSON structure with proper location formatting:
{{
    "personal_info": {{
        "name": "Full Name",
        "email": "email@example.com",
        "phone": "phone number", 
        "location": "city, state/country",
        "linkedin": "full LinkedIn URL if available"
    }},
    "summary": "Professional summary",
    "work_experience": [
        {{
            "company": "Company Name",
            "position": "Job Title",
            "location": "city, state/country (NOT department/division/team)",
            "start_date": "YYYY-MM",
            "end_date": "YYYY-MM or Present",
            "description": "Job description",
            "achievements": ["achievement1", "achievement2"],
            "technologies": ["tech1", "tech2"]
        }}
    ],
    "education": [
        {{
            "institution": "University/College Name",
            "degree": "Degree Name",
            "field_of_study": "Field of Study",
            "graduation_date": "YYYY-MM",
            "gpa": "GPA if available"
        }}
    ],
    "skills": [
        {{
            "category": "Technical/Soft/Other",
            "skills": ["skill1", "skill2", "skill3"]
        }}
    ],
    "certifications": [
        {{
            "name": "Certification Name",
            "issuer": "Issuing Organization",
            "date_earned": "YYYY-MM",
            "expiry_date": "YYYY-MM if applicable"
        }}
    ],
    "projects": [
        {{
            "name": "Project Name",
            "description": "Project description",
            "technologies": ["tech1", "tech2"],
            "url": "project URL if available"
        }}
    ]
}}

CRITICAL LOCATION INSTRUCTIONS:
1. Work experience location should be city/state/country format
2. DO NOT use department names, team names, or division names as location
3. If company name contains location (e.g., "Inchcape Australia"), extract the location part
4. If no explicit location, infer from company context or resume content
5. Examples of correct locations: "Sydney, Australia", "Melbourne, Australia", "Australia"
6. Examples of incorrect locations: "Data Team", "IT Department", "Global Division"
7. Return ONLY valid JSON, no other text.""",
        "Description": "Enhanced work experience extraction with proper location formatting",
        "ExpectedOutput": "Work experience with accurate location data",
        "ValidationRules": "Must use proper location format (city/state/country)",
        "IsActive": False,  # Don't activate yet, we'll test first
        "IsDefault": False,
        "PerformanceMetrics": "Work experience location accuracy"
    }
    
    try:
        prompt_service.create_prompt(improved_prompt_data)
        print("✅ Enhanced Work Experience prompt created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating enhanced work experience prompt: {e}")
        return False

def create_comprehensive_improved_prompt():
    """Create a comprehensive improved prompt addressing all accuracy issues"""
    
    db = next(get_db())
    prompt_service = PromptService(db)
    
    comprehensive_prompt_data = {
        "PromptName": "Resume Parser v1.7 (Comprehensive Enhanced)",
        "PromptType": "resume_parse",
        "PromptVersion": "1.7",
        "SystemPrompt": """You are an expert resume parser that extracts ALL available information with 100% accuracy. Pay special attention to personal details, locations, and social profiles.""",
        "UserPrompt": """Extract ALL information from this resume with maximum accuracy:

{resume_text}

Return this exact JSON structure with COMPLETE information:
{{
    "personal_info": {{
        "name": "Full Name",
        "email": "email@example.com",
        "phone": "phone number",
        "location": "city, state/country (extract or infer from context)",
        "linkedin": "full LinkedIn URL if available",
        "website": "personal website if available",
        "github": "GitHub profile if available"
    }},
    "summary": "Professional summary",
    "work_experience": [
        {{
            "company": "Company Name",
            "position": "Job Title",
            "location": "city, state/country (NOT department/division)",
            "start_date": "YYYY-MM",
            "end_date": "YYYY-MM or Present",
            "description": "Job description",
            "achievements": ["achievement1", "achievement2"],
            "technologies": ["tech1", "tech2"]
        }}
    ],
    "education": [
        {{
            "institution": "University/College Name",
            "degree": "Degree Name",
            "field_of_study": "Field of Study",
            "graduation_date": "YYYY-MM",
            "gpa": "GPA if available"
        }}
    ],
    "skills": [
        {{
            "category": "Technical/Soft/Other",
            "skills": ["skill1", "skill2", "skill3"]
        }}
    ],
    "certifications": [
        {{
            "name": "Certification Name",
            "issuer": "Issuing Organization",
            "date_earned": "YYYY-MM",
            "expiry_date": "YYYY-MM if applicable"
        }}
    ],
    "projects": [
        {{
            "name": "Project Name",
            "description": "Project description",
            "technologies": ["tech1", "tech2"],
            "url": "project URL if available"
        }}
    ]
}}

CRITICAL ACCURACY REQUIREMENTS:
1. PERSONAL INFO: Extract ALL available personal details including location and social profiles
2. LOCATION EXTRACTION: 
   - Personal location: Extract from resume or infer from context
   - Work locations: Use city/state/country format, NOT department names
   - If company name contains location (e.g., "Inchcape Australia"), extract location
3. SOCIAL PROFILES: Look for LinkedIn, GitHub, personal websites
4. COMPLETENESS: Extract every available piece of information
5. ACCURACY: Ensure all extracted data matches the resume exactly
6. Return ONLY valid JSON, no other text.""",
        "Description": "Comprehensive enhanced prompt addressing all accuracy issues",
        "ExpectedOutput": "Complete resume data with 100% accuracy",
        "ValidationRules": "Must achieve 100% accuracy for all sections",
        "IsActive": False,  # Don't activate yet, we'll test first
        "IsDefault": False,
        "PerformanceMetrics": "Overall accuracy and completeness"
    }
    
    try:
        prompt_service.create_prompt(comprehensive_prompt_data)
        print("✅ Comprehensive Enhanced prompt created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating comprehensive enhanced prompt: {e}")
        return False

def main():
    """Create improved prompts for sections with accuracy issues"""
    print("🔧 Creating improved prompts for sections with accuracy issues...")
    
    try:
        # Create improved prompts
        personal_success = create_improved_personal_info_prompt()
        work_success = create_improved_work_experience_prompt()
        comprehensive_success = create_comprehensive_improved_prompt()
        
        if personal_success and work_success and comprehensive_success:
            print("\n✅ All improved prompts created successfully!")
            print("\n📋 Created prompts:")
            print("   • Resume Parser v1.5 (Enhanced Personal Info)")
            print("   • Resume Parser v1.6 (Enhanced Work Experience)")
            print("   • Resume Parser v1.7 (Comprehensive Enhanced)")
            print("\n🚀 Next steps:")
            print("   1. Test these prompts against the baseline")
            print("   2. Compare accuracy improvements")
            print("   3. Select the best performing prompt")
            print("   4. Test different models with the selected prompt")
        else:
            print("\n❌ Some prompts failed to create")
            
    except Exception as e:
        print(f"❌ Error in main: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 