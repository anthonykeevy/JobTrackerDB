#!/usr/bin/env python3
"""
Script to truncate the ProfileAddress table
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

def truncate_profile_address():
    """Truncate the ProfileAddress table"""
    
    db = SessionLocal()
    
    try:
        print("🧹 Truncating ProfileAddress table...")
        
        # First, let's see how many records we have
        count_result = db.execute(text("SELECT COUNT(*) FROM ProfileAddress")).fetchone()
        record_count = count_result[0] if count_result else 0
        
        print(f"📊 Found {record_count} records in ProfileAddress table")
        
        if record_count > 0:
            # Truncate the table
            db.execute(text("TRUNCATE TABLE ProfileAddress"))
            db.commit()
            
            # Verify the table is empty
            verify_result = db.execute(text("SELECT COUNT(*) FROM ProfileAddress")).fetchone()
            verify_count = verify_result[0] if verify_result else 0
            
            if verify_count == 0:
                print("✅ ProfileAddress table successfully truncated")
                print(f"📊 Table now contains {verify_count} records")
            else:
                print(f"❌ Error: Table still contains {verify_count} records")
        else:
            print("ℹ️ ProfileAddress table is already empty")
            
    except Exception as e:
        print(f"❌ Error truncating table: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    truncate_profile_address()
