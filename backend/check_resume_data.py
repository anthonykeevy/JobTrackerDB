#!/usr/bin/env python3
"""
Check Resume Data Script
This script checks if resume data was successfully saved to the database.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

def check_resume_data():
    """Check if resume data was saved to the database"""
    
    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        return False
    
    try:
        # Create engine
        print("🔌 Connecting to database...")
        engine = create_engine(database_url, echo=False)
        
        # Test connection
        with engine.connect() as conn:
            print("✅ Database connection successful!")
            
            # Check Profile table
            result = conn.execute(text("SELECT COUNT(*) FROM Profile"))
            profile_count = result.scalar()
            print(f"📋 Total Profiles: {profile_count}")
            
            # Check ProfileWorkExperience table
            result = conn.execute(text("SELECT COUNT(*) FROM ProfileWorkExperience"))
            work_exp_count = result.scalar()
            print(f"💼 Work Experience Entries: {work_exp_count}")
            
            # Check ProfileEducation table
            result = conn.execute(text("SELECT COUNT(*) FROM ProfileEducation"))
            education_count = result.scalar()
            print(f"🎓 Education Entries: {education_count}")
            
            # Check ProfileCertification table
            result = conn.execute(text("SELECT COUNT(*) FROM ProfileCertification"))
            cert_count = result.scalar()
            print(f"🏆 Certification Entries: {cert_count}")
            
            # Check Skills table
            result = conn.execute(text("SELECT COUNT(*) FROM Skills"))
            skills_count = result.scalar()
            print(f"🛠️ Skills Entries: {skills_count}")
            
            # Check Resume table
            result = conn.execute(text("SELECT COUNT(*) FROM Resume"))
            resume_count = result.scalar()
            print(f"📄 Resume Files: {resume_count}")
            
            # Get Profile table structure
            result = conn.execute(text("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'Profile' 
                ORDER BY ORDINAL_POSITION
            """))
            columns = [row[0] for row in result.fetchall()]
            print(f"\n📋 Profile table columns: {', '.join(columns)}")
            
            # Get latest profile details (using available columns)
            if profile_count > 0:
                result = conn.execute(text("""
                    SELECT TOP 1 p.ProfileID, p.FirstName, p.LastName
                    FROM Profile p 
                    ORDER BY p.ProfileID DESC
                """))
                latest_profile = result.fetchone()
                
                if latest_profile:
                    print(f"\n📝 Latest Profile:")
                    print(f"   Profile ID: {latest_profile[0]}")
                    print(f"   Name: {latest_profile[1]} {latest_profile[2]}")
            
            # Check if there's any data from resume parsing
            if work_exp_count > 0 or education_count > 0 or cert_count > 0 or skills_count > 0:
                print("\n✅ Resume data appears to have been saved successfully!")
                return True
            else:
                print("\n⚠️ No resume data found in database.")
                return False
                
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Checking Resume Data in Database")
    print("=" * 40)
    
    success = check_resume_data()
    
    if success:
        print("\n✅ Resume data check completed successfully!")
    else:
        print("\n❌ Resume data check failed or no data found.") 