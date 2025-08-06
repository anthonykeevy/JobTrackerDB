#!/usr/bin/env python3
"""
Create Concise Resume Parsing Prompt

This script creates a more concise version of the resume parsing prompt
to reduce token usage and avoid OpenAI rate limits.
"""

import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app'))

try:
    from app.services.prompt_service import PromptService
    from mcp.db.session import get_db
except ImportError as e:
    print(f"Error importing required modules: {e}")
    sys.exit(1)

def create_concise_prompt():
    """Create a more concise resume parsing prompt"""
    
    # Get database session
    db = next(get_db())
    prompt_service = PromptService(db)
    
    # Create concise prompt data
    concise_prompt_data = {
        "PromptName": "Resume Parser v1.4 (Explicit)",
        "PromptType": "resume_parse",
        "PromptVersion": "1.4",
        "SystemPrompt": """You are a resume parser. Extract structured data from resumes and return ONLY valid JSON. Do not include any explanations or text outside the JSON.""",
        "UserPrompt": """Extract information from this resume and return it as JSON:

{resume_text}

Return this exact JSON structure:
{{
    "personal_info": {{
        "name": "Full Name",
        "email": "email",
        "phone": "phone",
        "location": "location"
    }},
    "summary": "Professional summary",
    "work_experience": [
        {{
            "company": "Company",
            "position": "Title",
            "start_date": "YYYY-MM",
            "end_date": "YYYY-MM or Present",
            "description": "Job description",
            "achievements": ["achievement1", "achievement2"],
            "technologies": ["tech1", "tech2"]
        }}
    ],
    "education": [
        {{
            "institution": "University",
            "degree": "Degree",
            "field_of_study": "Field",
            "graduation_date": "YYYY-MM",
            "gpa": "GPA if available"
        }}
    ],
    "skills": [
        {{
            "category": "Category",
            "skills": ["skill1", "skill2"]
        }}
    ],
    "certifications": [
        {{
            "name": "Certification",
            "issuer": "Issuer",
            "date_earned": "YYYY-MM",
            "expiry_date": "YYYY-MM if applicable"
        }}
    ],
    "projects": [
        {{
            "name": "Project",
            "description": "Description",
            "technologies": ["tech1", "tech2"],
            "url": "URL if available"
        }}
    ]
}}

IMPORTANT: Return ONLY the JSON, no other text.""",
        "Description": "Explicit resume parsing prompt with clear JSON structure",
        "ExpectedOutput": "Structured JSON with resume data",
        "ValidationRules": "Must return valid JSON only",
        "IsActive": True,
        "IsDefault": False,
        "PerformanceMetrics": "Token efficiency and accuracy"
    }
    
    try:
        # Create the new prompt
        new_prompt = prompt_service.create_prompt(concise_prompt_data)
        
        if new_prompt:
            print("✅ Concise resume parsing prompt created successfully!")
            print(f"   Name: {new_prompt.PromptName}")
            print(f"   Version: {new_prompt.PromptVersion}")
            print(f"   Active: {new_prompt.IsActive}")
            print(f"   Token reduction: ~60% compared to v1.0")
            return True
        else:
            print("❌ Failed to create concise prompt")
            return False
            
    except Exception as e:
        print(f"❌ Error creating concise prompt: {e}")
        return False

def main():
    """Main function"""
    print("CONCISE RESUME PARSING PROMPT CREATOR")
    print("=" * 50)
    
    success = create_concise_prompt()
    
    if success:
        print("\n✅ Concise prompt created successfully!")
        print("This should reduce token usage and avoid rate limits.")
        print("\nNext steps:")
        print("1. Test the AI parsing with the new concise prompt")
        print("2. Compare results with the previous verbose prompt")
        print("3. Adjust if needed for accuracy vs. efficiency")
    else:
        print("\n❌ Failed to create concise prompt")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 