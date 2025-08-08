#!/usr/bin/env python3
"""
Script to check if resume extracted data has been saved to the database
"""
import sys
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_resume_data_saved():
    """Check if resume data has been saved to the database"""
    
    # Database connection
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        return
    
    try:
        engine = create_engine(database_url)
        print("✅ Connected to database successfully")
        
        with engine.connect() as conn:
            print("\n🔍 Checking Profile Table...")
            result = conn.execute(text("SELECT COUNT(*) as count FROM Profile"))
            profile_count = result.fetchone()[0]
            print(f"   📊 Total Profiles: {profile_count}")
            
            if profile_count > 0:
                result = conn.execute(text("SELECT TOP 5 * FROM Profile"))
                profiles = result.fetchall()
                print("   📋 Sample Profile Data:")
                for profile in profiles:
                    print(f"      - ProfileID: {profile[0]}, Name: {profile[1]} {profile[2]}, Email: {profile[3]}")
            
            print("\n🔍 Checking ProfileWorkExperience Table...")
            result = conn.execute(text("SELECT COUNT(*) as count FROM ProfileWorkExperience"))
            work_exp_count = result.fetchone()[0]
            print(f"   📊 Total Work Experiences: {work_exp_count}")
            
            if work_exp_count > 0:
                result = conn.execute(text("SELECT TOP 3 * FROM ProfileWorkExperience"))
                work_exps = result.fetchall()
                print("   📋 Sample Work Experience Data:")
                for exp in work_exps:
                    print(f"      - Company: {exp[2]}, Position: {exp[3]}, Start: {exp[4]}, End: {exp[5]}")
            
            print("\n🔍 Checking ProfileEducation Table...")
            result = conn.execute(text("SELECT COUNT(*) as count FROM ProfileEducation"))
            education_count = result.fetchone()[0]
            print(f"   📊 Total Education Records: {education_count}")
            
            if education_count > 0:
                result = conn.execute(text("SELECT TOP 3 * FROM ProfileEducation"))
                educations = result.fetchall()
                print("   📋 Sample Education Data:")
                for edu in educations:
                    print(f"      - Institution: {edu[2]}, Degree: {edu[3]}, Field: {edu[4]}")
            
            print("\n🔍 Checking Skills Table...")
            result = conn.execute(text("SELECT COUNT(*) as count FROM Skills"))
            skills_count = result.fetchone()[0]
            print(f"   📊 Total Skills: {skills_count}")
            
            if skills_count > 0:
                result = conn.execute(text("SELECT TOP 10 SkillName FROM Skills"))
                skills = result.fetchall()
                print("   📋 Sample Skills:")
                for skill in skills:
                    print(f"      - {skill[0]}")
            
            print("\n🔍 Checking ProfileCertification Table...")
            result = conn.execute(text("SELECT COUNT(*) as count FROM ProfileCertification"))
            cert_count = result.fetchone()[0]
            print(f"   📊 Total Certifications: {cert_count}")
            
            if cert_count > 0:
                result = conn.execute(text("SELECT TOP 3 * FROM ProfileCertification"))
                certs = result.fetchall()
                print("   📋 Sample Certification Data:")
                for cert in certs:
                    print(f"      - Name: {cert[2]}, Issuer: {cert[3]}")
            
            print("\n🔍 Checking Resume Table...")
            result = conn.execute(text("SELECT COUNT(*) as count FROM Resume"))
            resume_count = result.fetchone()[0]
            print(f"   📊 Total Resume Files: {resume_count}")
            
            print("\n🔍 Checking APIUsageTracking Table...")
            result = conn.execute(text("SELECT COUNT(*) as count FROM APIUsageTracking"))
            api_count = result.fetchone()[0]
            print(f"   📊 Total API Usage Records: {api_count}")
            
            if api_count > 0:
                result = conn.execute(text("SELECT TOP 3 * FROM APIUsageTracking WHERE APIProvider = 'openai'"))
                api_records = result.fetchall()
                print("   📋 Sample AI Usage Data:")
                for record in api_records:
                    print(f"      - User: {record[1]}, Operation: {record[3]}, Cost: ${record[5]}")
            
            # Summary
            print("\n" + "="*50)
            print("📊 SUMMARY OF EXTRACTED DATA")
            print("="*50)
            print(f"✅ Profiles: {profile_count}")
            print(f"✅ Work Experiences: {work_exp_count}")
            print(f"✅ Education Records: {education_count}")
            print(f"✅ Skills: {skills_count}")
            print(f"✅ Certifications: {cert_count}")
            print(f"✅ Resume Files: {resume_count}")
            print(f"✅ AI Usage Records: {api_count}")
            
            # Check if data matches the screenshot
            print("\n" + "="*50)
            print("🎯 COMPARISON WITH SCREENSHOT")
            print("="*50)
            print("Screenshot showed:")
            print("   - 9 work experiences")
            print("   - 8 education records")
            print("   - 30 skills across 1 category")
            print("   - Personal information extracted")
            
            print(f"\nDatabase has:")
            print(f"   - {work_exp_count} work experiences {'✅' if work_exp_count >= 9 else '❌'}")
            print(f"   - {education_count} education records {'✅' if education_count >= 8 else '❌'}")
            print(f"   - {skills_count} skills {'✅' if skills_count >= 30 else '❌'}")
            print(f"   - {profile_count} profiles with personal info {'✅' if profile_count > 0 else '❌'}")
            
            if work_exp_count >= 9 and education_count >= 8 and skills_count >= 30 and profile_count > 0:
                print("\n🎉 SUCCESS: All extracted data appears to be saved to the database!")
            else:
                print("\n⚠️  WARNING: Some data may not have been saved properly.")
                
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_resume_data_saved() 