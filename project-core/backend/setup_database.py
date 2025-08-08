#!/usr/bin/env python3
"""
Database Setup Script for JobTrackerDB

This script helps set up the SQL Server database and create initial tables.
Run this after installing SQL Server and the ODBC driver.
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_database():
    """Set up the database and create tables"""
    
    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        print("Please create a .env file with:")
        print("DATABASE_URL=mssql+pyodbc://localhost/JobTrackerDB?driver=ODBC+Driver+17+for+SQL+Server")
        return False
    
    try:
        # Create engine
        print("🔌 Connecting to database...")
        engine = create_engine(database_url, echo=True)
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
        
        # Import models and create tables
        print("📋 Creating tables...")
        from app.models import Base
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully!")
        
        # Create default roles (let database auto-allocate RoleID)
        print("👥 Creating default roles...")
        with engine.connect() as conn:
            # Check if roles already exist
            result = conn.execute(text("SELECT COUNT(*) FROM Role"))
            role_count = result.scalar()
            
            if role_count == 0:
                # Insert default roles (let database auto-allocate RoleID)
                roles = [
                    ("Admin", "Full system administrator", True, 0.00, None, True, True, True, True),
                    ("User", "Standard user", False, 0.00, 10, False, False, False, False),
                    ("Premium", "Premium user with AI features", True, 10.00, None, True, True, False, False)
                ]
                
                for role in roles:
                    conn.execute(text("""
                        INSERT INTO Role (RoleName, Description, IsSubscription, MonthlyCost, 
                                        MaxJobApplications, CanGenerateAIContent, CanViewGamification, 
                                        CanManageUsers, CanAccessAnalytics)
                        VALUES (:name, :desc, :sub, :cost, :max_apps, :ai, :gamification, :manage, :analytics)
                    """), {
                        "name": role[0],
                        "desc": role[1], 
                        "sub": role[2],
                        "cost": role[3],
                        "max_apps": role[4],
                        "ai": role[5],
                        "gamification": role[6],
                        "manage": role[7],
                        "analytics": role[8]
                    })
                
                conn.commit()
                print("✅ Default roles created!")
                
                # Get the RoleID for "User" role to use in user creation
                result = conn.execute(text("SELECT RoleID FROM Role WHERE RoleName = 'User'"))
                user_role_id = result.scalar()
                print(f"✅ User role created with RoleID: {user_role_id}")
                
            else:
                print("ℹ️  Roles already exist, skipping...")
        
        print("\n🎉 Database setup completed successfully!")
        return True
        
    except SQLAlchemyError as e:
        print(f"❌ Database error: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure SQL Server is running")
        print("2. Verify the connection string in your .env file")
        print("3. Ensure the ODBC Driver 17 for SQL Server is installed")
        print("4. Check that the JobTrackerDB database exists")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 JobTrackerDB Database Setup")
    print("=" * 40)
    
    success = setup_database()
    
    if success:
        print("\n✅ Setup completed! You can now start the application.")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")
        sys.exit(1) 