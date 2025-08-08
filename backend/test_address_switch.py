#!/usr/bin/env python3
"""
Test script to verify address switch audit logic
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models import ProfileAddress, Profile, User

# Database connection
DATABASE_URL = "mssql+pyodbc://localhost/JobTrackerDB_Dev?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_address_switch_audit():
    """Test the address switch audit logic"""
    
    db = SessionLocal()
    
    try:
        print("🔍 Testing address switch audit logic...")
        
        # Get all ProfileAddress records for ProfileID 1
        addresses = db.query(ProfileAddress).filter(
            ProfileAddress.ProfileID == 1
        ).order_by(ProfileAddress.ProfileAddressID.desc()).all()
        
        if addresses:
            print(f"📊 Found {len(addresses)} ProfileAddress records for ProfileID 1:")
            print()
            
            for i, address in enumerate(addresses, 1):
                print(f"📍 Address Record #{i} (ID: {address.ProfileAddressID})")
                print(f"   Address: {address.StreetNumber} {address.StreetName} {address.StreetType}, {address.Suburb} {address.State} {address.Postcode}")
                print(f"   PropertyID: {address.PropertyID}")
                print(f"   IsActive: {address.IsActive}")
                print(f"   CreatedBy: {address.createdBy}")
                print(f"   LastUpdated: {address.lastUpdated}")
                print(f"   UpdatedBy: {address.updatedBy}")
                print()
                
                # Check if this is a deactivated address
                if not address.IsActive and address.updatedBy:
                    if address.updatedBy == "Geoscape":
                        print(f"❌ ISSUE: Address {address.ProfileAddressID} deactivated by 'Geoscape' - should be user")
                    elif "test@example.com" in address.updatedBy:
                        print(f"✅ CORRECT: Address {address.ProfileAddressID} deactivated by user")
                    else:
                        print(f"⚠️ UNKNOWN: Address {address.ProfileAddressID} deactivated by '{address.updatedBy}'")
                print()
        else:
            print("❌ No ProfileAddress records found")
            
    except Exception as e:
        print(f"❌ Error testing address switch audit: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_address_switch_audit()
