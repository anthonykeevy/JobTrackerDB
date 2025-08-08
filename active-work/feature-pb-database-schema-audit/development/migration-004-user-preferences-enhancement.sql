-- Migration 004: UserPreferences Enhancement
-- Description: Enhance UserPreferences table with Profile Builder tracking fields
-- Author: BMad Architect
-- Date: 2025-01-08
-- Rollback: Yes

-- =====================================================
-- ENHANCE USER PREFERENCES TABLE
-- =====================================================

-- Add ProfileBuilderMode column
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('UserPreferences') AND name = 'ProfileBuilderMode')
BEGIN
    ALTER TABLE [dbo].[UserPreferences] ADD [ProfileBuilderMode] [nvarchar](20) NULL
    PRINT 'ProfileBuilderMode column added to UserPreferences table'
END
ELSE
BEGIN
    PRINT 'ProfileBuilderMode column already exists in UserPreferences table'
END

-- Add ProfileCompletionPercentage column
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('UserPreferences') AND name = 'ProfileCompletionPercentage')
BEGIN
    ALTER TABLE [dbo].[UserPreferences] ADD [ProfileCompletionPercentage] [decimal](5,2) NULL
    PRINT 'ProfileCompletionPercentage column added to UserPreferences table'
END
ELSE
BEGIN
    PRINT 'ProfileCompletionPercentage column already exists in UserPreferences table'
END

-- Add LastProfileUpdate column
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('UserPreferences') AND name = 'LastProfileUpdate')
BEGIN
    ALTER TABLE [dbo].[UserPreferences] ADD [LastProfileUpdate] [datetime] NULL
    PRINT 'LastProfileUpdate column added to UserPreferences table'
END
ELSE
BEGIN
    PRINT 'LastProfileUpdate column already exists in UserPreferences table'
END

-- Add ProfileVersion column
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('UserPreferences') AND name = 'ProfileVersion')
BEGIN
    ALTER TABLE [dbo].[UserPreferences] ADD [ProfileVersion] [int] NOT NULL DEFAULT 1
    PRINT 'ProfileVersion column added to UserPreferences table'
END
ELSE
BEGIN
    PRINT 'ProfileVersion column already exists in UserPreferences table'
END

-- Add IsProfileComplete column
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('UserPreferences') AND name = 'IsProfileComplete')
BEGIN
    ALTER TABLE [dbo].[UserPreferences] ADD [IsProfileComplete] [bit] NOT NULL DEFAULT 0
    PRINT 'IsProfileComplete column added to UserPreferences table'
END
ELSE
BEGIN
    PRINT 'IsProfileComplete column already exists in UserPreferences table'
END

-- Add ProfileBuilderLastSessionID column
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('UserPreferences') AND name = 'ProfileBuilderLastSessionID')
BEGIN
    ALTER TABLE [dbo].[UserPreferences] ADD [ProfileBuilderLastSessionID] [nvarchar](100) NULL
    PRINT 'ProfileBuilderLastSessionID column added to UserPreferences table'
END
ELSE
BEGIN
    PRINT 'ProfileBuilderLastSessionID column already exists in UserPreferences table'
END

-- Add ProfileBuilderStepProgress column
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('UserPreferences') AND name = 'ProfileBuilderStepProgress')
BEGIN
    ALTER TABLE [dbo].[UserPreferences] ADD [ProfileBuilderStepProgress] [nvarchar](max) NULL
    PRINT 'ProfileBuilderStepProgress column added to UserPreferences table'
END
ELSE
BEGIN
    PRINT 'ProfileBuilderStepProgress column already exists in UserPreferences table'
END

-- Add ProfileBuilderValidationErrors column
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('UserPreferences') AND name = 'ProfileBuilderValidationErrors')
BEGIN
    ALTER TABLE [dbo].[UserPreferences] ADD [ProfileBuilderValidationErrors] [nvarchar](max) NULL
    PRINT 'ProfileBuilderValidationErrors column added to UserPreferences table'
END
ELSE
BEGIN
    PRINT 'ProfileBuilderValidationErrors column already exists in UserPreferences table'
END

-- =====================================================
-- USER PREFERENCES ENHANCEMENT STORED PROCEDURES
-- =====================================================

-- Stored Procedure to Update Profile Builder Progress
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[sp_UpdateProfileBuilderProgress]') AND type in (N'P'))
BEGIN
    EXEC('
    CREATE PROCEDURE [dbo].[sp_UpdateProfileBuilderProgress]
        @UserID INT,
        @ProfileID INT,
        @SessionID NVARCHAR(100) = NULL,
        @StepProgress NVARCHAR(max) = NULL,
        @ValidationErrors NVARCHAR(max) = NULL,
        @CompletionPercentage DECIMAL(5,2) = NULL,
        @IsComplete BIT = NULL
    AS
    BEGIN
        SET NOCOUNT ON;
        
        BEGIN TRY
            -- Update UserPreferences
            UPDATE [dbo].[UserPreferences]
            SET 
                [ProfileBuilderLastSessionID] = ISNULL(@SessionID, [ProfileBuilderLastSessionID]),
                [ProfileBuilderStepProgress] = ISNULL(@StepProgress, [ProfileBuilderStepProgress]),
                [ProfileBuilderValidationErrors] = ISNULL(@ValidationErrors, [ProfileBuilderValidationErrors]),
                [ProfileCompletionPercentage] = ISNULL(@CompletionPercentage, [ProfileCompletionPercentage]),
                [IsProfileComplete] = ISNULL(@IsComplete, [IsProfileComplete]),
                [LastProfileUpdate] = GETDATE(),
                [ProfileVersion] = [ProfileVersion] + 1,
                [lastUpdated] = GETDATE(),
                [updatedBy] = (SELECT [FirstName] + '' '' + [LastName] FROM [dbo].[User] WHERE [UserID] = @UserID)
            WHERE [UserID] = @UserID
            
            -- Update Profile lastUpdated
            UPDATE [dbo].[Profile]
            SET 
                [lastUpdated] = GETDATE(),
                [updatedBy] = (SELECT [FirstName] + '' '' + [LastName] FROM [dbo].[User] WHERE [UserID] = @UserID)
            WHERE [ProfileID] = @ProfileID
            
            SELECT ''Profile Builder progress updated successfully'' AS Message
            
        END TRY
        BEGIN CATCH
            SELECT ERROR_MESSAGE() AS Message
        END CATCH
    END
    ')
    
    PRINT 'sp_UpdateProfileBuilderProgress stored procedure created successfully'
END
ELSE
BEGIN
    PRINT 'sp_UpdateProfileBuilderProgress stored procedure already exists'
END

-- Stored Procedure to Get Profile Builder Status
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[sp_GetProfileBuilderStatus]') AND type in (N'P'))
BEGIN
    EXEC('
    CREATE PROCEDURE [dbo].[sp_GetProfileBuilderStatus]
        @UserID INT,
        @ProfileID INT = NULL
    AS
    BEGIN
        SET NOCOUNT ON;
        
        SELECT 
            up.[UserID],
            up.[ProfileBuilderMode],
            up.[ProfileCompletionPercentage],
            up.[LastProfileUpdate],
            up.[ProfileVersion],
            up.[IsProfileComplete],
            up.[ProfileBuilderLastSessionID],
            up.[ProfileBuilderStepProgress],
            up.[ProfileBuilderValidationErrors],
            -- Profile information
            p.[ProfileID],
            p.[FirstName],
            p.[LastName],
            p.[EmailAddress],
            -- Session information
            pbs.[SessionStart],
            pbs.[SessionEnd],
            pbs.[CurrentStep],
            pbs.[IPAddress],
            pbs.[UserAgent],
            -- Calculate session duration
            DATEDIFF(MINUTE, pbs.[SessionStart], ISNULL(pbs.[SessionEnd], GETDATE())) AS SessionDurationMinutes
        FROM [dbo].[UserPreferences] up
        INNER JOIN [dbo].[Profile] p ON up.[UserID] = p.[ProfileID]
        LEFT JOIN [dbo].[ProfileBuilderSession] pbs ON up.[ProfileBuilderLastSessionID] = pbs.[SessionID]
        WHERE up.[UserID] = @UserID
            AND (@ProfileID IS NULL OR p.[ProfileID] = @ProfileID)
    END
    ')
    
    PRINT 'sp_GetProfileBuilderStatus stored procedure created successfully'
END
ELSE
BEGIN
    PRINT 'sp_GetProfileBuilderStatus stored procedure already exists'
END

-- Stored Procedure to Reset Profile Builder Progress
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[sp_ResetProfileBuilderProgress]') AND type in (N'P'))
BEGIN
    EXEC('
    CREATE PROCEDURE [dbo].[sp_ResetProfileBuilderProgress]
        @UserID INT,
        @ProfileID INT
    AS
    BEGIN
        SET NOCOUNT ON;
        
        BEGIN TRY
            -- Reset UserPreferences
            UPDATE [dbo].[UserPreferences]
            SET 
                [ProfileBuilderMode] = NULL,
                [ProfileCompletionPercentage] = 0,
                [IsProfileComplete] = 0,
                [ProfileBuilderLastSessionID] = NULL,
                [ProfileBuilderStepProgress] = NULL,
                [ProfileBuilderValidationErrors] = NULL,
                [ProfileVersion] = 1,
                [lastUpdated] = GETDATE(),
                [updatedBy] = (SELECT [FirstName] + '' '' + [LastName] FROM [dbo].[User] WHERE [UserID] = @UserID)
            WHERE [UserID] = @UserID
            
            -- End any active sessions
            UPDATE [dbo].[ProfileBuilderSession]
            SET 
                [SessionEnd] = GETDATE(),
                [lastUpdated] = GETDATE(),
                [updatedBy] = (SELECT [FirstName] + '' '' + [LastName] FROM [dbo].[User] WHERE [UserID] = @UserID)
            WHERE [ProfileID] = @ProfileID AND [SessionEnd] IS NULL
            
            SELECT ''Profile Builder progress reset successfully'' AS Message
            
        END TRY
        BEGIN CATCH
            SELECT ERROR_MESSAGE() AS Message
        END CATCH
    END
    ')
    
    PRINT 'sp_ResetProfileBuilderProgress stored procedure created successfully'
END
ELSE
BEGIN
    PRINT 'sp_ResetProfileBuilderProgress stored procedure already exists'
END

-- Stored Procedure to Calculate Profile Completion
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[sp_CalculateProfileCompletion]') AND type in (N'P'))
BEGIN
    EXEC('
    CREATE PROCEDURE [dbo].[sp_CalculateProfileCompletion]
        @ProfileID INT
    AS
    BEGIN
        SET NOCOUNT ON;
        
        DECLARE @TotalSections INT = 8
        DECLARE @CompletedSections INT = 0
        DECLARE @CompletionPercentage DECIMAL(5,2)
        
        -- Check Basic Info (Profile table)
        IF EXISTS (SELECT 1 FROM [dbo].[Profile] WHERE [ProfileID] = @ProfileID 
                   AND [FirstName] IS NOT NULL AND [LastName] IS NOT NULL AND [EmailAddress] IS NOT NULL)
            SET @CompletedSections = @CompletedSections + 1
        
        -- Check Address
        IF EXISTS (SELECT 1 FROM [dbo].[ProfileAddress] WHERE [ProfileID] = @ProfileID)
            SET @CompletedSections = @CompletedSections + 1
        
        -- Check Education
        IF EXISTS (SELECT 1 FROM [dbo].[ProfileEducation] WHERE [ProfileID] = @ProfileID)
            SET @CompletedSections = @CompletedSections + 1
        
        -- Check Certifications
        IF EXISTS (SELECT 1 FROM [dbo].[ProfileCertification] WHERE [ProfileID] = @ProfileID)
            SET @CompletedSections = @CompletedSections + 1
        
        -- Check Work Experience
        IF EXISTS (SELECT 1 FROM [dbo].[ProfileWorkExperience] WHERE [ProfileID] = @ProfileID)
            SET @CompletedSections = @CompletedSections + 1
        
        -- Check Projects
        IF EXISTS (SELECT 1 FROM [dbo].[ProfileProject] WHERE [ProfileID] = @ProfileID)
            SET @CompletedSections = @CompletedSections + 1
        
        -- Check Career Aspiration
        IF EXISTS (SELECT 1 FROM [dbo].[ProfileCareerAspiration] WHERE [ProfileID] = @ProfileID)
            SET @CompletedSections = @CompletedSections + 1
        
        -- Check Resume (optional section)
        IF EXISTS (SELECT 1 FROM [dbo].[Resume] WHERE [ProfileID] = @ProfileID)
            SET @CompletedSections = @CompletedSections + 1
        
        -- Calculate percentage
        SET @CompletionPercentage = (@CompletedSections * 100.0) / @TotalSections
        
        -- Update UserPreferences
        UPDATE [dbo].[UserPreferences]
        SET 
            [ProfileCompletionPercentage] = @CompletionPercentage,
            [IsProfileComplete] = CASE WHEN @CompletionPercentage >= 100 THEN 1 ELSE 0 END,
            [LastProfileUpdate] = GETDATE(),
            [lastUpdated] = GETDATE()
        WHERE [UserID] = @ProfileID
        
        SELECT 
            @CompletedSections AS CompletedSections,
            @TotalSections AS TotalSections,
            @CompletionPercentage AS CompletionPercentage,
            CASE WHEN @CompletionPercentage >= 100 THEN 1 ELSE 0 END AS IsComplete
    END
    ')
    
    PRINT 'sp_CalculateProfileCompletion stored procedure created successfully'
END
ELSE
BEGIN
    PRINT 'sp_CalculateProfileCompletion stored procedure already exists'
END

PRINT 'Migration 004 completed successfully - UserPreferences enhancement created'
