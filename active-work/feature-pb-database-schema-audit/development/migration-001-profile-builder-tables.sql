-- Migration 001: Profile Builder Tables
-- Description: Add missing tables for Profile Builder workflow
-- Author: BMad Architect
-- Date: 2025-01-08
-- Rollback: Yes

-- =====================================================
-- PROFILE ADDRESS TABLE
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[ProfileAddress]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[ProfileAddress](
        [ProfileAddressID] [int] IDENTITY(1,1) NOT NULL,
        [ProfileID] [int] NOT NULL,
        [AddressLine1] [nvarchar](255) NOT NULL,
        [AddressLine2] [nvarchar](255) NULL,
        [AddressLine3] [nvarchar](255) NULL,
        [City] [nvarchar](100) NOT NULL,
        [State] [nvarchar](100) NULL,
        [PostalCode] [nvarchar](20) NULL,
        [Country] [nvarchar](100) NOT NULL,
        [Latitude] [decimal](10,8) NULL,
        [Longitude] [decimal](11,8) NULL,
        [ValidationStatus] [nvarchar](50) NULL,
        [ValidationSource] [nvarchar](100) NULL,
        [ValidationDate] [datetime] NULL,
        [IsPrimary] [bit] NOT NULL DEFAULT 1,
        [createdDate] [datetime] NOT NULL DEFAULT GETDATE(),
        [createdBy] [nvarchar](100) NULL,
        [lastUpdated] [datetime] NULL,
        [updatedBy] [nvarchar](100) NULL,
        CONSTRAINT [PK_ProfileAddress] PRIMARY KEY CLUSTERED ([ProfileAddressID] ASC)
    )
    
    -- Add foreign key constraint
    ALTER TABLE [dbo].[ProfileAddress] ADD CONSTRAINT [FK_ProfileAddress_Profile] 
        FOREIGN KEY([ProfileID]) REFERENCES [dbo].[Profile] ([ProfileID])
    
    -- Add indexes for performance
    CREATE NONCLUSTERED INDEX [IX_ProfileAddress_ProfileID] ON [dbo].[ProfileAddress] ([ProfileID])
    CREATE NONCLUSTERED INDEX [IX_ProfileAddress_IsPrimary] ON [dbo].[ProfileAddress] ([IsPrimary])
    
    PRINT 'ProfileAddress table created successfully'
END
ELSE
BEGIN
    PRINT 'ProfileAddress table already exists'
END

-- =====================================================
-- PROFILE EDUCATION TABLE
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[ProfileEducation]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[ProfileEducation](
        [ProfileEducationID] [int] IDENTITY(1,1) NOT NULL,
        [ProfileID] [int] NOT NULL,
        [InstitutionName] [nvarchar](255) NOT NULL,
        [Degree] [nvarchar](255) NOT NULL,
        [FieldOfStudy] [nvarchar](255) NOT NULL,
        [StartDate] [date] NULL,
        [EndDate] [date] NULL,
        [IsCurrent] [bit] NOT NULL DEFAULT 0,
        [GPA] [decimal](3,2) NULL,
        [Description] [nvarchar](1000) NULL,
        [createdDate] [datetime] NOT NULL DEFAULT GETDATE(),
        [createdBy] [nvarchar](100) NULL,
        [lastUpdated] [datetime] NULL,
        [updatedBy] [nvarchar](100) NULL,
        CONSTRAINT [PK_ProfileEducation] PRIMARY KEY CLUSTERED ([ProfileEducationID] ASC)
    )
    
    -- Add foreign key constraint
    ALTER TABLE [dbo].[ProfileEducation] ADD CONSTRAINT [FK_ProfileEducation_Profile] 
        FOREIGN KEY([ProfileID]) REFERENCES [dbo].[Profile] ([ProfileID])
    
    -- Add indexes for performance
    CREATE NONCLUSTERED INDEX [IX_ProfileEducation_ProfileID] ON [dbo].[ProfileEducation] ([ProfileID])
    CREATE NONCLUSTERED INDEX [IX_ProfileEducation_IsCurrent] ON [dbo].[ProfileEducation] ([IsCurrent])
    
    PRINT 'ProfileEducation table created successfully'
END
ELSE
BEGIN
    PRINT 'ProfileEducation table already exists'
END

-- =====================================================
-- PROFILE CERTIFICATION TABLE
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[ProfileCertification]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[ProfileCertification](
        [ProfileCertificationID] [int] IDENTITY(1,1) NOT NULL,
        [ProfileID] [int] NOT NULL,
        [CertificationName] [nvarchar](255) NOT NULL,
        [IssuingOrganization] [nvarchar](255) NOT NULL,
        [IssueDate] [date] NULL,
        [ExpiryDate] [date] NULL,
        [CredentialID] [nvarchar](100) NULL,
        [CredentialURL] [nvarchar](500) NULL,
        [Description] [nvarchar](1000) NULL,
        [createdDate] [datetime] NOT NULL DEFAULT GETDATE(),
        [createdBy] [nvarchar](100) NULL,
        [lastUpdated] [datetime] NULL,
        [updatedBy] [nvarchar](100) NULL,
        CONSTRAINT [PK_ProfileCertification] PRIMARY KEY CLUSTERED ([ProfileCertificationID] ASC)
    )
    
    -- Add foreign key constraint
    ALTER TABLE [dbo].[ProfileCertification] ADD CONSTRAINT [FK_ProfileCertification_Profile] 
        FOREIGN KEY([ProfileID]) REFERENCES [dbo].[Profile] ([ProfileID])
    
    -- Add indexes for performance
    CREATE NONCLUSTERED INDEX [IX_ProfileCertification_ProfileID] ON [dbo].[ProfileCertification] ([ProfileID])
    CREATE NONCLUSTERED INDEX [IX_ProfileCertification_ExpiryDate] ON [dbo].[ProfileCertification] ([ExpiryDate])
    
    PRINT 'ProfileCertification table created successfully'
END
ELSE
BEGIN
    PRINT 'ProfileCertification table already exists'
END

-- =====================================================
-- PROFILE WORK EXPERIENCE TABLE
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[ProfileWorkExperience]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[ProfileWorkExperience](
        [ProfileWorkExperienceID] [int] IDENTITY(1,1) NOT NULL,
        [ProfileID] [int] NOT NULL,
        [CompanyName] [nvarchar](255) NOT NULL,
        [JobTitle] [nvarchar](255) NOT NULL,
        [Location] [nvarchar](255) NULL,
        [StartDate] [date] NOT NULL,
        [EndDate] [date] NULL,
        [IsCurrent] [bit] NOT NULL DEFAULT 0,
        [Description] [nvarchar](2000) NULL,
        [createdDate] [datetime] NOT NULL DEFAULT GETDATE(),
        [createdBy] [nvarchar](100) NULL,
        [lastUpdated] [datetime] NULL,
        [updatedBy] [nvarchar](100) NULL,
        CONSTRAINT [PK_ProfileWorkExperience] PRIMARY KEY CLUSTERED ([ProfileWorkExperienceID] ASC)
    )
    
    -- Add foreign key constraint
    ALTER TABLE [dbo].[ProfileWorkExperience] ADD CONSTRAINT [FK_ProfileWorkExperience_Profile] 
        FOREIGN KEY([ProfileID]) REFERENCES [dbo].[Profile] ([ProfileID])
    
    -- Add indexes for performance
    CREATE NONCLUSTERED INDEX [IX_ProfileWorkExperience_ProfileID] ON [dbo].[ProfileWorkExperience] ([ProfileID])
    CREATE NONCLUSTERED INDEX [IX_ProfileWorkExperience_IsCurrent] ON [dbo].[ProfileWorkExperience] ([IsCurrent])
    CREATE NONCLUSTERED INDEX [IX_ProfileWorkExperience_StartDate] ON [dbo].[ProfileWorkExperience] ([StartDate])
    
    PRINT 'ProfileWorkExperience table created successfully'
END
ELSE
BEGIN
    PRINT 'ProfileWorkExperience table already exists'
END

-- =====================================================
-- PROFILE WORK ACHIEVEMENT TABLE
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[ProfileWorkAchievement]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[ProfileWorkAchievement](
        [ProfileWorkAchievementID] [int] IDENTITY(1,1) NOT NULL,
        [ProfileWorkExperienceID] [int] NOT NULL,
        [Achievement] [nvarchar](1000) NOT NULL,
        [AchievementType] [nvarchar](50) NULL,
        [createdDate] [datetime] NOT NULL DEFAULT GETDATE(),
        [createdBy] [nvarchar](100) NULL,
        [lastUpdated] [datetime] NULL,
        [updatedBy] [nvarchar](100) NULL,
        CONSTRAINT [PK_ProfileWorkAchievement] PRIMARY KEY CLUSTERED ([ProfileWorkAchievementID] ASC)
    )
    
    -- Add foreign key constraint
    ALTER TABLE [dbo].[ProfileWorkAchievement] ADD CONSTRAINT [FK_ProfileWorkAchievement_ProfileWorkExperience] 
        FOREIGN KEY([ProfileWorkExperienceID]) REFERENCES [dbo].[ProfileWorkExperience] ([ProfileWorkExperienceID])
    
    -- Add indexes for performance
    CREATE NONCLUSTERED INDEX [IX_ProfileWorkAchievement_ProfileWorkExperienceID] ON [dbo].[ProfileWorkAchievement] ([ProfileWorkExperienceID])
    
    PRINT 'ProfileWorkAchievement table created successfully'
END
ELSE
BEGIN
    PRINT 'ProfileWorkAchievement table already exists'
END

-- =====================================================
-- PROFILE PROJECT TABLE
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[ProfileProject]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[ProfileProject](
        [ProfileProjectID] [int] IDENTITY(1,1) NOT NULL,
        [ProfileID] [int] NOT NULL,
        [ProjectName] [nvarchar](255) NOT NULL,
        [Description] [nvarchar](2000) NULL,
        [ProjectURL] [nvarchar](500) NULL,
        [StartDate] [date] NULL,
        [EndDate] [date] NULL,
        [IsCurrent] [bit] NOT NULL DEFAULT 0,
        [createdDate] [datetime] NOT NULL DEFAULT GETDATE(),
        [createdBy] [nvarchar](100) NULL,
        [lastUpdated] [datetime] NULL,
        [updatedBy] [nvarchar](100) NULL,
        CONSTRAINT [PK_ProfileProject] PRIMARY KEY CLUSTERED ([ProfileProjectID] ASC)
    )
    
    -- Add foreign key constraint
    ALTER TABLE [dbo].[ProfileProject] ADD CONSTRAINT [FK_ProfileProject_Profile] 
        FOREIGN KEY([ProfileID]) REFERENCES [dbo].[Profile] ([ProfileID])
    
    -- Add indexes for performance
    CREATE NONCLUSTERED INDEX [IX_ProfileProject_ProfileID] ON [dbo].[ProfileProject] ([ProfileID])
    CREATE NONCLUSTERED INDEX [IX_ProfileProject_IsCurrent] ON [dbo].[ProfileProject] ([IsCurrent])
    
    PRINT 'ProfileProject table created successfully'
END
ELSE
BEGIN
    PRINT 'ProfileProject table already exists'
END

-- =====================================================
-- PROFILE PROJECT TECHNOLOGY TABLE
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[ProfileProjectTechnology]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[ProfileProjectTechnology](
        [ProfileProjectTechnologyID] [int] IDENTITY(1,1) NOT NULL,
        [ProfileProjectID] [int] NOT NULL,
        [TechnologyName] [nvarchar](100) NOT NULL,
        [TechnologyCategory] [nvarchar](50) NULL,
        [createdDate] [datetime] NOT NULL DEFAULT GETDATE(),
        [createdBy] [nvarchar](100) NULL,
        [lastUpdated] [datetime] NULL,
        [updatedBy] [nvarchar](100) NULL,
        CONSTRAINT [PK_ProfileProjectTechnology] PRIMARY KEY CLUSTERED ([ProfileProjectTechnologyID] ASC)
    )
    
    -- Add foreign key constraint
    ALTER TABLE [dbo].[ProfileProjectTechnology] ADD CONSTRAINT [FK_ProfileProjectTechnology_ProfileProject] 
        FOREIGN KEY([ProfileProjectID]) REFERENCES [dbo].[ProfileProject] ([ProfileProjectID])
    
    -- Add indexes for performance
    CREATE NONCLUSTERED INDEX [IX_ProfileProjectTechnology_ProfileProjectID] ON [dbo].[ProfileProjectTechnology] ([ProfileProjectID])
    CREATE NONCLUSTERED INDEX [IX_ProfileProjectTechnology_Category] ON [dbo].[ProfileProjectTechnology] ([TechnologyCategory])
    
    PRINT 'ProfileProjectTechnology table created successfully'
END
ELSE
BEGIN
    PRINT 'ProfileProjectTechnology table already exists'
END

-- =====================================================
-- PROFILE CAREER ASPIRATION TABLE
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[ProfileCareerAspiration]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[ProfileCareerAspiration](
        [ProfileCareerAspirationID] [int] IDENTITY(1,1) NOT NULL,
        [ProfileID] [int] NOT NULL,
        [CurrentTitle] [nvarchar](255) NULL,
        [DesiredTitle] [nvarchar](255) NULL,
        [TargetIndustry] [nvarchar](255) NULL,
        [SalaryRangeMin] [decimal](10,2) NULL,
        [SalaryRangeMax] [decimal](10,2) NULL,
        [WorkPreferences] [nvarchar](1000) NULL,
        [RelocationWillingness] [bit] NULL,
        [RemoteWorkPreference] [nvarchar](50) NULL,
        [createdDate] [datetime] NOT NULL DEFAULT GETDATE(),
        [createdBy] [nvarchar](100) NULL,
        [lastUpdated] [datetime] NULL,
        [updatedBy] [nvarchar](100) NULL,
        CONSTRAINT [PK_ProfileCareerAspiration] PRIMARY KEY CLUSTERED ([ProfileCareerAspirationID] ASC)
    )
    
    -- Add foreign key constraint
    ALTER TABLE [dbo].[ProfileCareerAspiration] ADD CONSTRAINT [FK_ProfileCareerAspiration_Profile] 
        FOREIGN KEY([ProfileID]) REFERENCES [dbo].[Profile] ([ProfileID])
    
    -- Add indexes for performance
    CREATE NONCLUSTERED INDEX [IX_ProfileCareerAspiration_ProfileID] ON [dbo].[ProfileCareerAspiration] ([ProfileID])
    
    PRINT 'ProfileCareerAspiration table created successfully'
END
ELSE
BEGIN
    PRINT 'ProfileCareerAspiration table already exists'
END

-- =====================================================
-- PROFILE RESUME PARSING DATA TABLE
-- =====================================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[ProfileResumeParsingData]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[ProfileResumeParsingData](
        [ProfileResumeParsingDataID] [int] IDENTITY(1,1) NOT NULL,
        [ProfileID] [int] NOT NULL,
        [ResumeID] [int] NULL,
        [ParsedContent] [nvarchar](max) NULL,
        [ParsingStatus] [nvarchar](50) NOT NULL,
        [ParsingSource] [nvarchar](100) NULL,
        [ParsingDate] [datetime] NULL,
        [ConfidenceScore] [decimal](3,2) NULL,
        [ExtractedSkills] [nvarchar](max) NULL,
        [ExtractedExperience] [nvarchar](max) NULL,
        [ExtractedEducation] [nvarchar](max) NULL,
        [createdDate] [datetime] NOT NULL DEFAULT GETDATE(),
        [createdBy] [nvarchar](100) NULL,
        [lastUpdated] [datetime] NULL,
        [updatedBy] [nvarchar](100) NULL,
        CONSTRAINT [PK_ProfileResumeParsingData] PRIMARY KEY CLUSTERED ([ProfileResumeParsingDataID] ASC)
    )
    
    -- Add foreign key constraints
    ALTER TABLE [dbo].[ProfileResumeParsingData] ADD CONSTRAINT [FK_ProfileResumeParsingData_Profile] 
        FOREIGN KEY([ProfileID]) REFERENCES [dbo].[Profile] ([ProfileID])
    ALTER TABLE [dbo].[ProfileResumeParsingData] ADD CONSTRAINT [FK_ProfileResumeParsingData_Resume] 
        FOREIGN KEY([ResumeID]) REFERENCES [dbo].[Resume] ([ResumeID])
    
    -- Add indexes for performance
    CREATE NONCLUSTERED INDEX [IX_ProfileResumeParsingData_ProfileID] ON [dbo].[ProfileResumeParsingData] ([ProfileID])
    CREATE NONCLUSTERED INDEX [IX_ProfileResumeParsingData_ResumeID] ON [dbo].[ProfileResumeParsingData] ([ResumeID])
    CREATE NONCLUSTERED INDEX [IX_ProfileResumeParsingData_Status] ON [dbo].[ProfileResumeParsingData] ([ParsingStatus])
    
    PRINT 'ProfileResumeParsingData table created successfully'
END
ELSE
BEGIN
    PRINT 'ProfileResumeParsingData table already exists'
END

PRINT 'Migration 001 completed successfully - Profile Builder tables created with correct hierarchical naming'
