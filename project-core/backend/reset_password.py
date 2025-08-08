#!/usr/bin/env python3
"""
Password Reset Script for JobTrackerDB

This script allows you to reset a user's password directly in the database.
Use this for development/testing purposes only.
"""

import os
import sys
import hashlib
import secrets
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def hash_password(password: str) -> str:
    """Hash a password using SHA-256 with salt"""
    salt = secrets.token_hex(16)
    hash_obj = hashlib.sha256((password + salt).encode())
    return f"{salt}${hash_obj.hexdigest()}"

def reset_password(email: str, new_password: str):
    """Reset password for a user"""
    
    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        return False
    
    try:
        # Create engine and session
        engine = create_engine(database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Import models
        from app.models import User
        
        # Find user by email
        user = db.query(User).filter(User.EmailAddress == email).first()
        
        if not user:
            print(f"❌ User with email '{email}' not found")
            return False
        
        # Hash the new password
        hashed_password = hash_password(new_password)
        
        # Update the password
        user.HashedPassword = hashed_password
        db.commit()
        
        print(f"✅ Password successfully reset for user: {email}")
        print(f"   User ID: {user.UserID}")
        print(f"   Username: {user.Username}")
        return True
        
    except Exception as e:
        print(f"❌ Error resetting password: {str(e)}")
        return False
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python reset_password.py <email> <new_password>")
        print("Example: python reset_password.py anthonykeevy@gmail.com '1qazXSW@'")
        sys.exit(1)
    
    email = sys.argv[1]
    new_password = sys.argv[2]
    
    print(f"🔄 Resetting password for: {email}")
    print(f"   New password: {new_password}")
    print("=" * 50)
    
    success = reset_password(email, new_password)
    
    if success:
        print("\n✅ Password reset completed successfully!")
        print("You can now log in with your new password.")
    else:
        print("\n❌ Password reset failed. Please check the error messages above.")
        sys.exit(1) 