#!/usr/bin/env python3
"""
Test Different Models
Tests different OpenAI models with the best-performing prompt to find the most cost-effective model.
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

class ModelTester:
    """Test different models with the best prompt"""
    
    def __init__(self):
        self.resume_file_path = Path("../Resume/Anthony Keevy Resume 202506.docx")
        self.baseline_file = Path("ai_baseline_results/corrected_baseline_dataset_20250806_143321.json")
        self.results_dir = Path("model_testing_results")
        self.results_dir.mkdir(exist_ok=True)
        self.best_prompt_name = "Resume Parser v1.5 (Enhanced Personal Info)"
        
    def load_baseline(self):
        """Load the corrected baseline dataset"""
        with open(self.baseline_file, 'r') as f:
            return json.load(f)
    
    def extract_resume_text(self):
        """Extract text from the resume file"""
        import docx
        doc = docx.Document(self.resume_file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    
    async def test_model(self, model_name, db):
        """Test a specific model with the best prompt"""
        print(f"🔄 Testing model: {model_name}")
        
        try:
            # Get the best prompt
            prompt_service = PromptService(db)
            prompt = prompt_service.get_prompt_by_name(self.best_prompt_name)
            
            if not prompt:
                print(f"❌ Best prompt not found: {self.best_prompt_name}")
                return None
            
            # Extract resume text
            resume_text = self.extract_resume_text()
            
            # Activate the best prompt
            prompt_service.activate_prompt(prompt.PromptID)
            
            # Temporarily modify the model in the resume parsing function
            # We'll need to patch the model name for testing
            import app.api.resume as resume_module
            
            # Store original model
            original_model = resume_module.client.chat.completions.create
            
            # Create a custom completion function for this model
            def custom_completion(*args, **kwargs):
                kwargs['model'] = model_name
                return original_model(*args, **kwargs)
            
            # Patch the function
            resume_module.client.chat.completions.create = custom_completion
            
            # Test the model
            result = await parse_resume_with_ai(resume_text, user_id=None, db=db)
            
            # Restore original function
            resume_module.client.chat.completions.create = original_model
            
            print(f"✅ Model test completed: {model_name}")
            return result
            
        except Exception as e:
            print(f"❌ Error testing model {model_name}: {e}")
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
    
    def get_model_pricing(self, model_name):
        """Get pricing information for different models"""
        pricing = {
            "gpt-3.5-turbo": {
                "input_cost_per_1k": 0.0015,
                "output_cost_per_1k": 0.002,
                "description": "Fast and cost-effective"
            },
            "gpt-4": {
                "input_cost_per_1k": 0.03,
                "output_cost_per_1k": 0.06,
                "description": "Most capable but expensive"
            },
            "gpt-4-turbo": {
                "input_cost_per_1k": 0.01,
                "output_cost_per_1k": 0.03,
                "description": "Good balance of capability and cost"
            },
            "gpt-4o": {
                "input_cost_per_1k": 0.005,
                "output_cost_per_1k": 0.015,
                "description": "Latest model, good performance"
            },
            "gpt-4o-mini": {
                "input_cost_per_1k": 0.00015,
                "output_cost_per_1k": 0.0006,
                "description": "Very cost-effective"
            }
        }
        return pricing.get(model_name, {"input_cost_per_1k": 0, "output_cost_per_1k": 0, "description": "Unknown model"})
    
    async def test_all_models(self):
        """Test all available models"""
        print("🧪 Testing different models with best prompt...")
        print(f"📋 Using best prompt: {self.best_prompt_name}")
        
        # Load baseline
        baseline = self.load_baseline()
        print(f"✅ Loaded baseline: {self.baseline_file.name}")
        
        # Get database session
        db = next(get_db())
        
        # Test models (in order of cost-effectiveness)
        models_to_test = [
            "gpt-4o-mini",      # Most cost-effective
            "gpt-3.5-turbo",    # Current baseline
            "gpt-4o",           # Good performance
            "gpt-4-turbo",      # High performance
            "gpt-4"             # Most capable
        ]
        
        results = {}
        
        for model_name in models_to_test:
            print(f"\n{'='*50}")
            print(f"Testing: {model_name}")
            print(f"{'='*50}")
            
            result = await self.test_model(model_name, db)
            
            if result:
                accuracy_scores = self.calculate_accuracy(result, baseline)
                pricing = self.get_model_pricing(model_name)
                
                results[model_name] = {
                    'result': result,
                    'accuracy': accuracy_scores,
                    'pricing': pricing
                }
                
                print(f"\n📊 Accuracy Scores for {model_name}:")
                for section, score in accuracy_scores.items():
                    print(f"   {section}: {score:.1f}%")
                
                # Calculate overall accuracy
                overall_accuracy = sum(accuracy_scores.values()) / len(accuracy_scores)
                print(f"   Overall: {overall_accuracy:.1f}%")
                print(f"   Pricing: {pricing['description']}")
        
        # Save results
        self.save_results(results, baseline)
        
        return results
    
    def save_results(self, results, baseline):
        """Save test results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed results
        detailed_results = {}
        for model_name, data in results.items():
            overall_accuracy = sum(data['accuracy'].values()) / len(data['accuracy'])
            detailed_results[model_name] = {
                'accuracy_scores': data['accuracy'],
                'overall_accuracy': overall_accuracy,
                'pricing': data['pricing'],
                'result': data['result']
            }
        
        # Save JSON results
        results_file = self.results_dir / f"model_testing_results_{timestamp}.json"
        with open(results_file, 'w') as f:
            json.dump(detailed_results, f, indent=2)
        
        # Create comparison CSV
        comparison_data = []
        for model_name, data in results.items():
            overall_accuracy = sum(data['accuracy'].values()) / len(data['accuracy'])
            pricing = data['pricing']
            
            row = {
                'Model': model_name,
                'Overall_Accuracy': overall_accuracy,
                'Input_Cost_Per_1K': pricing['input_cost_per_1k'],
                'Output_Cost_Per_1K': pricing['output_cost_per_1k'],
                'Description': pricing['description']
            }
            for section, score in data['accuracy'].items():
                row[f'{section}_accuracy'] = score
            comparison_data.append(row)
        
        comparison_df = pd.DataFrame(comparison_data)
        comparison_file = self.results_dir / f"model_comparison_{timestamp}.csv"
        comparison_df.to_csv(comparison_file, index=False)
        
        print(f"\n📁 Results saved:")
        print(f"   • Detailed results: {results_file}")
        print(f"   • Comparison CSV: {comparison_file}")
        
        # Print summary
        print(f"\n📊 MODEL TESTING SUMMARY")
        print(f"{'='*50}")
        for model_name, data in results.items():
            overall = sum(data['accuracy'].values()) / len(data['accuracy'])
            pricing = data['pricing']
            print(f"{model_name}: {overall:.1f}% accuracy, ${pricing['input_cost_per_1k']:.4f}/1K input")
        
        # Find best model (considering accuracy and cost)
        best_model = self.find_best_model(results)
        best_accuracy = sum(results[best_model]['accuracy'].values()) / len(results[best_model]['accuracy'])
        best_pricing = results[best_model]['pricing']
        
        print(f"\n🏆 Best performing model: {best_model}")
        print(f"   Overall accuracy: {best_accuracy:.1f}%")
        print(f"   Cost: ${best_pricing['input_cost_per_1k']:.4f}/1K input, ${best_pricing['output_cost_per_1k']:.4f}/1K output")
        print(f"   Description: {best_pricing['description']}")
        
        return best_model, best_accuracy
    
    def find_best_model(self, results):
        """Find the best model considering accuracy and cost"""
        # Simple scoring: accuracy * (1 / cost_factor)
        # Lower cost models get higher scores
        model_scores = {}
        
        for model_name, data in results.items():
            accuracy = sum(data['accuracy'].values()) / len(data['accuracy'])
            pricing = data['pricing']
            
            # Cost factor (higher cost = lower score)
            cost_factor = pricing['input_cost_per_1k'] + pricing['output_cost_per_1k']
            if cost_factor == 0:
                cost_factor = 0.001  # Avoid division by zero
            
            # Score = accuracy / cost_factor
            score = accuracy / cost_factor
            model_scores[model_name] = score
        
        return max(model_scores.keys(), key=lambda x: model_scores[x])

async def main():
    """Run model testing"""
    tester = ModelTester()
    results = await tester.test_all_models()
    
    if results:
        print(f"\n✅ Model testing completed successfully!")
        print(f"📊 Tested {len(results)} models")
        print(f"📁 Results saved in: {tester.results_dir}")
    else:
        print(f"\n❌ Model testing failed")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 