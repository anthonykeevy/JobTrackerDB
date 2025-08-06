#!/usr/bin/env python3
"""
AI Parsing Baseline Test Framework

This script tests the actual AI resume parsing process using the real resume file.
It runs the resume through the current AI prompt, extracts the results, and creates
a baseline dataset that can be manually corrected for future prompt testing.
"""

import sys
import os
import csv
import json
import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../../backend')
sys.path.insert(0, backend_path)

# Import the actual AI parsing function
try:
    from app.api.resume import parse_resume_with_ai
    from mcp.db.session import get_db
    from app.services.prompt_service import PromptService
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please ensure you're running this from the correct directory")
    sys.exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIBaselineTester:
    """Test AI parsing and create baseline dataset"""
    
    def __init__(self):
        self.resume_file_path = Path("../Resume/Anthony Keevy Resume 202506.docx")
        self.test_results_dir = Path("ai_baseline_results")
        self.test_results_dir.mkdir(exist_ok=True)
        
    async def test_ai_parsing(self) -> Dict[str, Any]:
        """Test the actual AI parsing process with the real resume file"""
        logger.info("Testing AI parsing with real resume file...")
        
        try:
            # Verify resume file exists
            if not self.resume_file_path.exists():
                raise FileNotFoundError(f"Resume file not found: {self.resume_file_path}")
            
            logger.info(f"Using resume file: {self.resume_file_path}")
            
            # Read and extract text from the resume file
            import docx
            doc = docx.Document(self.resume_file_path)
            resume_text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            
            logger.info(f"Resume text length: {len(resume_text)} characters")
            
            # Get database session
            db = next(get_db())
            
            # Test the actual AI parsing process
            logger.info("Running AI parsing...")
            ai_result = await parse_resume_with_ai(resume_text, user_id=None, db=db)
            
            logger.info("AI parsing completed successfully!")
            logger.info(f"AI extracted data structure: {list(ai_result.keys())}")
            
            return ai_result
            
        except Exception as e:
            logger.error(f"Error during AI parsing test: {e}")
            raise
    
    def save_ai_results(self, ai_result: Dict[str, Any]):
        """Save AI parsing results to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save raw AI result
        raw_filename = self.test_results_dir / f"ai_raw_result_{timestamp}.json"
        with open(raw_filename, 'w', encoding='utf-8') as f:
            json.dump(ai_result, f, indent=2)
        logger.info(f"Raw AI result saved to: {raw_filename}")
        
        # Save structured CSV files for manual review
        self._save_personal_info_csv(ai_result.get('personal_info', {}), timestamp)
        self._save_work_experience_csv(ai_result.get('work_experience', []), timestamp)
        self._save_education_csv(ai_result.get('education', []), timestamp)
        self._save_skills_csv(ai_result.get('skills', []), timestamp)
        self._save_certifications_csv(ai_result.get('certifications', []), timestamp)
        self._save_projects_csv(ai_result.get('projects', []), timestamp)
        self._save_summary_csv(ai_result.get('summary', ''), timestamp)
        
        # Create baseline template
        baseline_data = {
            "personal_info": ai_result.get('personal_info', {}),
            "summary": ai_result.get('summary', ''),
            "work_experience": ai_result.get('work_experience', []),
            "education": ai_result.get('education', []),
            "skills": ai_result.get('skills', []),
            "certifications": ai_result.get('certifications', []),
            "projects": ai_result.get('projects', [])
        }
        
        baseline_filename = self.test_results_dir / f"baseline_template_{timestamp}.json"
        with open(baseline_filename, 'w', encoding='utf-8') as f:
            json.dump(baseline_data, f, indent=2)
        logger.info(f"Baseline template saved to: {baseline_filename}")
        
        return baseline_filename
    
    def _save_personal_info_csv(self, data: Dict[str, Any], timestamp: str):
        """Save personal info to CSV"""
        filename = self.test_results_dir / f"ai_personal_info_{timestamp}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Field', 'AI_Extracted_Value', 'Manual_Correction', 'Notes'])
            for field, value in data.items():
                writer.writerow([field, value, '', ''])
        logger.info(f"Personal info CSV saved to: {filename}")
    
    def _save_work_experience_csv(self, data: List[Dict[str, Any]], timestamp: str):
        """Save work experience to CSV"""
        filename = self.test_results_dir / f"ai_work_experience_{timestamp}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Company', 'Position', 'Location', 'Start_Date', 'End_Date', 
                           'Description', 'Achievements', 'Technologies', 'AI_Extracted', 'Manual_Correction', 'Notes'])
            
            for i, exp in enumerate(data):
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
                    'AI_Extracted',  # Mark as AI extracted
                    '',  # Manual correction column
                    ''   # Notes column
                ])
        logger.info(f"Work experience CSV saved to: {filename}")
    
    def _save_education_csv(self, data: List[Dict[str, Any]], timestamp: str):
        """Save education to CSV"""
        filename = self.test_results_dir / f"ai_education_{timestamp}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Institution', 'Degree', 'Field_of_Study', 'Graduation_Date', 
                           'GPA', 'AI_Extracted', 'Manual_Correction', 'Notes'])
            
            for edu in data:
                writer.writerow([
                    edu.get('institution', ''),
                    edu.get('degree', ''),
                    edu.get('field_of_study', ''),
                    edu.get('graduation_date', ''),
                    edu.get('gpa', ''),
                    'AI_Extracted',  # Mark as AI extracted
                    '',  # Manual correction column
                    ''   # Notes column
                ])
        logger.info(f"Education CSV saved to: {filename}")
    
    def _save_skills_csv(self, data: List[Dict[str, Any]], timestamp: str):
        """Save skills to CSV"""
        filename = self.test_results_dir / f"ai_skills_{timestamp}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Category', 'Skill', 'AI_Extracted', 'Manual_Correction', 'Notes'])
            
            for skill_group in data:
                category = skill_group.get('category', '')
                for skill in skill_group.get('skills', []):
                    writer.writerow([category, skill, 'AI_Extracted', '', ''])
        logger.info(f"Skills CSV saved to: {filename}")
    
    def _save_certifications_csv(self, data: List[Dict[str, Any]], timestamp: str):
        """Save certifications to CSV"""
        filename = self.test_results_dir / f"ai_certifications_{timestamp}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Issuer', 'Date_Earned', 'Expiry_Date', 
                           'AI_Extracted', 'Manual_Correction', 'Notes'])
            
            for cert in data:
                writer.writerow([
                    cert.get('name', ''),
                    cert.get('issuer', ''),
                    cert.get('date_earned', ''),
                    cert.get('expiry_date', ''),
                    'AI_Extracted',  # Mark as AI extracted
                    '',  # Manual correction column
                    ''   # Notes column
                ])
        logger.info(f"Certifications CSV saved to: {filename}")
    
    def _save_projects_csv(self, data: List[Dict[str, Any]], timestamp: str):
        """Save projects to CSV"""
        filename = self.test_results_dir / f"ai_projects_{timestamp}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Description', 'Achievements', 'Technologies', 
                           'URL', 'AI_Extracted', 'Manual_Correction', 'Notes'])
            
            for project in data:
                achievements = '; '.join(project.get('achievements', []))
                technologies = '; '.join(project.get('technologies', []))
                writer.writerow([
                    project.get('name', ''),
                    project.get('description', ''),
                    achievements,
                    technologies,
                    project.get('url', ''),
                    'AI_Extracted',  # Mark as AI extracted
                    '',  # Manual correction column
                    ''   # Notes column
                ])
        logger.info(f"Projects CSV saved to: {filename}")
    
    def _save_summary_csv(self, summary: str, timestamp: str):
        """Save summary to CSV"""
        filename = self.test_results_dir / f"ai_summary_{timestamp}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Summary', 'AI_Extracted', 'Manual_Correction', 'Notes'])
            writer.writerow([summary, 'AI_Extracted', '', ''])
        logger.info(f"Summary CSV saved to: {filename}")
    
    def create_test_summary(self, ai_result: Dict[str, Any], baseline_file: Path):
        """Create a summary of the test results"""
        summary = {
            "test_timestamp": datetime.now().isoformat(),
            "resume_file": str(self.resume_file_path),
            "ai_extraction_summary": {
                "personal_info_fields": len(ai_result.get('personal_info', {})),
                "work_experience_entries": len(ai_result.get('work_experience', [])),
                "education_entries": len(ai_result.get('education', [])),
                "skills_categories": len(ai_result.get('skills', [])),
                "certifications_entries": len(ai_result.get('certifications', [])),
                "projects_entries": len(ai_result.get('projects', [])),
                "has_summary": bool(ai_result.get('summary', ''))
            },
            "files_created": [
                str(self.test_results_dir / "*.json"),
                str(self.test_results_dir / "*.csv")
            ],
            "next_steps": [
                "1. Review the CSV files and manually correct any errors",
                "2. Update the baseline_template.json with corrected data",
                "3. Use the corrected baseline for future prompt testing",
                "4. Run comparison tests against this baseline"
            ]
        }
        
        summary_file = self.test_results_dir / "test_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Test summary saved to: {summary_file}")
        return summary

async def main():
    """Main function"""
    print("AI PARSING BASELINE TEST FRAMEWORK")
    print("=" * 50)
    
    try:
        tester = AIBaselineTester()
        
        # Test AI parsing with real resume
        ai_result = await tester.test_ai_parsing()
        
        # Save results
        baseline_file = tester.save_ai_results(ai_result)
        
        # Create summary
        summary = tester.create_test_summary(ai_result, baseline_file)
        
        print("\nAI Parsing Test Completed Successfully!")
        print("=" * 50)
        print(f"Resume File: {tester.resume_file_path}")
        print(f"Results Directory: {tester.test_results_dir}")
        print("\nFiles Created:")
        print(f"  - Raw AI result: {tester.test_results_dir}/*.json")
        print(f"  - CSV files for manual review: {tester.test_results_dir}/*.csv")
        print(f"  - Baseline template: {baseline_file}")
        print(f"  - Test summary: {tester.test_results_dir}/test_summary.json")
        
        print("\nNEXT STEPS:")
        print("1. Review the CSV files and manually correct any AI extraction errors")
        print("2. Update the baseline_template.json with your corrected data")
        print("3. Use this corrected baseline for future prompt effectiveness testing")
        print("4. Run comparison tests to measure prompt improvements")
        
        return True
        
    except Exception as e:
        logger.error(f"Error during AI parsing test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1) 