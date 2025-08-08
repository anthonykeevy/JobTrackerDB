#!/usr/bin/env python3
"""
Resume Parser Performance Testing Framework

This script tests the effectiveness of the resume parser prompt by:
1. Tracking performance metrics by subject area (BasicInfo, Experience, Education, etc.)
2. Comparing results between different prompt versions
3. Providing detailed analysis of extraction accuracy
4. Enabling targeted prompt improvements
"""

import sys
import os
import json
import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp.db.session import get_db
from app.services.prompt_service import PromptService
from app.api.resume import parse_resume_with_ai
from app.models import PromptManagement

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SubjectAreaMetrics:
    """Metrics for a specific subject area"""
    area_name: str
    extraction_count: int
    expected_count: int
    accuracy_percentage: float
    completeness_percentage: float
    quality_score: float
    missing_fields: List[str]
    extracted_fields: List[str]
    issues: List[str]

@dataclass
class ParseResult:
    """Result of a resume parsing test"""
    test_id: str
    prompt_version: str
    timestamp: str
    total_extraction_count: int
    total_expected_count: int
    overall_accuracy: float
    overall_completeness: float
    subject_areas: Dict[str, SubjectAreaMetrics]
    raw_extracted_data: Dict[str, Any]
    expected_data: Dict[str, Any]
    processing_time: float
    token_usage: Dict[str, int]
    cost: float

class ResumeParserPerformanceTester:
    """Test framework for resume parser performance"""
    
    def __init__(self, db_session):
        self.db = db_session
        self.prompt_service = PromptService(db_session)
        
    def get_test_resume_content(self) -> str:
        """Get test resume content - you can replace this with actual resume text"""
        return """
        ANTHONY KEEVY
        Software Engineer & Technical Lead
        Email: anthony.keevy@example.com
        Phone: +61 400 123 456
        Location: Sydney, NSW, Australia
        LinkedIn: linkedin.com/in/anthonykeevy
        
        PROFESSIONAL SUMMARY
        Experienced software engineer with 8+ years in full-stack development, specializing in 
        React, Node.js, and cloud technologies. Proven track record of leading development teams 
        and delivering scalable solutions.
        
        WORK EXPERIENCE
        
        Senior Software Engineer
        TechCorp Australia | Sydney, NSW
        January 2022 - Present
        • Led development of microservices architecture using Node.js and React
        • Reduced API response time by 40% through optimization
        • Mentored 3 junior developers and conducted code reviews
        • Technologies: React, Node.js, AWS, Docker, MongoDB
        
        Software Developer
        Digital Solutions Inc | Melbourne, VIC
        March 2020 - December 2021
        • Developed full-stack web applications using React and Python
        • Implemented CI/CD pipelines using GitHub Actions
        • Collaborated with UX team to improve user experience
        • Technologies: React, Python, Django, PostgreSQL
        
        EDUCATION
        
        Bachelor of Computer Science
        University of Technology Sydney
        Graduated: May 2019
        GPA: 6.2/7.0
        
        Master of Information Technology
        University of Sydney
        Graduated: December 2021
        GPA: 6.8/7.0
        
        SKILLS
        
        Technical Skills:
        • Programming Languages: JavaScript, Python, TypeScript, Java
        • Frontend: React, Vue.js, HTML5, CSS3, SASS
        • Backend: Node.js, Express, Django, FastAPI
        • Databases: MongoDB, PostgreSQL, Redis
        • Cloud: AWS, Azure, Docker, Kubernetes
        • Tools: Git, GitHub, VS Code, Jira
        
        Soft Skills:
        • Leadership, Team Management, Problem Solving
        • Communication, Mentoring, Agile Methodologies
        
        CERTIFICATIONS
        
        AWS Certified Solutions Architect - Associate
        Amazon Web Services | Issued: March 2023 | Expires: March 2026
        
        Microsoft Certified: Azure Developer Associate
        Microsoft | Issued: June 2022 | Expires: June 2025
        
        PROJECTS
        
        E-commerce Platform
        • Built full-stack e-commerce solution with React and Node.js
        • Implemented payment processing with Stripe
        • Deployed on AWS with CI/CD pipeline
        • Technologies: React, Node.js, MongoDB, AWS, Stripe
        • URL: https://github.com/anthonykeevy/ecommerce
        
        Task Management App
        • Developed collaborative task management application
        • Real-time updates using WebSocket
        • User authentication and role-based access
        • Technologies: React, Node.js, Socket.io, PostgreSQL
        """
    
    def get_expected_data(self) -> Dict[str, Any]:
        """Define expected data structure for comparison"""
        return {
            "personal_info": {
                "name": "Anthony Keevy",
                "email": "anthony.keevy@example.com",
                "phone": "+61 400 123 456",
                "location": "Sydney, NSW, Australia"
            },
            "summary": "Experienced software engineer with 8+ years in full-stack development, specializing in React, Node.js, and cloud technologies. Proven track record of leading development teams and delivering scalable solutions.",
            "work_experience": [
                {
                    "company": "TechCorp Australia",
                    "position": "Senior Software Engineer",
                    "start_date": "2022-01",
                    "end_date": "Present",
                    "description": "Led development of microservices architecture using Node.js and React",
                    "achievements": [
                        "Reduced API response time by 40% through optimization",
                        "Mentored 3 junior developers and conducted code reviews"
                    ],
                    "technologies": ["React", "Node.js", "AWS", "Docker", "MongoDB"]
                },
                {
                    "company": "Digital Solutions Inc",
                    "position": "Software Developer",
                    "start_date": "2020-03",
                    "end_date": "2021-12",
                    "description": "Developed full-stack web applications using React and Python",
                    "achievements": [
                        "Implemented CI/CD pipelines using GitHub Actions",
                        "Collaborated with UX team to improve user experience"
                    ],
                    "technologies": ["React", "Python", "Django", "PostgreSQL"]
                }
            ],
            "education": [
                {
                    "institution": "University of Technology Sydney",
                    "degree": "Bachelor of Computer Science",
                    "field_of_study": "Computer Science",
                    "graduation_date": "2019-05",
                    "gpa": "6.2/7.0"
                },
                {
                    "institution": "University of Sydney",
                    "degree": "Master of Information Technology",
                    "field_of_study": "Information Technology",
                    "graduation_date": "2021-12",
                    "gpa": "6.8/7.0"
                }
            ],
            "skills": [
                {
                    "category": "Technical",
                    "skills": [
                        "JavaScript", "Python", "TypeScript", "Java",
                        "React", "Vue.js", "HTML5", "CSS3", "SASS",
                        "Node.js", "Express", "Django", "FastAPI",
                        "MongoDB", "PostgreSQL", "Redis",
                        "AWS", "Azure", "Docker", "Kubernetes",
                        "Git", "GitHub", "VS Code", "Jira"
                    ]
                },
                {
                    "category": "Soft",
                    "skills": [
                        "Leadership", "Team Management", "Problem Solving",
                        "Communication", "Mentoring", "Agile Methodologies"
                    ]
                }
            ],
            "certifications": [
                {
                    "name": "AWS Certified Solutions Architect - Associate",
                    "issuer": "Amazon Web Services",
                    "date_earned": "2023-03",
                    "expiry_date": "2026-03"
                },
                {
                    "name": "Microsoft Certified: Azure Developer Associate",
                    "issuer": "Microsoft",
                    "date_earned": "2022-06",
                    "expiry_date": "2025-06"
                }
            ],
            "projects": [
                {
                    "name": "E-commerce Platform",
                    "description": "Built full-stack e-commerce solution with React and Node.js",
                    "technologies": ["React", "Node.js", "MongoDB", "AWS", "Stripe"],
                    "url": "https://github.com/anthonykeevy/ecommerce"
                },
                {
                    "name": "Task Management App",
                    "description": "Developed collaborative task management application",
                    "technologies": ["React", "Node.js", "Socket.io", "PostgreSQL"],
                    "url": ""
                }
            ]
        }
    
    def analyze_subject_area(self, area_name: str, extracted_data: Dict[str, Any], 
                           expected_data: Dict[str, Any]) -> SubjectAreaMetrics:
        """Analyze performance for a specific subject area"""
        
        if area_name == "personal_info":
            return self._analyze_personal_info(extracted_data, expected_data)
        elif area_name == "work_experience":
            return self._analyze_work_experience(extracted_data, expected_data)
        elif area_name == "education":
            return self._analyze_education(extracted_data, expected_data)
        elif area_name == "skills":
            return self._analyze_skills(extracted_data, expected_data)
        elif area_name == "certifications":
            return self._analyze_certifications(extracted_data, expected_data)
        elif area_name == "projects":
            return self._analyze_projects(extracted_data, expected_data)
        else:
            return SubjectAreaMetrics(
                area_name=area_name,
                extraction_count=0,
                expected_count=0,
                accuracy_percentage=0.0,
                completeness_percentage=0.0,
                quality_score=0.0,
                missing_fields=[],
                extracted_fields=[],
                issues=["Unknown subject area"]
            )
    
    def _analyze_personal_info(self, extracted: Dict[str, Any], expected: Dict[str, Any]) -> SubjectAreaMetrics:
        """Analyze personal information extraction"""
        expected_fields = ["name", "email", "phone", "location"]
        extracted_fields = list(extracted.get("personal_info", {}).keys())
        
        missing_fields = [field for field in expected_fields if field not in extracted_fields]
        completeness = (len(extracted_fields) / len(expected_fields)) * 100
        
        # Check accuracy of extracted data
        accuracy_score = 0
        issues = []
        
        if "name" in extracted_fields:
            extracted_name = extracted["personal_info"]["name"].strip()
            expected_name = expected["personal_info"]["name"].strip()
            # Case-insensitive comparison for names
            if extracted_name.lower() == expected_name.lower():
                accuracy_score += 25
            else:
                issues.append(f"Name mismatch: expected '{expected_name}', got '{extracted_name}'")
        
        if "email" in extracted_fields:
            if extracted["personal_info"]["email"] == expected["personal_info"]["email"]:
                accuracy_score += 25
            else:
                issues.append(f"Email mismatch: expected '{expected['personal_info']['email']}', got '{extracted['personal_info']['email']}'")
        
        if "phone" in extracted_fields:
            if extracted["personal_info"]["phone"] == expected["personal_info"]["phone"]:
                accuracy_score += 25
            else:
                issues.append(f"Phone mismatch: expected '{expected['personal_info']['phone']}', got '{extracted['personal_info']['phone']}'")
        
        if "location" in extracted_fields:
            if extracted["personal_info"]["location"] == expected["personal_info"]["location"]:
                accuracy_score += 25
            else:
                issues.append(f"Location mismatch: expected '{expected['personal_info']['location']}', got '{extracted['personal_info']['location']}'")
        
        return SubjectAreaMetrics(
            area_name="personal_info",
            extraction_count=len(extracted_fields),
            expected_count=len(expected_fields),
            accuracy_percentage=accuracy_score,
            completeness_percentage=completeness,
            quality_score=(accuracy_score + completeness) / 2,
            missing_fields=missing_fields,
            extracted_fields=extracted_fields,
            issues=issues
        )
    
    def _analyze_work_experience(self, extracted: Dict[str, Any], expected: Dict[str, Any]) -> SubjectAreaMetrics:
        """Analyze work experience extraction"""
        expected_experiences = expected.get("work_experience", [])
        extracted_experiences = extracted.get("work_experience", [])
        
        completeness = (len(extracted_experiences) / len(expected_experiences)) * 100 if expected_experiences else 0
        
        # Analyze accuracy of each experience
        accuracy_score = 0
        issues = []
        
        for i, expected_exp in enumerate(expected_experiences):
            if i < len(extracted_experiences):
                extracted_exp = extracted_experiences[i]
                
                # Check key fields
                if extracted_exp.get("company") == expected_exp.get("company"):
                    accuracy_score += 20
                else:
                    issues.append(f"Company mismatch in experience {i+1}")
                
                if extracted_exp.get("position") == expected_exp.get("position"):
                    accuracy_score += 20
                else:
                    issues.append(f"Position mismatch in experience {i+1}")
                
                if extracted_exp.get("start_date") == expected_exp.get("start_date"):
                    accuracy_score += 20
                else:
                    issues.append(f"Start date mismatch in experience {i+1}")
                
                if extracted_exp.get("end_date") == expected_exp.get("end_date"):
                    accuracy_score += 20
                else:
                    issues.append(f"End date mismatch in experience {i+1}")
                
                # Check if description is present
                if extracted_exp.get("description"):
                    accuracy_score += 20
                else:
                    issues.append(f"Missing description in experience {i+1}")
        
        # Normalize accuracy score to percentage (max 100%)
        max_possible_score = len(expected_experiences) * 100
        if max_possible_score > 0:
            accuracy_percentage = (accuracy_score / max_possible_score) * 100
        else:
            accuracy_percentage = 0
        
        return SubjectAreaMetrics(
            area_name="work_experience",
            extraction_count=len(extracted_experiences),
            expected_count=len(expected_experiences),
            accuracy_percentage=accuracy_percentage,
            completeness_percentage=completeness,
            quality_score=(accuracy_percentage + completeness) / 2,
            missing_fields=[],
            extracted_fields=[f"experience_{i+1}" for i in range(len(extracted_experiences))],
            issues=issues
        )
    
    def _analyze_education(self, extracted: Dict[str, Any], expected: Dict[str, Any]) -> SubjectAreaMetrics:
        """Analyze education extraction"""
        expected_education = expected.get("education", [])
        extracted_education = extracted.get("education", [])
        
        completeness = (len(extracted_education) / len(expected_education)) * 100 if expected_education else 0
        
        accuracy_score = 0
        issues = []
        
        for i, expected_edu in enumerate(expected_education):
            if i < len(extracted_education):
                extracted_edu = extracted_education[i]
                
                if extracted_edu.get("institution") == expected_edu.get("institution"):
                    accuracy_score += 25
                else:
                    issues.append(f"Institution mismatch in education {i+1}")
                
                if extracted_edu.get("degree") == expected_edu.get("degree"):
                    accuracy_score += 25
                else:
                    issues.append(f"Degree mismatch in education {i+1}")
                
                if extracted_edu.get("graduation_date") == expected_edu.get("graduation_date"):
                    accuracy_score += 25
                else:
                    issues.append(f"Graduation date mismatch in education {i+1}")
                
                if extracted_edu.get("gpa") == expected_edu.get("gpa"):
                    accuracy_score += 25
                else:
                    issues.append(f"GPA mismatch in education {i+1}")
        
        # Normalize accuracy score to percentage (max 100%)
        max_possible_score = len(expected_education) * 100
        if max_possible_score > 0:
            accuracy_percentage = (accuracy_score / max_possible_score) * 100
        else:
            accuracy_percentage = 0
        
        return SubjectAreaMetrics(
            area_name="education",
            extraction_count=len(extracted_education),
            expected_count=len(expected_education),
            accuracy_percentage=accuracy_percentage,
            completeness_percentage=completeness,
            quality_score=(accuracy_percentage + completeness) / 2,
            missing_fields=[],
            extracted_fields=[f"education_{i+1}" for i in range(len(extracted_education))],
            issues=issues
        )
    
    def _analyze_skills(self, extracted: Dict[str, Any], expected: Dict[str, Any]) -> SubjectAreaMetrics:
        """Analyze skills extraction"""
        expected_skills = expected.get("skills", [])
        extracted_skills = extracted.get("skills", [])
        
        completeness = (len(extracted_skills) / len(expected_skills)) * 100 if expected_skills else 0
        
        accuracy_score = 0
        issues = []
        
        # Check if technical and soft skills are categorized correctly
        technical_skills = []
        soft_skills = []
        
        for skill_group in extracted_skills:
            if skill_group.get("category") == "Technical":
                technical_skills.extend(skill_group.get("skills", []))
            elif skill_group.get("category") == "Soft":
                soft_skills.extend(skill_group.get("skills", []))
        
        expected_technical = []
        expected_soft = []
        
        for skill_group in expected_skills:
            if skill_group.get("category") == "Technical":
                expected_technical.extend(skill_group.get("skills", []))
            elif skill_group.get("category") == "Soft":
                expected_soft.extend(skill_group.get("skills", []))
        
        # Calculate accuracy based on skill extraction
        if technical_skills:
            accuracy_score += 50
        else:
            issues.append("No technical skills extracted")
        
        if soft_skills:
            accuracy_score += 50
        else:
            issues.append("No soft skills extracted")
        
        return SubjectAreaMetrics(
            area_name="skills",
            extraction_count=len(extracted_skills),
            expected_count=len(expected_skills),
            accuracy_percentage=accuracy_score,
            completeness_percentage=completeness,
            quality_score=(accuracy_score + completeness) / 2,
            missing_fields=[],
            extracted_fields=[f"skill_group_{i+1}" for i in range(len(extracted_skills))],
            issues=issues
        )
    
    def _analyze_certifications(self, extracted: Dict[str, Any], expected: Dict[str, Any]) -> SubjectAreaMetrics:
        """Analyze certifications extraction"""
        expected_certs = expected.get("certifications", [])
        extracted_certs = extracted.get("certifications", [])
        
        completeness = (len(extracted_certs) / len(expected_certs)) * 100 if expected_certs else 0
        
        accuracy_score = 0
        issues = []
        
        for i, expected_cert in enumerate(expected_certs):
            if i < len(extracted_certs):
                extracted_cert = extracted_certs[i]
                
                if extracted_cert.get("name") == expected_cert.get("name"):
                    accuracy_score += 50
                else:
                    issues.append(f"Certification name mismatch in cert {i+1}")
                
                if extracted_cert.get("issuer") == expected_cert.get("issuer"):
                    accuracy_score += 50
                else:
                    issues.append(f"Certification issuer mismatch in cert {i+1}")
        
        # Normalize accuracy score to percentage (max 100%)
        max_possible_score = len(expected_certs) * 100
        if max_possible_score > 0:
            accuracy_percentage = (accuracy_score / max_possible_score) * 100
        else:
            accuracy_percentage = 0
        
        return SubjectAreaMetrics(
            area_name="certifications",
            extraction_count=len(extracted_certs),
            expected_count=len(expected_certs),
            accuracy_percentage=accuracy_percentage,
            completeness_percentage=completeness,
            quality_score=(accuracy_percentage + completeness) / 2,
            missing_fields=[],
            extracted_fields=[f"certification_{i+1}" for i in range(len(extracted_certs))],
            issues=issues
        )
    
    def _analyze_projects(self, extracted: Dict[str, Any], expected: Dict[str, Any]) -> SubjectAreaMetrics:
        """Analyze projects extraction"""
        expected_projects = expected.get("projects", [])
        extracted_projects = extracted.get("projects", [])
        
        completeness = (len(extracted_projects) / len(expected_projects)) * 100 if expected_projects else 0
        
        accuracy_score = 0
        issues = []
        
        for i, expected_proj in enumerate(expected_projects):
            if i < len(extracted_projects):
                extracted_proj = extracted_projects[i]
                
                if extracted_proj.get("name") == expected_proj.get("name"):
                    accuracy_score += 50
                else:
                    issues.append(f"Project name mismatch in project {i+1}")
                
                if extracted_proj.get("description"):
                    accuracy_score += 50
                else:
                    issues.append(f"Missing description in project {i+1}")
        
        # Normalize accuracy score to percentage (max 100%)
        max_possible_score = len(expected_projects) * 100
        if max_possible_score > 0:
            accuracy_percentage = (accuracy_score / max_possible_score) * 100
        else:
            accuracy_percentage = 0
        
        return SubjectAreaMetrics(
            area_name="projects",
            extraction_count=len(extracted_projects),
            expected_count=len(expected_projects),
            accuracy_percentage=accuracy_percentage,
            completeness_percentage=completeness,
            quality_score=(accuracy_percentage + completeness) / 2,
            missing_fields=[],
            extracted_fields=[f"project_{i+1}" for i in range(len(extracted_projects))],
            issues=issues
        )
    
    async def test_prompt_performance(self, prompt_version: str = None) -> ParseResult:
        """Test the performance of a specific prompt version"""
        start_time = datetime.now()
        
        # Get the prompt
        if prompt_version:
            prompt = self.prompt_service.get_active_prompt("resume_parse", prompt_version)
        else:
            prompt = self.prompt_service.get_active_prompt("resume_parse")
        
        if not prompt:
            raise Exception("No active prompt found")
        
        # Get test data
        resume_content = self.get_test_resume_content()
        expected_data = self.get_expected_data()
        
        # Parse resume
        extracted_data = await parse_resume_with_ai(resume_content, user_id=1, db=self.db)
        
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        # Analyze each subject area
        subject_areas = {}
        for area_name in ["personal_info", "work_experience", "education", "skills", "certifications", "projects"]:
            metrics = self.analyze_subject_area(area_name, extracted_data, expected_data)
            subject_areas[area_name] = metrics
        
        # Calculate overall metrics
        total_extraction = sum(metrics.extraction_count for metrics in subject_areas.values())
        total_expected = sum(metrics.expected_count for metrics in subject_areas.values())
        overall_accuracy = sum(metrics.accuracy_percentage for metrics in subject_areas.values()) / len(subject_areas)
        overall_completeness = sum(metrics.completeness_percentage for metrics in subject_areas.values()) / len(subject_areas)
        
        return ParseResult(
            test_id=f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            prompt_version=prompt.PromptVersion,
            timestamp=datetime.now().isoformat(),
            total_extraction_count=total_extraction,
            total_expected_count=total_expected,
            overall_accuracy=overall_accuracy,
            overall_completeness=overall_completeness,
            subject_areas=subject_areas,
            raw_extracted_data=extracted_data,
            expected_data=expected_data,
            processing_time=processing_time,
            token_usage={"input": 0, "output": 0},  # Would be populated from actual API response
            cost=0.0  # Would be calculated from token usage
        )
    
    def save_test_result(self, result: ParseResult) -> bool:
        """Save test result to database for comparison"""
        try:
            # Convert result to dictionary
            result_data = {
                "test_id": result.test_id,
                "prompt_version": result.prompt_version,
                "timestamp": result.timestamp,
                "total_extraction_count": result.total_extraction_count,
                "total_expected_count": result.total_expected_count,
                "overall_accuracy": result.overall_accuracy,
                "overall_completeness": result.overall_completeness,
                "raw_extracted_data": result.raw_extracted_data,
                "expected_data": result.expected_data,
                "processing_time": result.processing_time,
                "token_usage": result.token_usage,
                "cost": result.cost,
                "subject_areas": {}
            }
            
            # Convert subject areas to dictionaries
            for area_name, metrics in result.subject_areas.items():
                result_data["subject_areas"][area_name] = {
                    "area_name": metrics.area_name,
                    "extraction_count": metrics.extraction_count,
                    "expected_count": metrics.expected_count,
                    "accuracy_percentage": metrics.accuracy_percentage,
                    "completeness_percentage": metrics.completeness_percentage,
                    "quality_score": metrics.quality_score,
                    "missing_fields": metrics.missing_fields,
                    "extracted_fields": metrics.extracted_fields,
                    "issues": metrics.issues
                }
            
            # Save to file for now (could be extended to database)
            filename = f"test_results_{result.test_id}.json"
            with open(filename, 'w') as f:
                json.dump(result_data, f, indent=2)
            
            logger.info(f"Test result saved to {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving test result: {e}")
            return False
    
    def compare_results(self, result1: ParseResult, result2: ParseResult) -> Dict[str, Any]:
        """Compare two test results"""
        comparison = {
            "prompt_versions": {
                "baseline": result1.prompt_version,
                "new": result2.prompt_version
            },
            "overall_comparison": {
                "accuracy_change": result2.overall_accuracy - result1.overall_accuracy,
                "completeness_change": result2.overall_completeness - result1.overall_completeness,
                "extraction_change": result2.total_extraction_count - result1.total_extraction_count
            },
            "subject_area_comparison": {}
        }
        
        for area_name in result1.subject_areas.keys():
            if area_name in result2.subject_areas:
                baseline = result1.subject_areas[area_name]
                new = result2.subject_areas[area_name]
                
                comparison["subject_area_comparison"][area_name] = {
                    "accuracy_change": new.accuracy_percentage - baseline.accuracy_percentage,
                    "completeness_change": new.completeness_percentage - baseline.completeness_percentage,
                    "quality_change": new.quality_score - baseline.quality_score,
                    "extraction_change": new.extraction_count - baseline.extraction_count
                }
        
        return comparison

def main():
    """Main testing function"""
    print("🧪 RESUME PARSER PERFORMANCE TESTING")
    print("=" * 60)
    
    try:
        db = next(get_db())
        tester = ResumeParserPerformanceTester(db)
        
        # Test current prompt
        print("📝 Testing current prompt performance...")
        result = asyncio.run(tester.test_prompt_performance())
        
        # Save result
        tester.save_test_result(result)
        
        # Display results
        print(f"\n📊 TEST RESULTS - Prompt Version: {result.prompt_version}")
        print(f"Overall Accuracy: {result.overall_accuracy:.1f}%")
        print(f"Overall Completeness: {result.overall_completeness:.1f}%")
        print(f"Processing Time: {result.processing_time:.2f}s")
        
        print("\n📋 SUBJECT AREA BREAKDOWN:")
        for area_name, metrics in result.subject_areas.items():
            print(f"\n{area_name.upper()}:")
            print(f"  Accuracy: {metrics.accuracy_percentage:.1f}%")
            print(f"  Completeness: {metrics.completeness_percentage:.1f}%")
            print(f"  Quality Score: {metrics.quality_score:.1f}%")
            print(f"  Extracted: {metrics.extraction_count}/{metrics.expected_count}")
            
            if metrics.issues:
                print(f"  Issues: {', '.join(metrics.issues[:3])}")  # Show first 3 issues
        
        print("\n🎉 Performance testing completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 