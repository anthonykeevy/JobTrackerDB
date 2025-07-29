# EPC-15.1: Secure API Key Storage

**Epic:** Epic 15 - API Key & Cost Management  
**Story Owner:** Backend Developer  
**Priority:** High  
**Estimated Effort:** 8 hours  
**Status:** Draft  

## User Story

As a system administrator,  
I want API keys to be securely encrypted and stored using Azure Key Vault,  
So that sensitive credentials are protected and comply with security standards.

## Background

The platform needs to store API keys for AI services (OpenAI, Anthropic, etc.) securely. These keys must be encrypted at rest and only accessible to authorized backend services. Azure Key Vault will be used to store the encryption master key, ensuring compliance with GDPR, SOC2, and Australian data laws.

## Acceptance Criteria

1. **API Key Encryption**
   - [ ] API keys are encrypted using AES-256 encryption before storage
   - [ ] Encryption master key is stored in Azure Key Vault
   - [ ] No plaintext API keys are stored in the database
   - [ ] Encryption/decryption operations are performed only on the backend

2. **Azure Key Vault Integration**
   - [ ] Azure Key Vault connection is configured securely
   - [ ] Key Vault access is restricted to backend services only
   - [ ] Key rotation and management procedures are documented
   - [ ] Key Vault access is logged for audit purposes

3. **Database Schema**
   - [ ] `APIKeys` table is created with encrypted key storage
   - [ ] `KeyVaultSecrets` table tracks Key Vault references
   - [ ] Audit logging table for key operations
   - [ ] Proper foreign key relationships to Users table

4. **Security Compliance**
   - [ ] PCI DSS compliance for payment-related keys
   - [ ] GDPR compliance for data protection
   - [ ] SOC2 audit trail for key operations
   - [ ] Encryption key access is logged and monitored

5. **Error Handling**
   - [ ] Graceful handling of Key Vault connection failures
   - [ ] Fallback mechanisms for key retrieval
   - [ ] Comprehensive error logging for debugging
   - [ ] Alert system for security-related failures

## Technical Requirements

### Database Schema
```sql
CREATE TABLE APIKeys (
    APIKeyID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT,
    CompanyID INT,
    Scope NVARCHAR(20) NOT NULL, -- 'App', 'Company', 'User'
    Provider NVARCHAR(50) NOT NULL, -- 'OpenAI', 'Anthropic', etc.
    EncryptedKey NVARCHAR(MAX) NOT NULL,
    KeyVaultSecretID NVARCHAR(255) NOT NULL,
    PreferredModel NVARCHAR(100),
    IsActive BIT DEFAULT 1,
    ExpiresAt DATETIME2,
    CreatedAt DATETIME2 DEFAULT GETDATE(),
    UpdatedAt DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (CompanyID) REFERENCES Companies(CompanyID)
);

CREATE TABLE KeyVaultSecrets (
    SecretID INT PRIMARY KEY IDENTITY(1,1),
    SecretName NVARCHAR(255) NOT NULL,
    KeyVaultURL NVARCHAR(500) NOT NULL,
    Version NVARCHAR(50),
    CreatedAt DATETIME2 DEFAULT GETDATE(),
    LastAccessed DATETIME2
);

CREATE TABLE APIKeyAuditLog (
    LogID INT PRIMARY KEY IDENTITY(1,1),
    APIKeyID INT,
    Operation NVARCHAR(50) NOT NULL, -- 'CREATE', 'UPDATE', 'DELETE', 'ACCESS'
    UserID INT,
    IPAddress NVARCHAR(45),
    UserAgent NVARCHAR(500),
    Success BIT NOT NULL,
    ErrorMessage NVARCHAR(MAX),
    CreatedAt DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (APIKeyID) REFERENCES APIKeys(APIKeyID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);
```

### API Endpoints
- `POST /api/keys` - Create new API key (encrypted)
- `GET /api/keys/{keyId}` - Retrieve key metadata (not decrypted key)
- `PUT /api/keys/{keyId}` - Update key metadata
- `DELETE /api/keys/{keyId}` - Delete API key
- `POST /api/keys/{keyId}/decrypt` - Decrypt key for use (backend only)

### Security Requirements
- All API key operations require authentication
- Role-based access control (Admin for App/Company keys, User for own keys)
- Rate limiting on key operations
- Audit logging for all key access attempts
- Key rotation procedures documented

## Dev Notes

### Implementation Approach
1. Set up Azure Key Vault in development environment
2. Create encryption service using Azure Key Vault SDK
3. Implement database schema with encrypted storage
4. Create API endpoints with proper authentication
5. Add comprehensive audit logging
6. Test encryption/decryption workflows

### Key Dependencies
- Azure Key Vault subscription and configuration
- Azure Key Vault SDK for Python
- FastAPI authentication middleware
- Database migration system

### Testing Strategy
- Unit tests for encryption/decryption functions
- Integration tests with Azure Key Vault
- Security tests for key access controls
- Performance tests for key operations

### Security Considerations
- Never log decrypted keys
- Implement proper key rotation procedures
- Monitor for suspicious key access patterns
- Regular security audits of key operations

## Definition of Done

- [ ] API key encryption/decryption works correctly
- [ ] Azure Key Vault integration is functional
- [ ] Database schema is implemented and tested
- [ ] API endpoints are secure and authenticated
- [ ] Audit logging captures all key operations
- [ ] Error handling is comprehensive
- [ ] Security compliance requirements are met
- [ ] Documentation is complete
- [ ] Code review is approved
- [ ] Tests pass with >90% coverage

## File List

- `backend/services/encryption_service.py` - Encryption/decryption logic
- `backend/services/key_vault_service.py` - Azure Key Vault integration
- `backend/models/api_key.py` - API key data models
- `backend/api/keys.py` - API key endpoints
- `backend/database/migrations/001_create_api_keys.sql` - Database schema
- `backend/tests/test_encryption.py` - Encryption tests
- `backend/tests/test_key_vault.py` - Key Vault integration tests
- `docs/security/api-key-management.md` - Security documentation 