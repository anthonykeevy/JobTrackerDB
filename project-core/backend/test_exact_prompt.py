#!/usr/bin/env python3
"""
Test Exact Prompt - Debug Empty Response Issue
"""

import os
import sys
import asyncio
import openai
import json
from pathlib import Path

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app'))

# Set up OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

async def test_exact_prompt():
    """Test with the exact same prompt structure"""
    
    try:
        # Read resume content
        resume_file_path = Path("../Resume/Anthony Keevy Resume 202506.docx")
        if not resume_file_path.exists():
            print(f"Resume file not found: {resume_file_path}")
            return False
        
        # Extract text
        import docx
        doc = docx.Document(resume_file_path)
        resume_text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        
        print(f"Resume text length: {len(resume_text)} characters")
        
        # Use the exact same prompt structure as v1.4
        system_prompt = """You are a resume parser. Extract structured data from resumes and return ONLY valid JSON. Do not include any explanations or text outside the JSON."""
        
        user_prompt = f"""Extract information from this resume and return it as JSON:

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

IMPORTANT: Return ONLY the JSON, no other text."""
        
        print(f"System prompt length: {len(system_prompt)}")
        print(f"User prompt length: {len(user_prompt)}")
        print(f"Total prompt length: {len(system_prompt) + len(user_prompt)}")
        
        # Test the exact same call
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,
            max_tokens=2000
        )
        
        content = response.choices[0].message.content
        print(f"AI Response length: {len(content)} characters")
        print(f"AI Response preview: {content[:200]}...")
        
        if len(content) == 0:
            print("❌ Empty response received!")
            return False
        
        # Try to parse as JSON
        try:
            # Try to extract JSON from the response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1]
            
            parsed_data = json.loads(content.strip())
            print("✅ Successfully parsed JSON!")
            print(f"Keys found: {list(parsed_data.keys())}")
            return True
            
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse JSON: {e}")
            print(f"Raw response: {content}")
            return False
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    print("TEST EXACT PROMPT")
    print("=" * 50)
    
    success = asyncio.run(test_exact_prompt())
    
    if success:
        print("\n✅ Test completed successfully!")
    else:
        print("\n❌ Test failed")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 