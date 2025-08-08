#!/usr/bin/env python3
"""
Create UAT user account for regression testing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models import User, Profile
import hashlib
import secrets

# Database connection
DATABASE_URL = "mssql+pyodbc://localhost/JobTrackerDB_Dev?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def hash_password(password: str) -> str:
    """Hash a password using SHA-256 with salt"""
    salt = secrets.token_hex(16)
    hash_obj = hashlib.sha256((password + salt).encode())
    return f"{salt}${hash_obj.hexdigest()}"

def create_uat_user():
    """Create UAT user account"""
    
    db = SessionLocal()
    
    try:
        print("🔧 Creating UAT user account...")
        
        # Check if UAT user already exists
        existing_user = db.query(User).filter(User.EmailAddress == "uat@JobTrackerDB.com").first()
        
        if existing_user:
            print(f"✅ UAT user already exists (ID: {existing_user.UserID})")
            print(f"   Email: {existing_user.EmailAddress}")
            print(f"   Username: {existing_user.Username}")
            return existing_user.UserID
        
        # Create new UAT user
        password = "UAT@JobTrackerDB2025"
        hashed_password = hash_password(password)
        
        uat_user = User(
            EmailAddress="uat@JobTrackerDB.com",
            Username="uat@JobTrackerDB.com",
            HashedPassword=hashed_password,
            IsActive=True,
            createdDate=text("GETDATE()"),
            LastLogin=None
        )
        
        # Create profile for UAT user first
        uat_profile = Profile(
            FirstName="UAT",
            LastName="Tester",
            EmailAddress="uat@JobTrackerDB.com",
            PhoneNumber="",
            DateOfBirth=None,
            CountryOfBirth="",
            CurrentCitizenship="",
            createdDate=text("GETDATE()"),
            lastUpdated=text("GETDATE()")
        )
        
        db.add(uat_profile)
        db.commit()
        db.refresh(uat_profile)
        
        print(f"✅ UAT profile created successfully!")
        print(f"   ProfileID: {uat_profile.ProfileID}")
        
        # Now create user with ProfileID
        uat_user = User(
            EmailAddress="uat@JobTrackerDB.com",
            Username="uat@JobTrackerDB.com",
            HashedPassword=hashed_password,
            IsActive=True,
            ProfileID=uat_profile.ProfileID,
            createdDate=text("GETDATE()"),
            LastLogin=None
        )
        
        db.add(uat_user)
        db.commit()
        db.refresh(uat_user)
        
        print(f"✅ UAT user created successfully!")
        print(f"   UserID: {uat_user.UserID}")
        print(f"   Email: {uat_user.EmailAddress}")
        print(f"   Username: {uat_user.Username}")
        print(f"   Password: {password}")
        print(f"   ProfileID: {uat_user.ProfileID}")
        
        return uat_user.UserID
        
    except Exception as e:
        print(f"❌ Error creating UAT user: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return None
    finally:
        db.close()

if __name__ == "__main__":
    user_id = create_uat_user()
    if user_id:
        print(f"\n🎯 UAT user ready for testing (UserID: {user_id})")
    else:
        print("\n❌ Failed to create UAT user")
