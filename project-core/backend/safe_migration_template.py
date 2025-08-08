"""
Template for Safe Migration with Data Backup/Restore
Use this pattern for complex schema changes
"""

def upgrade():
    # 1. Create backup tables for data preservation
    connection = op.get_bind()
    
    # Example: If we need to modify the User table significantly
    # Step 1: Create backup
    connection.execute(text("""
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'User_Backup')
        BEGIN
            SELECT * INTO User_Backup FROM [User]
        END
    """))
    
    # Step 2: Drop and recreate with new structure (if needed)
    # op.drop_table('User')
    # create_new_user_table_with_enhanced_structure()
    
    # Step 3: Restore data with default values for new columns
    # connection.execute(text("""
    #     INSERT INTO [User] (UserID, Username, EmailAddress, HashedPassword, 
    #                        IsActive, RoleID, ProfileID, Provider, ProviderUserID, 
    #                        LoginEmailAddressID, createdDate, createdBy)
    #     SELECT UserID, Username, EmailAddress, HashedPassword, 
    #            IsActive, RoleID, ProfileID, Provider, ProviderUserID,
    #            NULL as LoginEmailAddressID,  -- New field with default
    #            createdDate, createdBy
    #     FROM User_Backup
    # """))
    
    # Step 4: Clean up backup table
    # connection.execute(text("DROP TABLE User_Backup"))
    
    pass

def handle_new_field_population():
    """Handle population of new fields with intelligent defaults"""
    connection = op.get_bind()
    
    # Example: Populate LoginEmailAddressID from existing EmailAddress
    connection.execute(text("""
        -- Create UserEmailAddress records for existing users
        INSERT INTO UserEmailAddress (UserID, EmailAddress, EmailType, IsVerified, IsActive, IsLoginEmail, createdDate)
        SELECT UserID, EmailAddress, 'primary', 1, 1, 1, GETDATE()
        FROM [User] 
        WHERE EmailAddress IS NOT NULL
        AND NOT EXISTS (
            SELECT 1 FROM UserEmailAddress 
            WHERE UserEmailAddress.UserID = [User].UserID
        )
    """))
    
    # Update User table with LoginEmailAddressID
    connection.execute(text("""
        UPDATE u 
        SET LoginEmailAddressID = uea.UserEmailAddressID
        FROM [User] u
        INNER JOIN UserEmailAddress uea ON u.UserID = uea.UserID
        WHERE uea.IsLoginEmail = 1 AND u.LoginEmailAddressID IS NULL
    """))