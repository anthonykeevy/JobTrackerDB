#!/usr/bin/env python3
"""
Prompt Effectiveness Comparison Tool

This script compares different prompt versions against a corrected baseline
to measure how effective each prompt is at extracting resume information.
"""

import sys
import os
import json
import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Tuple
from pathlib import Path
from dataclasses import dataclass, asdict

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../../backend'))

# Import the actual AI parsing function
try:
    from app.api.resume import parse_resume_with_ai
    from app.database import get_db
    from app.services.prompt_service import PromptService
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please ensure you're running this from the correct directory")
    sys.exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SubjectAreaMetrics:
    """Metrics for a specific subject area"""
    area: str
    total_fields: int
    correctly_extracted: int
    partially_extracted: int
    missing_fields: int
    accuracy_percentage: float
    completeness_percentage: float

@dataclass
class PromptTestResult:
    """Results of testing a specific prompt"""
    prompt_version: str
    test_timestamp: str
    resume_file: str
    baseline_file: str
    subject_areas: List[SubjectAreaMetrics]
    overall_accuracy: float
    overall_completeness: float
    total_cost: float
    token_usage: Dict[str, int]

class PromptEffectivenessTester:
    """Test and compare prompt effectiveness"""
    
    def __init__(self):
        self.resume_file_path = Path("../Resume/Anthony Keevy Resume 202506.docx")
        self.results_dir = Path("prompt_comparison_results")
        self.results_dir.mkdir(exist_ok=True)
        
    def load_baseline(self, baseline_file: str) -> Dict[str, Any]:
        """Load the corrected baseline data"""
        baseline_path = Path(baseline_file)
        if not baseline_path.exists():
            raise FileNotFoundError(f"Baseline file not found: {baseline_path}")
        
        with open(baseline_path, 'r', encoding='utf-8') as f:
            baseline = json.load(f)
        
        logger.info(f"Loaded baseline from: {baseline_path}")
        return baseline
    
    async def test_prompt_version(self, prompt_version: str, baseline: Dict[str, Any]) -> PromptTestResult:
        """Test a specific prompt version against the baseline"""
        logger.info(f"Testing prompt version: {prompt_version}")
        
        try:
            # Read the resume file
            with open(self.resume_file_path, 'rb') as f:
                resume_content = f.read()
            
            # Get database session
            db = next(get_db())
            
            # Run AI parsing
            ai_result = await parse_resume_with_ai(resume_content, db)
            
            # Compare with baseline
            subject_areas = self._compare_with_baseline(ai_result, baseline)
            
            # Calculate overall metrics
            total_fields = sum(area.total_fields for area in subject_areas)
            total_correct = sum(area.correctly_extracted for area in subject_areas)
            total_complete = sum(area.correctly_extracted + area.partially_extracted for area in subject_areas)
            
            overall_accuracy = (total_correct / total_fields * 100) if total_fields > 0 else 0
            overall_completeness = (total_complete / total_fields * 100) if total_fields > 0 else 0
            
            # Create result
            result = PromptTestResult(
                prompt_version=prompt_version,
                test_timestamp=datetime.now().isoformat(),
                resume_file=str(self.resume_file_path),
                baseline_file="baseline_template.json",  # This should be the corrected baseline
                subject_areas=subject_areas,
                overall_accuracy=overall_accuracy,
                overall_completeness=overall_completeness,
                total_cost=0.0,  # Would need to track from AI call
                token_usage={}  # Would need to track from AI call
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error testing prompt version {prompt_version}: {e}")
            raise
    
    def _compare_with_baseline(self, ai_result: Dict[str, Any], baseline: Dict[str, Any]) -> List[SubjectAreaMetrics]:
        """Compare AI result with baseline for each subject area"""
        subject_areas = []
        
        # Personal Info
        personal_metrics = self._compare_personal_info(
            ai_result.get('personal_info', {}),
            baseline.get('personal_info', {})
        )
        subject_areas.append(personal_metrics)
        
        # Work Experience
        work_metrics = self._compare_work_experience(
            ai_result.get('work_experience', []),
            baseline.get('work_experience', [])
        )
        subject_areas.append(work_metrics)
        
        # Education
        education_metrics = self._compare_education(
            ai_result.get('education', []),
            baseline.get('education', [])
        )
        subject_areas.append(education_metrics)
        
        # Skills
        skills_metrics = self._compare_skills(
            ai_result.get('skills', []),
            baseline.get('skills', [])
        )
        subject_areas.append(skills_metrics)
        
        # Certifications
        cert_metrics = self._compare_certifications(
            ai_result.get('certifications', []),
            baseline.get('certifications', [])
        )
        subject_areas.append(cert_metrics)
        
        # Projects
        project_metrics = self._compare_projects(
            ai_result.get('projects', []),
            baseline.get('projects', [])
        )
        subject_areas.append(project_metrics)
        
        # Summary
        summary_metrics = self._compare_summary(
            ai_result.get('summary', ''),
            baseline.get('summary', '')
        )
        subject_areas.append(summary_metrics)
        
        return subject_areas
    
    def _compare_personal_info(self, ai_data: Dict[str, Any], baseline_data: Dict[str, Any]) -> SubjectAreaMetrics:
        """Compare personal info extraction"""
        total_fields = len(baseline_data)
        correctly_extracted = 0
        partially_extracted = 0
        
        for field, expected_value in baseline_data.items():
            ai_value = ai_data.get(field, '')
            if ai_value == expected_value:
                correctly_extracted += 1
            elif ai_value and expected_value:  # Both have some value
                partially_extracted += 1
        
        missing_fields = total_fields - correctly_extracted - partially_extracted
        accuracy = (correctly_extracted / total_fields * 100) if total_fields > 0 else 0
        completeness = ((correctly_extracted + partially_extracted) / total_fields * 100) if total_fields > 0 else 0
        
        return SubjectAreaMetrics(
            area="Personal Info",
            total_fields=total_fields,
            correctly_extracted=correctly_extracted,
            partially_extracted=partially_extracted,
            missing_fields=missing_fields,
            accuracy_percentage=accuracy,
            completeness_percentage=completeness
        )
    
    def _compare_work_experience(self, ai_data: List[Dict[str, Any]], baseline_data: List[Dict[str, Any]]) -> SubjectAreaMetrics:
        """Compare work experience extraction"""
        total_entries = len(baseline_data)
        correctly_extracted = 0
        partially_extracted = 0
        
        for baseline_entry in baseline_data:
            # Find matching AI entry (by company/position)
            matching_ai_entry = None
            for ai_entry in ai_data:
                if (ai_entry.get('company', '').lower() == baseline_entry.get('company', '').lower() and
                    ai_entry.get('position', '').lower() == baseline_entry.get('position', '').lower()):
                    matching_ai_entry = ai_entry
                    break
            
            if matching_ai_entry:
                # Compare key fields
                key_fields = ['company', 'position', 'location', 'start_date', 'end_date', 'description']
                correct_fields = sum(1 for field in key_fields 
                                  if matching_ai_entry.get(field, '') == baseline_entry.get(field, ''))
                
                if correct_fields == len(key_fields):
                    correctly_extracted += 1
                elif correct_fields > 0:
                    partially_extracted += 1
        
        missing_entries = total_entries - correctly_extracted - partially_extracted
        accuracy = (correctly_extracted / total_entries * 100) if total_entries > 0 else 0
        completeness = ((correctly_extracted + partially_extracted) / total_entries * 100) if total_entries > 0 else 0
        
        return SubjectAreaMetrics(
            area="Work Experience",
            total_fields=total_entries,
            correctly_extracted=correctly_extracted,
            partially_extracted=partially_extracted,
            missing_fields=missing_entries,
            accuracy_percentage=accuracy,
            completeness_percentage=completeness
        )
    
    def _compare_education(self, ai_data: List[Dict[str, Any]], baseline_data: List[Dict[str, Any]]) -> SubjectAreaMetrics:
        """Compare education extraction"""
        total_entries = len(baseline_data)
        correctly_extracted = 0
        partially_extracted = 0
        
        for baseline_entry in baseline_data:
            # Find matching AI entry (by institution/degree)
            matching_ai_entry = None
            for ai_entry in ai_data:
                if (ai_entry.get('institution', '').lower() == baseline_entry.get('institution', '').lower() and
                    ai_entry.get('degree', '').lower() == baseline_entry.get('degree', '').lower()):
                    matching_ai_entry = ai_entry
                    break
            
            if matching_ai_entry:
                # Compare key fields
                key_fields = ['institution', 'degree', 'field_of_study', 'graduation_date', 'gpa']
                correct_fields = sum(1 for field in key_fields 
                                  if matching_ai_entry.get(field, '') == baseline_entry.get(field, ''))
                
                if correct_fields == len(key_fields):
                    correctly_extracted += 1
                elif correct_fields > 0:
                    partially_extracted += 1
        
        missing_entries = total_entries - correctly_extracted - partially_extracted
        accuracy = (correctly_extracted / total_entries * 100) if total_entries > 0 else 0
        completeness = ((correctly_extracted + partially_extracted) / total_entries * 100) if total_entries > 0 else 0
        
        return SubjectAreaMetrics(
            area="Education",
            total_fields=total_entries,
            correctly_extracted=correctly_extracted,
            partially_extracted=partially_extracted,
            missing_fields=missing_entries,
            accuracy_percentage=accuracy,
            completeness_percentage=completeness
        )
    
    def _compare_skills(self, ai_data: List[Dict[str, Any]], baseline_data: List[Dict[str, Any]]) -> SubjectAreaMetrics:
        """Compare skills extraction"""
        total_skills = sum(len(group.get('skills', [])) for group in baseline_data)
        correctly_extracted = 0
        partially_extracted = 0
        
        for baseline_group in baseline_data:
            baseline_category = baseline_group.get('category', '')
            baseline_skills = set(skill.lower() for skill in baseline_group.get('skills', []))
            
            # Find matching AI group
            matching_ai_group = None
            for ai_group in ai_data:
                if ai_group.get('category', '').lower() == baseline_category.lower():
                    matching_ai_group = ai_group
                    break
            
            if matching_ai_group:
                ai_skills = set(skill.lower() for skill in matching_ai_group.get('skills', []))
                correct_skills = len(baseline_skills.intersection(ai_skills))
                
                if correct_skills == len(baseline_skills):
                    correctly_extracted += len(baseline_skills)
                elif correct_skills > 0:
                    partially_extracted += correct_skills
        
        missing_skills = total_skills - correctly_extracted - partially_extracted
        accuracy = (correctly_extracted / total_skills * 100) if total_skills > 0 else 0
        completeness = ((correctly_extracted + partially_extracted) / total_skills * 100) if total_skills > 0 else 0
        
        return SubjectAreaMetrics(
            area="Skills",
            total_fields=total_skills,
            correctly_extracted=correctly_extracted,
            partially_extracted=partially_extracted,
            missing_fields=missing_skills,
            accuracy_percentage=accuracy,
            completeness_percentage=completeness
        )
    
    def _compare_certifications(self, ai_data: List[Dict[str, Any]], baseline_data: List[Dict[str, Any]]) -> SubjectAreaMetrics:
        """Compare certifications extraction"""
        total_entries = len(baseline_data)
        correctly_extracted = 0
        partially_extracted = 0
        
        for baseline_entry in baseline_data:
            # Find matching AI entry (by name)
            matching_ai_entry = None
            for ai_entry in ai_data:
                if ai_entry.get('name', '').lower() == baseline_entry.get('name', '').lower():
                    matching_ai_entry = ai_entry
                    break
            
            if matching_ai_entry:
                # Compare key fields
                key_fields = ['name', 'issuer', 'date_earned', 'expiry_date']
                correct_fields = sum(1 for field in key_fields 
                                  if matching_ai_entry.get(field, '') == baseline_entry.get(field, ''))
                
                if correct_fields == len(key_fields):
                    correctly_extracted += 1
                elif correct_fields > 0:
                    partially_extracted += 1
        
        missing_entries = total_entries - correctly_extracted - partially_extracted
        accuracy = (correctly_extracted / total_entries * 100) if total_entries > 0 else 0
        completeness = ((correctly_extracted + partially_extracted) / total_entries * 100) if total_entries > 0 else 0
        
        return SubjectAreaMetrics(
            area="Certifications",
            total_fields=total_entries,
            correctly_extracted=correctly_extracted,
            partially_extracted=partially_extracted,
            missing_fields=missing_entries,
            accuracy_percentage=accuracy,
            completeness_percentage=completeness
        )
    
    def _compare_projects(self, ai_data: List[Dict[str, Any]], baseline_data: List[Dict[str, Any]]) -> SubjectAreaMetrics:
        """Compare projects extraction"""
        total_entries = len(baseline_data)
        correctly_extracted = 0
        partially_extracted = 0
        
        for baseline_entry in baseline_data:
            # Find matching AI entry (by name)
            matching_ai_entry = None
            for ai_entry in ai_data:
                if ai_entry.get('name', '').lower() == baseline_entry.get('name', '').lower():
                    matching_ai_entry = ai_entry
                    break
            
            if matching_ai_entry:
                # Compare key fields
                key_fields = ['name', 'description', 'technologies', 'url']
                correct_fields = sum(1 for field in key_fields 
                                  if matching_ai_entry.get(field, '') == baseline_entry.get(field, ''))
                
                if correct_fields == len(key_fields):
                    correctly_extracted += 1
                elif correct_fields > 0:
                    partially_extracted += 1
        
        missing_entries = total_entries - correctly_extracted - partially_extracted
        accuracy = (correctly_extracted / total_entries * 100) if total_entries > 0 else 0
        completeness = ((correctly_extracted + partially_extracted) / total_entries * 100) if total_entries > 0 else 0
        
        return SubjectAreaMetrics(
            area="Projects",
            total_fields=total_entries,
            correctly_extracted=correctly_extracted,
            partially_extracted=partially_extracted,
            missing_fields=missing_entries,
            accuracy_percentage=accuracy,
            completeness_percentage=completeness
        )
    
    def _compare_summary(self, ai_data: str, baseline_data: str) -> SubjectAreaMetrics:
        """Compare summary extraction"""
        # Simple text similarity for summary
        ai_words = set(ai_data.lower().split())
        baseline_words = set(baseline_data.lower().split())
        
        total_words = len(baseline_words)
        common_words = len(ai_words.intersection(baseline_words))
        
        accuracy = (common_words / total_words * 100) if total_words > 0 else 0
        completeness = accuracy  # For summary, accuracy and completeness are the same
        
        return SubjectAreaMetrics(
            area="Summary",
            total_fields=total_words,
            correctly_extracted=common_words,
            partially_extracted=0,
            missing_fields=total_words - common_words,
            accuracy_percentage=accuracy,
            completeness_percentage=completeness
        )
    
    def save_comparison_results(self, results: List[PromptTestResult]):
        """Save comparison results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed results
        results_filename = self.results_dir / f"prompt_comparison_{timestamp}.json"
        with open(results_filename, 'w', encoding='utf-8') as f:
            json.dump([asdict(result) for result in results], f, indent=2)
        
        # Create summary report
        summary_filename = self.results_dir / f"comparison_summary_{timestamp}.txt"
        with open(summary_filename, 'w', encoding='utf-8') as f:
            f.write("PROMPT EFFECTIVENESS COMPARISON SUMMARY\n")
            f.write("=" * 50 + "\n\n")
            
            for result in results:
                f.write(f"Prompt Version: {result.prompt_version}\n")
                f.write(f"Overall Accuracy: {result.overall_accuracy:.2f}%\n")
                f.write(f"Overall Completeness: {result.overall_completeness:.2f}%\n")
                f.write("\nSubject Area Breakdown:\n")
                
                for area in result.subject_areas:
                    f.write(f"  {area.area}: {area.accuracy_percentage:.2f}% accuracy, {area.completeness_percentage:.2f}% completeness\n")
                
                f.write("\n" + "-" * 30 + "\n\n")
        
        logger.info(f"Comparison results saved to: {results_filename}")
        logger.info(f"Summary report saved to: {summary_filename}")
        
        return results_filename, summary_filename

async def main():
    """Main function"""
    print("PROMPT EFFECTIVENESS COMPARISON TOOL")
    print("=" * 50)
    
    try:
        tester = PromptEffectivenessTester()
        
        # Load the corrected baseline (you'll need to provide this)
        baseline_file = input("Enter the path to your corrected baseline file: ").strip()
        baseline = tester.load_baseline(baseline_file)
        
        # Test current prompt version
        current_result = await tester.test_prompt_version("Current", baseline)
        
        # Save results
        results = [current_result]
        results_file, summary_file = tester.save_comparison_results(results)
        
        print("\nPrompt Effectiveness Test Completed!")
        print("=" * 50)
        print(f"Results saved to: {results_file}")
        print(f"Summary saved to: {summary_file}")
        print(f"\nCurrent Prompt Performance:")
        print(f"  Overall Accuracy: {current_result.overall_accuracy:.2f}%")
        print(f"  Overall Completeness: {current_result.overall_completeness:.2f}%")
        
        return True
        
    except Exception as e:
        logger.error(f"Error during prompt comparison: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1) 