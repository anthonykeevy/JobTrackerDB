# BMAD Master Input Summary - Database Schema Enhancement

## Current State
- **Database**: MSSQL Server 2022 with 31+ tables
- **Application**: Job tracking system with profile management
- **Issue**: Profile Builder steps not persisting data to database
- **Goal**: Ensure all user inputs are stored with audit trails

## Critical Gaps Identified

### **Missing Tables for Profile Builder Steps**
1. **Education/Certifications** - No education history tables
2. **Work Experience** - No work history tables  
3. **Projects** - No portfolio projects table
4. **Career Aspirations** - No career goals table
5. **ProfileAddress** - No dedicated address table with geolocation
6. **ResumeParsingData** - No parsed resume data storage

### **Audit Trail Enhancements Needed**
1. **Dedicated audit tables** for detailed change tracking
2. **Before/after value storage** for complete history
3. **Change reason tracking** (why changes were made)
4. **User session tracking** during profile building

### **Profile Builder Workflow Data**
1. **Step completion tracking** not implemented
2. **Form validation errors** not logged
3. **User progress through builder** not tracked
4. **Draft vs final data** not distinguished

## Current Schema Strengths
- ✅ Most tables have basic audit fields (`createdDate`, `createdBy`, `lastUpdated`, `updatedBy`)
- ✅ Proper foreign key relationships
- ✅ Good indexing strategy
- ✅ Comprehensive job application tracking

## Requirements for @bmad-master

### **Task 1: Design Missing Tables**
- Create tables for all missing Profile Builder step data
- Ensure proper relationships and constraints
- Include audit fields on all new tables
- Consider performance implications

### **Task 2: Design Enhanced Audit Trail System**
- Create dedicated audit trail tables
- Design before/after value storage
- Include change reason tracking
- Optimize for performance

### **Task 3: Design Migration Strategy**
- Plan schema evolution approach
- Ensure backward compatibility
- Design data migration for existing data
- Create rollback strategy

### **Task 4: API Design Considerations**
- Design CRUD operations for new tables
- Plan real-time data persistence
- Include error handling and recovery
- Consider bulk operations

## Technology Stack
- **Database**: MSSQL Server 2022
- **ORM**: SQLAlchemy + Alembic
- **Backend**: FastAPI
- **Frontend**: React + TypeScript

## Success Criteria
- [ ] All Profile Builder steps have database persistence
- [ ] Complete audit trail for all data changes
- [ ] Performance acceptable under load
- [ ] Migration strategy documented
- [ ] API endpoints designed for new tables

## BMAD Commands to Use
```bash
@bmad-master *task brownfield-create-epic
# For: Database schema evolution with audit trails

@bmad-master *kb
# For: Database best practices and audit trail patterns

@bmad-master *create-doc brownfield-architecture-tmpl
# For: Documenting schema evolution strategy
```

## Expected Output
1. **Complete schema design** with all missing tables
2. **Enhanced audit trail system** design
3. **Migration strategy** with step-by-step plan
4. **Performance considerations** and optimization recommendations
5. **API design patterns** for new tables
