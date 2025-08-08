-- Migration 002: Audit Trail System
-- Description: Create comprehensive audit trail system for all Profile Builder operations
-- Author: BMad Architect
-- Date: 2025-01-08
-- Rollback: Yes

-- =====================================================
-- AUDIT TRAIL TABLE
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[AuditTrail]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[AuditTrail](
        [AuditTrailID] [int] IDENTITY(1,1) NOT NULL,
        [TableName] [nvarchar](100) NOT NULL,
        [RecordID] [int] NOT NULL,
        [OperationType] [nvarchar](20) NOT NULL, -- INSERT, UPDATE, DELETE
        [FieldName] [nvarchar](100) NULL,
        [OldValue] [nvarchar](max) NULL,
        [NewValue] [nvarchar](max) NULL,
        [ChangeReason] [nvarchar](500) NULL,
        [UserID] [int] NULL,
        [SessionID] [nvarchar](100) NULL,
        [IPAddress] [nvarchar](50) NULL,
        [ChangeTimestamp] [datetime] NOT NULL DEFAULT GETDATE(),
        CONSTRAINT [PK_AuditTrail] PRIMARY KEY CLUSTERED ([AuditTrailID] ASC)
    )
    
    -- Add indexes for performance
    CREATE NONCLUSTERED INDEX [IX_AuditTrail_TableRecord] ON [dbo].[AuditTrail] ([TableName], [RecordID])
    CREATE NONCLUSTERED INDEX [IX_AuditTrail_Timestamp] ON [dbo].[AuditTrail] ([ChangeTimestamp])
    CREATE NONCLUSTERED INDEX [IX_AuditTrail_User] ON [dbo].[AuditTrail] ([UserID])
    CREATE NONCLUSTERED INDEX [IX_AuditTrail_Operation] ON [dbo].[AuditTrail] ([OperationType])
    
    PRINT 'AuditTrail table created successfully'
END
ELSE
BEGIN
    PRINT 'AuditTrail table already exists'
END

-- =====================================================
-- AUDIT TRAIL TRIGGERS FOR PROFILE BUILDER TABLES
-- =====================================================

-- ProfileAddress Audit Trigger
IF NOT EXISTS (SELECT * FROM sys.triggers WHERE name = 'TR_ProfileAddress_Audit')
BEGIN
    EXEC('
    CREATE TRIGGER [dbo].[TR_ProfileAddress_Audit]
    ON [dbo].[ProfileAddress]
    AFTER INSERT, UPDATE, DELETE
    AS
    BEGIN
        SET NOCOUNT ON;
        
        DECLARE @OperationType NVARCHAR(20)
        DECLARE @UserID INT = ISNULL(CONTEXT_INFO(), 0)
        DECLARE @SessionID NVARCHAR(100) = ISNULL(SESSION_CONTEXT(N''session_id''), '''')
        DECLARE @IPAddress NVARCHAR(50) = ISNULL(SESSION_CONTEXT(N''client_ip''), '''')
        
        IF EXISTS(SELECT * FROM INSERTED) AND EXISTS(SELECT * FROM DELETED)
            SET @OperationType = ''UPDATE''
        ELSE IF EXISTS(SELECT * FROM INSERTED)
            SET @OperationType = ''INSERT''
        ELSE
            SET @OperationType = ''DELETE''
        
        -- Log the operation
        INSERT INTO [dbo].[AuditTrail] (
            [TableName], [RecordID], [OperationType], [UserID], [SessionID], [IPAddress]
        )
        SELECT 
            ''ProfileAddress'',
            ISNULL(i.[ProfileAddressID], d.[ProfileAddressID]),
            @OperationType,
            @UserID,
            @SessionID,
            @IPAddress
        FROM INSERTED i
        FULL OUTER JOIN DELETED d ON i.[ProfileAddressID] = d.[ProfileAddressID]
        WHERE i.[ProfileAddressID] IS NOT NULL OR d.[ProfileAddressID] IS NOT NULL
    END
    ')
    
    PRINT 'ProfileAddress audit trigger created successfully'
END
ELSE
BEGIN
    PRINT 'ProfileAddress audit trigger already exists'
END

-- ProfileEducation Audit Trigger
IF NOT EXISTS (SELECT * FROM sys.triggers WHERE name = 'TR_ProfileEducation_Audit')
BEGIN
    EXEC('
    CREATE TRIGGER [dbo].[TR_ProfileEducation_Audit]
    ON [dbo].[ProfileEducation]
    AFTER INSERT, UPDATE, DELETE
    AS
    BEGIN
        SET NOCOUNT ON;
        
        DECLARE @OperationType NVARCHAR(20)
        DECLARE @UserID INT = ISNULL(CONTEXT_INFO(), 0)
        DECLARE @SessionID NVARCHAR(100) = ISNULL(SESSION_CONTEXT(N''session_id''), '''')
        DECLARE @IPAddress NVARCHAR(50) = ISNULL(SESSION_CONTEXT(N''client_ip''), '''')
        
        IF EXISTS(SELECT * FROM INSERTED) AND EXISTS(SELECT * FROM DELETED)
            SET @OperationType = ''UPDATE''
        ELSE IF EXISTS(SELECT * FROM INSERTED)
            SET @OperationType = ''INSERT''
        ELSE
            SET @OperationType = ''DELETE''
        
        -- Log the operation
        INSERT INTO [dbo].[AuditTrail] (
            [TableName], [RecordID], [OperationType], [UserID], [SessionID], [IPAddress]
        )
        SELECT 
            ''ProfileEducation'',
            ISNULL(i.[ProfileEducationID], d.[ProfileEducationID]),
            @OperationType,
            @UserID,
            @SessionID,
            @IPAddress
        FROM INSERTED i
        FULL OUTER JOIN DELETED d ON i.[ProfileEducationID] = d.[ProfileEducationID]
        WHERE i.[ProfileEducationID] IS NOT NULL OR d.[ProfileEducationID] IS NOT NULL
    END
    ')
    
    PRINT 'ProfileEducation audit trigger created successfully'
END
ELSE
BEGIN
    PRINT 'ProfileEducation audit trigger already exists'
END

-- ProfileCertification Audit Trigger
IF NOT EXISTS (SELECT * FROM sys.triggers WHERE name = 'TR_ProfileCertification_Audit')
BEGIN
    EXEC('
    CREATE TRIGGER [dbo].[TR_ProfileCertification_Audit]
    ON [dbo].[ProfileCertification]
    AFTER INSERT, UPDATE, DELETE
    AS
    BEGIN
        SET NOCOUNT ON;
        
        DECLARE @OperationType NVARCHAR(20)
        DECLARE @UserID INT = ISNULL(CONTEXT_INFO(), 0)
        DECLARE @SessionID NVARCHAR(100) = ISNULL(SESSION_CONTEXT(N''session_id''), '''')
        DECLARE @IPAddress NVARCHAR(50) = ISNULL(SESSION_CONTEXT(N''client_ip''), '''')
        
        IF EXISTS(SELECT * FROM INSERTED) AND EXISTS(SELECT * FROM DELETED)
            SET @OperationType = ''UPDATE''
        ELSE IF EXISTS(SELECT * FROM INSERTED)
            SET @OperationType = ''INSERT''
        ELSE
            SET @OperationType = ''DELETE''
        
        -- Log the operation
        INSERT INTO [dbo].[AuditTrail] (
            [TableName], [RecordID], [OperationType], [UserID], [SessionID], [IPAddress]
        )
        SELECT 
            ''ProfileCertification'',
            ISNULL(i.[ProfileCertificationID], d.[ProfileCertificationID]),
            @OperationType,
            @UserID,
            @SessionID,
            @IPAddress
        FROM INSERTED i
        FULL OUTER JOIN DELETED d ON i.[ProfileCertificationID] = d.[ProfileCertificationID]
        WHERE i.[ProfileCertificationID] IS NOT NULL OR d.[ProfileCertificationID] IS NOT NULL
    END
    ')
    
    PRINT 'ProfileCertification audit trigger created successfully'
END
ELSE
BEGIN
    PRINT 'ProfileCertification audit trigger already exists'
END

-- ProfileWorkExperience Audit Trigger
IF NOT EXISTS (SELECT * FROM sys.triggers WHERE name = 'TR_ProfileWorkExperience_Audit')
BEGIN
    EXEC('
    CREATE TRIGGER [dbo].[TR_ProfileWorkExperience_Audit]
    ON [dbo].[ProfileWorkExperience]
    AFTER INSERT, UPDATE, DELETE
    AS
    BEGIN
        SET NOCOUNT ON;
        
        DECLARE @OperationType NVARCHAR(20)
        DECLARE @UserID INT = ISNULL(CONTEXT_INFO(), 0)
        DECLARE @SessionID NVARCHAR(100) = ISNULL(SESSION_CONTEXT(N''session_id''), '''')
        DECLARE @IPAddress NVARCHAR(50) = ISNULL(SESSION_CONTEXT(N''client_ip''), '''')
        
        IF EXISTS(SELECT * FROM INSERTED) AND EXISTS(SELECT * FROM DELETED)
            SET @OperationType = ''UPDATE''
        ELSE IF EXISTS(SELECT * FROM INSERTED)
            SET @OperationType = ''INSERT''
        ELSE
            SET @OperationType = ''DELETE''
        
        -- Log the operation
        INSERT INTO [dbo].[AuditTrail] (
            [TableName], [RecordID], [OperationType], [UserID], [SessionID], [IPAddress]
        )
        SELECT 
            ''ProfileWorkExperience'',
            ISNULL(i.[ProfileWorkExperienceID], d.[ProfileWorkExperienceID]),
            @OperationType,
            @UserID,
            @SessionID,
            @IPAddress
        FROM INSERTED i
        FULL OUTER JOIN DELETED d ON i.[ProfileWorkExperienceID] = d.[ProfileWorkExperienceID]
        WHERE i.[ProfileWorkExperienceID] IS NOT NULL OR d.[ProfileWorkExperienceID] IS NOT NULL
    END
    ')
    
    PRINT 'ProfileWorkExperience audit trigger created successfully'
END
ELSE
BEGIN
    PRINT 'ProfileWorkExperience audit trigger already exists'
END

-- ProfileProject Audit Trigger
IF NOT EXISTS (SELECT * FROM sys.triggers WHERE name = 'TR_ProfileProject_Audit')
BEGIN
    EXEC('
    CREATE TRIGGER [dbo].[TR_ProfileProject_Audit]
    ON [dbo].[ProfileProject]
    AFTER INSERT, UPDATE, DELETE
    AS
    BEGIN
        SET NOCOUNT ON;
        
        DECLARE @OperationType NVARCHAR(20)
        DECLARE @UserID INT = ISNULL(CONTEXT_INFO(), 0)
        DECLARE @SessionID NVARCHAR(100) = ISNULL(SESSION_CONTEXT(N''session_id''), '''')
        DECLARE @IPAddress NVARCHAR(50) = ISNULL(SESSION_CONTEXT(N''client_ip''), '''')
        
        IF EXISTS(SELECT * FROM INSERTED) AND EXISTS(SELECT * FROM DELETED)
            SET @OperationType = ''UPDATE''
        ELSE IF EXISTS(SELECT * FROM INSERTED)
            SET @OperationType = ''INSERT''
        ELSE
            SET @OperationType = ''DELETE''
        
        -- Log the operation
        INSERT INTO [dbo].[AuditTrail] (
            [TableName], [RecordID], [OperationType], [UserID], [SessionID], [IPAddress]
        )
        SELECT 
            ''ProfileProject'',
            ISNULL(i.[ProfileProjectID], d.[ProfileProjectID]),
            @OperationType,
            @UserID,
            @SessionID,
            @IPAddress
        FROM INSERTED i
        FULL OUTER JOIN DELETED d ON i.[ProfileProjectID] = d.[ProfileProjectID]
        WHERE i.[ProfileProjectID] IS NOT NULL OR d.[ProfileProjectID] IS NOT NULL
    END
    ')
    
    PRINT 'ProfileProject audit trigger created successfully'
END
ELSE
BEGIN
    PRINT 'ProfileProject audit trigger already exists'
END

-- ProfileCareerAspiration Audit Trigger
IF NOT EXISTS (SELECT * FROM sys.triggers WHERE name = 'TR_ProfileCareerAspiration_Audit')
BEGIN
    EXEC('
    CREATE TRIGGER [dbo].[TR_ProfileCareerAspiration_Audit]
    ON [dbo].[ProfileCareerAspiration]
    AFTER INSERT, UPDATE, DELETE
    AS
    BEGIN
        SET NOCOUNT ON;
        
        DECLARE @OperationType NVARCHAR(20)
        DECLARE @UserID INT = ISNULL(CONTEXT_INFO(), 0)
        DECLARE @SessionID NVARCHAR(100) = ISNULL(SESSION_CONTEXT(N''session_id''), '''')
        DECLARE @IPAddress NVARCHAR(50) = ISNULL(SESSION_CONTEXT(N''client_ip''), '''')
        
        IF EXISTS(SELECT * FROM INSERTED) AND EXISTS(SELECT * FROM DELETED)
            SET @OperationType = ''UPDATE''
        ELSE IF EXISTS(SELECT * FROM INSERTED)
            SET @OperationType = ''INSERT''
        ELSE
            SET @OperationType = ''DELETE''
        
        -- Log the operation
        INSERT INTO [dbo].[AuditTrail] (
            [TableName], [RecordID], [OperationType], [UserID], [SessionID], [IPAddress]
        )
        SELECT 
            ''ProfileCareerAspiration'',
            ISNULL(i.[ProfileCareerAspirationID], d.[ProfileCareerAspirationID]),
            @OperationType,
            @UserID,
            @SessionID,
            @IPAddress
        FROM INSERTED i
        FULL OUTER JOIN DELETED d ON i.[ProfileCareerAspirationID] = d.[ProfileCareerAspirationID]
        WHERE i.[ProfileCareerAspirationID] IS NOT NULL OR d.[ProfileCareerAspirationID] IS NOT NULL
    END
    ')
    
    PRINT 'ProfileCareerAspiration audit trigger created successfully'
END
ELSE
BEGIN
    PRINT 'ProfileCareerAspiration audit trigger already exists'
END

-- =====================================================
-- AUDIT TRAIL STORED PROCEDURES
-- =====================================================

-- Stored Procedure to Set Audit Context
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[sp_SetAuditContext]') AND type in (N'P'))
BEGIN
    EXEC('
    CREATE PROCEDURE [dbo].[sp_SetAuditContext]
        @UserID INT,
        @SessionID NVARCHAR(100) = NULL,
        @IPAddress NVARCHAR(50) = NULL
    AS
    BEGIN
        SET NOCOUNT ON;
        
        -- Set context info for triggers to access
        DECLARE @ContextInfo VARBINARY(128) = CAST(@UserID AS VARBINARY(128))
        SET CONTEXT_INFO @ContextInfo
        
        -- Set session context for additional info
        IF @SessionID IS NOT NULL
            EXEC sp_set_session_context @key = ''session_id'', @value = @SessionID
        
        IF @IPAddress IS NOT NULL
            EXEC sp_set_session_context @key = ''client_ip'', @value = @IPAddress
    END
    ')
    
    PRINT 'sp_SetAuditContext stored procedure created successfully'
END
ELSE
BEGIN
    PRINT 'sp_SetAuditContext stored procedure already exists'
END

-- Stored Procedure to Get Audit Trail
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[sp_GetAuditTrail]') AND type in (N'P'))
BEGIN
    EXEC('
    CREATE PROCEDURE [dbo].[sp_GetAuditTrail]
        @TableName NVARCHAR(100) = NULL,
        @RecordID INT = NULL,
        @UserID INT = NULL,
        @StartDate DATETIME = NULL,
        @EndDate DATETIME = NULL,
        @OperationType NVARCHAR(20) = NULL
    AS
    BEGIN
        SET NOCOUNT ON;
        
        SELECT 
            at.[AuditTrailID],
            at.[TableName],
            at.[RecordID],
            at.[OperationType],
            at.[FieldName],
            at.[OldValue],
            at.[NewValue],
            at.[ChangeReason],
            at.[UserID],
            u.[FirstName] + '' '' + u.[LastName] AS UserName,
            at.[SessionID],
            at.[IPAddress],
            at.[ChangeTimestamp]
        FROM [dbo].[AuditTrail] at
        LEFT JOIN [dbo].[User] u ON at.[UserID] = u.[UserID]
        WHERE (@TableName IS NULL OR at.[TableName] = @TableName)
            AND (@RecordID IS NULL OR at.[RecordID] = @RecordID)
            AND (@UserID IS NULL OR at.[UserID] = @UserID)
            AND (@StartDate IS NULL OR at.[ChangeTimestamp] >= @StartDate)
            AND (@EndDate IS NULL OR at.[ChangeTimestamp] <= @EndDate)
            AND (@OperationType IS NULL OR at.[OperationType] = @OperationType)
        ORDER BY at.[ChangeTimestamp] DESC
    END
    ')
    
    PRINT 'sp_GetAuditTrail stored procedure created successfully'
END
ELSE
BEGIN
    PRINT 'sp_GetAuditTrail stored procedure already exists'
END

PRINT 'Migration 002 completed successfully - Audit trail system created'
