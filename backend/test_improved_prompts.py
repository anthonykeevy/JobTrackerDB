#!/usr/bin/env python3
"""
Test Improved Prompts
Tests all improved prompts against the baseline to measure accuracy improvements.
"""

import sys
import os
import json
import pandas as pd
from pathlib import Path
from datetime import datetime

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.')
sys.path.insert(0, backend_path)

from app.services.prompt_service import PromptService
from mcp.db.session import get_db
from app.api.resume import parse_resume_with_ai

class PromptTester:
    """Test different prompts against the baseline"""
    
    def __init__(self):
        self.resume_file_path = Path("../Resume/Anthony Keevy Resume 202506.docx")
        self.baseline_file = Path("ai_baseline_results/corrected_baseline_dataset_20250806_143321.json")
        self.results_dir = Path("prompt_testing_results")
        self.results_dir.mkdir(exist_ok=True)
        
    def load_baseline(self):
        """Load the corrected baseline dataset"""
        with open(self.baseline_file, 'r') as f:
            return json.load(f)
    
    def extract_resume_text(self):
        """Extract text from the resume file"""
        import docx
        doc = docx.Document(self.resume_file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    
    async def test_prompt(self, prompt_name, db):
        """Test a specific prompt"""
        print(f"🔄 Testing prompt: {prompt_name}")
        
        try:
            # Get the prompt
            prompt_service = PromptService(db)
            prompt = prompt_service.get_prompt_by_name(prompt_name)
            
            if not prompt:
                print(f"❌ Prompt not found: {prompt_name}")
                return None
            
            # Extract resume text
            resume_text = self.extract_resume_text()
            
            # Temporarily activate this prompt
            prompt_service.activate_prompt(prompt.PromptID)
            
            # Test the prompt
            result = await parse_resume_with_ai(resume_text, user_id=None, db=db)
            
            print(f"✅ Prompt test completed: {prompt_name}")
            return result
            
        except Exception as e:
            print(f"❌ Error testing prompt {prompt_name}: {e}")
            return None
    
    def calculate_accuracy(self, ai_result, baseline):
        """Calculate accuracy for each section"""
        accuracy_scores = {}
        
        # Personal Info Accuracy
        personal_accuracy = self.calculate_personal_info_accuracy(ai_result, baseline)
        accuracy_scores['personal_info'] = personal_accuracy
        
        # Work Experience Accuracy
        work_accuracy = self.calculate_work_experience_accuracy(ai_result, baseline)
        accuracy_scores['work_experience'] = work_accuracy
        
        # Education Accuracy
        education_accuracy = self.calculate_education_accuracy(ai_result, baseline)
        accuracy_scores['education'] = education_accuracy
        
        # Skills Accuracy
        skills_accuracy = self.calculate_skills_accuracy(ai_result, baseline)
        accuracy_scores['skills'] = skills_accuracy
        
        # Certifications Accuracy
        cert_accuracy = self.calculate_certifications_accuracy(ai_result, baseline)
        accuracy_scores['certifications'] = cert_accuracy
        
        # Projects Accuracy
        projects_accuracy = self.calculate_projects_accuracy(ai_result, baseline)
        accuracy_scores['projects'] = projects_accuracy
        
        # Summary Accuracy
        summary_accuracy = self.calculate_summary_accuracy(ai_result, baseline)
        accuracy_scores['summary'] = summary_accuracy
        
        return accuracy_scores
    
    def calculate_personal_info_accuracy(self, ai_result, baseline):
        """Calculate personal info accuracy"""
        ai_personal = ai_result.get('personal_info', {})
        baseline_personal = baseline.get('personal_info', {})
        
        total_fields = len(baseline_personal)
        correct_fields = 0
        
        for field, expected_value in baseline_personal.items():
            ai_value = ai_personal.get(field, '')
            if ai_value == expected_value:
                correct_fields += 1
        
        return (correct_fields / total_fields * 100) if total_fields > 0 else 0
    
    def calculate_work_experience_accuracy(self, ai_result, baseline):
        """Calculate work experience accuracy"""
        ai_work = ai_result.get('work_experience', [])
        baseline_work = baseline.get('work_experience', [])
        
        if len(baseline_work) == 0:
            return 100 if len(ai_work) == 0 else 0
        
        total_entries = len(baseline_work)
        correct_entries = 0
        
        for i, baseline_entry in enumerate(baseline_work):
            if i < len(ai_work):
                ai_entry = ai_work[i]
                # Check key fields
                if (ai_entry.get('company') == baseline_entry.get('company') and
                    ai_entry.get('position') == baseline_entry.get('position') and
                    ai_entry.get('location') == baseline_entry.get('location')):
                    correct_entries += 1
        
        return (correct_entries / total_entries * 100) if total_entries > 0 else 0
    
    def calculate_education_accuracy(self, ai_result, baseline):
        """Calculate education accuracy"""
        ai_education = ai_result.get('education', [])
        baseline_education = baseline.get('education', [])
        
        if len(baseline_education) == 0:
            return 100 if len(ai_education) == 0 else 0
        
        total_entries = len(baseline_education)
        correct_entries = 0
        
        for i, baseline_entry in enumerate(baseline_education):
            if i < len(ai_education):
                ai_entry = ai_education[i]
                # Check key fields
                if (ai_entry.get('institution') == baseline_entry.get('institution') and
                    ai_entry.get('degree') == baseline_entry.get('degree')):
                    correct_entries += 1
        
        return (correct_entries / total_entries * 100) if total_entries > 0 else 0
    
    def calculate_skills_accuracy(self, ai_result, baseline):
        """Calculate skills accuracy"""
        ai_skills = ai_result.get('skills', [])
        baseline_skills = baseline.get('skills', [])
        
        if len(baseline_skills) == 0:
            return 100 if len(ai_skills) == 0 else 0
        
        # Count total skills in baseline
        total_baseline_skills = sum(len(category['skills']) for category in baseline_skills)
        total_ai_skills = sum(len(category['skills']) for category in ai_skills)
        
        if total_baseline_skills == 0:
            return 100 if total_ai_skills == 0 else 0
        
        # Simple accuracy based on skill count (could be enhanced with exact matching)
        accuracy = min(total_ai_skills / total_baseline_skills * 100, 100)
        return accuracy
    
    def calculate_certifications_accuracy(self, ai_result, baseline):
        """Calculate certifications accuracy"""
        ai_certs = ai_result.get('certifications', [])
        baseline_certs = baseline.get('certifications', [])
        
        if len(baseline_certs) == 0:
            return 100 if len(ai_certs) == 0 else 0
        
        total_entries = len(baseline_certs)
        correct_entries = 0
        
        for i, baseline_entry in enumerate(baseline_certs):
            if i < len(ai_certs):
                ai_entry = ai_certs[i]
                # Check key fields
                if (ai_entry.get('name') == baseline_entry.get('name') and
                    ai_entry.get('issuer') == baseline_entry.get('issuer')):
                    correct_entries += 1
        
        return (correct_entries / total_entries * 100) if total_entries > 0 else 0
    
    def calculate_projects_accuracy(self, ai_result, baseline):
        """Calculate projects accuracy"""
        ai_projects = ai_result.get('projects', [])
        baseline_projects = baseline.get('projects', [])
        
        if len(baseline_projects) == 0:
            return 100 if len(ai_projects) == 0 else 0
        
        total_entries = len(baseline_projects)
        correct_entries = 0
        
        for i, baseline_entry in enumerate(baseline_projects):
            if i < len(ai_projects):
                ai_entry = ai_projects[i]
                # Check key fields
                if ai_entry.get('name') == baseline_entry.get('name'):
                    correct_entries += 1
        
        return (correct_entries / total_entries * 100) if total_entries > 0 else 0
    
    def calculate_summary_accuracy(self, ai_result, baseline):
        """Calculate summary accuracy"""
        ai_summary = ai_result.get('summary', '')
        baseline_summary = baseline.get('summary', '')
        
        if not baseline_summary:
            return 100 if not ai_summary else 0
        
        # Simple length-based accuracy (could be enhanced with semantic similarity)
        if len(ai_summary) > 0 and len(baseline_summary) > 0:
            return min(len(ai_summary) / len(baseline_summary) * 100, 100)
        elif len(ai_summary) == 0 and len(baseline_summary) == 0:
            return 100
        else:
            return 0
    
    async def test_all_prompts(self):
        """Test all improved prompts"""
        print("🧪 Testing all improved prompts against baseline...")
        
        # Load baseline
        baseline = self.load_baseline()
        print(f"✅ Loaded baseline: {self.baseline_file.name}")
        
        # Get database session
        db = next(get_db())
        
        # Test prompts
        prompts_to_test = [
            "Resume Parser v1.4 (Explicit)",  # Current baseline
            "Resume Parser v1.5 (Enhanced Personal Info)",
            "Resume Parser v1.6 (Enhanced Work Experience)", 
            "Resume Parser v1.7 (Comprehensive Enhanced)"
        ]
        
        results = {}
        
        for prompt_name in prompts_to_test:
            print(f"\n{'='*50}")
            print(f"Testing: {prompt_name}")
            print(f"{'='*50}")
            
            result = await self.test_prompt(prompt_name, db)
            
            if result:
                accuracy_scores = self.calculate_accuracy(result, baseline)
                results[prompt_name] = {
                    'result': result,
                    'accuracy': accuracy_scores
                }
                
                print(f"\n📊 Accuracy Scores for {prompt_name}:")
                for section, score in accuracy_scores.items():
                    print(f"   {section}: {score:.1f}%")
                
                # Calculate overall accuracy
                overall_accuracy = sum(accuracy_scores.values()) / len(accuracy_scores)
                print(f"   Overall: {overall_accuracy:.1f}%")
        
        # Save results
        self.save_results(results, baseline)
        
        return results
    
    def save_results(self, results, baseline):
        """Save test results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed results
        detailed_results = {}
        for prompt_name, data in results.items():
            detailed_results[prompt_name] = {
                'accuracy_scores': data['accuracy'],
                'overall_accuracy': sum(data['accuracy'].values()) / len(data['accuracy']),
                'result': data['result']
            }
        
        # Save JSON results
        results_file = self.results_dir / f"prompt_testing_results_{timestamp}.json"
        with open(results_file, 'w') as f:
            json.dump(detailed_results, f, indent=2)
        
        # Create comparison CSV
        comparison_data = []
        for prompt_name, data in results.items():
            row = {
                'Prompt': prompt_name,
                'Overall_Accuracy': sum(data['accuracy'].values()) / len(data['accuracy'])
            }
            for section, score in data['accuracy'].items():
                row[f'{section}_accuracy'] = score
            comparison_data.append(row)
        
        comparison_df = pd.DataFrame(comparison_data)
        comparison_file = self.results_dir / f"prompt_comparison_{timestamp}.csv"
        comparison_df.to_csv(comparison_file, index=False)
        
        print(f"\n📁 Results saved:")
        print(f"   • Detailed results: {results_file}")
        print(f"   • Comparison CSV: {comparison_file}")
        
        # Print summary
        print(f"\n📊 PROMPT TESTING SUMMARY")
        print(f"{'='*50}")
        for prompt_name, data in results.items():
            overall = sum(data['accuracy'].values()) / len(data['accuracy'])
            print(f"{prompt_name}: {overall:.1f}% overall accuracy")
        
        # Find best prompt
        best_prompt = max(results.keys(), 
                         key=lambda x: sum(results[x]['accuracy'].values()) / len(results[x]['accuracy']))
        best_accuracy = sum(results[best_prompt]['accuracy'].values()) / len(results[best_prompt]['accuracy'])
        
        print(f"\n🏆 Best performing prompt: {best_prompt}")
        print(f"   Overall accuracy: {best_accuracy:.1f}%")
        
        return best_prompt, best_accuracy

async def main():
    """Run prompt testing"""
    tester = PromptTester()
    results = await tester.test_all_prompts()
    
    if results:
        print(f"\n✅ Prompt testing completed successfully!")
        print(f"📊 Tested {len(results)} prompts")
        print(f"📁 Results saved in: {tester.results_dir}")
    else:
        print(f"\n❌ Prompt testing failed")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 