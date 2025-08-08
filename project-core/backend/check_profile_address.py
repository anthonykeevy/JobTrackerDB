#!/usr/bin/env python3
"""
Script to check ProfileAddress table records
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

def check_profile_address():
    """Check ProfileAddress table records"""
    
    db = SessionLocal()
    
    try:
        print("🔍 Checking ProfileAddress table...")
        
        # Get all ProfileAddress records
        addresses = db.query(ProfileAddress).order_by(ProfileAddress.ProfileAddressID.desc()).all()
        
        if addresses:
            print(f"📊 Found {len(addresses)} ProfileAddress records:")
            print()
            
            for i, address in enumerate(addresses, 1):
                print(f"📍 Address Record #{i} (ID: {address.ProfileAddressID})")
                print(f"   ProfileID: {address.ProfileID}")
                print(f"   Street Number: {address.StreetNumber}")
                print(f"   Street Name: {address.StreetName}")
                print(f"   Street Type: {address.StreetType}")
                print(f"   Unit Number: {address.UnitNumber}")
                print(f"   Unit Type: {address.UnitType}")
                print(f"   Suburb: {address.Suburb}")
                print(f"   State: {address.State}")
                print(f"   Postcode: {address.Postcode}")
                print(f"   Country: {address.Country}")
                print(f"   PropertyID: {address.PropertyID}")
                print(f"   Latitude: {address.Latitude}")
                print(f"   Longitude: {address.Longitude}")
                print(f"   PropertyType: {address.PropertyType}")
                print(f"   LandArea: {address.LandArea}")
                print(f"   FloorArea: {address.FloorArea}")
                print(f"   IsValidated: {address.IsValidated}")
                print(f"   ValidationSource: {address.ValidationSource}")
                print(f"   ConfidenceScore: {address.ConfidenceScore}")
                print(f"   ValidationDate: {address.ValidationDate}")
                print(f"   IsActive: {address.IsActive}")
                print(f"   IsPrimary: {address.IsPrimary}")
                print(f"   AddressType: {address.AddressType}")
                print(f"   CreatedDate: {address.createdDate}")
                print(f"   CreatedBy: {address.createdBy}")
                print(f"   LastUpdated: {address.lastUpdated}")
                print(f"   UpdatedBy: {address.updatedBy}")
                print()
        else:
            print("❌ No ProfileAddress records found")
            
        # Check for active addresses
        active_addresses = db.query(ProfileAddress).filter(ProfileAddress.IsActive == True).all()
        print(f"✅ Active addresses: {len(active_addresses)}")
        
        if active_addresses:
            print("📍 Active Address Details:")
            for addr in active_addresses:
                print(f"   - {addr.StreetNumber} {addr.StreetName} {addr.StreetType}, {addr.Suburb} {addr.State} {addr.Postcode}")
                print(f"     PropertyID: {addr.PropertyID}, CreatedBy: {addr.createdBy}, UpdatedBy: {addr.updatedBy}")
                print()
            
    except Exception as e:
        print(f"❌ Error checking ProfileAddress: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    check_profile_address()
