-- Migration 005: Execute All Profile Builder Schema Migrations
-- Description: Execute all Profile Builder database schema enhancements in order
-- Author: BMad Architect
-- Date: 2025-01-08
-- Rollback: Yes

-- =====================================================
-- MIGRATION EXECUTION SCRIPT
-- =====================================================

PRINT '====================================================='
PRINT 'STARTING PROFILE BUILDER SCHEMA MIGRATION'
PRINT '====================================================='
PRINT ''

-- Set transaction isolation level
SET TRANSACTION ISOLATION LEVEL READ COMMITTED

-- Begin transaction
BEGIN TRANSACTION

BEGIN TRY
    -- =====================================================
    -- MIGRATION 001: PROFILE BUILDER TABLES
    -- =====================================================
    PRINT 'Executing Migration 001: Profile Builder Tables...'
    
    -- Execute Migration 001 content
    :r "active-work/feature-pb-database-schema-audit/development/migration-001-profile-builder-tables.sql"
    
    PRINT 'Migration 001 completed successfully'
    PRINT ''
    
    -- =====================================================
    -- MIGRATION 002: AUDIT TRAIL SYSTEM
    -- =====================================================
    PRINT 'Executing Migration 002: Audit Trail System...'
    
    -- Execute Migration 002 content
    :r "active-work/feature-pb-database-schema-audit/development/migration-002-audit-trail-system.sql"
    
    PRINT 'Migration 002 completed successfully'
    PRINT ''
    
    -- =====================================================
    -- MIGRATION 003: PROFILE BUILDER SESSION TRACKING
    -- =====================================================
    PRINT 'Executing Migration 003: Profile Builder Session Tracking...'
    
    -- Execute Migration 003 content
    :r "active-work/feature-pb-database-schema-audit/development/migration-003-profile-builder-session-tracking.sql"
    
    PRINT 'Migration 003 completed successfully'
    PRINT ''
    
    -- =====================================================
    -- MIGRATION 004: USER PREFERENCES ENHANCEMENT
    -- =====================================================
    PRINT 'Executing Migration 004: UserPreferences Enhancement...'
    
    -- Execute Migration 004 content
    :r "active-work/feature-pb-database-schema-audit/development/migration-004-user-preferences-enhancement.sql"
    
    PRINT 'Migration 004 completed successfully'
    PRINT ''
    
    -- =====================================================
    -- VERIFICATION AND VALIDATION
    -- =====================================================
    PRINT 'Verifying migration results...'
    
    -- Check if all tables were created
    DECLARE @TableCount INT = 0
    DECLARE @ExpectedTables INT = 12
    
    SELECT @TableCount = COUNT(*) FROM sys.tables 
    WHERE name IN (
        'ProfileAddress', 'ProfileEducation', 'ProfileCertification', 
        'ProfileWorkExperience', 'ProfileWorkAchievement', 'ProfileProject',
        'ProfileProjectTechnology', 'ProfileCareerAspiration', 'ProfileResumeParsingData',
        'AuditTrail', 'ProfileBuilderSession', 'ProfileBuilderStep'
    )
    
    IF @TableCount = @ExpectedTables
    BEGIN
        PRINT '✅ All Profile Builder tables created successfully'
    END
    ELSE
    BEGIN
        PRINT '❌ Expected ' + CAST(@ExpectedTables AS VARCHAR) + ' tables, found ' + CAST(@TableCount AS VARCHAR)
        RAISERROR('Table count mismatch', 16, 1)
    END
    
    -- Check if all stored procedures were created
    DECLARE @ProcCount INT = 0
    DECLARE @ExpectedProcs INT = 12
    
    SELECT @ProcCount = COUNT(*) FROM sys.procedures 
    WHERE name IN (
        'sp_SetAuditContext', 'sp_GetAuditTrail',
        'sp_StartProfileBuilderSession', 'sp_UpdateProfileBuilderStep',
        'sp_EndProfileBuilderSession', 'sp_GetProfileBuilderProgress',
        'sp_GetUserProfileBuilderHistory', 'sp_UpdateProfileBuilderProgress',
        'sp_GetProfileBuilderStatus', 'sp_ResetProfileBuilderProgress',
        'sp_CalculateProfileCompletion'
    )
    
    IF @ProcCount = @ExpectedProcs
    BEGIN
        PRINT '✅ All Profile Builder stored procedures created successfully'
    END
    ELSE
    BEGIN
        PRINT '❌ Expected ' + CAST(@ExpectedProcs AS VARCHAR) + ' procedures, found ' + CAST(@ProcCount AS VARCHAR)
        RAISERROR('Stored procedure count mismatch', 16, 1)
    END
    
    -- Check UserPreferences enhancements
    DECLARE @ColumnCount INT = 0
    DECLARE @ExpectedColumns INT = 8
    
    SELECT @ColumnCount = COUNT(*) FROM sys.columns 
    WHERE object_id = OBJECT_ID('UserPreferences')
    AND name IN (
        'ProfileBuilderMode', 'ProfileCompletionPercentage', 'LastProfileUpdate',
        'ProfileVersion', 'IsProfileComplete', 'ProfileBuilderLastSessionID',
        'ProfileBuilderStepProgress', 'ProfileBuilderValidationErrors'
    )
    
    IF @ColumnCount = @ExpectedColumns
    BEGIN
        PRINT '✅ All UserPreferences enhancements applied successfully'
    END
    ELSE
    BEGIN
        PRINT '❌ Expected ' + CAST(@ExpectedColumns AS VARCHAR) + ' columns, found ' + CAST(@ColumnCount AS VARCHAR)
        RAISERROR('UserPreferences column count mismatch', 16, 1)
    END
    
    -- =====================================================
    -- PERFORMANCE OPTIMIZATION
    -- =====================================================
    PRINT 'Applying performance optimizations...'
    
    -- Update statistics on new tables
    UPDATE STATISTICS [dbo].[ProfileAddress]
    UPDATE STATISTICS [dbo].[ProfileEducation]
    UPDATE STATISTICS [dbo].[ProfileCertification]
    UPDATE STATISTICS [dbo].[ProfileWorkExperience]
    UPDATE STATISTICS [dbo].[ProfileWorkAchievement]
    UPDATE STATISTICS [dbo].[ProfileProject]
    UPDATE STATISTICS [dbo].[ProfileProjectTechnology]
    UPDATE STATISTICS [dbo].[ProfileCareerAspiration]
    UPDATE STATISTICS [dbo].[ProfileResumeParsingData]
    UPDATE STATISTICS [dbo].[AuditTrail]
    UPDATE STATISTICS [dbo].[ProfileBuilderSession]
    UPDATE STATISTICS [dbo].[ProfileBuilderStep]
    
    PRINT '✅ Statistics updated for all new tables'
    
    -- =====================================================
    -- MIGRATION COMPLETION
    -- =====================================================
    PRINT ''
    PRINT '====================================================='
    PRINT 'PROFILE BUILDER SCHEMA MIGRATION COMPLETED SUCCESSFULLY'
    PRINT '====================================================='
    PRINT ''
    PRINT '📊 Migration Summary:'
    PRINT '   • 12 new tables created with hierarchical naming'
    PRINT '   • Comprehensive audit trail system implemented'
    PRINT '   • Profile Builder session tracking enabled'
    PRINT '   • UserPreferences enhanced with progress tracking'
    PRINT '   • 12 stored procedures created for workflow management'
    PRINT '   • Performance optimizations applied'
    PRINT ''
    PRINT '🎯 Next Steps:'
    PRINT '   1. Test the new API endpoints'
    PRINT '   2. Verify data persistence in Profile Builder'
    PRINT '   3. Validate audit trail functionality'
    PRINT '   4. Test session tracking and progress calculation'
    PRINT ''
    
    -- Commit transaction
    COMMIT TRANSACTION
    
    PRINT '✅ All migrations committed successfully'
    
END TRY
BEGIN CATCH
    -- Rollback transaction on error
    IF @@TRANCOUNT > 0
        ROLLBACK TRANSACTION
    
    PRINT '❌ Migration failed with error:'
    PRINT ERROR_MESSAGE()
    PRINT ''
    PRINT 'Error Details:'
    PRINT 'Error Number: ' + CAST(ERROR_NUMBER() AS VARCHAR)
    PRINT 'Error Line: ' + CAST(ERROR_LINE() AS VARCHAR)
    PRINT 'Error Procedure: ' + ISNULL(ERROR_PROCEDURE(), 'N/A')
    
    RAISERROR('Migration failed - see error details above', 16, 1)
END CATCH

PRINT ''
PRINT 'Migration execution completed'
