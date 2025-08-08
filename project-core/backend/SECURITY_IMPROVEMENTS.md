# Security Improvements for UAT User Creation

## Issue Resolved
GitGuardian detected hardcoded credentials in `create_uat_user.py`. While the email `uat@JobTrackerDB.com` is not a real company email, having hardcoded passwords in source code violates security best practices.

## Changes Made

### 1. Environment Variable Integration
- **Before**: Hardcoded password `"UAT@JobTrackerDB2025"` and email `"uat@JobTrackerDB.com"`
- **After**: Uses environment variables `UAT_EMAIL` and `UAT_PASSWORD`

### 2. Secure Password Generation
- If `UAT_PASSWORD` is not set in environment, generates a secure random password using `secrets.token_urlsafe(12)`
- Provides clear instructions to add the generated password to `.env` file for consistency

### 3. Environment Variable Loading
- Added `dotenv` integration to load `.env` file
- Uses `find_dotenv()` for robust environment file discovery
- Falls back to default values if environment variables are not set

## Usage

### Option 1: Use Environment Variables (Recommended)
Create a `.env` file in `project-core/backend/` with:
```
UAT_EMAIL=uat@JobTrackerDB.com
UAT_PASSWORD=your-secure-password-here
```

### Option 2: Auto-Generate Password
Leave `UAT_PASSWORD` unset in environment. The script will:
1. Generate a secure random password
2. Display it for you to copy
3. Suggest adding it to `.env` for consistency

## Security Benefits

1. **No Hardcoded Credentials**: Sensitive data is not stored in source code
2. **Environment-Specific**: Different credentials for different environments
3. **Secure Generation**: Uses cryptographically secure random generation
4. **Clear Documentation**: Script provides clear guidance on credential management
5. **GitGuardian Compliance**: Eliminates false positives from security scanners

## File Locations

- **Active Script**: `project-core/backend/create_uat_user.py` (updated)
- **Legacy Script**: `backend/create_uat_user.py` (deleted)
- **Environment Template**: Create `.env` file in `project-core/backend/` based on the pattern above

## Next Steps

1. Create `.env` file in `project-core/backend/` with your preferred UAT credentials
2. Test the updated script: `python create_uat_user.py`
3. Consider rotating the UAT password periodically
4. Review other scripts for similar hardcoded credential issues
