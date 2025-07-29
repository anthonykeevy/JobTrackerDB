# EPC-15.2: API Key Hierarchy Management

**Epic:** Epic 15 - API Key & Cost Management  
**Story Owner:** Backend Developer  
**Priority:** High  
**Estimated Effort:** 6 hours  
**Status:** Draft  

## User Story

As a user or company administrator,  
I want to manage API keys with a clear hierarchy (User > Company > App),  
So that I can control costs and use preferred AI providers while maintaining fallback options.

## Background

The platform supports multiple scopes for API keys: App-level (default), Company-level (for organizations), and User-level (individual preferences). The system must implement a fallback hierarchy where User keys override Company keys, which override App keys. This allows for cost control, provider preferences, and organizational management of AI service usage.

## Acceptance Criteria

1. **Key Hierarchy Implementation**
   - [ ] User keys override Company and App keys
   - [ ] Company keys apply to all users in organization unless overridden
   - [ ] App keys serve as default fallback
   - [ ] Hierarchy is enforced for all AI service requests

2. **Key Resolution Logic**
   - [ ] System correctly resolves key based on hierarchy
   - [ ] Fallback logic works when higher-level keys are unavailable
   - [ ] Key resolution is logged for audit purposes
   - [ ] Performance is optimized for key lookups

3. **Company Key Management**
   - [ ] Company administrators can set company-wide API keys
   - [ ] Company keys apply to all users in the company
   - [ ] Individual users can override company keys with their own
   - [ ] Company key changes are propagated to all users

4. **User Key Override**
   - [ ] Users can provide their own API keys
   - [ ] User keys take precedence over company and app keys
   - [ ] Users can revert to company/app keys by removing their key
   - [ ] Key override status is clearly visible to users

5. **Admin Console**
   - [ ] Admin can view all key assignments across scopes
   - [ ] Admin can manage company and app-level keys
   - [ ] Admin can see which users have overridden company keys
   - [ ] Admin can force users to use company keys if needed

## Technical Requirements

### Database Schema Updates
```sql
-- Add CompanyID to existing APIKeys table
ALTER TABLE APIKeys ADD CompanyID INT;
ALTER TABLE APIKeys ADD FOREIGN KEY (CompanyID) REFERENCES Companies(CompanyID);

-- Add key hierarchy tracking
CREATE TABLE KeyHierarchy (
    HierarchyID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT,
    CompanyID INT,
    ActiveKeyID INT,
    Scope NVARCHAR(20) NOT NULL, -- 'App', 'Company', 'User'
    IsOverride BIT DEFAULT 0,
    CreatedAt DATETIME2 DEFAULT GETDATE(),
    UpdatedAt DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (CompanyID) REFERENCES Companies(CompanyID),
    FOREIGN KEY (ActiveKeyID) REFERENCES APIKeys(APIKeyID)
);
```

### Key Resolution Service
```python
class KeyResolutionService:
    def resolve_key_for_user(self, user_id: int, provider: str) -> Optional[APIKey]:
        # 1. Check for user-specific key
        # 2. Check for company key
        # 3. Fall back to app key
        # 4. Return None if no key available
        pass
    
    def get_key_hierarchy(self, user_id: int) -> Dict[str, APIKey]:
        # Return all available keys for user (User, Company, App)
        pass
```

### API Endpoints
- `GET /api/keys/hierarchy/{userId}` - Get key hierarchy for user
- `POST /api/keys/company/{companyId}` - Set company API key
- `PUT /api/keys/user/{userId}/override` - Set user key override
- `DELETE /api/keys/user/{userId}/override` - Remove user override
- `GET /api/keys/resolve/{userId}/{provider}` - Resolve key for specific provider

### Business Logic
- Key resolution happens on every AI service request
- Hierarchy changes are logged for audit
- Company key changes trigger notifications to affected users
- Key usage is tracked per scope for cost allocation

## Dev Notes

### Implementation Approach
1. Implement key resolution service with hierarchy logic
2. Add database schema for hierarchy tracking
3. Create API endpoints for key management
4. Implement admin console for key oversight
5. Add audit logging for hierarchy changes
6. Test key resolution with various scenarios

### Key Dependencies
- EPC-15.1 (Secure API Key Storage) must be completed first
- User authentication and authorization system
- Company/Organization management system
- AI service integration layer

### Testing Strategy
- Unit tests for key resolution logic
- Integration tests for hierarchy scenarios
- Performance tests for key lookups
- Security tests for key access controls

### Performance Considerations
- Cache key resolution results
- Optimize database queries for key lookups
- Implement connection pooling for AI service calls
- Monitor key resolution performance

## Definition of Done

- [ ] Key hierarchy logic works correctly
- [ ] Key resolution service is implemented and tested
- [ ] Database schema supports hierarchy tracking
- [ ] API endpoints for key management are functional
- [ ] Admin console shows key hierarchy clearly
- [ ] Audit logging captures hierarchy changes
- [ ] Performance meets requirements (<100ms key resolution)
- [ ] Error handling is comprehensive
- [ ] Documentation is complete
- [ ] Code review is approved
- [ ] Tests pass with >90% coverage

## File List

- `backend/services/key_resolution_service.py` - Key hierarchy logic
- `backend/models/key_hierarchy.py` - Hierarchy data models
- `backend/api/key_hierarchy.py` - Hierarchy management endpoints
- `backend/database/migrations/002_add_key_hierarchy.sql` - Database updates
- `backend/tests/test_key_resolution.py` - Key resolution tests
- `frontend/components/KeyHierarchyManager.tsx` - Admin UI component
- `frontend/components/UserKeyOverride.tsx` - User key management
- `docs/api/key-hierarchy.md` - API documentation 