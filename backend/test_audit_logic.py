#!/usr/bin/env python3
"""
Test script to verify audit logic for ProfileAddress creation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models import ProfileAddress, Profile, User
import pyodbc

# Database connection
DATABASE_URL = "mssql+pyodbc://localhost/JobTrackerDB_Dev?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_audit_logic():
    """Test the audit logic for ProfileAddress creation"""
    
    db = SessionLocal()
    
    try:
        # Get a test profile
        profile = db.query(Profile).first()
        if not profile:
            print("❌ No profile found in database")
            return
            
        print(f"✅ Found profile: {profile.ProfileID}")
        
        # Test 1: Create a new address with NULL audit fields
        print("\n🧪 Test 1: Creating new address with NULL audit fields")
        
        test_address = ProfileAddress(
            ProfileID=profile.ProfileID,
            StreetName="Test Street",
            Suburb="Test Suburb",
            State="NSW",
            Postcode="2000",
            Country="Australia",
            IsActive=True,
            # Audit fields - should be NULL for new records
            createdDate=datetime.utcnow(),
            createdBy="Test Script",
            lastUpdated=None,  # NULL for new records
            updatedBy=None  # NULL for new records
        )
        
        print(f"🔍 Before save - lastUpdated: {test_address.lastUpdated}")
        print(f"🔍 Before save - updatedBy: {test_address.updatedBy}")
        
        db.add(test_address)
        db.commit()
        
        print(f"🔍 After save - lastUpdated: {test_address.lastUpdated}")
        print(f"🔍 After save - updatedBy: {test_address.updatedBy}")
        
        # Test 2: Check database directly
        print("\n🧪 Test 2: Checking database directly")
        
        # Query the database directly to see what was actually saved
        result = db.execute(text("""
            SELECT TOP 1 
                ProfileAddressID,
                createdDate,
                createdBy,
                lastUpdated,
                updatedBy
            FROM ProfileAddress 
            WHERE ProfileID = :profile_id 
            ORDER BY ProfileAddressID DESC
        """), {"profile_id": profile.ProfileID}).fetchone()
        
        if result:
            print(f"📊 Database values:")
            print(f"   ProfileAddressID: {result[0]}")
            print(f"   createdDate: {result[1]}")
            print(f"   createdBy: {result[2]}")
            print(f"   lastUpdated: {result[3]}")
            print(f"   updatedBy: {result[4]}")
            
            if result[3] is not None:
                print("❌ ISSUE: lastUpdated is NOT NULL for new record!")
            else:
                print("✅ SUCCESS: lastUpdated is NULL for new record")
                
            if result[4] is not None:
                print("❌ ISSUE: updatedBy is NOT NULL for new record!")
            else:
                print("✅ SUCCESS: updatedBy is NULL for new record")
        else:
            print("❌ No address record found in database")
            
        # Clean up test data
        db.delete(test_address)
        db.commit()
        print("\n🧹 Cleaned up test data")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_audit_logic()
