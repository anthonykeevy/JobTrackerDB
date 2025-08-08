# JobTrackerDB API Testing with Postman

This directory contains Postman collection and environment files for testing the JobTrackerDB address validation API and direct Geoscape API endpoints with OAuth 2.0 support.

## Files

- `JobTrackerDB_API.postman_collection.json` - Postman collection with all API endpoints (JobTrackerDB and Geoscape with OAuth 2.0)
- `JobTrackerDB_API.postman_environment.json` - Postman environment with variables
- `README_Postman_Testing.md` - This instruction file

## How to Import and Use

### 1. Import the Collection
1. Open Postman
2. Click "Import" button
3. Select the `JobTrackerDB_API.postman_collection.json` file
4. The collection will be imported with all endpoints

### 2. Import the Environment
1. In Postman, click "Import" again
2. Select the `JobTrackerDB_API.postman_environment.json` file
3. The environment will be imported with all variables

### 3. Select the Environment
1. In the top-right corner of Postman, select "JobTrackerDB API Environment"
2. This will enable all the variables for use in requests

## Available Endpoints

### JobTrackerDB API (Local Backend)
- **Address Search**: `GET /api/address/search` - Search for addresses using autocomplete
- **Address Validation**: `POST /api/address/validate` - Validate and geocode an address
- **API Health Check**: `GET /api/address/health` - Check the health status of the API

### Geoscape API (Direct External)
- **OAuth 2.0 Token Request**: `POST /oauth/token` - Request OAuth 2.0 access token
- **Address Search (OAuth 2.0)**: `GET /v1/predictive/address/search` - Search using OAuth 2.0
- **Address Validation (OAuth 2.0)**: `POST /v1/predictive/address/validate` - Validate using OAuth 2.0
- **Address Search (Simple API Key)**: `GET /v1/predictive/address/search` - Search using simple API key
- **Alternative Auth Test**: `GET /v1/predictive/address/search` - Test alternative authentication methods

## Environment Variables

### JobTrackerDB API Variables
- `base_url`: Local backend server URL
- `api_url`: Local API base URL
- `query`: Address search query
- `country`: Country code (AU for Australia)
- `limit`: Maximum number of suggestions
- `address`: Full address to validate

### Geoscape API Variables
- `geoscape_api_key`: Geoscape API Key
- `geoscape_consumer_secret`: Geoscape Consumer Secret
- `geoscape_query`: Geoscape API search query
- `geoscape_country`: Geoscape API country code
- `geoscape_limit`: Geoscape API limit for suggestions
- `geoscape_address`: Geoscape API address for validation

### OAuth 2.0 Variables
- `geoscape_oauth_token_url`: OAuth 2.0 token endpoint
- `geoscape_oauth_client_id`: OAuth 2.0 client ID
- `geoscape_oauth_client_secret`: OAuth 2.0 client secret
- `geoscape_oauth_scope`: OAuth 2.0 scopes
- `geoscape_oauth_access_token`: OAuth 2.0 access token (obtain from token request)

## Prerequisites

1. **Backend Server**: Ensure the FastAPI backend is running
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload --port 8000
   ```

2. **Test Backend Accessibility**:
   ```bash
   curl http://127.0.0.1:8000/api/address/health
   ```

## Testing Scenarios

### 1. JobTrackerDB API Testing
1. **Health Check**: Run "API Health Check" to verify backend is running
2. **Address Search**: Run "Address Search" with different queries
3. **Address Validation**: Run "Address Validation" with full addresses

### 2. Geoscape API OAuth 2.0 Testing
1. **Get OAuth Token**: Run "Geoscape OAuth 2.0 Token Request" first
2. **Copy Access Token**: From the response, copy the `access_token` value
3. **Update Environment**: Set the `geoscape_oauth_access_token` variable with the token
4. **Test OAuth Endpoints**: Run "Geoscape Address Search (OAuth 2.0)" and "Geoscape Address Validation (OAuth 2.0)"

### 3. Geoscape API Simple Authentication Testing
1. **Simple API Key**: Run "Geoscape Address Search (Simple API Key)"
2. **Alternative Methods**: Run "Geoscape API Test (Alternative Auth)"

## Authentication Methods

### OAuth 2.0 (Recommended)
- **Grant Type**: `client_credentials`
- **Client ID**: Your Geoscape API Key
- **Client Secret**: Your Geoscape Consumer Secret
- **Scopes**: `addresses predictive`
- **Token Endpoint**: `https://api.psma.com.au/oauth/token`

### Simple API Key
- **Method**: Bearer token in Authorization header
- **Format**: `Authorization: Bearer {api_key}`

### Alternative Methods
- **X-API-Key Header**: `X-API-Key: {api_key}`
- **Query Parameters**: `api_key={api_key}&consumer_secret={consumer_secret}`

## Troubleshooting

### Common Issues

1. **401 Unauthorized Errors**:
   - Check if API key is valid and active
   - Try OAuth 2.0 authentication instead of simple API key
   - Verify account has required permissions

2. **404 Not Found Errors**:
   - Verify API endpoints are correct
   - Check if your subscription includes the required API products

3. **DNS Resolution Errors**:
   - Check network connectivity
   - Verify API domain is accessible

4. **Token Expiration**:
   - OAuth tokens expire after 1 hour by default
   - Request a new token when needed

### Testing Workflow

1. **Start with OAuth 2.0**:
   ```
   Geoscape OAuth 2.0 Token Request → 
   Copy access_token → 
   Update environment variable → 
   Test OAuth endpoints
   ```

2. **Fallback to Simple API Key**:
   ```
   If OAuth fails → 
   Test Simple API Key endpoints
   ```

3. **Try Alternative Methods**:
   ```
   If both fail → 
   Test Alternative Auth methods
   ```

## Expected Behavior

### With Valid API Credentials
- **OAuth 2.0**: Should return access token and allow API calls
- **Simple API Key**: Should work directly with Bearer token
- **All endpoints**: Should return address data or validation results

### With Invalid API Credentials
- **OAuth 2.0**: Token request will fail with 401/400
- **Simple API Key**: API calls will fail with 401
- **Error messages**: Will indicate authentication failure

### Current Status
Since the Geoscape API key is currently invalid, you should see:
- **OAuth Token Request**: Returns 401/400 authentication error
- **Simple API Key**: Returns 401 authentication error
- **All endpoints**: Return authentication failure messages

This is the expected behavior until a valid Geoscape API key is provided.

## Next Steps

1. **Contact Geoscape Support**: Request valid API credentials
2. **Verify Account Status**: Check if account is active and has required permissions
3. **Test with Valid Credentials**: Once you have valid credentials, update the environment variables and test again
4. **Monitor Logs**: Check the backend logs for detailed error information 