# JobTrackerDB Audit Process Guide

## Overview
This document defines the standardized audit process for all database operations in the JobTrackerDB application. The audit system ensures data integrity, provides complete change history, and enables compliance with data governance requirements.

## Core Audit Principles

### 1. **CreatedDate/CreatedBy - Immutable Pair on Creation**
- **Set together once**: When a record is first created
- **Never modified**: These fields remain unchanged throughout the record's lifecycle
- **Reflects source and time**: Who/what created the record and when

### 2. **LastUpdated/UpdatedBy - Dynamic Pair on Every Change**
- **Updated together**: Every time a record is changed
- **Reflects current source and time**: Who/what made the most recent change and when
- **Tracks all changes**: Complete history of modifications

### 3. **Source Distinction**
- **API Operations**: Use service name (e.g., "Geoscape", "OpenAI")
- **Manual User Actions**: Use `{username}_{userid}` format
- **System Operations**: Use "System" or specific system identifier

## Audit Field Standards

### Standard Audit Fields
All tables with audit capabilities include these fields:
```sql
createdDate    DATETIME    -- When record was created
createdBy      NVARCHAR(100) -- Who/what created the record
lastUpdated    DATETIME    -- When record was last modified
updatedBy      NVARCHAR(100) -- Who/what made the last change
```

### User Identifier Format
- **Manual User Actions**: `{username}_{userid}`
- **Example**: `test@example.com_1`

### API Service Identifiers
- **Geoscape API**: `"Geoscape"`
- **OpenAI API**: `"OpenAI"`
- **System Operations**: `"System"`

## Audit Process Rules

### Rule 1: Record Creation
```python
# When creating a new record - CreatedDate and CreatedBy set together
current_time = datetime.utcnow()
new_record = ModelName(
    # ... other fields ...
    createdDate=current_time,
    createdBy=source_identifier,  # API service or user identifier
    lastUpdated=None,  # NULL for new records - no updates yet
    updatedBy=None  # NULL for new records - no updates yet
)
```

### Rule 2: Record Updates
```python
# When updating an existing record - LastUpdated and UpdatedBy updated together
current_time = datetime.utcnow()
existing_record.field = new_value
existing_record.lastUpdated = current_time
existing_record.updatedBy = source_identifier  # Current change source
# NEVER modify createdBy or createdDate
```

### Rule 3: Record Deletion/Deactivation
```python
# When deactivating or soft-deleting records - LastUpdated and UpdatedBy updated together
current_time = datetime.utcnow()
record.IsActive = False
record.lastUpdated = current_time
record.updatedBy = source_identifier
# NEVER modify createdBy or createdDate
```

## Implementation Examples

### Address Management Audit
```python
# Scenario 1: New address from Geoscape API
if is_geoscape_api:
    profile_address = ProfileAddress(
        # ... address fields ...
        createdDate=datetime.utcnow(),
        createdBy="Geoscape",
        lastUpdated=None,  # NULL for new records
        updatedBy=None  # NULL for new records
    )

# Scenario 2: Manual address edit
else:
    existing_address.lastUpdated = datetime.utcnow()
    existing_address.updatedBy = f"{user.Username}_{user.UserID}"
    # createdBy and createdDate remain unchanged
```

### Profile Updates Audit
```python
# When updating profile information
profile.FirstName = new_first_name
profile.lastUpdated = datetime.utcnow()
profile.updatedBy = f"{user.Username}_{user.UserID}"
# createdBy and createdDate remain unchanged
```

### AI Usage Tracking Audit
```python
# When logging AI operations
usage_record = APIUsageTracking(
    # ... usage fields ...
    createdDate=datetime.utcnow(),
    createdBy="OpenAI",
    lastUpdated=None,  # NULL for new records
    updatedBy=None  # NULL for new records
)
```

## Complex Audit Scenarios

### Scenario 1: Address Switching
When a user switches from one address to another:

1. **Deactivate current address**:
   ```python
   current_address.IsActive = False
   current_address.lastUpdated = datetime.utcnow()
   current_address.updatedBy = user_identifier
   ```

2. **Activate new address**:
   ```python
   new_address.IsActive = True
   new_address.lastUpdated = datetime.utcnow()
   new_address.updatedBy = user_identifier
   ```

### Scenario 2: Bulk Operations
When performing bulk updates:

```python
for record in records_to_update:
    record.field = new_value
    record.lastUpdated = datetime.utcnow()
    record.updatedBy = source_identifier
    # createdBy and createdDate remain unchanged
```

### Scenario 3: System-Generated Changes
When the system automatically updates records:

```python
# Example: Auto-calculated profile scores
profile.ProfileScore = calculated_score
profile.lastUpdated = datetime.utcnow()
profile.updatedBy = "System"
# createdBy and createdDate remain unchanged
```

## Audit Trail Queries

### View Complete Change History
```sql
SELECT 
    ProfileAddressID,
    StreetName,
    Suburb,
    createdDate,
    createdBy,
    lastUpdated,
    updatedBy,
    IsActive
FROM ProfileAddress 
WHERE ProfileID = @ProfileID
ORDER BY createdDate DESC
```

### Track Address Changes Over Time
```sql
SELECT 
    'Address Change' as ChangeType,
    createdDate as ChangeDate,
    createdBy as ChangedBy,
    'Created' as Action
FROM ProfileAddress 
WHERE ProfileID = @ProfileID

UNION ALL

SELECT 
    'Address Update' as ChangeType,
    lastUpdated as ChangeDate,
    updatedBy as ChangedBy,
    'Modified' as Action
FROM ProfileAddress 
WHERE ProfileID = @ProfileID AND lastUpdated != createdDate
ORDER BY ChangeDate DESC
```

## Compliance and Reporting

### Data Governance
- **Complete audit trail**: Every change is tracked
- **Source attribution**: Clear identification of change sources
- **Temporal tracking**: When changes occurred
- **Non-repudiation**: Cannot deny who made changes

### Reporting Capabilities
- **Change frequency analysis**: How often records are modified
- **User activity tracking**: Which users make the most changes
- **API usage monitoring**: Track external service interactions
- **Data quality metrics**: Identify patterns in data modifications

## Best Practices

### 1. **Consistency**
- Always use the same audit field names across all tables
- Maintain consistent user identifier format
- Use standardized API service names

### 2. **Performance**
- Index audit fields for efficient querying
- Consider archiving old audit data for performance
- Use appropriate data types for audit fields

### 3. **Security**
- Audit fields should be read-only for end users
- Log all audit field modifications
- Implement audit field validation

### 4. **Maintenance**
- Regular audit trail cleanup for old records
- Monitor audit table growth
- Archive audit data based on retention policies

## Error Handling

### Audit Field Validation
```python
def validate_audit_fields(record):
    """Ensure audit fields are properly set"""
    if not record.createdDate:
        raise ValueError("createdDate must be set on record creation")
    if not record.createdBy:
        raise ValueError("createdBy must be set on record creation")
    if not record.lastUpdated:
        raise ValueError("lastUpdated must be set on record modification")
    if not record.updatedBy:
        raise ValueError("updatedBy must be set on record modification")
```

### Audit Field Protection
```python
def protect_audit_fields(record):
    """Prevent modification of creation audit fields"""
    if hasattr(record, '_original_created_by'):
        record.createdBy = record._original_created_by
    if hasattr(record, '_original_created_date'):
        record.createdDate = record._original_created_date
```

## Testing Audit Compliance

### Unit Tests
```python
def test_audit_field_immutability():
    """Test that createdBy/createdDate cannot be modified"""
    address = ProfileAddress(...)
    original_created_by = address.createdBy
    original_created_date = address.createdDate
    
    # Attempt to modify audit fields
    address.createdBy = "Modified"
    address.createdDate = datetime.utcnow()
    
    # Verify audit fields are protected
    assert address.createdBy == original_created_by
    assert address.createdDate == original_created_date
```

### Integration Tests
```python
def test_address_audit_trail():
    """Test complete address change audit trail"""
    # Create address via API
    # Modify address manually
    # Switch to different address
    # Verify audit trail is complete and accurate
```

## Future Audit Considerations

### Full Change Tracking for Critical Services
For services that require complete audit trails (e.g., financial transactions, security events), consider implementing a separate audit log table:

```sql
CREATE TABLE AuditLog (
    AuditLogID INT IDENTITY(1,1) PRIMARY KEY,
    TableName NVARCHAR(100) NOT NULL,
    RecordID INT NOT NULL,
    Action NVARCHAR(50) NOT NULL, -- INSERT, UPDATE, DELETE
    FieldName NVARCHAR(100),
    OldValue NVARCHAR(MAX),
    NewValue NVARCHAR(MAX),
    ChangedBy NVARCHAR(100) NOT NULL,
    ChangedAt DATETIME NOT NULL,
    SessionID NVARCHAR(100),
    IPAddress NVARCHAR(45)
)
```

### When to Implement Full Audit Tracking
- **Financial transactions**: Every field change must be tracked
- **Security events**: Complete audit trail for compliance
- **Regulatory requirements**: Specific industries require detailed logging
- **Debugging complex workflows**: When troubleshooting requires field-level history

### Current Approach Benefits
- **Performance**: Minimal overhead on regular operations
- **Simplicity**: Easy to implement and maintain
- **Sufficient for most use cases**: Provides "who and when" for most scenarios
- **Scalable**: Can be enhanced later if needed

### Migration Strategy
If full audit tracking becomes necessary:
1. **Phase 1**: Implement audit log table alongside existing audit fields
2. **Phase 2**: Gradually migrate critical services to use full audit tracking
3. **Phase 3**: Maintain both systems during transition period
4. **Phase 4**: Deprecate simple audit fields for critical services

This audit process ensures data integrity, provides complete change history, and enables compliance with data governance requirements across the entire JobTrackerDB application.
