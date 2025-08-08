import os
import logging
from typing import Optional, Dict, Any
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from openai import OpenAI
from mcp.db.session import get_db
from app.models import User, Profile, ProfileWorkExperience, ProfileEducation, Skills, ProfileCertification, ProfileSocialLink, GlobalLinkType, ProfileAddress
import tempfile
import docx
import PyPDF2
import io
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1",
    tags=["Resume"]
)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ResumeParseResponse(BaseModel):
    success: bool
    message: str
    extracted_data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF file"""
    try:
        pdf_file = io.BytesIO(file_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        raise HTTPException(status_code=400, detail="Failed to extract text from PDF")

def extract_text_from_docx(file_content: bytes) -> str:
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(io.BytesIO(file_content))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        logger.error(f"Error extracting text from DOCX: {e}")
        raise HTTPException(status_code=400, detail="Failed to extract text from DOCX")

def truncate_resume_content(resume_text: str, max_tokens: int = 8000) -> str:
    """
    Truncate resume content to fit within token limits.
    Prioritizes important sections like personal info, work experience, and skills.
    """
    # Rough estimation: 1 token ≈ 4 characters
    max_chars = max_tokens * 4
    
    if len(resume_text) <= max_chars:
        return resume_text
    
    # Split into sections
    lines = resume_text.split('\n')
    
    # Priority sections to keep
    priority_keywords = [
        'name', 'email', 'phone', 'linkedin',
        'summary', 'objective',
        'experience', 'work', 'career',
        'education', 'degree', 'university',
        'skills', 'technologies',
        'certifications', 'certificates',
        'projects'
    ]
    
    # Find important sections
    important_lines = []
    current_section = []
    
    for line in lines:
        line_lower = line.lower()
        
        # Check if this line contains priority keywords
        is_important = any(keyword in line_lower for keyword in priority_keywords)
        
        if is_important:
            # Add current section if it has content
            if current_section:
                important_lines.extend(current_section)
                important_lines.append('')  # Add separator
            current_section = [line]
        else:
            # Add to current section if we're in one
            if current_section:
                current_section.append(line)
    
    # Add the last section
    if current_section:
        important_lines.extend(current_section)
    
    # If we still have too much content, truncate further
    truncated_text = '\n'.join(important_lines)
    
    if len(truncated_text) > max_chars:
        # Take the first part that fits
        truncated_text = truncated_text[:max_chars]
        # Try to end at a complete line
        last_newline = truncated_text.rfind('\n')
        if last_newline > max_chars * 0.8:  # If we can find a good break point
            truncated_text = truncated_text[:last_newline]
    
    return truncated_text

async def parse_resume_with_ai(resume_text: str, user_id: int = None, db: Session = None) -> Dict[str, Any]:
    """Use OpenAI to parse resume and extract structured data using managed prompts"""
    try:
        # Truncate resume content to fit within token limits
        original_length = len(resume_text)
        resume_text = truncate_resume_content(resume_text, max_tokens=8000)
        if len(resume_text) < original_length:
            logger.info(f"Truncated resume from {original_length} to {len(resume_text)} characters")
        
        # If still too long, take only the first part
        if len(resume_text) > 6000:  # Much more conservative limit
            resume_text = resume_text[:6000]
            logger.info(f"Further truncated resume to {len(resume_text)} characters")
        
        # Get the active prompt for resume parsing
        from app.services.prompt_service import PromptService
        if db:
            prompt_service = PromptService(db)
            active_prompt = prompt_service.get_active_prompt("resume_parse")
        else:
            active_prompt = None
        
        if not active_prompt:
            logger.warning("No active prompt found for resume parsing, using fallback")
            # Fallback to basic prompt if no managed prompt is available
            system_prompt = "You are an expert at parsing resumes and extracting structured career information. Always respond with valid JSON."
            user_prompt = f"""
            Please analyze the following resume and extract structured information. 
            Return the data in JSON format with the following structure:
            {{
                "personal_info": {{
                    "name": "Full Name",
                    "email": "email@example.com",
                    "phone": "phone number",
                    "location": "city, state/country"
                }},
                "summary": "Professional summary or objective",
                "work_experience": [
                    {{
                        "company": "Company Name",
                        "position": "Job Title",
                        "start_date": "YYYY-MM",
                        "end_date": "YYYY-MM or Present",
                        "description": "Job description and achievements"
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

            Resume text:
            {resume_text}
            """
        else:
            # Use the managed prompt
            system_prompt = active_prompt.SystemPrompt
            user_prompt = active_prompt.UserPrompt.format(resume_text=resume_text)
            logger.info(f"Using managed prompt: {active_prompt.PromptName} v{active_prompt.PromptVersion}")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,
            max_tokens=4000
        )

        # Calculate costs (GPT-4 pricing as of 2024)
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        total_tokens = response.usage.total_tokens
        
        # GPT-4 pricing: $0.03 per 1K input tokens, $0.06 per 1K output tokens
        input_cost = (input_tokens / 1000) * 0.03
        output_cost = (output_tokens / 1000) * 0.06
        total_cost = input_cost + output_cost

        # Track AI usage if user_id is provided
        if user_id:
            try:
                import httpx
                async with httpx.AsyncClient() as http_client:
                    await http_client.post(
                        "http://localhost:8000/api/v1/ai/usage",
                        json={
                            "user_id": user_id,
                            "operation": "resume_parse",
                            "tokens_used": total_tokens,
                            "cost": round(total_cost, 4),
                            "model": "gpt-4"
                        }
                    )
                logger.info(f"🤖 AI Usage tracked - User: {user_id}, Tokens: {total_tokens}, Cost: ${total_cost:.4f}")
            except Exception as e:
                logger.error(f"Failed to track AI usage: {e}")

        # Parse the response
        content = response.choices[0].message.content
        import json
        try:
            # Try to extract JSON from the response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1]
            
            logger.info(f"AI Response length: {len(content)} characters")
            logger.info(f"AI Response preview: {content[:200]}...")
            
            parsed_data = json.loads(content.strip())
            return parsed_data
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            logger.error(f"AI Response: {content}")
            raise HTTPException(status_code=500, detail="Failed to parse AI response")

    except Exception as e:
        logger.error(f"Error in AI parsing: {e}")
        raise HTTPException(status_code=500, detail="Failed to parse resume with AI")

def parse_gpa_string(gpa_str: str) -> Optional[float]:
    """
    Parse GPA string and convert to numeric value.
    Handles formats like "6.2/7.0", "3.8/4.0", "85%", etc.
    """
    if not gpa_str:
        return None
    
    try:
        # Remove any extra whitespace
        gpa_str = gpa_str.strip()
        
        # Handle "X.X/Y.Y" format (e.g., "6.2/7.0")
        if "/" in gpa_str:
            parts = gpa_str.split("/")
            if len(parts) == 2:
                numerator = float(parts[0])
                denominator = float(parts[1])
                return round((numerator / denominator) * 4.0, 2)  # Convert to 4.0 scale
        
        # Handle percentage format (e.g., "85%")
        if "%" in gpa_str:
            percentage = float(gpa_str.replace("%", ""))
            return round((percentage / 100) * 4.0, 2)  # Convert to 4.0 scale
        
        # Handle direct numeric values
        gpa_value = float(gpa_str)
        if gpa_value > 4.0:  # Likely on a different scale
            return round((gpa_value / 7.0) * 4.0, 2)  # Convert from 7.0 scale to 4.0
        
        return gpa_value
        
    except (ValueError, TypeError):
        logger.warning(f"Could not parse GPA value: {gpa_str}")
        return None

def parse_date_string(date_str: str) -> Optional[datetime]:
    """Convert date string to datetime object"""
    if not date_str:
        return None
    
    # Try different date formats
    date_formats = [
        "%Y-%m-%d",  # 2020-01-15
        "%Y-%m",     # 2020-01
        "%m/%d/%Y",  # 01/15/2020
        "%d/%m/%Y",  # 15/01/2020
        "%Y",        # 2020
    ]
    
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    return None

@router.post("/resume/parse", response_model=ResumeParseResponse)
async def parse_resume(
    file: UploadFile = File(...),
    user_id: int = None,
    db: Session = Depends(get_db)
):
    """
    Parse a resume file using AI to extract structured profile information.
    
    Supports PDF, DOC, and DOCX files.
    Returns structured data that can be used to pre-populate a user's profile.
    """
    try:
        # Validate file type
        allowed_types = [
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/msword"
        ]
        
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail="Invalid file type. Only PDF, DOC, and DOCX files are supported."
            )

        # Read file content
        file_content = await file.read()
        
        # Extract text based on file type
        if file.content_type == "application/pdf":
            resume_text = extract_text_from_pdf(file_content)
        elif file.content_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
            resume_text = extract_text_from_docx(file_content)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="No text could be extracted from the file")

        # Parse with AI (now with cost tracking and managed prompts)
        extracted_data = await parse_resume_with_ai(resume_text, user_id, db)

        return ResumeParseResponse(
            success=True,
            message="Resume parsed successfully",
            extracted_data=extracted_data
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in resume parsing: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during resume parsing")

@router.post("/resume/save-to-profile")
async def save_resume_data_to_profile(
    user_id: int,
    resume_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """
    Save parsed resume data to a user's profile in the database.
    """
    try:
        # Get user and profile
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        if not profile:
            # Create profile if it doesn't exist
            profile = Profile(user_id=user_id)
            db.add(profile)
            db.flush()  # Get the profile ID

        # Update profile with extracted data
        if "personal_info" in resume_data:
            personal_info = resume_data["personal_info"]
            if "name" in personal_info:
                profile.first_name = personal_info["name"].split()[0] if personal_info["name"] else None
                profile.last_name = " ".join(personal_info["name"].split()[1:]) if len(personal_info["name"].split()) > 1 else None
            if "email" in personal_info:
                profile.email = personal_info["email"]
            if "phone" in personal_info:
                profile.phone = personal_info["phone"]

        if "summary" in resume_data:
            profile.summary = resume_data["summary"]

        # Save work experience
        if "work_experience" in resume_data:
            # This would need to be implemented with the ProfileWorkExperience model
            # For now, we'll store it as JSON in a field or create the relationships
            pass

        # Save education
        if "education" in resume_data:
            # This would need to be implemented with the ProfileEducation model
            pass

        # Save skills
        if "skills" in resume_data:
            # This would need to be implemented with the Skills model
            pass

        db.commit()

        return {
            "success": True,
            "message": "Profile updated with resume data",
            "profile_id": profile.id
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error saving resume data to profile: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to save resume data to profile") 

class SaveFirstResumeRequest(BaseModel):
    user_id: int
    resume_data: Dict[str, Any]

@router.post("/resume/save-first", response_model=ResumeParseResponse)
async def save_first_resume_to_profile(
    request: SaveFirstResumeRequest,
    db: Session = Depends(get_db)
):
    """
    Save the first resume upload directly to the user's profile in the database.
    This is used for initial profile creation from resume upload.
    """
    try:
        user_id = request.user_id
        resume_data = request.resume_data
        logger.info(f"🔍 Saving first resume data for user {user_id}")
        
        # Get user and profile
        user = db.query(User).filter(User.UserID == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        profile = db.query(Profile).filter(Profile.ProfileID == user.ProfileID).first()
        if not profile:
            # Create profile if it doesn't exist
            profile = Profile()
            db.add(profile)
            db.flush()  # Get the profile ID
            logger.info(f"✅ Created new profile for user {user_id}")

        # Update profile with extracted data
        updated_fields = []
        
        if "personal_info" in resume_data:
            personal_info = resume_data["personal_info"]
            if "name" in personal_info and personal_info["name"]:
                name_parts = personal_info["name"].split()
                profile.FirstName = name_parts[0] if name_parts else None
                profile.LastName = " ".join(name_parts[1:]) if len(name_parts) > 1 else None
                updated_fields.append("name")
            
            if "email" in personal_info and personal_info["email"]:
                profile.EmailAddress = personal_info["email"]
                updated_fields.append("email")
            
            if "phone" in personal_info and personal_info["phone"]:
                profile.PhoneNumber = personal_info["phone"]
                updated_fields.append("phone")

        if "summary" in resume_data and resume_data["summary"]:
            profile.Subtitle = resume_data["summary"]
            updated_fields.append("summary")

        # Save work experience
        if "work_experience" in resume_data and resume_data["work_experience"]:
            for exp in resume_data["work_experience"]:
                work_exp = ProfileWorkExperience(
                    ProfileID=profile.ProfileID,
                    CompanyName=exp.get("company", ""),
                    JobTitle=exp.get("position", ""),
                    StartDate=parse_date_string(exp.get("start_date")),
                    EndDate=parse_date_string(exp.get("end_date")),
                    Description=exp.get("description", ""),
                    createdBy=str(user_id)
                )
                db.add(work_exp)
            updated_fields.append(f"{len(resume_data['work_experience'])} work experiences")

        # Save education
        if "education" in resume_data and resume_data["education"]:
            for edu in resume_data["education"]:
                education = ProfileEducation(
                    ProfileID=profile.ProfileID,
                    InstitutionName=edu.get("institution", ""),
                    Degree=edu.get("degree", ""),
                    FieldOfStudy=edu.get("field_of_study", ""),
                    EndDate=parse_date_string(edu.get("graduation_date")),
                    GPA=parse_gpa_string(edu.get("gpa")),
                    createdBy=str(user_id)
                )
                db.add(education)
            updated_fields.append(f"{len(resume_data['education'])} education entries")

        # Save skills
        if "skills" in resume_data and resume_data["skills"]:
            for skill_category in resume_data["skills"]:
                category = skill_category.get("category", "General")
                for skill_name in skill_category.get("skills", []):
                    skill = Skills(
                        ProfileID=profile.ProfileID,
                        SkillName=skill_name,
                        createdBy=str(user_id)
                    )
                    db.add(skill)
            updated_fields.append("skills")

        # Save certifications
        if "certifications" in resume_data and resume_data["certifications"]:
            for cert in resume_data["certifications"]:
                certification = ProfileCertification(
                    ProfileID=profile.ProfileID,
                    CertificationName=cert.get("name", ""),
                    IssuingOrganization=cert.get("issuer", ""),
                    IssueDate=parse_date_string(cert.get("date_earned")),
                    ExpiryDate=parse_date_string(cert.get("expiry_date")),
                    createdBy=str(user_id)
                )
                db.add(certification)
            updated_fields.append(f"{len(resume_data['certifications'])} certifications")

        # Commit all changes
        db.commit()
        
        logger.info(f"✅ Successfully saved resume data for user {user_id}. Updated fields: {', '.join(updated_fields)}")
        
        return ResumeParseResponse(
            success=True,
            message=f"Resume data saved successfully. Updated: {', '.join(updated_fields)}",
            extracted_data=resume_data
        )

    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error saving resume data for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save resume data: {str(e)}") 

@router.get("/resume/load-profile/{user_id}")
async def load_user_profile_data(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Load all saved profile data for a user to populate the profile builder steps.
    """
    try:
        logger.info(f"🔍 Loading profile data for user {user_id}")
        
        # Get user and profile
        user = db.query(User).filter(User.UserID == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        profile = db.query(Profile).filter(Profile.ProfileID == user.ProfileID).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        # Load work experience
        work_experience = db.query(ProfileWorkExperience).filter(
            ProfileWorkExperience.ProfileID == profile.ProfileID
        ).all()

        # Load education
        education = db.query(ProfileEducation).filter(
            ProfileEducation.ProfileID == profile.ProfileID
        ).all()

        # Load skills
        skills = db.query(Skills).filter(
            Skills.ProfileID == profile.ProfileID
        ).all()

        # Load certifications
        certifications = db.query(ProfileCertification).filter(
            ProfileCertification.ProfileID == profile.ProfileID
        ).all()

        # Load social links
        social_links = db.query(ProfileSocialLink).filter(
            ProfileSocialLink.ProfileID == profile.ProfileID,
            ProfileSocialLink.IsActive == True
        ).all()

        # Load address data - check both new ProfileAddress and legacy fields
        profile_addresses = db.query(ProfileAddress).filter(
            ProfileAddress.ProfileID == profile.ProfileID,
            ProfileAddress.IsActive == True
        ).all()
        
        # Parse legacy address fields
        legacy_address = {
            "streetNumber": "",
            "streetName": "",
            "streetType": "",
            "unitNumber": "",
            "unitType": "",
            "suburb": profile.AddressLine2 or "",
            "state": "",
            "postcode": "",
            "country": "Australia",
            "propertyId": "",
            "latitude": None,
            "longitude": None,
            "propertyType": "",
            "landArea": None,
            "floorArea": None,
            "isValidated": False,
            "validationSource": None,
            "confidenceScore": None,
            "validationDate": "",
            "isPrimary": True,
            "addressType": "residential",
        }
        
        # Try to parse legacy AddressLine1 (format: "4 MILBURN PL")
        if profile.AddressLine1:
            address_parts = profile.AddressLine1.strip().split()
            if len(address_parts) >= 2:
                # First part is usually street number
                legacy_address["streetNumber"] = address_parts[0]
                # Last part is usually street type
                legacy_address["streetType"] = address_parts[-1]
                # Middle parts are street name
                legacy_address["streetName"] = " ".join(address_parts[1:-1])
        
        # Try to parse legacy AddressLine3 (format: "NSW 2075")
        if profile.AddressLine3:
            state_postcode_parts = profile.AddressLine3.strip().split()
            if len(state_postcode_parts) >= 2:
                legacy_address["state"] = state_postcode_parts[0]
                legacy_address["postcode"] = state_postcode_parts[1]
        
        # Use ProfileAddress if available, otherwise use parsed legacy data
        if profile_addresses:
            primary_address = next((addr for addr in profile_addresses if addr.IsPrimary), profile_addresses[0])
            address_data = {
                "streetNumber": primary_address.StreetNumber or "",
                "streetName": primary_address.StreetName or "",
                "streetType": primary_address.StreetType or "",
                "unitNumber": primary_address.UnitNumber or "",
                "unitType": primary_address.UnitType or "",
                "suburb": primary_address.Suburb or "",
                "state": primary_address.State or "",
                "postcode": primary_address.Postcode or "",
                "country": primary_address.Country or "Australia",
                "propertyId": primary_address.PropertyID or "",
                "latitude": float(primary_address.Latitude) if primary_address.Latitude else None,
                "longitude": float(primary_address.Longitude) if primary_address.Longitude else None,
                "propertyType": primary_address.PropertyType or "",
                "landArea": float(primary_address.LandArea) if primary_address.LandArea else None,
                "floorArea": float(primary_address.FloorArea) if primary_address.FloorArea else None,
                "isValidated": primary_address.IsValidated or False,
                "validationSource": primary_address.ValidationSource,
                "confidenceScore": float(primary_address.ConfidenceScore) if primary_address.ConfidenceScore else None,
                "validationDate": primary_address.ValidationDate.isoformat() if primary_address.ValidationDate else "",
                "isPrimary": primary_address.IsPrimary or True,
                "addressType": primary_address.AddressType or "residential",
            }
        else:
            address_data = legacy_address

        # Format the data for frontend
        profile_data = {
            "basic_info": {
                "firstName": profile.FirstName or "",
                "lastName": profile.LastName or "",
                "email": profile.EmailAddress or "",
                "phone": profile.PhoneNumber or "",
                "summary": profile.Subtitle or "",
                "location": profile.AddressLine1 or "",
                "dateOfBirth": profile.DateOfBirth.strftime("%Y-%m-%d") if profile.DateOfBirth else "",
                "countryOfBirth": profile.CountryOfBirth or "",
                "currentCitizenship": profile.CurrentCitizenship or "",
                "socialLinks": [
                    {
                        "id": link.ProfileSocialLinkID,
                        "name": link.LinkName,
                        "url": link.LinkURL,
                        "type": link.LinkType,
                        "icon": link.LinkIcon,
                        "isPublic": link.IsPublic
                    }
                    for link in social_links
                ],
                "address": address_data,
            },
            "work_experience": [
                {
                    "company": exp.CompanyName or "",
                    "position": exp.JobTitle or "",
                    "startDate": exp.StartDate.strftime("%Y-%m-%d") if exp.StartDate and hasattr(exp.StartDate, 'strftime') else "",
                    "endDate": exp.EndDate.strftime("%Y-%m-%d") if exp.EndDate and hasattr(exp.EndDate, 'strftime') else "",
                    "description": exp.Description or "",
                    "achievements": [],
                    "technologies": []
                }
                for exp in work_experience
            ],
            "education": [
                {
                    "institution": edu.InstitutionName or "",
                    "degree": edu.Degree or "",
                    "fieldOfStudy": edu.FieldOfStudy or "",
                    "graduationDate": edu.EndDate.strftime("%Y-%m-%d") if edu.EndDate and hasattr(edu.EndDate, 'strftime') else "",
                    "gpa": str(edu.GPA) if edu.GPA else "",
                    "certifications": []
                }
                for edu in education
            ],
            "skills": {
                "technical": [skill.SkillName for skill in skills if skill.SkillName],
                "soft": [],
                "languages": [],
                "other": []
            },
            "certifications": [
                {
                    "name": cert.CertificationName or "",
                    "issuer": cert.IssuingOrganization or "",
                    "dateEarned": cert.IssueDate.strftime("%Y-%m-%d") if cert.IssueDate and hasattr(cert.IssueDate, 'strftime') else "",
                    "expiryDate": cert.ExpiryDate.strftime("%Y-%m-%d") if cert.ExpiryDate and hasattr(cert.ExpiryDate, 'strftime') else "",
                    "credentialId": cert.CredentialID or ""
                }
                for cert in certifications
            ],
            "projects": []
        }

        logger.info(f"✅ Profile data loaded for user {user_id}")
        
        return {
            "success": True,
            "data": profile_data
        }

    except Exception as e:
        logger.error(f"❌ Error loading profile data for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to load profile data: {str(e)}") 

class ProfileUpdateRequest(BaseModel):
    user_id: int
    section: str  # 'basic_info', 'work_experience', 'education', etc.
    data: Dict[str, Any]

class AIUsageRequest(BaseModel):
    user_id: int
    operation: str  # 'resume_parse', 'address_validation', etc.
    tokens_used: int
    cost: float
    model: str

@router.post("/profile/save-section")
async def save_profile_section(
    request: ProfileUpdateRequest,
    db: Session = Depends(get_db)
):
    """
    Save a specific section of profile data.
    """
    try:
        user_id = request.user_id
        section = request.section
        data = request.data
        
        logger.info(f"🔍 Saving profile section '{section}' for user {user_id}")
        logger.info(f"📊 Data received: {data}")
        
        # Get user and profile
        user = db.query(User).filter(User.UserID == user_id).first()
        if not user:
            logger.error(f"❌ User {user_id} not found")
            raise HTTPException(status_code=404, detail="User not found")

        profile = db.query(Profile).filter(Profile.ProfileID == user.ProfileID).first()
        if not profile:
            logger.error(f"❌ Profile not found for user {user_id}")
            raise HTTPException(status_code=404, detail="Profile not found")

        logger.info(f"✅ Found profile {profile.ProfileID} for user {user_id}")
        updated_fields = []
        
        if section == "basic_info":
            # Update basic profile information
            logger.info(f"📝 Processing basic_info section for user {user_id}")
            
            if "firstName" in data:
                profile.FirstName = data["firstName"]
                updated_fields.append("firstName")
                logger.info(f"✅ Updated firstName: {data['firstName']}")
            if "lastName" in data:
                profile.LastName = data["lastName"]
                updated_fields.append("lastName")
                logger.info(f"✅ Updated lastName: {data['lastName']}")
            if "email" in data:
                profile.EmailAddress = data["email"]
                updated_fields.append("email")
                logger.info(f"✅ Updated email: {data['email']}")
            if "phone" in data:
                profile.PhoneNumber = data["phone"]
                updated_fields.append("phone")
                logger.info(f"✅ Updated phone: {data['phone']}")
            if "dateOfBirth" in data:
                parsed_date = parse_date_string(data["dateOfBirth"])
                profile.DateOfBirth = parsed_date
                updated_fields.append("dateOfBirth")
                logger.info(f"✅ Updated dateOfBirth: {data['dateOfBirth']} -> {parsed_date}")
            if "countryOfBirth" in data:
                profile.CountryOfBirth = data["countryOfBirth"]
                updated_fields.append("countryOfBirth")
                logger.info(f"✅ Updated countryOfBirth: {data['countryOfBirth']}")
            if "currentCitizenship" in data:
                profile.CurrentCitizenship = data["currentCitizenship"]
                updated_fields.append("currentCitizenship")
                logger.info(f"✅ Updated currentCitizenship: {data['currentCitizenship']}")
            
            # Handle address data - save to both legacy fields and ProfileAddress table
            if "address" in data:
                address = data["address"]
                logger.info(f"🏠 Processing address data: {address}")
                
                # Save to legacy fields for backward compatibility
                if address.get("streetName") and address.get("suburb") and address.get("state") and address.get("postcode"):
                    # Construct legacy address format
                    street_parts = []
                    if address.get("streetNumber"):
                        street_parts.append(address["streetNumber"])
                    street_parts.append(address["streetName"])
                    if address.get("streetType"):
                        street_parts.append(address["streetType"])
                    
                    profile.AddressLine1 = " ".join(street_parts)
                    profile.AddressLine2 = address.get("suburb", "")
                    profile.AddressLine3 = f"{address.get('state', '')} {address.get('postcode', '')}".strip()
                    
                    updated_fields.append("address")
                    logger.info(f"✅ Updated legacy address fields")
                    
                    # Also save to new ProfileAddress table if we have complete address data
                    if address.get('streetName') and address.get('suburb') and address.get('state') and address.get('postcode'):
                        logger.info(f"🔍 Address validation passed - creating ProfileAddress record")
                        logger.info(f"📊 Address data: streetName='{address.get('streetName')}', suburb='{address.get('suburb')}', state='{address.get('state')}', postcode='{address.get('postcode')}'")
                        
                        # Determine if this is a Geoscape API call or manual entry
                        is_geoscape_api = address.get('validationSource') == 'geoscape' and address.get('propertyId')
                        user_identifier = f"{user.Username}_{user.UserID}"
                        
                        logger.info(f"🔍 Address source: {'Geoscape API' if is_geoscape_api else 'Manual entry'}")
                        
                        # Check if PropertyID already exists for this profile
                        property_id = address.get('propertyId')
                        existing_address = None
                        
                        if property_id:
                            existing_address = db.query(ProfileAddress).filter(
                                ProfileAddress.ProfileID == profile.ProfileID,
                                ProfileAddress.PropertyID == property_id
                            ).first()
                            logger.info(f"🔍 Checking for existing PropertyID '{property_id}' for ProfileID {profile.ProfileID}")
                        
                        # Get current active address for this profile
                        current_active_address = db.query(ProfileAddress).filter(
                            ProfileAddress.ProfileID == profile.ProfileID,
                            ProfileAddress.IsActive == True
                        ).first()
                        
                        if existing_address:
                            logger.info(f"🔄 Updating existing ProfileAddress record with PropertyID '{property_id}'")
                            
                            # Determine if this is a manual edit by comparing current data with existing record
                            # Check if any address fields have been manually changed by the user
                            address_changed = (
                                existing_address.StreetNumber != address.get('streetNumber', '') or
                                existing_address.StreetName != address.get('streetName', '') or
                                existing_address.StreetType != address.get('streetType', '') or
                                existing_address.UnitNumber != address.get('unitNumber', '') or
                                existing_address.UnitType != address.get('unitType', '') or
                                existing_address.Suburb != address.get('suburb', '') or
                                existing_address.State != address.get('state', '') or
                                existing_address.Postcode != address.get('postcode', '') or
                                existing_address.Country != address.get('country', 'Australia')
                            )
                            
                            # If address fields changed, it's a manual edit by the user
                            is_manual_edit = address_changed
                            
                            logger.info(f"🔍 Address fields changed: {address_changed}")
                            if address_changed:
                                logger.info(f"🔍 Manual edit detected - user modified address fields")
                            else:
                                logger.info(f"🔍 No manual changes detected - treating as API update")
                            
                            # Update existing record - NEVER change CreatedBy/CreatedDate
                            existing_address.StreetNumber = address.get('streetNumber', '')
                            existing_address.StreetName = address.get('streetName', '')
                            existing_address.StreetType = address.get('streetType', '')
                            existing_address.UnitNumber = address.get('unitNumber', '')
                            existing_address.UnitType = address.get('unitType', '')
                            existing_address.Suburb = address.get('suburb', '')
                            existing_address.State = address.get('state', '')
                            existing_address.Postcode = address.get('postcode', '')
                            existing_address.Country = address.get('country', 'Australia')
                            existing_address.PropertyID = address.get('propertyId', '')
                            existing_address.Latitude = address.get('latitude')
                            existing_address.Longitude = address.get('longitude')
                            existing_address.PropertyType = address.get('propertyType', '')
                            existing_address.LandArea = address.get('landArea')
                            existing_address.FloorArea = address.get('floorArea')
                            existing_address.IsValidated = address.get('isValidated', False)
                            existing_address.ValidationSource = address.get('validationSource', '')
                            existing_address.ConfidenceScore = address.get('confidenceScore')
                            existing_address.ValidationDate = datetime.utcnow() if address.get('isValidated') else None
                            existing_address.IsActive = True
                            existing_address.IsPrimary = address.get('isPrimary', True)
                            existing_address.AddressType = address.get('addressType', 'residential')
                            
                            # Update audit fields together - LastUpdated and UpdatedBy
                            current_time = datetime.utcnow()
                            existing_address.lastUpdated = current_time
                            if is_manual_edit:
                                existing_address.updatedBy = user_identifier
                                logger.info(f"🔍 Manual edit - UpdatedBy: {user_identifier}")
                            else:
                                existing_address.updatedBy = "Geoscape"
                                logger.info(f"🔍 API update - UpdatedBy: Geoscape")
                            
                            # Deactivate all other addresses for this profile
                            other_addresses = db.query(ProfileAddress).filter(
                                ProfileAddress.ProfileID == profile.ProfileID,
                                ProfileAddress.ProfileAddressID != existing_address.ProfileAddressID
                            ).all()
                            
                            for other_address in other_addresses:
                                other_address.IsActive = False
                                other_address.lastUpdated = current_time
                                # When deactivating other addresses, it's always a user action
                                other_address.updatedBy = user_identifier
                                logger.info(f"🔄 Deactivated address ID {other_address.ProfileAddressID} - User action")
                            
                            logger.info(f"✅ Updated existing ProfileAddress record")
                        else:
                            logger.info(f"🆕 Creating new ProfileAddress record")
                            
                            # Deactivate all existing addresses for this profile
                            existing_addresses = db.query(ProfileAddress).filter(
                                ProfileAddress.ProfileID == profile.ProfileID
                            ).all()
                            
                            current_time = datetime.utcnow()
                            for existing_addr in existing_addresses:
                                existing_addr.IsActive = False
                                existing_addr.lastUpdated = current_time
                                # When switching to a new address, it's always a user action
                                existing_addr.updatedBy = user_identifier
                                logger.info(f"🔄 Deactivated existing address ID {existing_addr.ProfileAddressID} - User action")
                            
                            # Create new ProfileAddress record
                            profile_address = ProfileAddress(
                                ProfileID=profile.ProfileID,
                                StreetNumber=address.get('streetNumber', ''),
                                StreetName=address.get('streetName', ''),
                                StreetType=address.get('streetType', ''),
                                UnitNumber=address.get('unitNumber', ''),
                                UnitType=address.get('unitType', ''),
                                Suburb=address.get('suburb', ''),
                                State=address.get('state', ''),
                                Postcode=address.get('postcode', ''),
                                Country=address.get('country', 'Australia'),
                                PropertyID=address.get('propertyId', ''),
                                Latitude=address.get('latitude'),
                                Longitude=address.get('longitude'),
                                PropertyType=address.get('propertyType', ''),
                                LandArea=address.get('landArea'),
                                FloorArea=address.get('floorArea'),
                                IsValidated=address.get('isValidated', False),
                                ValidationSource=address.get('validationSource', ''),
                                ConfidenceScore=address.get('confidenceScore'),
                                ValidationDate=datetime.utcnow() if address.get('isValidated') else None,
                                IsActive=True,
                                IsPrimary=address.get('isPrimary', True),
                                AddressType=address.get('addressType', 'residential'),
                                # Audit fields - CreatedDate and CreatedBy set together on creation
                                createdDate=current_time,
                                createdBy="Geoscape" if is_geoscape_api else user_identifier,
                                lastUpdated=None,  # NULL for new records - no updates yet
                                updatedBy=None  # NULL for new records - no updates yet
                            )
                            
                            try:
                                db.add(profile_address)
                                logger.info(f"✅ ProfileAddress record created successfully")
                                logger.info(f"🔍 ProfileAddress object state: {profile_address}")
                                
                            except Exception as e:
                                logger.error(f"❌ Error creating ProfileAddress: {e}")
                                logger.error(f"❌ Error type: {type(e)}")
                                import traceback
                                logger.error(f"❌ Traceback: {traceback.format_exc()}")
                                raise
                    else:
                        logger.warning(f"⚠️ Address validation failed - missing required fields")
                        logger.warning(f"📊 Address data: streetName='{address.get('streetName')}', suburb='{address.get('suburb')}', state='{address.get('state')}', postcode='{address.get('postcode')}'")
            
            # Handle social links
            if "socialLinks" in data:
                # Clear existing social links
                db.query(ProfileSocialLink).filter(ProfileSocialLink.ProfileID == profile.ProfileID).delete()
                
                # Handle socialLinks as either a list or dictionary
                social_links_data = data["socialLinks"]
                if isinstance(social_links_data, dict):
                    # Convert dictionary to list format
                    social_links_list = []
                    for key, value in social_links_data.items():
                        if value:  # Only add non-empty values
                            social_links_list.append({
                                "name": key,
                                "url": value,
                                "type": "social",
                                "icon": "",
                                "isPublic": True
                            })
                    social_links_data = social_links_list
                
                # Add new social links
                for link_data in social_links_data:
                    if isinstance(link_data, dict):
                        social_link = ProfileSocialLink(
                            ProfileID=profile.ProfileID,
                            LinkName=link_data.get("name", ""),
                            LinkURL=link_data.get("url", ""),
                            LinkType=link_data.get("type", "other"),
                            LinkIcon=link_data.get("icon", ""),
                            IsApproved=True,  # Auto-approve for now
                            IsActive=True,
                            IsPublic=link_data.get("isPublic", True),
                            createdBy=str(user_id)
                        )
                        db.add(social_link)
                updated_fields.append(f"{len(social_links_data)} social links")
                logger.info(f"✅ Updated social links: {len(social_links_data)} links")

        elif section == "work_experience":
            # Clear existing work experience and add new ones
            db.query(ProfileWorkExperience).filter(ProfileWorkExperience.ProfileID == profile.ProfileID).delete()
            
            for exp in data.get("experiences", []):
                work_exp = ProfileWorkExperience(
                    ProfileID=profile.ProfileID,
                    CompanyName=exp.get("company", ""),
                    JobTitle=exp.get("position", ""),
                    StartDate=parse_date_string(exp.get("startDate")),
                    EndDate=parse_date_string(exp.get("endDate")),
                    Description=exp.get("description", ""),
                    createdBy=str(user_id)
                )
                db.add(work_exp)
            updated_fields.append(f"{len(data.get('experiences', []))} work experiences")

        elif section == "education":
            # Clear existing education and add new ones
            db.query(ProfileEducation).filter(ProfileEducation.ProfileID == profile.ProfileID).delete()
            
            for edu in data.get("institutions", []):
                education = ProfileEducation(
                    ProfileID=profile.ProfileID,
                    InstitutionName=edu.get("institution", ""),
                    Degree=edu.get("degree", ""),
                    FieldOfStudy=edu.get("fieldOfStudy", ""),
                    EndDate=parse_date_string(edu.get("graduationDate")),
                    GPA=parse_gpa_string(edu.get("gpa")),
                    createdBy=str(user_id)
                )
                db.add(education)
            updated_fields.append(f"{len(data.get('institutions', []))} education entries")

        elif section == "skills":
            # Clear existing skills and add new ones
            db.query(Skills).filter(Skills.ProfileID == profile.ProfileID).delete()
            
            for skill_type, skills_list in data.items():
                for skill_name in skills_list:
                    skill = Skills(
                        ProfileID=profile.ProfileID,
                        SkillName=skill_name,
                        Category=skill_type,
                        createdBy=str(user_id)
                    )
                    db.add(skill)
            updated_fields.append("skills")

        # Commit changes
        logger.info(f"💾 Committing database changes for user {user_id}")
        try:
            db.commit()
            logger.info(f"✅ Database commit successful")
        except Exception as e:
            logger.error(f"❌ Database commit failed: {e}")
            logger.error(f"❌ Error type: {type(e)}")
            import traceback
            logger.error(f"❌ Commit traceback: {traceback.format_exc()}")
            raise
        
        logger.info(f"✅ Successfully saved profile section '{section}' for user {user_id}. Updated: {', '.join(updated_fields)}")
        
        return {
            "success": True,
            "message": f"Profile section '{section}' saved successfully",
            "updated_fields": updated_fields
        }

    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error saving profile section '{section}' for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save profile section: {str(e)}")

@router.post("/ai/usage")
async def track_ai_usage(
    request: AIUsageRequest,
    db: Session = Depends(get_db)
):
    """
    Track AI usage and costs for billing/auditing purposes.
    """
    try:
        # Use existing APIUsageTracking table
        from app.models import APIUsageTracking
        
        # Create new usage record
        usage_record = APIUsageTracking(
            UserID=request.user_id,
            APIProvider='openai',
            APIEndpoint=f'ai/{request.operation}',
            RequestType=request.operation,  # Add the missing RequestType field
            CallCount=1,
            CreditCost=request.cost,
            ResponseTime=None,  # Could be added if needed
            RequestData=f'{{"operation": "{request.operation}", "model": "{request.model}", "tokens": {request.tokens_used}}}',
            ResponseStatus='success',
            ResponseData=f'{{"tokens_used": {request.tokens_used}, "cost": {request.cost}}}',
            BillingPeriod=datetime.now().strftime('%Y-%m'),
            IsBillable=True
        )
        
        db.add(usage_record)
        db.commit()
        
        logger.info(f"🤖 AI Usage tracked - User: {request.user_id}, Operation: {request.operation}, Tokens: {request.tokens_used}, Cost: ${request.cost}")
        
        return {
            "success": True,
            "message": "AI usage tracked successfully",
            "usage_id": usage_record.APIUsageID
        }
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error tracking AI usage: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to track AI usage: {str(e)}")

class ProfileScoreRequest(BaseModel):
    user_id: int

@router.get("/profile/score/{user_id}")
async def get_profile_completion_score(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Calculate profile completion score and gamification points.
    """
    try:
        logger.info(f"🎯 Calculating profile score for user {user_id}")
        
        # Get user and profile
        user = db.query(User).filter(User.UserID == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        profile = db.query(Profile).filter(Profile.ProfileID == user.ProfileID).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        # Calculate scores for each section
        scores = {}
        total_points = 0
        max_points = 0

        # Basic Info (25 points)
        basic_info_score = 0
        basic_info_max = 25
        if profile.FirstName and profile.LastName:
            basic_info_score += 10
        if profile.EmailAddress:
            basic_info_score += 5
        if profile.PhoneNumber:
            basic_info_score += 5
        if profile.DateOfBirth:
            basic_info_score += 5
        scores["basic_info"] = {
            "score": basic_info_score,
            "max": basic_info_max,
            "percentage": (basic_info_score / basic_info_max) * 100
        }
        total_points += basic_info_score
        max_points += basic_info_max

        # Work Experience (30 points)
        work_exp_count = db.query(ProfileWorkExperience).filter(
            ProfileWorkExperience.ProfileID == profile.ProfileID
        ).count()
        work_exp_score = min(work_exp_count * 10, 30)  # 10 points per experience, max 30
        work_exp_max = 30
        scores["work_experience"] = {
            "score": work_exp_score,
            "max": work_exp_max,
            "percentage": (work_exp_score / work_exp_max) * 100,
            "count": work_exp_count
        }
        total_points += work_exp_score
        max_points += work_exp_max

        # Education (20 points)
        education_count = db.query(ProfileEducation).filter(
            ProfileEducation.ProfileID == profile.ProfileID
        ).count()
        education_score = min(education_count * 10, 20)  # 10 points per education, max 20
        education_max = 20
        scores["education"] = {
            "score": education_score,
            "max": education_max,
            "percentage": (education_score / education_max) * 100,
            "count": education_count
        }
        total_points += education_score
        max_points += education_max

        # Skills (15 points)
        skills_count = db.query(Skills).filter(
            Skills.ProfileID == profile.ProfileID
        ).count()
        skills_score = min(skills_count * 2, 15)  # 2 points per skill, max 15
        skills_max = 15
        scores["skills"] = {
            "score": skills_score,
            "max": skills_max,
            "percentage": (skills_score / skills_max) * 100,
            "count": skills_count
        }
        total_points += skills_score
        max_points += skills_max

        # Certifications (10 points)
        cert_count = db.query(ProfileCertification).filter(
            ProfileCertification.ProfileID == profile.ProfileID
        ).count()
        cert_score = min(cert_count * 5, 10)  # 5 points per certification, max 10
        cert_max = 10
        scores["certifications"] = {
            "score": cert_score,
            "max": cert_max,
            "percentage": (cert_score / cert_max) * 100,
            "count": cert_count
        }
        total_points += cert_score
        max_points += cert_max

        # Calculate overall score
        overall_percentage = (total_points / max_points) * 100 if max_points > 0 else 0
        
        # Determine profile level
        if overall_percentage >= 90:
            level = "Expert"
            badge = "🏆"
        elif overall_percentage >= 75:
            level = "Advanced"
            badge = "🥇"
        elif overall_percentage >= 50:
            level = "Intermediate"
            badge = "🥈"
        elif overall_percentage >= 25:
            level = "Beginner"
            badge = "🥉"
        else:
            level = "New"
            badge = "🌟"

        # Generate recommendations
        recommendations = []
        if basic_info_score < basic_info_max:
            recommendations.append("Complete your basic information")
        if work_exp_score < work_exp_max:
            recommendations.append("Add more work experience")
        if education_score < education_max:
            recommendations.append("Add your education details")
        if skills_score < skills_max:
            recommendations.append("Add more skills to your profile")
        if cert_score < cert_max:
            recommendations.append("Add certifications to boost your profile")

        logger.info(f"✅ Profile score calculated for user {user_id}: {overall_percentage:.1f}% ({level})")
        
        return {
            "success": True,
            "data": {
                "overall_score": {
                    "points": total_points,
                    "max_points": max_points,
                    "percentage": overall_percentage,
                    "level": level,
                    "badge": badge
                },
                "section_scores": scores,
                "recommendations": recommendations,
                "next_milestone": get_next_milestone(overall_percentage)
            }
        }

    except Exception as e:
        logger.error(f"❌ Error calculating profile score for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to calculate profile score: {str(e)}")

def get_next_milestone(current_percentage: float) -> dict:
    """Get the next milestone to achieve"""
    milestones = [
        {"percentage": 25, "title": "Beginner", "description": "Complete basic profile"},
        {"percentage": 50, "title": "Intermediate", "description": "Add work experience"},
        {"percentage": 75, "title": "Advanced", "description": "Add skills and certifications"},
        {"percentage": 90, "title": "Expert", "description": "Complete all sections"}
    ]
    
    for milestone in milestones:
        if current_percentage < milestone["percentage"]:
            return {
                "target_percentage": milestone["percentage"],
                "points_needed": milestone["percentage"] - current_percentage,
                "title": milestone["title"],
                "description": milestone["description"]
            }
    
    return {
        "target_percentage": 100,
        "points_needed": 0,
        "title": "Perfect",
        "description": "Your profile is complete!"
    } 

@router.post("/profile/reset-score/{user_id}")
async def reset_profile_score(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Reset profile score for testing purposes.
    """
    try:
        logger.info(f"🔄 Resetting profile score for user {user_id}")
        
        # Get user and profile
        user = db.query(User).filter(User.UserID == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        profile = db.query(Profile).filter(Profile.ProfileID == user.ProfileID).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")

        # Clear all profile data
        db.query(ProfileWorkExperience).filter(ProfileWorkExperience.ProfileID == profile.ProfileID).delete()
        db.query(ProfileEducation).filter(ProfileEducation.ProfileID == profile.ProfileID).delete()
        db.query(Skills).filter(Skills.ProfileID == profile.ProfileID).delete()
        db.query(ProfileCertification).filter(ProfileCertification.ProfileID == profile.ProfileID).delete()
        
        # Reset basic profile info
        profile.FirstName = ""
        profile.LastName = ""
        profile.EmailAddress = ""
        profile.PhoneNumber = ""
        profile.Subtitle = ""
        profile.DateOfBirth = ""
        profile.Nationality = ""
        
        db.commit()
        
        logger.info(f"✅ Profile score reset for user {user_id}")
        
        return {
            "success": True,
            "message": "Profile score reset successfully"
        }

    except Exception as e:
        logger.error(f"❌ Error resetting profile score for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to reset profile score: {str(e)}") 

@router.get("/profile/social-links/{user_id}")
async def get_user_social_links(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get all social links for a user"""
    try:
        user = db.query(User).filter(User.UserID == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        profile = db.query(Profile).filter(Profile.ProfileID == user.ProfileID).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        social_links = db.query(ProfileSocialLink).filter(
            ProfileSocialLink.ProfileID == profile.ProfileID,
            ProfileSocialLink.IsActive == True
        ).all()
        
        return {
            "success": True,
            "data": [
                {
                    "id": link.ProfileSocialLinkID,
                    "name": link.LinkName,
                    "url": link.LinkURL,
                    "type": link.LinkType,
                    "icon": link.LinkIcon,
                    "isPublic": link.IsPublic,
                    "isApproved": link.IsApproved
                }
                for link in social_links
            ]
        }
    except Exception as e:
        logger.error(f"❌ Error getting social links for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get social links: {str(e)}")

@router.get("/profile/global-link-types")
async def get_global_link_types(
    db: Session = Depends(get_db)
):
    """Get all available global link types for users to select from"""
    try:
        link_types = db.query(GlobalLinkType).filter(
            GlobalLinkType.IsActive == True
        ).order_by(GlobalLinkType.DisplayOrder).all()
        
        return {
            "success": True,
            "data": [
                {
                    "id": link_type.GlobalLinkTypeID,
                    "name": link_type.LinkName,
                    "type": link_type.LinkType,
                    "icon": link_type.LinkIcon,
                    "displayOrder": link_type.DisplayOrder
                }
                for link_type in link_types
            ]
        }
    except Exception as e:
        logger.error(f"❌ Error getting global link types: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get global link types: {str(e)}")

@router.post("/profile/social-link")
async def add_social_link(
    user_id: int,
    link_name: str,
    link_url: str,
    link_type: str = "other",
    link_icon: str = "",
    is_public: bool = True,
    db: Session = Depends(get_db)
):
    """Add a new social link for a user"""
    try:
        user = db.query(User).filter(User.UserID == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        profile = db.query(Profile).filter(Profile.ProfileID == user.ProfileID).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        # Check if this is a custom link type (not in global types)
        global_link = db.query(GlobalLinkType).filter(
            GlobalLinkType.LinkName == link_name,
            GlobalLinkType.IsActive == True
        ).first()
        
        is_approved = global_link is not None  # Auto-approve if it's a global type
        
        social_link = ProfileSocialLink(
            ProfileID=profile.ProfileID,
            LinkName=link_name,
            LinkURL=link_url,
            LinkType=link_type,
            LinkIcon=link_icon,
            IsApproved=is_approved,
            IsActive=True,
            IsPublic=is_public,
            createdBy=str(user_id)
        )
        
        db.add(social_link)
        db.commit()
        
        logger.info(f"✅ Added social link for user {user_id}: {link_name} - {link_url}")
        
        return {
            "success": True,
            "message": f"Social link '{link_name}' added successfully",
            "data": {
                "id": social_link.ProfileSocialLinkID,
                "name": social_link.LinkName,
                "url": social_link.LinkURL,
                "type": social_link.LinkType,
                "icon": social_link.LinkIcon,
                "isPublic": social_link.IsPublic,
                "isApproved": social_link.IsApproved
            }
        }
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error adding social link for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to add social link: {str(e)}")

@router.delete("/profile/social-link/{link_id}")
async def delete_social_link(
    link_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Delete a social link for a user"""
    try:
        # Verify the link belongs to the user
        user = db.query(User).filter(User.UserID == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        profile = db.query(Profile).filter(Profile.ProfileID == user.ProfileID).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        social_link = db.query(ProfileSocialLink).filter(
            ProfileSocialLink.ProfileSocialLinkID == link_id,
            ProfileSocialLink.ProfileID == profile.ProfileID
        ).first()
        
        if not social_link:
            raise HTTPException(status_code=404, detail="Social link not found")
        
        db.delete(social_link)
        db.commit()
        
        logger.info(f"✅ Deleted social link {link_id} for user {user_id}")
        
        return {
            "success": True,
            "message": "Social link deleted successfully"
        }
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error deleting social link {link_id} for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete social link: {str(e)}") 