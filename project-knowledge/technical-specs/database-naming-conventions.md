# Database Naming Conventions & Schema Standards

## Overview
This document defines the standardized naming conventions and schema patterns for the JobTrackerDB project. All database objects must adhere to these conventions to ensure consistency, maintainability, and proper agent awareness.

## Database Configuration
- **Database Name**: `JobTrackerDB` (Production)
- **Development Database**: `JobTrackerDB_Dev`
- **Staging Database**: `JobTrackerDB_Staging`
- **Schema**: `dbo` (default)

## Table Naming Conventions

### Core Principles
1. **Singular Table Names**: Use singular form (e.g., `Profile`, `User`, `Job`)
2. **Hierarchical Naming**: Child tables prefix with parent table name
3. **Avoid Redundancy**: Don't repeat parent name unnecessarily

### Hierarchical Naming Pattern
```
ParentTable + ChildTable = FullTableName
```

**Examples:**
- `Profile` + `Address` = `ProfileAddress` ✅
- `Profile` + `Education` = `ProfileEducation` ✅
- `Profile` + `WorkExperience` = `ProfileWorkExperience` ✅
- `Profile` + `CareerAspiration` = `ProfileCareerAspiration` ✅

**Avoid:**
- `User` + `UserProfile` = `UserUserProfile` ❌ (redundant)
- `Profile` + `ProfileAddress` = `ProfileProfileAddress` ❌ (redundant)

### Profile Builder Tables (2025-01-08 Update)
The following tables follow the hierarchical naming convention:

#### Core Profile Tables
- `ProfileAddress` - User address information
- `ProfileEducation` - Educational background
- `ProfileCertification` - Professional certifications
- `ProfileWorkExperience` - Work history
- `ProfileWorkAchievement` - Work achievements
- `ProfileProject` - Project portfolio
- `ProfileProjectTechnology` - Technologies used in projects
- `ProfileCareerAspiration` - Career goals and aspirations
- `ProfileResumeParsingData` - AI parsing results

#### Session & Audit Tables
- `ProfileBuilderSession` - User session tracking
- `ProfileBuilderStep` - Step-by-step progress tracking
- `AuditTrail` - Comprehensive audit logging

## Column Naming Conventions

### Primary Keys
- **Pattern**: `[TableName]ID`
- **Type**: `INT IDENTITY(1,1)`
- **Examples**:
  - `ProfileAddressID`
  - `ProfileEducationID`
  - `ProfileWorkExperienceID`

### Foreign Keys
- **Pattern**: `[ReferencedTableName]ID`
- **Examples**:
  - `ProfileID` (references `Profile` table)
  - `UserID` (references `User` table)

### Audit Fields (Standard)
All tables include these audit fields:
- `createdDate` - `DATETIME NOT NULL DEFAULT GETDATE()`
- `createdBy` - `NVARCHAR(100) NULL`
- `lastUpdated` - `DATETIME NULL`
- `updatedBy` - `NVARCHAR(100) NULL`

### Data Type Standards
- **Text Fields**: `NVARCHAR` for Unicode support
- **Long Text**: `NVARCHAR(MAX)` for large content
- **Dates**: `DATE` for dates only, `DATETIME` for timestamps
- **Booleans**: `BIT` for true/false values
- **Decimals**: `DECIMAL(precision,scale)` for precise numbers

## Index Naming Conventions

### Pattern: `IX_[TableName]_[ColumnName(s)]`
- **Primary Key**: `PK_[TableName]`
- **Foreign Key**: `IX_[TableName]_[FKColumnName]`
- **Composite**: `IX_[TableName]_[Column1]_[Column2]`

**Examples:**
- `IX_ProfileAddress_ProfileID`
- `IX_ProfileEducation_IsCurrent`
- `IX_AuditTrail_TableRecord`

## Stored Procedure Naming

### Pattern: `sp_[Action][Entity]`
- **Examples**:
  - `sp_SetAuditContext`
  - `sp_GetAuditTrail`
  - `sp_StartProfileBuilderSession`
  - `sp_UpdateProfileBuilderProgress`

## View Naming

### Pattern: `v_[Purpose][Entity]`
- **Examples**:
  - `v_ProfileSummary`
  - `v_UserAnalytics`
  - `v_JobApplicationStatus`

## Trigger Naming

### Pattern: `TR_[TableName]_[Action]`
- **Examples**:
  - `TR_ProfileAddress_Audit`
  - `TR_ProfileEducation_Audit`
  - `TR_ProfileWorkExperience_Audit`

## Recent Schema Updates (2025-01-08)

### Profile Builder Schema Enhancement
**Status**: ✅ **COMPLETED**

#### New Tables Created:
1. `ProfileWorkAchievement` - Work achievements tracking
2. `ProfileProjectTechnology` - Technology stack for projects
3. `ProfileResumeParsingData` - AI parsing results storage
4. `AuditTrail` - Comprehensive audit logging
5. `ProfileBuilderSession` - User session management
6. `ProfileBuilderStep` - Step-by-step progress tracking

#### Enhanced UserPreferences:
Added 8 new columns for Profile Builder tracking:
- `ProfileBuilderMode`
- `ProfileCompletionPercentage`
- `LastProfileUpdate`
- `ProfileVersion`
- `IsProfileComplete`
- `ProfileBuilderLastSessionID`
- `ProfileBuilderStepProgress`
- `ProfileBuilderValidationErrors`

#### Stored Procedures Created:
- `sp_SetAuditContext` - Set audit context for triggers
- `sp_GetAuditTrail` - Query audit trail data
- `sp_StartProfileBuilderSession` - Initialize user session
- `sp_UpdateProfileBuilderStep` - Update step progress
- `sp_EndProfileBuilderSession` - End user session
- `sp_GetProfileBuilderProgress` - Get session progress
- `sp_GetUserProfileBuilderHistory` - Get user history
- `sp_UpdateProfileBuilderProgress` - Update progress
- `sp_GetProfileBuilderStatus` - Get builder status
- `sp_ResetProfileBuilderProgress` - Reset progress
- `sp_CalculateProfileCompletion` - Calculate completion %

## Known Issues & Resolutions

### Column Reference Issues
**Issue**: Some stored procedures reference `UserID` instead of `ProfileID` in UserPreferences table
**Resolution**: UserPreferences uses `ProfileID`, not `UserID`

### Time Column Naming
**Issue**: ProfileBuilderStep uses `StartTime`/`EndTime` instead of `StartedAt`/`CompletedAt`
**Resolution**: Use actual column names: `StartTime`, `EndTime`

## Agent Awareness Requirements

### For All Agents
1. **Always use hierarchical naming** for new Profile-related tables
2. **Reference this document** before creating database objects
3. **Follow audit field standards** for all new tables
4. **Use correct column references** (ProfileID vs UserID)
5. **Check actual table structures** before writing stored procedures

### For Database Agents
1. **Verify table existence** before creating objects
2. **Use IF NOT EXISTS** patterns for idempotent scripts
3. **Handle column name mismatches** gracefully
4. **Test stored procedures** with actual table structures

### For Development Agents
1. **Reference Profile Builder tables** when building features
2. **Use correct foreign key relationships**
3. **Implement audit trails** for all data modifications
4. **Follow session tracking patterns** for user workflows

## Validation Checklist

Before creating any database object, verify:
- [ ] Table name follows hierarchical convention
- [ ] Primary key uses correct naming pattern
- [ ] Foreign keys reference correct tables
- [ ] Audit fields are included
- [ ] Indexes follow naming convention
- [ ] Stored procedures use correct column references
- [ ] Triggers follow naming pattern
- [ ] Data types match standards

## Migration Notes

### Profile Builder Migration Status
- **Target Database**: `JobTrackerDB_Dev` (Development only)
- **Migration Scripts**: Located in `active-work/feature-pb-database-schema-audit/development/`
- **Execution Order**: 001 → 002 → 003 → 004
- **Validation**: Comprehensive post-migration checks included

### Rollback Procedures
All migration scripts include rollback capabilities and are idempotent (safe to run multiple times).

---

**Last Updated**: 2025-01-08
**Author**: BMad Architect
**Status**: Active
**Version**: 1.0
