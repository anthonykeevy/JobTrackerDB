-- Migration 003: Profile Builder Session Tracking
-- Description: Create session tracking system for Profile Builder workflow
-- Author: BMad Architect
-- Date: 2025-01-08
-- Rollback: Yes

-- =====================================================
-- PROFILE BUILDER SESSION TABLE
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[ProfileBuilderSession]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[ProfileBuilderSession](
        [SessionID] [nvarchar](100) NOT NULL,
        [ProfileID] [int] NOT NULL,
        [UserID] [int] NOT NULL,
        [SessionStart] [datetime] NOT NULL DEFAULT GETDATE(),
        [SessionEnd] [datetime] NULL,
        [CurrentStep] [nvarchar](50) NULL,
        [StepProgress] [nvarchar](max) NULL, -- JSON of step completion status
        [FormValidationErrors] [nvarchar](max) NULL, -- JSON of validation errors
        [IPAddress] [nvarchar](50) NULL,
        [UserAgent] [nvarchar](500) NULL,
        [createdDate] [datetime] NOT NULL DEFAULT GETDATE(),
        [createdBy] [nvarchar](100) NULL,
        [lastUpdated] [datetime] NULL,
        [updatedBy] [nvarchar](100) NULL,
        CONSTRAINT [PK_ProfileBuilderSession] PRIMARY KEY CLUSTERED ([SessionID] ASC)
    )
    
    -- Add foreign key constraints
    ALTER TABLE [dbo].[ProfileBuilderSession] ADD CONSTRAINT [FK_ProfileBuilderSession_Profile] 
        FOREIGN KEY([ProfileID]) REFERENCES [dbo].[Profile] ([ProfileID])
    ALTER TABLE [dbo].[ProfileBuilderSession] ADD CONSTRAINT [FK_ProfileBuilderSession_User] 
        FOREIGN KEY([UserID]) REFERENCES [dbo].[User] ([UserID])
    
    -- Add indexes for performance
    CREATE NONCLUSTERED INDEX [IX_ProfileBuilderSession_ProfileID] ON [dbo].[ProfileBuilderSession] ([ProfileID])
    CREATE NONCLUSTERED INDEX [IX_ProfileBuilderSession_UserID] ON [dbo].[ProfileBuilderSession] ([UserID])
    CREATE NONCLUSTERED INDEX [IX_ProfileBuilderSession_Start] ON [dbo].[ProfileBuilderSession] ([SessionStart])
    CREATE NONCLUSTERED INDEX [IX_ProfileBuilderSession_CurrentStep] ON [dbo].[ProfileBuilderSession] ([CurrentStep])
    
    PRINT 'ProfileBuilderSession table created successfully'
END
ELSE
BEGIN
    PRINT 'ProfileBuilderSession table already exists'
END

-- =====================================================
-- PROFILE BUILDER STEP TABLE
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[ProfileBuilderStep]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[ProfileBuilderStep](
        [StepID] [int] IDENTITY(1,1) NOT NULL,
        [SessionID] [nvarchar](100) NOT NULL,
        [StepName] [nvarchar](50) NOT NULL,
        [StepOrder] [int] NOT NULL,
        [StartTime] [datetime] NULL,
        [EndTime] [datetime] NULL,
        [CompletionStatus] [nvarchar](20) NULL, -- PENDING, IN_PROGRESS, COMPLETED, SKIPPED
        [ValidationErrors] [nvarchar](max) NULL, -- JSON of validation errors
        [DataSnapshot] [nvarchar](max) NULL, -- JSON of step data
        [createdDate] [datetime] NOT NULL DEFAULT GETDATE(),
        [createdBy] [nvarchar](100) NULL,
        [lastUpdated] [datetime] NULL,
        [updatedBy] [nvarchar](100) NULL,
        CONSTRAINT [PK_ProfileBuilderStep] PRIMARY KEY CLUSTERED ([StepID] ASC)
    )
    
    -- Add foreign key constraint
    ALTER TABLE [dbo].[ProfileBuilderStep] ADD CONSTRAINT [FK_ProfileBuilderStep_ProfileBuilderSession] 
        FOREIGN KEY([SessionID]) REFERENCES [dbo].[ProfileBuilderSession] ([SessionID])
    
    -- Add indexes for performance
    CREATE NONCLUSTERED INDEX [IX_ProfileBuilderStep_SessionID] ON [dbo].[ProfileBuilderStep] ([SessionID])
    CREATE NONCLUSTERED INDEX [IX_ProfileBuilderStep_StepOrder] ON [dbo].[ProfileBuilderStep] ([StepOrder])
    CREATE NONCLUSTERED INDEX [IX_ProfileBuilderStep_Status] ON [dbo].[ProfileBuilderStep] ([CompletionStatus])
    
    PRINT 'ProfileBuilderStep table created successfully'
END
ELSE
BEGIN
    PRINT 'ProfileBuilderStep table already exists'
END

-- =====================================================
-- PROFILE BUILDER SESSION STORED PROCEDURES
-- =====================================================

-- Stored Procedure to Start Profile Builder Session
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[sp_StartProfileBuilderSession]') AND type in (N'P'))
BEGIN
    EXEC('
    CREATE PROCEDURE [dbo].[sp_StartProfileBuilderSession]
        @SessionID NVARCHAR(100),
        @ProfileID INT,
        @UserID INT,
        @IPAddress NVARCHAR(50) = NULL,
        @UserAgent NVARCHAR(500) = NULL
    AS
    BEGIN
        SET NOCOUNT ON;
        
        BEGIN TRY
            -- Start session
            INSERT INTO [dbo].[ProfileBuilderSession] (
                [SessionID], [ProfileID], [UserID], [IPAddress], [UserAgent], [createdBy]
            )
            VALUES (
                @SessionID, @ProfileID, @UserID, @IPAddress, @UserAgent, 
                (SELECT [FirstName] + '' '' + [LastName] FROM [dbo].[User] WHERE [UserID] = @UserID)
            )
            
            -- Initialize steps
            INSERT INTO [dbo].[ProfileBuilderStep] (
                [SessionID], [StepName], [StepOrder], [CompletionStatus], [createdBy]
            )
            VALUES 
                (@SessionID, ''BasicInfo'', 1, ''PENDING'', 
                 (SELECT [FirstName] + '' '' + [LastName] FROM [dbo].[User] WHERE [UserID] = @UserID)),
                (@SessionID, ''Address'', 2, ''PENDING'', 
                 (SELECT [FirstName] + '' '' + [LastName] FROM [dbo].[User] WHERE [UserID] = @UserID)),
                (@SessionID, ''Education'', 3, ''PENDING'', 
                 (SELECT [FirstName] + '' '' + [LastName] FROM [dbo].[User] WHERE [UserID] = @UserID)),
                (@SessionID, ''Certifications'', 4, ''PENDING'', 
                 (SELECT [FirstName] + '' '' + [LastName] FROM [dbo].[User] WHERE [UserID] = @UserID)),
                (@SessionID, ''WorkExperience'', 5, ''PENDING'', 
                 (SELECT [FirstName] + '' '' + [LastName] FROM [dbo].[User] WHERE [UserID] = @UserID)),
                (@SessionID, ''Projects'', 6, ''PENDING'', 
                 (SELECT [FirstName] + '' '' + [LastName] FROM [dbo].[User] WHERE [UserID] = @UserID)),
                (@SessionID, ''CareerAspiration'', 7, ''PENDING'', 
                 (SELECT [FirstName] + '' '' + [LastName] FROM [dbo].[User] WHERE [UserID] = @UserID)),
                (@SessionID, ''ReviewConfirm'', 8, ''PENDING'', 
                 (SELECT [FirstName] + '' '' + [LastName] FROM [dbo].[User] WHERE [UserID] = @UserID))
            
            SELECT @SessionID AS SessionID, ''Session started successfully'' AS Message
            
        END TRY
        BEGIN CATCH
            SELECT NULL AS SessionID, ERROR_MESSAGE() AS Message
        END CATCH
    END
    ')
    
    PRINT 'sp_StartProfileBuilderSession stored procedure created successfully'
END
ELSE
BEGIN
    PRINT 'sp_StartProfileBuilderSession stored procedure already exists'
END

-- Stored Procedure to Update Step Progress
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[sp_UpdateProfileBuilderStep]') AND type in (N'P'))
BEGIN
    EXEC('
    CREATE PROCEDURE [dbo].[sp_UpdateProfileBuilderStep]
        @SessionID NVARCHAR(100),
        @StepName NVARCHAR(50),
        @CompletionStatus NVARCHAR(20),
        @ValidationErrors NVARCHAR(max) = NULL,
        @DataSnapshot NVARCHAR(max) = NULL,
        @UserID INT
    AS
    BEGIN
        SET NOCOUNT ON;
        
        BEGIN TRY
            -- Update step
            UPDATE [dbo].[ProfileBuilderStep]
            SET 
                [CompletionStatus] = @CompletionStatus,
                [ValidationErrors] = @ValidationErrors,
                [DataSnapshot] = @DataSnapshot,
                [EndTime] = CASE WHEN @CompletionStatus IN (''COMPLETED'', ''SKIPPED'') THEN GETDATE() ELSE [EndTime] END,
                [StartTime] = CASE WHEN [StartTime] IS NULL THEN GETDATE() ELSE [StartTime] END,
                [lastUpdated] = GETDATE(),
                [updatedBy] = (SELECT [FirstName] + '' '' + [LastName] FROM [dbo].[User] WHERE [UserID] = @UserID)
            WHERE [SessionID] = @SessionID AND [StepName] = @StepName
            
            -- Update session current step
            UPDATE [dbo].[ProfileBuilderSession]
            SET 
                [CurrentStep] = @StepName,
                [lastUpdated] = GETDATE(),
                [updatedBy] = (SELECT [FirstName] + '' '' + [LastName] FROM [dbo].[User] WHERE [UserID] = @UserID)
            WHERE [SessionID] = @SessionID
            
            SELECT ''Step updated successfully'' AS Message
            
        END TRY
        BEGIN CATCH
            SELECT ERROR_MESSAGE() AS Message
        END CATCH
    END
    ')
    
    PRINT 'sp_UpdateProfileBuilderStep stored procedure created successfully'
END
ELSE
BEGIN
    PRINT 'sp_UpdateProfileBuilderStep stored procedure already exists'
END

-- Stored Procedure to End Profile Builder Session
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[sp_EndProfileBuilderSession]') AND type in (N'P'))
BEGIN
    EXEC('
    CREATE PROCEDURE [dbo].[sp_EndProfileBuilderSession]
        @SessionID NVARCHAR(100),
        @UserID INT
    AS
    BEGIN
        SET NOCOUNT ON;
        
        BEGIN TRY
            -- End session
            UPDATE [dbo].[ProfileBuilderSession]
            SET 
                [SessionEnd] = GETDATE(),
                [lastUpdated] = GETDATE(),
                [updatedBy] = (SELECT [FirstName] + '' '' + [LastName] FROM [dbo].[User] WHERE [UserID] = @UserID)
            WHERE [SessionID] = @SessionID
            
            SELECT ''Session ended successfully'' AS Message
            
        END TRY
        BEGIN CATCH
            SELECT ERROR_MESSAGE() AS Message
        END CATCH
    END
    ')
    
    PRINT 'sp_EndProfileBuilderSession stored procedure created successfully'
END
ELSE
BEGIN
    PRINT 'sp_EndProfileBuilderSession stored procedure already exists'
END

-- Stored Procedure to Get Session Progress
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[sp_GetProfileBuilderProgress]') AND type in (N'P'))
BEGIN
    EXEC('
    CREATE PROCEDURE [dbo].[sp_GetProfileBuilderProgress]
        @SessionID NVARCHAR(100)
    AS
    BEGIN
        SET NOCOUNT ON;
        
        SELECT 
            pbs.[SessionID],
            pbs.[ProfileID],
            pbs.[UserID],
            pbs.[SessionStart],
            pbs.[SessionEnd],
            pbs.[CurrentStep],
            pbs.[StepProgress],
            pbs.[FormValidationErrors],
            pbs.[IPAddress],
            pbs.[UserAgent],
            pbs.[createdDate],
            pbs.[lastUpdated],
            -- Step details
            pbst.[StepName],
            pbst.[StepOrder],
            pbst.[StartTime],
            pbst.[EndTime],
            pbst.[CompletionStatus],
            pbst.[ValidationErrors],
            pbst.[DataSnapshot]
        FROM [dbo].[ProfileBuilderSession] pbs
        LEFT JOIN [dbo].[ProfileBuilderStep] pbst ON pbs.[SessionID] = pbst.[SessionID]
        WHERE pbs.[SessionID] = @SessionID
        ORDER BY pbst.[StepOrder]
    END
    ')
    
    PRINT 'sp_GetProfileBuilderProgress stored procedure created successfully'
END
ELSE
BEGIN
    PRINT 'sp_GetProfileBuilderProgress stored procedure already exists'
END

-- Stored Procedure to Get User Session History
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[sp_GetUserProfileBuilderHistory]') AND type in (N'P'))
BEGIN
    EXEC('
    CREATE PROCEDURE [dbo].[sp_GetUserProfileBuilderHistory]
        @UserID INT,
        @ProfileID INT = NULL
    AS
    BEGIN
        SET NOCOUNT ON;
        
        SELECT 
            pbs.[SessionID],
            pbs.[ProfileID],
            pbs.[SessionStart],
            pbs.[SessionEnd],
            pbs.[CurrentStep],
            pbs.[IPAddress],
            pbs.[UserAgent],
            -- Calculate session duration
            DATEDIFF(MINUTE, pbs.[SessionStart], ISNULL(pbs.[SessionEnd], GETDATE())) AS SessionDurationMinutes,
            -- Count completed steps
            (SELECT COUNT(*) FROM [dbo].[ProfileBuilderStep] pbst 
             WHERE pbst.[SessionID] = pbs.[SessionID] AND pbst.[CompletionStatus] = ''COMPLETED'') AS CompletedSteps,
            -- Total steps
            (SELECT COUNT(*) FROM [dbo].[ProfileBuilderStep] pbst 
             WHERE pbst.[SessionID] = pbs.[SessionID]) AS TotalSteps
        FROM [dbo].[ProfileBuilderSession] pbs
        WHERE pbs.[UserID] = @UserID
            AND (@ProfileID IS NULL OR pbs.[ProfileID] = @ProfileID)
        ORDER BY pbs.[SessionStart] DESC
    END
    ')
    
    PRINT 'sp_GetUserProfileBuilderHistory stored procedure created successfully'
END
ELSE
BEGIN
    PRINT 'sp_GetUserProfileBuilderHistory stored procedure already exists'
END

PRINT 'Migration 003 completed successfully - Profile Builder session tracking created'
