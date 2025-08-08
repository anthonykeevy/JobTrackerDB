"""
Migration script to add social links functionality and reorganize profile structure
"""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "mssql+pyodbc://localhost/JobTrackerDB_Dev?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes")

def run_migration():
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        # Create ProfileSocialLink table
        conn.execute(text("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='ProfileSocialLink' AND xtype='U')
            CREATE TABLE ProfileSocialLink (
                ProfileSocialLinkID INT IDENTITY(1,1) PRIMARY KEY,
                ProfileID INT NOT NULL,
                LinkName NVARCHAR(100) NOT NULL,
                LinkURL NVARCHAR(500) NOT NULL,
                LinkType NVARCHAR(50),
                LinkIcon NVARCHAR(100),
                IsApproved BIT DEFAULT 0,
                IsActive BIT DEFAULT 1,
                IsPublic BIT DEFAULT 1,
                createdDate DATETIME DEFAULT GETDATE(),
                createdBy NVARCHAR(100),
                lastUpdated DATETIME,
                updatedBy NVARCHAR(100),
                FOREIGN KEY (ProfileID) REFERENCES Profile(ProfileID)
            )
        """))
        
        # Create GlobalLinkType table
        conn.execute(text("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='GlobalLinkType' AND xtype='U')
            CREATE TABLE GlobalLinkType (
                GlobalLinkTypeID INT IDENTITY(1,1) PRIMARY KEY,
                LinkName NVARCHAR(100) NOT NULL UNIQUE,
                LinkType NVARCHAR(50) NOT NULL,
                LinkIcon NVARCHAR(100),
                DisplayOrder INT DEFAULT 999,
                IsActive BIT DEFAULT 1,
                createdDate DATETIME DEFAULT GETDATE(),
                createdBy NVARCHAR(100),
                lastUpdated DATETIME,
                updatedBy NVARCHAR(100)
            )
        """))
        
        # Add new columns to Profile table
        conn.execute(text("""
            IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('Profile') AND name = 'CountryOfBirth')
            ALTER TABLE Profile ADD CountryOfBirth NVARCHAR(100)
        """))
        
        conn.execute(text("""
            IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('Profile') AND name = 'CurrentCitizenship')
            ALTER TABLE Profile ADD CurrentCitizenship NVARCHAR(100)
        """))
        
        # Insert default global link types
        conn.execute(text("""
            IF NOT EXISTS (SELECT * FROM GlobalLinkType WHERE LinkName = 'LinkedIn')
            INSERT INTO GlobalLinkType (LinkName, LinkType, LinkIcon, DisplayOrder, createdBy)
            VALUES ('LinkedIn', 'professional', 'linkedin', 1, 'system')
        """))
        
        conn.execute(text("""
            IF NOT EXISTS (SELECT * FROM GlobalLinkType WHERE LinkName = 'GitHub')
            INSERT INTO GlobalLinkType (LinkName, LinkType, LinkIcon, DisplayOrder, createdBy)
            VALUES ('GitHub', 'professional', 'github', 2, 'system')
        """))
        
        conn.execute(text("""
            IF NOT EXISTS (SELECT * FROM GlobalLinkType WHERE LinkName = 'Twitter')
            INSERT INTO GlobalLinkType (LinkName, LinkType, LinkIcon, DisplayOrder, createdBy)
            VALUES ('Twitter', 'social', 'twitter', 3, 'system')
        """))
        
        conn.execute(text("""
            IF NOT EXISTS (SELECT * FROM GlobalLinkType WHERE LinkName = 'Facebook')
            INSERT INTO GlobalLinkType (LinkName, LinkType, LinkIcon, DisplayOrder, createdBy)
            VALUES ('Facebook', 'social', 'facebook', 4, 'system')
        """))
        
        conn.execute(text("""
            IF NOT EXISTS (SELECT * FROM GlobalLinkType WHERE LinkName = 'Instagram')
            INSERT INTO GlobalLinkType (LinkName, LinkType, LinkIcon, DisplayOrder, createdBy)
            VALUES ('Instagram', 'social', 'instagram', 5, 'system')
        """))
        
        conn.execute(text("""
            IF NOT EXISTS (SELECT * FROM GlobalLinkType WHERE LinkName = 'Portfolio')
            INSERT INTO GlobalLinkType (LinkName, LinkType, LinkIcon, DisplayOrder, createdBy)
            VALUES ('Portfolio', 'portfolio', 'portfolio', 6, 'system')
        """))
        
        conn.execute(text("""
            IF NOT EXISTS (SELECT * FROM GlobalLinkType WHERE LinkName = 'Personal Website')
            INSERT INTO GlobalLinkType (LinkName, LinkType, LinkIcon, DisplayOrder, createdBy)
            VALUES ('Personal Website', 'portfolio', 'website', 7, 'system')
        """))
        
        # Migrate existing data
        # Move Nationality to CurrentCitizenship
        conn.execute(text("""
            UPDATE Profile 
            SET CurrentCitizenship = Nationality 
            WHERE CurrentCitizenship IS NULL AND Nationality IS NOT NULL
        """))
        
        # Migrate existing LinkedIn URLs
        conn.execute(text("""
            INSERT INTO ProfileSocialLink (ProfileID, LinkName, LinkURL, LinkType, LinkIcon, IsApproved, IsActive, IsPublic, createdBy)
            SELECT ProfileID, 'LinkedIn', LinkedInURL, 'professional', 'linkedin', 1, 1, 1, 'system'
            FROM Profile 
            WHERE LinkedInURL IS NOT NULL AND LinkedInURL != ''
        """))
        
        # Migrate existing GitHub URLs
        conn.execute(text("""
            INSERT INTO ProfileSocialLink (ProfileID, LinkName, LinkURL, LinkType, LinkIcon, IsApproved, IsActive, IsPublic, createdBy)
            SELECT ProfileID, 'GitHub', GitHubURL, 'professional', 'github', 1, 1, 1, 'system'
            FROM Profile 
            WHERE GitHubURL IS NOT NULL AND GitHubURL != ''
        """))
        
        # Migrate existing Facebook URLs (from OtherSocialProfiles)
        conn.execute(text("""
            INSERT INTO ProfileSocialLink (ProfileID, LinkName, LinkURL, LinkType, LinkIcon, IsApproved, IsActive, IsPublic, createdBy)
            SELECT ProfileID, 'Facebook', OtherSocialProfiles, 'social', 'facebook', 1, 1, 1, 'system'
            FROM Profile 
            WHERE OtherSocialProfiles IS NOT NULL AND OtherSocialProfiles != ''
        """))
        
        conn.commit()
        print("✅ Migration completed successfully!")

if __name__ == "__main__":
    run_migration() 