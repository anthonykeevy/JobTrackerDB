#!/usr/bin/env python3
"""
Comprehensive test script for resume upload and data saving process
Tests the complete workflow from resume parsing to database saving
"""
import asyncio
import sys
import os
import json
from pathlib import Path

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.api.resume import parse_resume_with_ai
from app.models import get_db
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_test_resume_content():
    """Get test resume content for Anthony Keevy"""
    return """
    ANTHONY KEEVY
    Software Engineer & Technical Lead
    Email: anthony.keevy@example.com
    Phone: +61 400 123 456
    Location: Sydney, NSW, Australia
    LinkedIn: linkedin.com/in/anthonykeevy
    
    SUMMARY
    Experienced software engineer with 15+ years in full-stack development, technical leadership, and cloud architecture. 
    Specialized in Python, React, AWS, and microservices. Proven track record of delivering scalable solutions and leading development teams.
    
    WORK EXPERIENCE
    
    Senior Software Engineer
    TechCorp Australia | Sydney, NSW | 2022 - Present
    • Led development of microservices architecture using Python, FastAPI, and AWS
    • Implemented CI/CD pipelines reducing deployment time by 60%
    • Mentored 5 junior developers and conducted code reviews
    • Technologies: Python, FastAPI, React, AWS, Docker, Kubernetes
    
    Technical Lead
    Digital Solutions Inc | Melbourne, VIC | 2020 - 2022
    • Managed team of 8 developers across multiple projects
    • Designed and implemented scalable REST APIs
    • Reduced system downtime by 40% through improved monitoring
    • Technologies: Java, Spring Boot, Angular, Azure, SQL Server
    
    Full Stack Developer
    WebTech Solutions | Brisbane, QLD | 2018 - 2020
    • Developed responsive web applications using modern frameworks
    • Implemented automated testing increasing code coverage to 85%
    • Collaborated with UX/UI designers to improve user experience
    • Technologies: JavaScript, React, Node.js, MongoDB, AWS
    
    Software Developer
    StartupXYZ | Sydney, NSW | 2016 - 2018
    • Built MVP applications for startup clients
    • Implemented real-time features using WebSockets
    • Optimized database queries improving performance by 50%
    • Technologies: Python, Django, JavaScript, PostgreSQL
    
    Junior Developer
    CodeWorks | Melbourne, VIC | 2014 - 2016
    • Developed web applications using PHP and MySQL
    • Created responsive designs using HTML, CSS, and JavaScript
    • Participated in agile development processes
    • Technologies: PHP, MySQL, HTML, CSS, JavaScript
    
    EDUCATION
    
    Master of Information Technology
    University of Technology Sydney | 2012 - 2014
    • Specialization in Software Engineering
    • GPA: 6.2/7.0
    • Thesis: "Scalable Microservices Architecture for E-commerce Platforms"
    
    Bachelor of Computer Science
    University of Melbourne | 2009 - 2012
    • Major in Software Engineering
    • Minor in Mathematics
    • GPA: 6.5/7.0
    
    Diploma of Information Technology
    TAFE NSW | 2008 - 2009
    • Web Development Specialization
    • Distinction Average
    
    CERTIFICATIONS
    
    AWS Certified Solutions Architect - Associate
    Amazon Web Services | 2023
    • Valid until: 2026
    
    Microsoft Certified: Azure Developer Associate
    Microsoft | 2022
    • Valid until: 2025
    
    Google Cloud Professional Cloud Developer
    Google Cloud | 2021
    • Valid until: 2024
    
    SKILLS
    
    Programming Languages: Python, JavaScript, TypeScript, Java, C#, PHP, SQL
    Frontend: React, Angular, Vue.js, HTML5, CSS3, SASS, Bootstrap
    Backend: FastAPI, Django, Spring Boot, Node.js, Express.js
    Databases: PostgreSQL, MySQL, MongoDB, Redis, SQL Server
    Cloud Platforms: AWS, Azure, Google Cloud Platform
    DevOps: Docker, Kubernetes, Jenkins, GitLab CI/CD, Terraform
    Tools: Git, VS Code, IntelliJ IDEA, Postman, Jira, Confluence
    Methodologies: Agile, Scrum, Kanban, TDD, BDD
    
    PROJECTS
    
    E-commerce Platform
    • Built scalable e-commerce platform using microservices architecture
    • Implemented real-time inventory management and payment processing
    • Technologies: Python, FastAPI, React, PostgreSQL, Redis, AWS
    
    Real-time Chat Application
    • Developed real-time chat application with WebSocket support
    • Features: group chats, file sharing, message encryption
    • Technologies: Node.js, Socket.io, React, MongoDB, Redis
    
    Task Management System
    • Created comprehensive task management system for enterprise clients
    • Features: project tracking, team collaboration, reporting dashboard
    • Technologies: Java, Spring Boot, Angular, MySQL, Docker
    
    LANGUAGES
    
    English: Native
    Spanish: Intermediate
    French: Basic
    
    INTERESTS
    
    • Open source contribution
    • Technical writing and blogging
    • Machine learning and AI
    • Cloud architecture and DevOps
    • Mentoring and teaching
    """

async def test_resume_parsing():
    """Test the resume parsing functionality"""
    print("🔍 Testing Resume Parsing...")
    
    try:
        # Get test resume content
        resume_content = get_test_resume_content()
        
        # Test AI parsing
        print("📝 Testing AI resume parsing...")
        extracted_data = await parse_resume_with_ai(resume_content, user_id=1)
        
        print("✅ Resume parsing successful!")
        print(f"📊 Extracted data summary:")
        print(f"   - Personal Info: {bool(extracted_data.get('personal_info'))}")
        print(f"   - Work Experience: {len(extracted_data.get('work_experience', []))} entries")
        print(f"   - Education: {len(extracted_data.get('education', []))} entries")
        print(f"   - Skills: {len(extracted_data.get('skills', []))} categories")
        print(f"   - Certifications: {len(extracted_data.get('certifications', []))} entries")
        print(f"   - Projects: {len(extracted_data.get('projects', []))} entries")
        
        return extracted_data
        
    except Exception as e:
        print(f"❌ Resume parsing failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_database_save(extracted_data):
    """Test saving the extracted data to database"""
    print("\n💾 Testing Database Save...")
    
    try:
        # Database connection
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            print("❌ DATABASE_URL not found in environment variables")
            return False
        
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Get current counts before save
            print("📊 Current database state:")
            
            result = conn.execute(text("SELECT COUNT(*) as count FROM Profile"))
            profile_count_before = result.fetchone()[0]
            print(f"   - Profiles: {profile_count_before}")
            
            result = conn.execute(text("SELECT COUNT(*) as count FROM ProfileWorkExperience"))
            work_exp_count_before = result.fetchone()[0]
            print(f"   - Work Experiences: {work_exp_count_before}")
            
            result = conn.execute(text("SELECT COUNT(*) as count FROM ProfileEducation"))
            education_count_before = result.fetchone()[0]
            print(f"   - Education Records: {education_count_before}")
            
            result = conn.execute(text("SELECT COUNT(*) as count FROM Skills"))
            skills_count_before = result.fetchone()[0]
            print(f"   - Skills: {skills_count_before}")
            
            result = conn.execute(text("SELECT COUNT(*) as count FROM ProfileCertification"))
            cert_count_before = result.fetchone()[0]
            print(f"   - Certifications: {cert_count_before}")
            
            # Test the save endpoint via HTTP request
            import httpx
            import asyncio
            
            async def test_save_endpoint():
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        "http://localhost:8000/api/v1/resume/save-first",
                        json={
                            "user_id": 1,
                            "resume_data": extracted_data
                        },
                        timeout=30.0
                    )
                    return response
            
            # Run the async test
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(test_save_endpoint())
            loop.close()
            
            if response.status_code == 200:
                print("✅ Save endpoint test successful!")
                save_result = response.json()
                print(f"📋 Save result: {save_result.get('message', 'Unknown')}")
                
                # Check database after save
                print("\n📊 Database state after save:")
                
                result = conn.execute(text("SELECT COUNT(*) as count FROM Profile"))
                profile_count_after = result.fetchone()[0]
                print(f"   - Profiles: {profile_count_after} (was {profile_count_before})")
                
                result = conn.execute(text("SELECT COUNT(*) as count FROM ProfileWorkExperience"))
                work_exp_count_after = result.fetchone()[0]
                print(f"   - Work Experiences: {work_exp_count_after} (was {work_exp_count_before})")
                
                result = conn.execute(text("SELECT COUNT(*) as count FROM ProfileEducation"))
                education_count_after = result.fetchone()[0]
                print(f"   - Education Records: {education_count_after} (was {education_count_before})")
                
                result = conn.execute(text("SELECT COUNT(*) as count FROM Skills"))
                skills_count_after = result.fetchone()[0]
                print(f"   - Skills: {skills_count_after} (was {skills_count_before})")
                
                result = conn.execute(text("SELECT COUNT(*) as count FROM ProfileCertification"))
                cert_count_after = result.fetchone()[0]
                print(f"   - Certifications: {cert_count_after} (was {cert_count_before})")
                
                # Check if data was actually saved
                if (work_exp_count_after > work_exp_count_before or 
                    education_count_after > education_count_before or 
                    skills_count_after > skills_count_before):
                    print("✅ Data was successfully saved to database!")
                    return True
                else:
                    print("⚠️  No new data was saved to database")
                    return False
                    
            else:
                print(f"❌ Save endpoint test failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Database save test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ai_cost_tracking():
    """Test AI cost tracking functionality"""
    print("\n💰 Testing AI Cost Tracking...")
    
    try:
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            print("❌ DATABASE_URL not found in environment variables")
            return False
        
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Check for AI usage records
            result = conn.execute(text("SELECT COUNT(*) as count FROM APIUsageTracking WHERE APIProvider = 'openai'"))
            ai_usage_count = result.fetchone()[0]
            print(f"📊 AI Usage Records: {ai_usage_count}")
            
            if ai_usage_count > 0:
                # Get recent AI usage
                result = conn.execute(text("""
                    SELECT TOP 5 UserID, APIEndpoint, CallCount, CreditCost, ResponseStatus, RequestData
                    FROM APIUsageTracking 
                    WHERE APIProvider = 'openai' 
                    ORDER BY APIUsageID DESC
                """))
                recent_usage = result.fetchall()
                
                print("📋 Recent AI Usage:")
                for usage in recent_usage:
                    print(f"   - User: {usage[0]}, Endpoint: {usage[1]}, Cost: ${usage[3]}, Status: {usage[4]}")
                
                return True
            else:
                print("⚠️  No AI usage records found")
                return False
                
    except Exception as e:
        print(f"❌ AI cost tracking test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function"""
    print("🧪 COMPREHENSIVE RESUME UPLOAD TEST")
    print("=" * 50)
    
    # Test 1: Resume Parsing
    extracted_data = await test_resume_parsing()
    if not extracted_data:
        print("❌ Resume parsing test failed. Stopping tests.")
        return
    
    # Test 2: Database Save
    save_success = test_database_save(extracted_data)
    
    # Test 3: AI Cost Tracking
    cost_tracking_success = test_ai_cost_tracking()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)
    print(f"✅ Resume Parsing: {'PASS' if extracted_data else 'FAIL'}")
    print(f"✅ Database Save: {'PASS' if save_success else 'FAIL'}")
    print(f"✅ AI Cost Tracking: {'PASS' if cost_tracking_success else 'FAIL'}")
    
    if extracted_data and save_success and cost_tracking_success:
        print("\n🎉 ALL TESTS PASSED! Resume upload workflow is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the logs above.")

if __name__ == "__main__":
    asyncio.run(main()) 