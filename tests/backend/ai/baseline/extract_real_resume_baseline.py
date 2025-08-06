#!/usr/bin/env python3
"""
Extract Real Resume Baseline Data

This script extracts all information from the actual resume file
'Resume/Anthony Keevy Resume 202506.docx' and saves it to CSV files
for each subject area. This creates a real baseline for testing prompt effectiveness.
"""

import sys
import os
import csv
import json
import logging
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../../backend'))

# Import docx for reading Word documents
try:
    from docx import Document
except ImportError:
    print("Error: python-docx not installed. Please run: pip install python-docx")
    sys.exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealResumeBaselineExtractor:
    """Extract baseline data from actual resume file"""
    
    def __init__(self):
        self.resume_file_path = Path("../../../../Resume/Anthony Keevy Resume 202506.docx")
        self.resume_content = self.read_resume_file()
        
    def read_resume_file(self) -> str:
        """Read the actual resume file"""
        try:
            if not self.resume_file_path.exists():
                raise FileNotFoundError(f"Resume file not found: {self.resume_file_path}")
            
            doc = Document(self.resume_file_path)
            content = []
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    content.append(paragraph.text)
            
            resume_text = '\n'.join(content)
            logger.info(f"Successfully read resume file: {self.resume_file_path}")
            logger.info(f"Resume content length: {len(resume_text)} characters")
            
            return resume_text
            
        except Exception as e:
            logger.error(f"Error reading resume file: {e}")
            raise
    
    def extract_personal_info(self) -> Dict[str, Any]:
        """Extract personal information from actual resume"""
        # This will need to be manually extracted and verified
        # For now, we'll create a template structure
        return {
            "name": "ANTHONY KEEVY",  # To be verified from actual resume
            "email": "",  # To be extracted from actual resume
            "phone": "",  # To be extracted from actual resume
            "location": "",  # To be extracted from actual resume
            "linkedin": ""  # To be extracted from actual resume
        }
    
    def extract_work_experience(self) -> List[Dict[str, Any]]:
        """Extract work experience from actual resume"""
        # This will need to be manually extracted and verified
        return [
            # To be populated from actual resume content
        ]
    
    def extract_education(self) -> List[Dict[str, Any]]:
        """Extract education from actual resume"""
        # This will need to be manually extracted and verified
        return [
            # To be populated from actual resume content
        ]
    
    def extract_skills(self) -> List[Dict[str, Any]]:
        """Extract skills from actual resume"""
        # This will need to be manually extracted and verified
        return [
            # To be populated from actual resume content
        ]
    
    def extract_certifications(self) -> List[Dict[str, Any]]:
        """Extract certifications from actual resume"""
        # This will need to be manually extracted and verified
        return [
            # To be populated from actual resume content
        ]
    
    def extract_projects(self) -> List[Dict[str, Any]]:
        """Extract projects from actual resume"""
        # This will need to be manually extracted and verified
        return [
            # To be populated from actual resume content
        ]
    
    def extract_summary(self) -> str:
        """Extract professional summary from actual resume"""
        # This will need to be manually extracted and verified
        return ""  # To be extracted from actual resume
    
    def save_personal_info_csv(self, data: Dict[str, Any]):
        """Save personal info to CSV"""
        filename = "real_baseline_personal_info.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Field', 'Value', 'Notes'])
            for field, value in data.items():
                writer.writerow([field, value, ''])
        logger.info(f"Personal info saved to {filename}")
    
    def save_work_experience_csv(self, data: List[Dict[str, Any]]):
        """Save work experience to CSV"""
        filename = "real_baseline_work_experience.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Company', 'Position', 'Location', 'Start Date', 'End Date', 'Description', 'Achievements', 'Technologies', 'Notes'])
            
            for exp in data:
                achievements = '; '.join(exp.get('achievements', []))
                technologies = '; '.join(exp.get('technologies', []))
                writer.writerow([
                    exp.get('company', ''),
                    exp.get('position', ''),
                    exp.get('location', ''),
                    exp.get('start_date', ''),
                    exp.get('end_date', ''),
                    exp.get('description', ''),
                    achievements,
                    technologies,
                    ''
                ])
        logger.info(f"Work experience saved to {filename}")
    
    def save_education_csv(self, data: List[Dict[str, Any]]):
        """Save education to CSV"""
        filename = "real_baseline_education.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Institution', 'Degree', 'Field of Study', 'Graduation Date', 'GPA', 'Notes'])
            
            for edu in data:
                writer.writerow([
                    edu.get('institution', ''),
                    edu.get('degree', ''),
                    edu.get('field_of_study', ''),
                    edu.get('graduation_date', ''),
                    edu.get('gpa', ''),
                    ''
                ])
        logger.info(f"Education saved to {filename}")
    
    def save_skills_csv(self, data: List[Dict[str, Any]]):
        """Save skills to CSV"""
        filename = "real_baseline_skills.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Category', 'Skill', 'Notes'])
            
            for skill_group in data:
                category = skill_group.get('category', '')
                for skill in skill_group.get('skills', []):
                    writer.writerow([category, skill, ''])
        logger.info(f"Skills saved to {filename}")
    
    def save_certifications_csv(self, data: List[Dict[str, Any]]):
        """Save certifications to CSV"""
        filename = "real_baseline_certifications.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Issuer', 'Date Earned', 'Expiry Date', 'Notes'])
            
            for cert in data:
                writer.writerow([
                    cert.get('name', ''),
                    cert.get('issuer', ''),
                    cert.get('date_earned', ''),
                    cert.get('expiry_date', ''),
                    ''
                ])
        logger.info(f"Certifications saved to {filename}")
    
    def save_projects_csv(self, data: List[Dict[str, Any]]):
        """Save projects to CSV"""
        filename = "real_baseline_projects.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Description', 'Achievements', 'Technologies', 'URL', 'Notes'])
            
            for project in data:
                achievements = '; '.join(project.get('achievements', []))
                technologies = '; '.join(project.get('technologies', []))
                writer.writerow([
                    project.get('name', ''),
                    project.get('description', ''),
                    achievements,
                    technologies,
                    project.get('url', ''),
                    ''
                ])
        logger.info(f"Projects saved to {filename}")
    
    def save_summary_csv(self, summary: str):
        """Save summary to CSV"""
        filename = "real_baseline_summary.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Summary', 'Notes'])
            writer.writerow([summary, ''])
        logger.info(f"Summary saved to {filename}")
    
    def save_resume_content(self):
        """Save the raw resume content"""
        filename = "real_baseline_resume_content.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.resume_content)
        logger.info(f"Resume content saved to {filename}")
    
    def create_baseline_dataset(self):
        """Create comprehensive baseline dataset from actual resume"""
        logger.info("Creating baseline dataset from actual resume file...")
        
        # Save the raw resume content first
        self.save_resume_content()
        
        # Extract all data (these will be empty templates for manual population)
        personal_info = self.extract_personal_info()
        work_experience = self.extract_work_experience()
        education = self.extract_education()
        skills = self.extract_skills()
        certifications = self.extract_certifications()
        projects = self.extract_projects()
        summary = self.extract_summary()
        
        # Save to CSV files
        self.save_personal_info_csv(personal_info)
        self.save_work_experience_csv(work_experience)
        self.save_education_csv(education)
        self.save_skills_csv(skills)
        self.save_certifications_csv(certifications)
        self.save_projects_csv(projects)
        self.save_summary_csv(summary)
        
        # Create JSON baseline for easy comparison
        baseline_data = {
            "personal_info": personal_info,
            "summary": summary,
            "work_experience": work_experience,
            "education": education,
            "skills": skills,
            "certifications": certifications,
            "projects": projects
        }
        
        filename = "real_baseline_dataset.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(baseline_data, f, indent=2)
        logger.info(f"Baseline dataset saved to {filename}")
        
        # Print summary
        logger.info("\nREAL BASELINE DATASET SUMMARY:")
        logger.info(f"  Source File: {self.resume_file_path}")
        logger.info(f"  Resume Content Length: {len(self.resume_content)} characters")
        logger.info(f"  Personal Info: {len(personal_info)} fields (to be populated)")
        logger.info(f"  Work Experience: {len(work_experience)} entries (to be populated)")
        logger.info(f"  Education: {len(education)} entries (to be populated)")
        logger.info(f"  Skills: {sum(len(group.get('skills', [])) for group in skills)} skills (to be populated)")
        logger.info(f"  Certifications: {len(certifications)} entries (to be populated)")
        logger.info(f"  Projects: {len(projects)} entries (to be populated)")
        
        logger.info("\nNEXT STEPS:")
        logger.info("1. Review the real_baseline_resume_content.txt file")
        logger.info("2. Manually populate the CSV files with actual data from your resume")
        logger.info("3. Update the real_baseline_dataset.json with the corrected data")
        logger.info("4. Use the corrected baseline for prompt testing")
        
        return baseline_data

def main():
    """Main function"""
    print("REAL RESUME BASELINE DATA EXTRACTOR")
    print("=" * 50)
    
    try:
        extractor = RealResumeBaselineExtractor()
        baseline_data = extractor.create_baseline_dataset()
        
        print("\nReal baseline dataset created successfully!")
        print("Files created:")
        print("  - real_baseline_resume_content.txt (actual resume content)")
        print("  - real_baseline_personal_info.csv (template for manual population)")
        print("  - real_baseline_work_experience.csv (template for manual population)")
        print("  - real_baseline_education.csv (template for manual population)")
        print("  - real_baseline_skills.csv (template for manual population)")
        print("  - real_baseline_certifications.csv (template for manual population)")
        print("  - real_baseline_projects.csv (template for manual population)")
        print("  - real_baseline_summary.csv (template for manual population)")
        print("  - real_baseline_dataset.json (template for manual population)")
        
        print("\nIMPORTANT: Please manually populate the CSV files with actual data from your resume!")
        
        return True
        
    except Exception as e:
        logger.error(f"Error creating real baseline dataset: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 