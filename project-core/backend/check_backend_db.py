"""
Check which database the backend is connecting to
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Check environment variables
print("Backend Database Connection Check:")
print("=" * 40)
print(f"DATABASE_URL from env: {os.getenv('DATABASE_URL')}")

# Check if .env file exists
if os.path.exists('.env'):
    print("✅ .env file exists")
    with open('.env', 'r') as f:
        print("Contents of .env file:")
        for line in f:
            if 'DATABASE_URL' in line:
                print(f"  {line.strip()}")
else:
    print("❌ .env file not found")

# Check default connection string
default_url = "mssql+pyodbc:///?odbc_connect=DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=JobTrackerDB;Trusted_Connection=yes;"
print(f"\nDefault URL used by migration: {default_url}")

# Test both connections
from sqlalchemy import create_engine, text

def test_connection(url, name):
    try:
        engine = create_engine(url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT DB_NAME() as db_name"))
            db_name = result.fetchone()[0]
            print(f"✅ {name} connects to: {db_name}")
            
            # Check if Profile table has the new columns
            result = conn.execute(text("""
                SELECT COUNT(*) as count 
                FROM sys.columns 
                WHERE object_id = OBJECT_ID('Profile') AND name = 'CountryOfBirth'
            """))
            country_exists = result.fetchone()[0] > 0
            print(f"   CountryOfBirth column exists: {country_exists}")
            
            result = conn.execute(text("""
                SELECT COUNT(*) as count 
                FROM sys.columns 
                WHERE object_id = OBJECT_ID('Profile') AND name = 'CurrentCitizenship'
            """))
            citizenship_exists = result.fetchone()[0] > 0
            print(f"   CurrentCitizenship column exists: {citizenship_exists}")
            
    except Exception as e:
        print(f"❌ {name} connection failed: {str(e)}")

print("\nTesting connections:")
test_connection(os.getenv("DATABASE_URL"), "Backend DATABASE_URL")
test_connection(default_url, "Migration default URL")
