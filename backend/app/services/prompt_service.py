"""
Prompt Management Service

This service handles AI prompts for different operations including:
- Resume parsing
- Address validation
- Job matching
- Profile optimization
- Cover letter generation
"""

import json
import logging
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from app.models import PromptManagement

logger = logging.getLogger(__name__)

class PromptService:
    """Service for managing AI prompts"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_active_prompt(self, prompt_type: str, version: str = None) -> Optional[PromptManagement]:
        """Get the active prompt for a specific type and version"""
        try:
            query = self.db.query(PromptManagement).filter(
                PromptManagement.PromptType == prompt_type,
                PromptManagement.IsActive == True
            )
            
            if version:
                query = query.filter(PromptManagement.PromptVersion == version)
            # Remove the IsDefault filter - just get the active prompt
            
            return query.first()
        except Exception as e:
            logger.error(f"Error getting active prompt for type {prompt_type}: {e}")
            return None
    
    def get_prompt_by_name(self, prompt_name: str) -> Optional[PromptManagement]:
        """Get a prompt by its name"""
        try:
            return self.db.query(PromptManagement).filter(
                PromptManagement.PromptName == prompt_name
            ).first()
        except Exception as e:
            logger.error(f"Error getting prompt by name {prompt_name}: {e}")
            return None
    
    def activate_prompt(self, prompt_id: int) -> bool:
        """Activate a specific prompt by ID"""
        try:
            # Deactivate all prompts of the same type
            prompt = self.db.query(PromptManagement).filter(PromptManagement.PromptID == prompt_id).first()
            if not prompt:
                return False
            
            # Deactivate all prompts of the same type
            self.db.query(PromptManagement).filter(
                PromptManagement.PromptType == prompt.PromptType
            ).update({"IsActive": False})
            
            # Activate the specific prompt
            prompt.IsActive = True
            self.db.commit()
            
            logger.info(f"Activated prompt: {prompt.PromptName}")
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error activating prompt {prompt_id}: {e}")
            return False
    
    def create_prompt(self, prompt_data: Dict[str, Any]) -> Optional[PromptManagement]:
        """Create a new prompt"""
        try:
            prompt = PromptManagement(**prompt_data)
            self.db.add(prompt)
            self.db.commit()
            logger.info(f"Created new prompt: {prompt.PromptName}")
            return prompt
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating prompt: {e}")
            return None
    
    def update_prompt(self, prompt_id: int, updates: Dict[str, Any]) -> Optional[PromptManagement]:
        """Update an existing prompt"""
        try:
            prompt = self.db.query(PromptManagement).filter(PromptManagement.PromptID == prompt_id).first()
            if not prompt:
                return None
            
            for key, value in updates.items():
                if hasattr(prompt, key):
                    setattr(prompt, key, value)
            
            self.db.commit()
            logger.info(f"Updated prompt: {prompt.PromptName}")
            return prompt
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating prompt: {e}")
            return None
    
    def get_prompt_history(self, prompt_type: str) -> List[PromptManagement]:
        """Get all prompts for a specific type"""
        try:
            return self.db.query(PromptManagement).filter(
                PromptManagement.PromptType == prompt_type
            ).order_by(PromptManagement.PromptVersion.desc()).all()
        except Exception as e:
            logger.error(f"Error getting prompt history for type {prompt_type}: {e}")
            return []
    
    def initialize_default_prompts(self) -> bool:
        """Initialize default prompts for the system"""
        try:
            # Check if default prompts already exist
            existing_prompts = self.db.query(PromptManagement).count()
            if existing_prompts > 0:
                logger.info("Default prompts already exist, skipping initialization")
                return True
            
            # Resume Parsing Prompt v1.0
            resume_prompt_data = {
                "PromptName": "Resume Parser v1.0",
                "PromptType": "resume_parse",
                "PromptVersion": "1.0",
                "SystemPrompt": """You are an expert resume parser with deep knowledge of career information extraction. Your task is to analyze resumes and extract structured, accurate information that can be used to populate a professional profile database.

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

Output Format: Return valid JSON only, no additional text or explanations.""",
                "UserPrompt": """Please analyze the following resume and extract structured information with high accuracy.

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
            "gpa": "GPA if available (numeric or string)"
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
7. Include GPA only if explicitly mentioned
8. Validate and clean all extracted data""",
                "Description": "Advanced resume parsing prompt for extracting structured career information",
                "ExpectedOutput": """{
    "personal_info": {
        "name": "John Doe",
        "email": "john.doe@email.com",
        "phone": "+1-555-123-4567",
        "location": "San Francisco, CA"
    },
    "summary": "Experienced software engineer with 5+ years in full-stack development",
    "work_experience": [
        {
            "company": "Tech Corp",
            "position": "Senior Software Engineer",
            "start_date": "2022-01",
            "end_date": "Present",
            "description": "Led development of microservices architecture",
            "achievements": ["Reduced API response time by 40%", "Mentored 3 junior developers"],
            "technologies": ["Python", "React", "AWS"]
        }
    ],
    "education": [
        {
            "institution": "University of Technology",
            "degree": "Bachelor of Science",
            "field_of_study": "Computer Science",
            "graduation_date": "2019-05",
            "gpa": "3.8"
        }
    ],
    "skills": [
        {
            "category": "Technical",
            "skills": ["Python", "JavaScript", "React", "Node.js", "AWS"]
        },
        {
            "category": "Soft",
            "skills": ["Leadership", "Problem Solving", "Communication"]
        }
    ],
    "certifications": [
        {
            "name": "AWS Certified Solutions Architect",
            "issuer": "Amazon Web Services",
            "date_earned": "2023-03",
            "expiry_date": "2026-03"
        }
    ],
    "projects": [
        {
            "name": "E-commerce Platform",
            "description": "Built full-stack e-commerce solution",
            "technologies": ["React", "Node.js", "MongoDB"],
            "url": "https://github.com/johndoe/ecommerce"
        }
    ]
}""",
                "ValidationRules": """{
    "personal_info": {
        "name": {"type": "string", "required": true},
        "email": {"type": "string", "pattern": "^[^@]+@[^@]+\\.[^@]+$"},
        "phone": {"type": "string"},
        "location": {"type": "string"}
    },
    "work_experience": {
        "type": "array",
        "items": {
            "company": {"type": "string", "required": true},
            "position": {"type": "string", "required": true},
            "start_date": {"type": "string", "pattern": "^\\d{4}-\\d{2}$"},
            "end_date": {"type": "string"},
            "description": {"type": "string"},
            "achievements": {"type": "array", "items": {"type": "string"}},
            "technologies": {"type": "array", "items": {"type": "string"}}
        }
    },
    "education": {
        "type": "array",
        "items": {
            "institution": {"type": "string", "required": true},
            "degree": {"type": "string"},
            "field_of_study": {"type": "string"},
            "graduation_date": {"type": "string", "pattern": "^\\d{4}-\\d{2}$"},
            "gpa": {"type": ["string", "number"]}
        }
    }
}""",
                "IsActive": True,
                "IsDefault": True,
                "PerformanceMetrics": """{
    "extraction_accuracy": 0.95,
    "field_completeness": 0.88,
    "date_accuracy": 0.92,
    "skill_categorization": 0.90
}""",
                "createdBy": "system"
            }
            
            self.create_prompt(resume_prompt_data)
            
            logger.info("Successfully initialized default prompts")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing default prompts: {e}")
            return False 