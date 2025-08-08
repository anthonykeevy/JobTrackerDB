#!/usr/bin/env python3
"""
Script to check user credentials in the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models import User, Profile

# Database connection
DATABASE_URL = "mssql+pyodbc://localhost/JobTrackerDB_Dev?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def check_user_credentials():
    """Check user credentials in the database"""
    
    db = SessionLocal()
    
    try:
        print("🔍 Checking user credentials in database...")
        
        # Get all users
        users = db.query(User).all()
        
        if users:
            print(f"📊 Found {len(users)} users in database:")
            print()
            
            for user in users:
                print(f"👤 User ID: {user.UserID}")
                print(f"   Username: {user.Username}")
                print(f"   Email: {user.EmailAddress}")
                print(f"   IsActive: {user.IsActive}")
                print(f"   ProfileID: {user.ProfileID}")
                print(f"   HashedPassword: {user.HashedPassword[:20]}..." if user.HashedPassword else "   HashedPassword: None")
                print(f"   LastLogin: {user.LastLogin}")
                print(f"   CreatedDate: {user.createdDate}")
                print(f"   CreatedBy: {user.createdBy}")
                print()
        else:
            print("❌ No users found in database")
            
        # Check if there's a test user
        test_user = db.query(User).filter(User.EmailAddress == "test@example.com").first()
        if test_user:
            print("✅ Test user found:")
            print(f"   UserID: {test_user.UserID}")
            print(f"   Username: {test_user.Username}")
            print(f"   Email: {test_user.EmailAddress}")
            print(f"   IsActive: {test_user.IsActive}")
            print(f"   HashedPassword: {test_user.HashedPassword[:20]}..." if test_user.HashedPassword else "   HashedPassword: None")
        else:
            print("❌ Test user (test@example.com) not found")
            
    except Exception as e:
        print(f"❌ Error checking credentials: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    check_user_credentials()
