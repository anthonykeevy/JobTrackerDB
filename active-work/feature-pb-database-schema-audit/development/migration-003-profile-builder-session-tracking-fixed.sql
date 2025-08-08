-- Migration 003: Profile Builder Session Tracking (FIXED VERSION)
-- Description: Implement session tracking for Profile Builder workflow
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
        [CompletionStatus] [nvarchar](20) NOT NULL DEFAULT 'PENDING', -- PENDING, IN_PROGRESS, COMPLETED, ERROR
        [ValidationErrors] [nvarchar](max) NULL, -- JSON of validation errors
        [DataSnapshot] [nvarchar](max) NULL, -- JSON of step data
        [StartedAt] [datetime] NULL,
        [CompletedAt] [datetime] NULL,
        [TimeSpent] [int] NULL, -- seconds
        [createdDate] [datetime] NOT NULL DEFAULT GETDATE(),
        [createdBy] [nvarchar](100) NULL,
        [lastUpdated] [datetime] NULL,
        [updatedBy] [nvarchar](100) NULL,
        CONSTRAINT [PK_ProfileBuilderStep] PRIMARY KEY CLUSTERED ([StepID] ASC)
    )

    -- Add foreign key constraint
    ALTER TABLE [dbo].[ProfileBuilderStep] ADD CONSTRAINT [FK_ProfileBuilderStep_Session]
        FOREIGN KEY([SessionID]) REFERENCES [dbo].[ProfileBuilderSession] ([SessionID])

    -- Add indexes for performance
    CREATE NONCLUSTERED INDEX [IX_ProfileBuilderStep_SessionID] ON [dbo].[ProfileBuilderStep] ([SessionID])
    CREATE NONCLUSTERED INDEX [IX_ProfileBuilderStep_StepName] ON [dbo].[ProfileBuilderStep] ([StepName])
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
                (SELECT [FirstName] + '' '' + [LastName] FROM [dbo].[Profile] WHERE [ProfileID] = @ProfileID)
            )

            -- Initialize steps
            INSERT INTO [dbo].[ProfileBuilderStep] (
                [SessionID], [StepName], [StepOrder], [CompletionStatus], [createdBy]
            )
            VALUES
                (@SessionID, ''BasicInfo'', 1, ''PENDING'',
                 (SELECT [FirstName] + '' '' + [LastName] FROM [dbo].[Profile] WHERE [ProfileID] = @ProfileID)),
                (@SessionID, ''Address'', 2, ''PENDING'',
                 (SELECT [FirstName] + '' '' + [LastName] FROM [dbo].[Profile] WHERE [ProfileID] = @ProfileID)),
                (@SessionID, ''Education'', 3, ''PENDING'',
                 (SELECT [FirstName] + '' '' + [LastName] FROM [dbo].[Profile] WHERE [ProfileID] = @ProfileID)),
                (@SessionID, ''Certifications'', 4, ''PENDING'',
                 (SELECT [FirstName] + '' '' + [LastName] FROM [dbo].[Profile] WHERE [ProfileID] = @ProfileID)),
                (@SessionID, ''WorkExperience'', 5, ''PENDING'',
                 (SELECT [FirstName] + '' '' + [LastName] FROM [dbo].[Profile] WHERE [ProfileID] = @ProfileID)),
                (@SessionID, ''Projects'', 6, ''PENDING'',
                 (SELECT [FirstName] + '' '' + [LastName] FROM [dbo].[Profile] WHERE [ProfileID] = @ProfileID)),
                (@SessionID, ''CareerAspiration'', 7, ''PENDING'',
                 (SELECT [FirstName] + '' '' + [LastName] FROM [dbo].[Profile] WHERE [ProfileID] = @ProfileID)),
                (@SessionID, ''ReviewConfirm'', 8, ''PENDING'',
                 (SELECT [FirstName] + '' '' + [LastName] FROM [dbo].[Profile] WHERE [ProfileID] = @ProfileID))

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

-- Stored Procedure to Update Profile Builder Step
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[sp_UpdateProfileBuilderStep]') AND type in (N'P'))
BEGIN
    EXEC('
    CREATE PROCEDURE [dbo].[sp_UpdateProfileBuilderStep]
        @SessionID NVARCHAR(100),
        @StepName NVARCHAR(50),
        @CompletionStatus NVARCHAR(20),
        @ValidationErrors NVARCHAR(max) = NULL,
        @DataSnapshot NVARCHAR(max) = NULL,
        @ProfileID INT
    AS
    BEGIN
        SET NOCOUNT ON;

        BEGIN TRY
            UPDATE [dbo].[ProfileBuilderStep]
            SET
                [CompletionStatus] = @CompletionStatus,
                [ValidationErrors] = @ValidationErrors,
                [DataSnapshot] = @DataSnapshot,
                [StartedAt] = CASE WHEN @CompletionStatus = ''IN_PROGRESS'' AND [StartedAt] IS NULL THEN GETDATE() ELSE [StartedAt] END,
                [CompletedAt] = CASE WHEN @CompletionStatus = ''COMPLETED'' THEN GETDATE() ELSE [CompletedAt] END,
                [TimeSpent] = CASE WHEN @CompletionStatus = ''COMPLETED'' AND [StartedAt] IS NOT NULL 
                                   THEN DATEDIFF(SECOND, [StartedAt], GETDATE()) ELSE [TimeSpent] END,
                [lastUpdated] = GETDATE(),
                [updatedBy] = (SELECT [FirstName] + '' '' + [LastName] FROM [dbo].[Profile] WHERE [ProfileID] = @ProfileID)
            WHERE [SessionID] = @SessionID AND [StepName] = @StepName

            -- Update session current step
            UPDATE [dbo].[ProfileBuilderSession]
            SET
                [CurrentStep] = @StepName,
                [lastUpdated] = GETDATE(),
                [updatedBy] = (SELECT [FirstName] + '' '' + [LastName] FROM [dbo].[Profile] WHERE [ProfileID] = @ProfileID)
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
        @ProfileID INT
    AS
    BEGIN
        SET NOCOUNT ON;

        BEGIN TRY
            UPDATE [dbo].[ProfileBuilderSession]
            SET
                [SessionEnd] = GETDATE(),
                [lastUpdated] = GETDATE(),
                [updatedBy] = (SELECT [FirstName] + '' '' + [LastName] FROM [dbo].[Profile] WHERE [ProfileID] = @ProfileID)
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

-- Stored Procedure to Get Profile Builder Progress
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[sp_GetProfileBuilderProgress]') AND type in (N'P'))
BEGIN
    EXEC('
    CREATE PROCEDURE [dbo].[sp_GetProfileBuilderProgress]
        @SessionID NVARCHAR(100)
    AS
    BEGIN
        SET NOCOUNT ON;

        SELECT 
            s.[SessionID],
            s.[ProfileID],
            s.[UserID],
            s.[SessionStart],
            s.[SessionEnd],
            s.[CurrentStep],
            s.[StepProgress],
            s.[FormValidationErrors],
            st.[StepName],
            st.[StepOrder],
            st.[CompletionStatus],
            st.[ValidationErrors],
            st.[DataSnapshot],
            st.[StartedAt],
            st.[CompletedAt],
            st.[TimeSpent]
        FROM [dbo].[ProfileBuilderSession] s
        LEFT JOIN [dbo].[ProfileBuilderStep] st ON s.[SessionID] = st.[SessionID]
        WHERE s.[SessionID] = @SessionID
        ORDER BY st.[StepOrder]
    END
    ')

    PRINT 'sp_GetProfileBuilderProgress stored procedure created successfully'
END
ELSE
BEGIN
    PRINT 'sp_GetProfileBuilderProgress stored procedure already exists'
END

-- Stored Procedure to Get User Profile Builder History
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
            [SessionID],
            [ProfileID],
            [SessionStart],
            [SessionEnd],
            [CurrentStep],
            [StepProgress],
            [FormValidationErrors],
            DATEDIFF(MINUTE, [SessionStart], ISNULL([SessionEnd], GETDATE())) AS DurationMinutes
        FROM [dbo].[ProfileBuilderSession]
        WHERE [UserID] = @UserID
            AND (@ProfileID IS NULL OR [ProfileID] = @ProfileID)
        ORDER BY [SessionStart] DESC
    END
    ')

    PRINT 'sp_GetUserProfileBuilderHistory stored procedure created successfully'
END
ELSE
BEGIN
    PRINT 'sp_GetUserProfileBuilderHistory stored procedure already exists'
END

PRINT 'Migration 003 completed successfully - Profile Builder session tracking created with corrected column references'
