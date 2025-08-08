#!/usr/bin/env python3
"""
Script to reset the test user password
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models import User
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

def reset_test_user_password():
    """Reset the test user password to 'J0bTr@ck3rDB'"""
    
    db = SessionLocal()
    
    try:
        print("🔧 Resetting test user password...")
        
        # Find the test user
        test_user = db.query(User).filter(User.EmailAddress == "test@example.com").first()
        
        if test_user:
            print(f"✅ Found test user: {test_user.Username}")
            
            # Set password to 'J0bTr@ck3rDB' using the same hashing method as the login system
            new_password = "J0bTr@ck3rDB"
            hashed_password = hash_password(new_password)
            
            # Update the user's password
            test_user.HashedPassword = hashed_password
            test_user.lastUpdated = datetime.utcnow()
            test_user.updatedBy = "system"
            
            db.commit()
            
            print("✅ Password reset successfully!")
            print(f"📋 New credentials:")
            print(f"   Email: test@example.com")
            print(f"   Password: J0bTr@ck3rDB")
            print()
            print("🔐 You can now login with these credentials")
            
        else:
            print("❌ Test user not found")
            
    except Exception as e:
        print(f"❌ Error resetting password: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    from datetime import datetime
    reset_test_user_password()
