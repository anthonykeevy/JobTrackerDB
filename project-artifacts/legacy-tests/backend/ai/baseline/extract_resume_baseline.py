#!/usr/bin/env python3
"""
Extract Resume Baseline Data

This script extracts all information from the test resume and saves it to CSV files
for each subject area. The user can then manually verify and perfect this data
to create an accurate baseline for testing prompt effectiveness.
"""

import sys
import os
import csv
import json
import logging
from datetime import datetime
from typing import Dict, List, Any

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../../backend'))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResumeBaselineExtractor:
    """Extract baseline data from test resume"""
    
    def __init__(self):
        self.resume_content = self.get_test_resume_content()
        
    def get_test_resume_content(self) -> str:
        """Get the test resume content"""
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
    
    def extract_personal_info(self) -> Dict[str, Any]:
        """Extract personal information from resume"""
        return {
            "name": "ANTHONY KEEVY",
            "email": "anthony.keevy@example.com",
            "phone": "+61 400 123 456",
            "location": "Sydney, NSW, Australia",
            "linkedin": "linkedin.com/in/anthonykeevy"
        }
    
    def extract_work_experience(self) -> List[Dict[str, Any]]:
        """Extract work experience from resume"""
        return [
            {
                "company": "TechCorp Australia",
                "position": "Senior Software Engineer",
                "location": "Sydney, NSW",
                "start_date": "January 2022",
                "end_date": "Present",
                "description": "Led development of microservices architecture using Node.js and React",
                "achievements": [
                    "Led development of microservices architecture using Node.js and React",
                    "Reduced API response time by 40% through optimization",
                    "Mentored 3 junior developers and conducted code reviews"
                ],
                "technologies": ["React", "Node.js", "AWS", "Docker", "MongoDB"]
            },
            {
                "company": "Digital Solutions Inc",
                "position": "Software Developer",
                "location": "Melbourne, VIC",
                "start_date": "March 2020",
                "end_date": "December 2021",
                "description": "Developed full-stack web applications using React and Python",
                "achievements": [
                    "Developed full-stack web applications using React and Python",
                    "Implemented CI/CD pipelines using GitHub Actions",
                    "Collaborated with UX team to improve user experience"
                ],
                "technologies": ["React", "Python", "Django", "PostgreSQL"]
            }
        ]
    
    def extract_education(self) -> List[Dict[str, Any]]:
        """Extract education from resume"""
        return [
            {
                "institution": "University of Technology Sydney",
                "degree": "Bachelor of Computer Science",
                "field_of_study": "Computer Science",
                "graduation_date": "May 2019",
                "gpa": "6.2/7.0"
            },
            {
                "institution": "University of Sydney",
                "degree": "Master of Information Technology",
                "field_of_study": "Information Technology",
                "graduation_date": "December 2021",
                "gpa": "6.8/7.0"
            }
        ]
    
    def extract_skills(self) -> List[Dict[str, Any]]:
        """Extract skills from resume"""
        return [
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
        ]
    
    def extract_certifications(self) -> List[Dict[str, Any]]:
        """Extract certifications from resume"""
        return [
            {
                "name": "AWS Certified Solutions Architect - Associate",
                "issuer": "Amazon Web Services",
                "date_earned": "March 2023",
                "expiry_date": "March 2026"
            },
            {
                "name": "Microsoft Certified: Azure Developer Associate",
                "issuer": "Microsoft",
                "date_earned": "June 2022",
                "expiry_date": "June 2025"
            }
        ]
    
    def extract_projects(self) -> List[Dict[str, Any]]:
        """Extract projects from resume"""
        return [
            {
                "name": "E-commerce Platform",
                "description": "Built full-stack e-commerce solution with React and Node.js",
                "achievements": [
                    "Built full-stack e-commerce solution with React and Node.js",
                    "Implemented payment processing with Stripe",
                    "Deployed on AWS with CI/CD pipeline"
                ],
                "technologies": ["React", "Node.js", "MongoDB", "AWS", "Stripe"],
                "url": "https://github.com/anthonykeevy/ecommerce"
            },
            {
                "name": "Task Management App",
                "description": "Developed collaborative task management application",
                "achievements": [
                    "Developed collaborative task management application",
                    "Real-time updates using WebSocket",
                    "User authentication and role-based access"
                ],
                "technologies": ["React", "Node.js", "Socket.io", "PostgreSQL"],
                "url": ""
            }
        ]
    
    def extract_summary(self) -> str:
        """Extract professional summary"""
        return "Experienced software engineer with 8+ years in full-stack development, specializing in React, Node.js, and cloud technologies. Proven track record of leading development teams and delivering scalable solutions."
    
    def save_personal_info_csv(self, data: Dict[str, Any]):
        """Save personal info to CSV"""
        filename = "baseline_personal_info.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Field', 'Value', 'Notes'])
            for field, value in data.items():
                writer.writerow([field, value, ''])
        logger.info(f"Personal info saved to {filename}")
    
    def save_work_experience_csv(self, data: List[Dict[str, Any]]):
        """Save work experience to CSV"""
        filename = "baseline_work_experience.csv"
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
        filename = "baseline_education.csv"
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
        filename = "baseline_skills.csv"
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
        filename = "baseline_certifications.csv"
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
        filename = "baseline_projects.csv"
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
        filename = "baseline_summary.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Summary', 'Notes'])
            writer.writerow([summary, ''])
        logger.info(f"Summary saved to {filename}")
    
    def save_resume_content(self):
        """Save the raw resume content"""
        filename = "baseline_resume_content.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.resume_content)
        logger.info(f"Resume content saved to {filename}")
    
    def create_baseline_dataset(self):
        """Create comprehensive baseline dataset"""
        logger.info("Creating baseline dataset from test resume...")
        
        # Extract all data
        personal_info = self.extract_personal_info()
        work_experience = self.extract_work_experience()
        education = self.extract_education()
        skills = self.extract_skills()
        certifications = self.extract_certifications()
        projects = self.extract_projects()
        summary = self.extract_summary()
        
        # Save to CSV files
        self.save_resume_content()
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
        
        filename = "baseline_dataset.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(baseline_data, f, indent=2)
        logger.info(f"Baseline dataset saved to {filename}")
        
        # Print summary
        logger.info("\nBASELINE DATASET SUMMARY:")
        logger.info(f"  Personal Info: {len(personal_info)} fields")
        logger.info(f"  Work Experience: {len(work_experience)} entries")
        logger.info(f"  Education: {len(education)} entries")
        logger.info(f"  Skills: {sum(len(group['skills']) for group in skills)} skills in {len(skills)} categories")
        logger.info(f"  Certifications: {len(certifications)} entries")
        logger.info(f"  Projects: {len(projects)} entries")
        
        logger.info("\nNEXT STEPS:")
        logger.info("1. Review and edit the CSV files to ensure accuracy")
        logger.info("2. Update the baseline_dataset.json with corrected data")
        logger.info("3. Use the corrected baseline for prompt testing")
        
        return baseline_data

def main():
    """Main function"""
    print("RESUME BASELINE DATA EXTRACTOR")
    print("=" * 50)
    
    try:
        extractor = ResumeBaselineExtractor()
        baseline_data = extractor.create_baseline_dataset()
        
        print("\nBaseline dataset created successfully!")
        print("Files created:")
        print("  - baseline_resume_content.txt")
        print("  - baseline_personal_info.csv")
        print("  - baseline_work_experience.csv")
        print("  - baseline_education.csv")
        print("  - baseline_skills.csv")
        print("  - baseline_certifications.csv")
        print("  - baseline_projects.csv")
        print("  - baseline_summary.csv")
        print("  - baseline_dataset.json")
        
        return True
        
    except Exception as e:
        logger.error(f"Error creating baseline dataset: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 