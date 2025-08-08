"""
Check if the new database columns exist
"""
from sqlalchemy import create_engine, text
import os

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "mssql+pyodbc:///?odbc_connect=DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=JobTrackerDB;Trusted_Connection=yes;")

def check_columns():
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        # Check if CountryOfBirth column exists
        result = conn.execute(text("""
            SELECT COUNT(*) as count 
            FROM sys.columns 
            WHERE object_id = OBJECT_ID('Profile') AND name = 'CountryOfBirth'
        """))
        country_exists = result.fetchone()[0] > 0
        
        # Check if CurrentCitizenship column exists
        result = conn.execute(text("""
            SELECT COUNT(*) as count 
            FROM sys.columns 
            WHERE object_id = OBJECT_ID('Profile') AND name = 'CurrentCitizenship'
        """))
        citizenship_exists = result.fetchone()[0] > 0
        
        # Check if ProfileSocialLink table exists
        result = conn.execute(text("""
            SELECT COUNT(*) as count 
            FROM sysobjects 
            WHERE name = 'ProfileSocialLink' AND xtype = 'U'
        """))
        social_link_table_exists = result.fetchone()[0] > 0
        
        # Check if GlobalLinkType table exists
        result = conn.execute(text("""
            SELECT COUNT(*) as count 
            FROM sysobjects 
            WHERE name = 'GlobalLinkType' AND xtype = 'U'
        """))
        global_link_table_exists = result.fetchone()[0] > 0
        
        print("Database Column Check Results:")
        print("=" * 40)
        print(f"CountryOfBirth column exists: {country_exists}")
        print(f"CurrentCitizenship column exists: {citizenship_exists}")
        print(f"ProfileSocialLink table exists: {social_link_table_exists}")
        print(f"GlobalLinkType table exists: {global_link_table_exists}")
        
        if not country_exists or not citizenship_exists:
            print("\n❌ MIGRATION INCOMPLETE - Missing columns!")
            print("The migration script needs to be run again.")
        else:
            print("\n✅ MIGRATION COMPLETE - All columns exist!")

if __name__ == "__main__":
    check_columns()
