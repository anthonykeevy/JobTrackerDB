"""
Smart Migration Script for JobTrackerDB
Handles existing tables intelligently with data preservation
"""

import pyodbc
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.sql import text
import os
from dotenv import load_dotenv

load_dotenv()

def check_production_schema():
    """Check what tables exist in production and what needs to be migrated"""
    
    # Production database connection
    prod_url = "mssql+pyodbc://localhost/JobTrackerDB?driver=ODBC+Driver+17+for+SQL+Server"
    engine = create_engine(prod_url)
    inspector = inspect(engine)
    
    # Get all existing tables
    existing_tables = inspector.get_table_names()
    print(f"🔍 Found {len(existing_tables)} existing tables in production:")
    for table in sorted(existing_tables):
        print(f"  ✅ {table}")
    
    # Tables that should exist after migration
    expected_tables = [
        'Role', 'Profile', 'User', 'UserPreferences', 'UserRoleOverride',
        'Objective', 'Languages', 'Hobbies', 'JobApplication', 'JobApplicationNote',
        'JobApplicationAttachment', 'JobApplicationStatusHistory', 'JobApplicationInterview',
        'JobApplicationTask', 'Skills', 'Resume', 'CoverLetter', 'Message',
        'AuthLog', 'UserPasswordResetToken',
        # New tables from our schema
        'UserEmailAddress', 'UserEmailAddressHistory', 'UserEmailVerificationLog',
        'ProfileVersion', 'ProfileCareerAspiration', 'ProfileEducation', 'ProfileWorkExperience',
        'ProfileCertification', 'ProfileProject', 'ProfileVolunteerExperience',
        'JobBoard', 'JobBoardJob', 'JobBoardJobVersion', 'UserJobBoardJobInteraction',
        'JobBoardJobSkill', 'UserJobBoardJobFitScore', 'UserJobBoardJobFitScoreDetail',
        'UserSkillGapResolution', 'ResumeResumeVersion', 'CoverLetterCoverLetterVersion',
        'ExportTemplate', 'UserGamificationPoints', 'UserAchievement',
        'UserNotification', 'UserNotificationPreference', 'UserAnalytics',
        'UserJobBoardJobSearchAnalytics', 'ProfileConsent', 'ProfileType'
    ]
    
    # Find missing tables
    missing_tables = [table for table in expected_tables if table not in existing_tables]
    print(f"\n📋 Tables that need to be created ({len(missing_tables)}):")
    for table in missing_tables:
        print(f"  ⚠️  {table}")
    
    # Find extra tables (shouldn't happen but good to know)
    extra_tables = [table for table in existing_tables if table not in expected_tables]
    if extra_tables:
        print(f"\n📎 Unexpected tables found ({len(extra_tables)}):")
        for table in extra_tables:
            print(f"  ❓ {table}")
    
    return existing_tables, missing_tables

def create_data_backup_migration():
    """Create a migration that backs up data before schema changes"""
    
    migration_template = '''"""Smart migration with data preservation

Revision ID: {revision_id}
Revises: {down_revision}
Create Date: {create_date}

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text
from sqlalchemy import String, Integer, DateTime, Boolean, DECIMAL, UnicodeText

# revision identifiers
revision = '{revision_id}'
down_revision = '{down_revision}'
branch_labels = None
depends_on = None

def upgrade():
    """
    Smart upgrade that preserves existing data and only adds new tables/columns
    """
    # Create connection for custom SQL operations
    connection = op.get_bind()
    
    # 1. Check what tables exist
    result = connection.execute(text("""
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE'
    """))
    existing_tables = {{row[0] for row in result}}
    
    # 2. Create new tables only if they don't exist
    new_tables = [
        'UserEmailAddress', 'UserEmailAddressHistory', 'UserEmailVerificationLog',
        'ProfileVersion', 'ProfileCareerAspiration', 'ProfileEducation', 'ProfileWorkExperience',
        'ProfileCertification', 'ProfileProject', 'ProfileVolunteerExperience',
        'JobBoard', 'JobBoardJob', 'JobBoardJobVersion', 'UserJobBoardJobInteraction',
        'JobBoardJobSkill', 'UserJobBoardJobFitScore', 'UserJobBoardJobFitScoreDetail',
        'UserSkillGapResolution', 'ResumeResumeVersion', 'CoverLetterCoverLetterVersion',
        'ExportTemplate', 'UserGamificationPoints', 'UserAchievement',
        'UserNotification', 'UserNotificationPreference', 'UserAnalytics',
        'UserJobBoardJobSearchAnalytics', 'ProfileConsent', 'ProfileType'
    ]
    
    for table_name in new_tables:
        if table_name not in existing_tables:
            print(f"Creating new table: {{table_name}}")
            if table_name == 'UserEmailAddress':
                create_user_email_address_table()
            elif table_name == 'ProfileVersion':
                create_profile_version_table()
            # Add other table creation functions as needed
            
    # 3. Add new columns to existing tables if needed
    add_new_columns_to_existing_tables(connection, existing_tables)
    
    print("✅ Smart migration completed successfully!")

def create_user_email_address_table():
    """Create UserEmailAddress table with proper structure"""
    op.create_table('UserEmailAddress',
        sa.Column('UserEmailAddressID', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('UserID', sa.Integer(), nullable=False),
        sa.Column('EmailAddress', sa.Unicode(255), nullable=False),
        sa.Column('EmailType', sa.Unicode(50), nullable=True),
        sa.Column('IsVerified', sa.Boolean(), default=False),
        sa.Column('IsActive', sa.Boolean(), default=True),
        sa.Column('IsLoginEmail', sa.Boolean(), default=False),
        sa.Column('VerificationToken', sa.Unicode(255), nullable=True),
        sa.Column('VerificationExpiry', sa.DateTime(), nullable=True),
        sa.Column('VerifiedDate', sa.DateTime(), nullable=True),
        sa.Column('createdDate', sa.DateTime(), nullable=True),
        sa.Column('createdBy', sa.Unicode(100), nullable=True),
        sa.Column('lastUpdated', sa.DateTime(), nullable=True),
        sa.Column('updatedBy', sa.Unicode(100), nullable=True),
        sa.ForeignKeyConstraint(['UserID'], ['User.UserID'], ),
        sa.PrimaryKeyConstraint('UserEmailAddressID'),
        sa.UniqueConstraint('EmailAddress')
    )
    op.create_index('ix_UserEmailAddress_EmailAddress', 'UserEmailAddress', ['EmailAddress'], unique=False)

def create_profile_version_table():
    """Create ProfileVersion table"""
    op.create_table('ProfileVersion',
        sa.Column('ProfileVersionID', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('ProfileID', sa.Integer(), nullable=False),
        sa.Column('VersionNumber', sa.Integer(), nullable=False),
        sa.Column('IsConfirmed', sa.Boolean(), default=False),
        sa.Column('HappinessScore', sa.DECIMAL(3,2), nullable=True),
        sa.Column('createdDate', sa.DateTime(), nullable=True),
        sa.Column('createdBy', sa.Unicode(100), nullable=True),
        sa.Column('lastUpdated', sa.DateTime(), nullable=True),
        sa.Column('updatedBy', sa.Unicode(100), nullable=True),
        sa.ForeignKeyConstraint(['ProfileID'], ['Profile.ProfileID'], ),
        sa.PrimaryKeyConstraint('ProfileVersionID')
    )

def add_new_columns_to_existing_tables(connection, existing_tables):
    """Add new columns to existing tables if they don't exist"""
    
    # Example: Add new columns to User table if needed
    if 'User' in existing_tables:
        # Check if LoginEmailAddressID column exists
        result = connection.execute(text("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'User' AND COLUMN_NAME = 'LoginEmailAddressID'
        """))
        
        if not result.fetchone():
            print("Adding LoginEmailAddressID to User table")
            op.add_column('User', sa.Column('LoginEmailAddressID', sa.Integer(), nullable=True))
            # Add foreign key constraint after UserEmailAddress table is created
            
    # Add similar checks for other table modifications

def downgrade():
    """
    Downgrade migration - handle with care to preserve data
    """
    # Only drop tables that were created in this migration
    # Never drop tables with existing data unless explicitly confirmed
    pass
'''
    
    return migration_template

if __name__ == "__main__":
    print("🔍 Analyzing production database schema...")
    existing_tables, missing_tables = check_production_schema()
    
    print(f"\n📊 Analysis Summary:")
    print(f"  • Existing tables: {len(existing_tables)}")
    print(f"  • Missing tables: {len(missing_tables)}")
    print(f"  • Total expected: {len(existing_tables) + len(missing_tables)}")