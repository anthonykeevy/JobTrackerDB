#!/usr/bin/env python3
"""
Create Real Baseline Dataset

This script creates a baseline dataset from the actual resume content
extracted from Anthony Keevy's real resume.
"""

import sys
import os
import csv
import json
import logging
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealBaselineCreator:
    """Create baseline dataset from real resume content"""
    
    def __init__(self):
        self.results_dir = Path("real_baseline_results")
        self.results_dir.mkdir(exist_ok=True)
        
    def create_baseline_from_real_resume(self) -> Dict[str, Any]:
        """Create baseline dataset from Anthony's real resume"""
        
        # Personal Info (extracted from resume)
        personal_info = {
            "name": "Anthony Keevy",
            "email": "anthonykeevy@gmail.com",
            "phone": "0414785260",
            "location": "Australia",  # Inferred from context
            "linkedin": "LinkedIn"  # Mentioned in resume
        }
        
        # Professional Summary
        summary = "Results-driven Data & Product Lead with extensive experience spearheading strategic IT transformation, particularly in Data, Automation, and AI. Proven ability to build and scale high-performing teams, design robust data ecosystems, and implement innovative continuous improvement solutions that consistently deliver significant business impact and achieve ambitious organizational goals."
        
        # Work Experience (extracted from resume)
        work_experience = [
            {
                "company": "Inchcape Global",
                "position": "Data Lead and Product Manager",
                "location": "Digital Parts",
                "start_date": "Nov 2022",
                "end_date": "May 2025",
                "description": "Defined and led the enterprise data vision and delivery strategy for PartsLane's B2B e-commerce platform across multiple international markets.",
                "achievements": [
                    "Reduced product categorization effort by 80% through the design and deployment of a machine learning classification model",
                    "Delivered a harmonized multi-country data supply chain, transforming fragmented ERP outputs into a scalable, production-grade ecosystem",
                    "Enabled automated product lifecycle management via rule-based triggers, improving accuracy and reducing manual intervention",
                    "Achieved and maintained EMPS scores >80% while actively representing data in strategic customer forums and onboarding sessions",
                    "Sustained 70% team focus on innovation and platform evolution by implementing a structured pipeline for project prioritization and delivery"
                ],
                "technologies": ["SAP Commerce Cloud", "Machine Learning", "Data Pipelines", "APIs", "SAP ERP", "Autoline DMS"]
            },
            {
                "company": "Inchcape Australia",
                "position": "IT Manager",
                "location": "Peugeot Citroën Australia",
                "start_date": "Dec 2020",
                "end_date": "Jan 2023",
                "description": "Managed all IT systems and services across distribution and retail operations, including ERP, CRM, application development, and vendor relationships.",
                "achievements": [
                    "Delivered improved reporting and operational stability through end-to-end system automation",
                    "Successfully implemented a modern digital portal, streamlining dealer access and communications"
                ],
                "technologies": ["ERP", "CRM", "APIs", "ITIL", "SLA"]
            },
            {
                "company": "Inchcape Australia",
                "position": "Automation Lead",
                "location": "Finance",
                "start_date": "Mar 2020",
                "end_date": "Nov 2020",
                "description": "Established and led a UiPath-based RPA Center of Excellence, defining governance, infrastructure, and delivery frameworks.",
                "achievements": [
                    "Reduced invoice processing effort by 60% through AP automation",
                    "Automated 70% of bank-statement reconciliation using RPA and ML",
                    "Delivered cross-system automation for SAP, Concur, Coupa, and Basware"
                ],
                "technologies": ["UiPath", "RPA", "SAP", "Concur", "Coupa", "Basware", "Machine Learning"]
            },
            {
                "company": "Inchcape Australia",
                "position": "Infrastructure Engineer",
                "location": "IT",
                "start_date": "Feb 2018",
                "end_date": "Feb 2020",
                "description": "Rolled out Office 365 across two major business units (300+ users).",
                "achievements": [
                    "Achieved a 20% telco cost reduction through analytical review and renegotiation",
                    "Improved infrastructure ROI through targeted system reviews"
                ],
                "technologies": ["Office 365", "Cisco", "UiPath"]
            },
            {
                "company": "Dicker Data Ltd",
                "position": "Network & Infrastructure Administrator",
                "location": "ANZ",
                "start_date": "Mar 2015",
                "end_date": "Feb 2018",
                "description": "Managed IT infrastructure and applications for 500 users across 10 sites in ANZ.",
                "achievements": [
                    "Migrated 90% of on-prem servers to a data centre with zero downtime",
                    "Rolled out Office 365 and transitioned workloads to Azure, reducing storage and licensing costs"
                ],
                "technologies": ["Office 365", "Azure", "Data Centre", "Infrastructure"]
            },
            {
                "company": "Fuji Xerox Asia Pacific",
                "position": "IT Manager – Asia Pacific",
                "location": "FXPC",
                "start_date": "Jan 2010",
                "end_date": "Feb 2015",
                "description": "Led all IT services for the Printer Channel across 12 countries and 8 offices, supporting 350 users.",
                "achievements": [
                    "Designed and implemented a custom CRM system for distributor performance, lead tracking, and quote configuration",
                    "Offshored application development to India and outsourced desktop support, reducing costs by 42% and 20% respectively",
                    "Virtualized regional server infrastructure, reducing licensing and power costs by over 30%",
                    "Delivered regional web-based customer portals and operational tools, improving communication efficiency by 50%",
                    "Recognized with the President Club Award (FY2008) for outstanding contribution"
                ],
                "technologies": ["CRM", "Virtualization", "Web Portals", "Infrastructure"]
            },
            {
                "company": "Fuji Xerox Asia Pacific",
                "position": "Supply Chain Project Manager",
                "location": "FXPC",
                "start_date": "Oct 2007",
                "end_date": "Dec 2009",
                "description": "Project managed the regional rollout of Infor Demand Planner across 12 countries.",
                "achievements": [
                    "Delivered a scalable, forecast-driven MRP implementation that significantly improved planning accuracy",
                    "Reduced regional inventory by 40% and streamlined replenishment through enriched data insights"
                ],
                "technologies": ["Infor Demand Planner", "MRP", "Data Architecture"]
            },
            {
                "company": "Fuji Xerox Asia Pacific",
                "position": "Regional Supply Chain Analyst & Demand Planner",
                "location": "FXPC",
                "start_date": "Jan 2005",
                "end_date": "Sep 2007",
                "description": "Developed and deployed automated demand planning tools using Excel and MS Access.",
                "achievements": [
                    "Built and rolled out automated planning solutions to 8 countries, significantly reducing manual workload and improving forecast reliability",
                    "Initiated evaluation of commercial MRP systems, leading to Infor's selection"
                ],
                "technologies": ["Excel", "MS Access", "Demand Planning", "MRP"]
            },
            {
                "company": "Teleperformance Australia",
                "position": "IT Manager",
                "location": "Australia",
                "start_date": "Sep 2002",
                "end_date": "Jan 2005",
                "description": "IT management role at Teleperformance Australia.",
                "achievements": [],
                "technologies": []
            }
        ]
        
        # Education (extracted from resume)
        education = [
            {
                "institution": "UNSW",
                "degree": "Accounting",
                "field_of_study": "Accounting",
                "graduation_date": "2004",
                "gpa": ""
            },
            {
                "institution": "UNSW",
                "degree": "Project Management",
                "field_of_study": "Project Management",
                "graduation_date": "2004",
                "gpa": ""
            },
            {
                "institution": "UNSW",
                "degree": "Marketing for Technical Managers",
                "field_of_study": "Marketing",
                "graduation_date": "2005",
                "gpa": ""
            }
        ]
        
        # Skills (extracted from resume)
        skills = [
            {
                "category": "Strategic Leadership & Management",
                "skills": [
                    "Team Leadership", "Project Management", "Agile", "Waterfall", "SCRUM Master",
                    "Vendor Management", "ITIL", "SDLC", "Process Engineering", "Planning & Budgeting", "Outsourcing"
                ]
            },
            {
                "category": "Data & Analytics",
                "skills": [
                    "Data Strategy", "ETL Pipeline Design", "Data Modeling", "Data Governance", "SQL Server",
                    "Power BI", "Operational Data Warehouses", "Data Analysis", "Reporting", "AI Model Development",
                    "Machine Learning", "Categorization"
                ]
            },
            {
                "category": "Automation & Systems",
                "skills": [
                    "Robotic Process Automation", "RPA", "UiPath", "Power Automate", "API Development",
                    "API Integration", "System Automation", "ERP Systems", "Oracle 11i", "Pronto", "SAP", "AS400",
                    "CRM", "Microsoft CRM", "Salesforce", "MRP", "Infor", "Office 365", "Azure", "AWS", "Zabbix",
                    "VDI", "Apigee"
                ]
            },
            {
                "category": "Key Technologies",
                "skills": [
                    "Python", "SQL Server", "Azure Data Factory", "Databricks", "CI/CD", "UiPath", "Azure",
                    "SSIS", "Power Automate", "Office 365", "SAP", "IDS(AS400)", "ERA", "Autoline",
                    "SAP Commerce cloud", "Emarsys", "Salesforce Marketing Cloud", "Oracle 11i eBS",
                    "BI", "Cognos", "TM1", "Yellowfin", "SSRS", "Microsoft Exchange", "SharePoint", "Lync",
                    ".NET", "Cursor", "ChatGPT Suite", "Loveable", "Gemini Suite"
                ]
            }
        ]
        
        # Certifications (extracted from resume)
        certifications = [
            {
                "name": "T-SQL05 Writing & Queries in SQL Server 2005",
                "issuer": "New Horizons",
                "date_earned": "2008",
                "expiry_date": ""
            },
            {
                "name": "XPPS Operations",
                "issuer": "Xerox Corporation USA",
                "date_earned": "2010",
                "expiry_date": ""
            },
            {
                "name": "XOS Technical Analyst",
                "issuer": "Fuji Xerox Australia",
                "date_earned": "2010",
                "expiry_date": ""
            },
            {
                "name": "SCRUM Master",
                "issuer": "Access Agile",
                "date_earned": "2014",
                "expiry_date": ""
            },
            {
                "name": "Implementing Office 365",
                "issuer": "Microsoft (Certified)",
                "date_earned": "2015",
                "expiry_date": ""
            }
        ]
        
        # Projects (extracted from achievements)
        projects = [
            {
                "name": "Machine Learning Classification Model",
                "description": "Designed and deployed a machine learning classification model for product categorization",
                "achievements": [
                    "Reduced product categorization effort by 80%",
                    "Improved accuracy and reduced manual intervention"
                ],
                "technologies": ["Machine Learning", "Python", "Data Science"],
                "url": ""
            },
            {
                "name": "Multi-Country Data Supply Chain",
                "description": "Delivered a harmonized multi-country data supply chain for PartsLane's B2B e-commerce platform",
                "achievements": [
                    "Transformed fragmented ERP outputs into a scalable, production-grade ecosystem",
                    "Supported real-time product, pricing, and service data flows"
                ],
                "technologies": ["SAP Commerce Cloud", "Data Pipelines", "APIs", "SAP ERP"],
                "url": ""
            },
            {
                "name": "Custom CRM System",
                "description": "Designed and implemented a custom CRM system for distributor performance and lead tracking",
                "achievements": [
                    "Improved visibility of sales pipelines across APAC",
                    "Enhanced quote configuration capabilities"
                ],
                "technologies": ["CRM", "Custom Development", "APAC"],
                "url": ""
            },
            {
                "name": "RPA Center of Excellence",
                "description": "Established and led a UiPath-based RPA Center of Excellence",
                "achievements": [
                    "Reduced invoice processing effort by 60% through AP automation",
                    "Automated 70% of bank-statement reconciliation using RPA and ML"
                ],
                "technologies": ["UiPath", "RPA", "Machine Learning", "SAP", "Concur", "Coupa", "Basware"],
                "url": ""
            }
        ]
        
        # Create baseline dataset
        baseline_data = {
            "personal_info": personal_info,
            "summary": summary,
            "work_experience": work_experience,
            "education": education,
            "skills": skills,
            "certifications": certifications,
            "projects": projects
        }
        
        return baseline_data
    
    def save_baseline_files(self, baseline_data: Dict[str, Any]):
        """Save baseline data to various file formats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON baseline
        json_filename = self.results_dir / f"real_baseline_dataset_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(baseline_data, f, indent=2)
        logger.info(f"Baseline JSON saved to: {json_filename}")
        
        # Save CSV files for each section
        self._save_personal_info_csv(baseline_data['personal_info'], timestamp)
        self._save_work_experience_csv(baseline_data['work_experience'], timestamp)
        self._save_education_csv(baseline_data['education'], timestamp)
        self._save_skills_csv(baseline_data['skills'], timestamp)
        self._save_certifications_csv(baseline_data['certifications'], timestamp)
        self._save_projects_csv(baseline_data['projects'], timestamp)
        self._save_summary_csv(baseline_data['summary'], timestamp)
        
        return json_filename
    
    def _save_personal_info_csv(self, data: Dict[str, Any], timestamp: str):
        """Save personal info to CSV"""
        filename = self.results_dir / f"real_baseline_personal_info_{timestamp}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Field', 'Value', 'Source', 'Notes'])
            for field, value in data.items():
                writer.writerow([field, value, 'Resume', ''])
        logger.info(f"Personal info CSV saved to: {filename}")
    
    def _save_work_experience_csv(self, data: List[Dict[str, Any]], timestamp: str):
        """Save work experience to CSV"""
        filename = self.results_dir / f"real_baseline_work_experience_{timestamp}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Company', 'Position', 'Location', 'Start_Date', 'End_Date', 
                           'Description', 'Achievements', 'Technologies', 'Source', 'Notes'])
            
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
                    'Resume',
                    ''
                ])
        logger.info(f"Work experience CSV saved to: {filename}")
    
    def _save_education_csv(self, data: List[Dict[str, Any]], timestamp: str):
        """Save education to CSV"""
        filename = self.results_dir / f"real_baseline_education_{timestamp}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Institution', 'Degree', 'Field_of_Study', 'Graduation_Date', 
                           'GPA', 'Source', 'Notes'])
            
            for edu in data:
                writer.writerow([
                    edu.get('institution', ''),
                    edu.get('degree', ''),
                    edu.get('field_of_study', ''),
                    edu.get('graduation_date', ''),
                    edu.get('gpa', ''),
                    'Resume',
                    ''
                ])
        logger.info(f"Education CSV saved to: {filename}")
    
    def _save_skills_csv(self, data: List[Dict[str, Any]], timestamp: str):
        """Save skills to CSV"""
        filename = self.results_dir / f"real_baseline_skills_{timestamp}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Category', 'Skill', 'Source', 'Notes'])
            
            for skill_group in data:
                category = skill_group.get('category', '')
                for skill in skill_group.get('skills', []):
                    writer.writerow([category, skill, 'Resume', ''])
        logger.info(f"Skills CSV saved to: {filename}")
    
    def _save_certifications_csv(self, data: List[Dict[str, Any]], timestamp: str):
        """Save certifications to CSV"""
        filename = self.results_dir / f"real_baseline_certifications_{timestamp}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Issuer', 'Date_Earned', 'Expiry_Date', 'Source', 'Notes'])
            
            for cert in data:
                writer.writerow([
                    cert.get('name', ''),
                    cert.get('issuer', ''),
                    cert.get('date_earned', ''),
                    cert.get('expiry_date', ''),
                    'Resume',
                    ''
                ])
        logger.info(f"Certifications CSV saved to: {filename}")
    
    def _save_projects_csv(self, data: List[Dict[str, Any]], timestamp: str):
        """Save projects to CSV"""
        filename = self.results_dir / f"real_baseline_projects_{timestamp}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Description', 'Achievements', 'Technologies', 
                           'URL', 'Source', 'Notes'])
            
            for project in data:
                achievements = '; '.join(project.get('achievements', []))
                technologies = '; '.join(project.get('technologies', []))
                writer.writerow([
                    project.get('name', ''),
                    project.get('description', ''),
                    achievements,
                    technologies,
                    project.get('url', ''),
                    'Resume',
                    ''
                ])
        logger.info(f"Projects CSV saved to: {filename}")
    
    def _save_summary_csv(self, summary: str, timestamp: str):
        """Save summary to CSV"""
        filename = self.results_dir / f"real_baseline_summary_{timestamp}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Summary', 'Source', 'Notes'])
            writer.writerow([summary, 'Resume', ''])
        logger.info(f"Summary CSV saved to: {filename}")
    
    def create_summary_report(self, baseline_data: Dict[str, Any], json_file: Path):
        """Create a summary report of the baseline dataset"""
        summary = {
            "baseline_creation_timestamp": datetime.now().isoformat(),
            "source_resume": "Anthony Keevy Resume 202506.docx",
            "dataset_summary": {
                "personal_info_fields": len(baseline_data['personal_info']),
                "work_experience_entries": len(baseline_data['work_experience']),
                "education_entries": len(baseline_data['education']),
                "skills_categories": len(baseline_data['skills']),
                "total_skills": sum(len(group['skills']) for group in baseline_data['skills']),
                "certifications_entries": len(baseline_data['certifications']),
                "projects_entries": len(baseline_data['projects']),
                "summary_length": len(baseline_data['summary'])
            },
            "files_created": [
                str(json_file),
                str(self.results_dir / "*.csv")
            ],
            "usage_instructions": [
                "1. This baseline represents the 'ground truth' extracted from Anthony's real resume",
                "2. Use this baseline to test AI prompt effectiveness",
                "3. Compare AI extraction results against this baseline to measure accuracy",
                "4. Update this baseline if you find any errors or missing information"
            ]
        }
        
        summary_file = self.results_dir / "baseline_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Baseline summary saved to: {summary_file}")
        return summary

def main():
    """Main function"""
    print("REAL BASELINE DATASET CREATOR")
    print("=" * 50)
    
    try:
        creator = RealBaselineCreator()
        
        # Create baseline from real resume
        baseline_data = creator.create_baseline_from_real_resume()
        
        # Save files
        json_file = creator.save_baseline_files(baseline_data)
        
        # Create summary
        summary = creator.create_summary_report(baseline_data, json_file)
        
        print("\nReal Baseline Dataset Created Successfully!")
        print("=" * 50)
        print(f"Source: Anthony Keevy Resume 202506.docx")
        print(f"Results Directory: {creator.results_dir}")
        print(f"Main JSON File: {json_file}")
        
        print("\nDataset Summary:")
        print(f"  Personal Info: {summary['dataset_summary']['personal_info_fields']} fields")
        print(f"  Work Experience: {summary['dataset_summary']['work_experience_entries']} entries")
        print(f"  Education: {summary['dataset_summary']['education_entries']} entries")
        print(f"  Skills: {summary['dataset_summary']['total_skills']} skills in {summary['dataset_summary']['skills_categories']} categories")
        print(f"  Certifications: {summary['dataset_summary']['certifications_entries']} entries")
        print(f"  Projects: {summary['dataset_summary']['projects_entries']} entries")
        print(f"  Summary: {summary['dataset_summary']['summary_length']} characters")
        
        print("\nNEXT STEPS:")
        print("1. Review the CSV files to ensure accuracy")
        print("2. Use this baseline for AI prompt effectiveness testing")
        print("3. Run comparison tests against this baseline")
        
        return True
        
    except Exception as e:
        logger.error(f"Error creating real baseline dataset: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 