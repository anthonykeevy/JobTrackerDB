#!/usr/bin/env python3
"""
Resume Parser Prompt Version Comparison Tool

This tool compares different prompt versions and shows:
1. Performance differences between versions
2. Subject area improvements
3. Cost and efficiency analysis
4. Recommendations for which version to use
"""

import sys
import os
import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp.db.session import get_db
from app.services.prompt_service import PromptService
from app.models import PromptManagement

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class VersionComparison:
    """Comparison between two prompt versions"""
    baseline_version: str
    new_version: str
    overall_accuracy_change: float
    overall_completeness_change: float
    subject_area_changes: Dict[str, Dict[str, float]]
    cost_efficiency: Dict[str, float]
    recommendations: List[str]

class PromptComparisonTool:
    """Tool for comparing prompt versions"""
    
    def __init__(self, db_session):
        self.db = db_session
        self.prompt_service = PromptService(db_session)
    
    def load_test_results(self, test_result_file: str) -> Dict[str, Any]:
        """Load test results from file"""
        try:
            with open(test_result_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading test results: {e}")
            return {}
    
    def compare_versions(self, baseline_file: str, new_file: str) -> VersionComparison:
        """Compare two test result files"""
        baseline_data = self.load_test_results(baseline_file)
        new_data = self.load_test_results(new_file)
        
        if not baseline_data or not new_data:
            raise Exception("Failed to load test results")
        
        # Calculate overall changes
        accuracy_change = new_data["overall_accuracy"] - baseline_data["overall_accuracy"]
        completeness_change = new_data["overall_completeness"] - baseline_data["overall_completeness"]
        
        # Compare subject areas
        subject_area_changes = {}
        baseline_areas = baseline_data["subject_areas"]
        new_areas = new_data["subject_areas"]
        
        for area_name in baseline_areas.keys():
            if area_name in new_areas:
                baseline_metrics = baseline_areas[area_name]
                new_metrics = new_areas[area_name]
                
                subject_area_changes[area_name] = {
                    "accuracy_change": new_metrics["accuracy_percentage"] - baseline_metrics["accuracy_percentage"],
                    "completeness_change": new_metrics["completeness_percentage"] - baseline_metrics["completeness_percentage"],
                    "quality_change": new_metrics["quality_score"] - baseline_metrics["quality_score"],
                    "extraction_change": new_metrics["extraction_count"] - baseline_metrics["extraction_count"]
                }
        
        # Calculate cost efficiency (if cost data is available)
        cost_efficiency = {
            "baseline_cost": baseline_data.get("cost", 0.0),
            "new_cost": new_data.get("cost", 0.0),
            "cost_change": new_data.get("cost", 0.0) - baseline_data.get("cost", 0.0),
            "baseline_tokens": baseline_data.get("token_usage", {}).get("total", 0),
            "new_tokens": new_data.get("token_usage", {}).get("total", 0)
        }
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            accuracy_change, completeness_change, subject_area_changes, cost_efficiency
        )
        
        return VersionComparison(
            baseline_version=baseline_data["prompt_version"],
            new_version=new_data["prompt_version"],
            overall_accuracy_change=accuracy_change,
            overall_completeness_change=completeness_change,
            subject_area_changes=subject_area_changes,
            cost_efficiency=cost_efficiency,
            recommendations=recommendations
        )
    
    def _generate_recommendations(self, accuracy_change: float, completeness_change: float,
                                subject_area_changes: Dict[str, Dict[str, float]],
                                cost_efficiency: Dict[str, float]) -> List[str]:
        """Generate recommendations based on comparison results"""
        recommendations = []
        
        # Overall performance recommendations
        if accuracy_change > 5:
            recommendations.append("✅ Significant accuracy improvement - consider adopting new version")
        elif accuracy_change < -5:
            recommendations.append("⚠️ Accuracy decreased - investigate what went wrong")
        
        if completeness_change > 5:
            recommendations.append("✅ Significant completeness improvement - consider adopting new version")
        elif completeness_change < -5:
            recommendations.append("⚠️ Completeness decreased - investigate what went wrong")
        
        # Subject area specific recommendations
        improved_areas = []
        declined_areas = []
        
        for area_name, changes in subject_area_changes.items():
            quality_change = changes["quality_change"]
            if quality_change > 10:
                improved_areas.append(area_name)
            elif quality_change < -10:
                declined_areas.append(area_name)
        
        if improved_areas:
            recommendations.append(f"✅ Areas with significant improvement: {', '.join(improved_areas)}")
        
        if declined_areas:
            recommendations.append(f"⚠️ Areas with significant decline: {', '.join(declined_areas)}")
        
        # Cost efficiency recommendations
        cost_change = cost_efficiency["cost_change"]
        if cost_change < 0:
            recommendations.append("💰 Cost decreased - good efficiency improvement")
        elif cost_change > 0.01:  # More than 1 cent increase
            recommendations.append("💰 Cost increased - consider if performance gains justify the cost")
        
        # Final recommendation
        if accuracy_change > 0 and completeness_change > 0 and cost_change <= 0:
            recommendations.append("🎉 Strong recommendation: Adopt the new version")
        elif accuracy_change > 0 and completeness_change > 0:
            recommendations.append("👍 Good improvement: Consider adopting with cost monitoring")
        elif accuracy_change < 0 or completeness_change < 0:
            recommendations.append("❌ Do not adopt: Performance declined")
        else:
            recommendations.append("🤔 Mixed results: Further testing recommended")
        
        return recommendations
    
    def generate_comparison_report(self, comparison: VersionComparison) -> str:
        """Generate a detailed comparison report"""
        report = []
        report.append("📊 PROMPT VERSION COMPARISON REPORT")
        report.append("=" * 60)
        report.append("")
        
        # Version information
        report.append("🔄 VERSION COMPARISON:")
        report.append(f"  Baseline: v{comparison.baseline_version}")
        report.append(f"  New Version: v{comparison.new_version}")
        report.append("")
        
        # Overall performance changes
        report.append("🎯 OVERALL PERFORMANCE CHANGES:")
        report.append(f"  Accuracy Change: {comparison.overall_accuracy_change:+.1f}%")
        report.append(f"  Completeness Change: {comparison.overall_completeness_change:+.1f}%")
        report.append("")
        
        # Subject area changes
        report.append("📋 SUBJECT AREA CHANGES:")
        for area_name, changes in comparison.subject_area_changes.items():
            report.append(f"\n{area_name.upper()}:")
            report.append(f"  Accuracy: {changes['accuracy_change']:+.1f}%")
            report.append(f"  Completeness: {changes['completeness_change']:+.1f}%")
            report.append(f"  Quality Score: {changes['quality_change']:+.1f}%")
            report.append(f"  Extraction Count: {changes['extraction_change']:+d}")
        report.append("")
        
        # Cost efficiency
        report.append("💰 COST EFFICIENCY:")
        report.append(f"  Baseline Cost: ${comparison.cost_efficiency['baseline_cost']:.4f}")
        report.append(f"  New Cost: ${comparison.cost_efficiency['new_cost']:.4f}")
        report.append(f"  Cost Change: ${comparison.cost_efficiency['cost_change']:+.4f}")
        report.append(f"  Token Usage: {comparison.cost_efficiency['baseline_tokens']} → {comparison.cost_efficiency['new_tokens']}")
        report.append("")
        
        # Recommendations
        report.append("💡 RECOMMENDATIONS:")
        for i, recommendation in enumerate(comparison.recommendations, 1):
            report.append(f"  {i}. {recommendation}")
        
        return "\n".join(report)
    
    def find_test_files(self) -> List[str]:
        """Find all test result files"""
        test_files = [f for f in os.listdir('.') if f.startswith('test_results_') and f.endswith('.json')]
        return sorted(test_files)
    
    def get_prompt_versions(self) -> List[Dict[str, Any]]:
        """Get all prompt versions from database"""
        try:
            prompts = self.db.query(PromptManagement).filter(
                PromptManagement.PromptType == "resume_parse"
            ).order_by(PromptManagement.PromptVersion.desc()).all()
            
            return [
                {
                    "prompt_id": prompt.PromptID,
                    "name": prompt.PromptName,
                    "version": prompt.PromptVersion,
                    "is_active": prompt.IsActive,
                    "is_default": prompt.IsDefault,
                    "description": prompt.Description
                }
                for prompt in prompts
            ]
        except Exception as e:
            logger.error(f"Error getting prompt versions: {e}")
            return []

def main():
    """Main comparison function"""
    print("🔍 RESUME PARSER PROMPT VERSION COMPARISON")
    print("=" * 60)
    
    try:
        db = next(get_db())
        tool = PromptComparisonTool(db)
        
        # Find test files
        test_files = tool.find_test_files()
        if len(test_files) < 2:
            print("❌ Need at least 2 test result files to compare")
            print("Available files:", test_files)
            return False
        
        # Show available test files
        print("📁 Available test result files:")
        for i, file in enumerate(test_files, 1):
            print(f"  {i}. {file}")
        
        # For now, compare the two most recent files
        baseline_file = test_files[-2]  # Second most recent
        new_file = test_files[-1]       # Most recent
        
        print(f"\n🔄 Comparing:")
        print(f"  Baseline: {baseline_file}")
        print(f"  New Version: {new_file}")
        
        # Perform comparison
        comparison = tool.compare_versions(baseline_file, new_file)
        
        # Generate and display report
        report = tool.generate_comparison_report(comparison)
        print("\n" + report)
        
        # Show available prompt versions
        print("\n📋 Available Prompt Versions in Database:")
        versions = tool.get_prompt_versions()
        for version in versions:
            status = "ACTIVE" if version["is_active"] else "INACTIVE"
            print(f"  • {version['name']} v{version['version']} ({status})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during comparison: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 