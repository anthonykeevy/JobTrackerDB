from sqlalchemy import create_engine, text
import os

# Database connection
DATABASE_URL = "mssql+pyodbc:///?odbc_connect=DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=JobTrackerDB;Trusted_Connection=yes;"

def check_and_fix_database():
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        # Check if new columns exist
        result = conn.execute(text("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Profile'"))
        columns = [row[0] for row in result.fetchall()]
        print("Current Profile table columns:", columns)
        
        # Add missing columns if they don't exist
        if 'CountryOfBirth' not in columns:
            print("Adding CountryOfBirth column...")
            conn.execute(text("ALTER TABLE Profile ADD CountryOfBirth NVARCHAR(100)"))
        
        if 'CurrentCitizenship' not in columns:
            print("Adding CurrentCitizenship column...")
            conn.execute(text("ALTER TABLE Profile ADD CurrentCitizenship NVARCHAR(100)"))
        
        # Check if tables exist
        result = conn.execute(text("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME IN ('ProfileSocialLink', 'GlobalLinkType')"))
        tables = [row[0] for row in result.fetchall()]
        print("Existing tables:", tables)
        
        if 'ProfileSocialLink' not in tables:
            print("Creating ProfileSocialLink table...")
            conn.execute(text("""
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
        
        if 'GlobalLinkType' not in tables:
            print("Creating GlobalLinkType table...")
            conn.execute(text("""
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
            
            # Insert default link types
            print("Inserting default link types...")
            default_links = [
                ('LinkedIn', 'professional', 'linkedin', 1),
                ('GitHub', 'professional', 'github', 2),
                ('Twitter', 'social', 'twitter', 3),
                ('Facebook', 'social', 'facebook', 4),
                ('Instagram', 'social', 'instagram', 5),
                ('Portfolio', 'portfolio', 'portfolio', 6),
                ('Personal Website', 'portfolio', 'website', 7)
            ]
            
            for link_name, link_type, link_icon, display_order in default_links:
                conn.execute(text("""
                    INSERT INTO GlobalLinkType (LinkName, LinkType, LinkIcon, DisplayOrder, createdBy)
                    VALUES (?, ?, ?, ?, 'system')
                """), (link_name, link_type, link_icon, display_order))
        
        conn.commit()
        print("✅ Database structure updated successfully!")

if __name__ == "__main__":
    check_and_fix_database() 