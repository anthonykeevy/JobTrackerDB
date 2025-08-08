#!/usr/bin/env python3
"""
Script to check the latest address record in ProfileAddress table
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Database connection
DATABASE_URL = "mssql+pyodbc://localhost/JobTrackerDB_Dev?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def check_latest_address():
    """Check the latest address record in ProfileAddress table"""
    
    db = SessionLocal()
    
    try:
        print("🔍 Checking latest address record in ProfileAddress table...")
        
        # Get the latest record
        result = db.execute(text("""
            SELECT TOP 1 
                ProfileAddressID,
                ProfileID,
                StreetNumber,
                StreetName,
                StreetType,
                Suburb,
                State,
                Postcode,
                Country,
                PropertyID,
                IsValidated,
                ValidationSource,
                IsActive,
                createdDate,
                createdBy,
                lastUpdated,
                updatedBy
            FROM ProfileAddress 
            ORDER BY ProfileAddressID DESC
        """)).fetchone()
        
        if result:
            print("📊 Latest ProfileAddress record:")
            print(f"   ProfileAddressID: {result[0]}")
            print(f"   ProfileID: {result[1]}")
            print(f"   Address: {result[2]} {result[3]} {result[4]}, {result[5]} {result[6]} {result[7]}")
            print(f"   Country: {result[8]}")
            print(f"   PropertyID: {result[9]}")
            print(f"   IsValidated: {result[10]}")
            print(f"   ValidationSource: {result[11]}")
            print(f"   IsActive: {result[12]}")
            print(f"   createdDate: {result[13]}")
            print(f"   createdBy: {result[14]}")
            print(f"   lastUpdated: {result[15]}")
            print(f"   updatedBy: {result[16]}")
            
            print("\n🎯 Audit Field Verification:")
            
            # Check createdDate
            if result[13] is not None:
                print("✅ createdDate: Set correctly")
            else:
                print("❌ createdDate: Should be set")
                
            # Check createdBy
            if result[14] is not None:
                print(f"✅ createdBy: '{result[14]}' (correct)")
            else:
                print("❌ createdBy: Should be set")
                
            # Check lastUpdated
            if result[15] is None:
                print("✅ lastUpdated: NULL (correct for new record)")
            else:
                print(f"❌ lastUpdated: Should be NULL, but is '{result[15]}'")
                
            # Check updatedBy
            if result[16] is None:
                print("✅ updatedBy: NULL (correct for new record)")
            else:
                print(f"❌ updatedBy: Should be NULL, but is '{result[16]}'")
                
            # Check if it's a Geoscape API record
            if result[11] == 'geoscape' and result[14] == 'Geoscape':
                print("✅ Source: Geoscape API (correct audit fields)")
            elif result[14] and result[14] != 'Geoscape':
                print("✅ Source: Manual entry (correct audit fields)")
            else:
                print("⚠️ Source: Unknown (check audit fields)")
                
        else:
            print("❌ No records found in ProfileAddress table")
            
    except Exception as e:
        print(f"❌ Error checking address: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    check_latest_address()
