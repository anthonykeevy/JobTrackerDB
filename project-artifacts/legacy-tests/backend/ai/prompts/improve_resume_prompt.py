#!/usr/bin/env python3
"""
Improve Resume Parsing Prompt

This script creates an improved version of the resume parsing prompt that addresses:
1. GPA format handling issues
2. Better date parsing
3. More robust extraction
4. Improved accuracy for education section
"""

import sys
import os
import logging
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp.db.session import get_db
from app.services.prompt_service import PromptService
from app.models import PromptManagement

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_improved_prompt():
    """Create an improved resume parsing prompt"""
    
    improved_system_prompt = """You are an expert resume parser with deep knowledge of career information extraction. Your task is to analyze resumes and extract structured, accurate information that can be used to populate a professional profile database.

Key Responsibilities:
1. Extract personal information (name, contact details, location)
2. Identify professional summary/objective
3. Parse work experience with accurate dates, titles, companies, and achievements
4. Extract education details including institutions, degrees, fields of study, and GPA
5. Identify skills and categorize them appropriately
6. Find certifications and their details
7. Extract project information when available

Data Quality Requirements:
- Always use ISO date format (YYYY-MM) when possible
- Normalize company names and job titles
- Extract specific achievements and responsibilities
- Categorize skills as Technical, Soft, Languages, or Other
- Validate email addresses and phone numbers
- Handle missing or unclear information gracefully
- Preserve GPA format exactly as written (e.g., "6.2/7.0", "3.8/4.0", "85%")
- Extract field of study when available

Output Format: Return valid JSON only, no additional text or explanations.

For education, extract GPA values exactly as written, including scale if mentioned. Do not convert or normalize GPA values."""

    improved_user_prompt = """Please analyze the following resume and extract structured information with high accuracy.

RESUME TEXT:
{resume_text}

EXTRACT THE FOLLOWING INFORMATION IN JSON FORMAT:

{{
    "personal_info": {{
        "name": "Full Name (as it appears on resume)",
        "email": "email@example.com (if present)",
        "phone": "phone number (if present)",
        "location": "city, state/country (if present)"
    }},
    "summary": "Professional summary or objective statement",
    "work_experience": [
        {{
            "company": "Company Name",
            "position": "Job Title",
            "start_date": "YYYY-MM",
            "end_date": "YYYY-MM or Present",
            "description": "Detailed job description and key achievements",
            "achievements": ["achievement1", "achievement2"],
            "technologies": ["tech1", "tech2"] (if mentioned)
        }}
    ],
    "education": [
        {{
            "institution": "University/College Name",
            "degree": "Degree Name (e.g., Bachelor of Science)",
            "field_of_study": "Field of Study (e.g., Computer Science)",
            "graduation_date": "YYYY-MM",
            "gpa": "GPA if available (preserve exact format: 6.2/7.0, 3.8/4.0, 85%, etc.)"
        }}
    ],
    "skills": [
        {{
            "category": "Technical|Soft|Languages|Other",
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

IMPORTANT GUIDELINES:
1. Extract only information that is explicitly stated in the resume
2. Use "Present" for current positions with no end date
3. If information is unclear or missing, use null or empty string
4. Normalize dates to YYYY-MM format when possible
5. Categorize skills appropriately (Technical for programming languages, tools, etc.)
6. Extract specific achievements and responsibilities from work experience
7. Include GPA only if explicitly mentioned - preserve exact format (6.2/7.0, 3.8/4.0, 85%, etc.)
8. Validate and clean all extracted data
9. Extract field of study when available in education section
10. Handle various GPA formats: "6.2/7.0", "3.8/4.0", "85%", "3.5 GPA", etc.

Extract education details including institution, degree, field of study, graduation date, and GPA if available. Preserve GPA format exactly as written."""

    return {
        "PromptName": "Resume Parser v1.2 (Enhanced)",
        "PromptType": "resume_parse",
        "PromptVersion": "1.2",
        "SystemPrompt": improved_system_prompt,
        "UserPrompt": improved_user_prompt,
        "Description": "Enhanced resume parsing prompt with improved GPA handling and better education extraction",
        "ExpectedOutput": """{
    "personal_info": {
        "name": "string",
        "email": "string",
        "phone": "string", 
        "location": "string"
    },
    "summary": "string",
    "work_experience": [
        {
            "company": "string",
            "position": "string",
            "start_date": "YYYY-MM",
            "end_date": "YYYY-MM or Present",
            "description": "string",
            "achievements": ["string"],
            "technologies": ["string"]
        }
    ],
    "education": [
        {
            "institution": "string",
            "degree": "string",
            "field_of_study": "string",
            "graduation_date": "YYYY-MM",
            "gpa": "string (exact format preserved)"
        }
    ],
    "skills": [
        {
            "category": "Technical|Soft|Languages|Other",
            "skills": ["string"]
        }
    ],
    "certifications": [
        {
            "name": "string",
            "issuer": "string",
            "date_earned": "YYYY-MM",
            "expiry_date": "YYYY-MM or null"
        }
    ],
    "projects": [
        {
            "name": "string",
            "description": "string",
            "technologies": ["string"],
            "url": "string or null"
        }
    ]
}""",
        "ValidationRules": """{
    "required_fields": ["personal_info.name"],
    "date_formats": ["YYYY-MM"],
    "gpa_formats": ["6.2/7.0", "3.8/4.0", "85%", "3.5 GPA", "3.5/4.0"],
    "skill_categories": ["Technical", "Soft", "Languages", "Other"]
}""",
        "IsActive": True,
        "IsDefault": False,
        "PerformanceMetrics": """{
    "target_accuracy": 95.0,
    "target_completeness": 100.0,
    "focus_areas": ["education.gpa_format", "education.field_of_study", "work_experience.achievements"]
}""",
        "createdBy": "system_improvement"
    }

def main():
    """Create improved prompt version"""
    try:
        logger.info("🚀 Creating improved resume parsing prompt...")
        
        db = next(get_db())
        prompt_service = PromptService(db)
        
        # Deactivate current active prompt
        current_active = prompt_service.get_active_prompt("resume_parse")
        if current_active:
            current_active.IsActive = False
            db.commit()
            logger.info(f"Deactivated current active prompt: {current_active.PromptName}")
        
        # Create improved prompt
        improved_prompt_data = create_improved_prompt()
        new_prompt = prompt_service.create_prompt(improved_prompt_data)
        
        if new_prompt:
            logger.info(f"✅ Successfully created improved prompt: {new_prompt.PromptName} v{new_prompt.PromptVersion}")
            logger.info("📊 Key improvements:")
            logger.info("   - Enhanced GPA format handling")
            logger.info("   - Better field of study extraction")
            logger.info("   - Improved education accuracy")
            logger.info("   - More robust date parsing")
        else:
            logger.error("❌ Failed to create improved prompt")
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"❌ Error creating improved prompt: {e}")
        return False
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 