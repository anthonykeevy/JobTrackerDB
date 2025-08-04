# User Story 1.15: Address Validation Backend Integration

**Epic:** Unified Career Profile Intake for Resume Generation  
**Story ID:** EPC-1.15  
**Priority:** High  
**Status:** In Progress  
**Owner:** Backend Developer

---

## Description

As a **backend developer**,  
I want to **implement the address validation API endpoints and services**,  
So that **the frontend address validation UI can connect to real Geoscape API and store validated address data**.

---

## Current Frontend Implementation Status

### ✅ Completed UI Features
- **Address Search Input**: Autocomplete with debounced search (500ms)
- **Geoscape API Integration**: Mock implementation with realistic responses
- **Map Visualization**: Mapbox integration with dynamic pin updates
- **Address Parsing**: Street Name/Type separation logic
- **Form Validation**: Zod schema with comprehensive address fields
- **User Experience**: Focus stability, loading indicators, error handling

### 📍 Current Test Addresses
- **Primary Test**: "4 Milburn Place, St Ives Chase NSW 2075"
- **Secondary Test**: "14 Milburn Place, St Ives Chase NSW 2075"
- **Coordinates**: `-33.70131425995992, 151.16600576829697` (Google Maps verified)

### 🔧 Technical Implementation Details
- **File**: `frontend/src/components/ProfileBuilder/steps/BasicInfoStep.tsx`
- **Map Component**: `frontend/src/components/Map/MapComponent.tsx`
- **Test Tools**: `frontend/address-test.html`, `frontend/src/test-address-api.js`
- **API Config**: `backend/app/core/api_config.py` (Geoscape keys configured)

---

## Acceptance Criteria

### 1. **Geoscape API Integration**
- [ ] Implement `/api/address/search` endpoint for address autocomplete
- [ ] Implement `/api/address/validate` endpoint for address validation
- [ ] Handle Geoscape API authentication and error responses
- [ ] Implement request/response logging for billing tracking
- [ ] Add rate limiting and quota management

### 2. **Address Data Storage**
- [ ] Store validated addresses in `ProfileAddress` table
- [ ] Capture Geoscape metadata (PropertyID, confidence scores, etc.)
- [ ] Support multiple addresses per profile (primary, work, mailing)
- [ ] Implement address versioning and history tracking

### 3. **API Usage Tracking**
- [ ] Log all Geoscape API calls in `APIUsageTracking` table
- [ ] Track costs, response times, and success rates
- [ ] Implement billing alerts and quota monitoring
- [ ] Support regional API provider switching

### 4. **Error Handling & Fallbacks**
- [ ] Implement SmartyStreets fallback for US addresses
- [ ] Handle API timeouts and network failures gracefully
- [ ] Provide meaningful error messages to frontend
- [ ] Support manual address entry when APIs fail

### 5. **Performance & Security**
- [ ] Implement caching for frequently searched addresses
- [ ] Validate and sanitize all address inputs
- [ ] Rate limit API calls per user/IP
- [ ] Secure API keys and sensitive configuration

---

## Technical Requirements

### Backend Endpoints
```python
# Address Search (Autocomplete)
GET /api/address/search?q={query}&country={country}
Response: {
  "suggestions": [
    {
      "address": "4 Milburn Place, St Ives Chase NSW 2075",
      "id": "GNSW2075190",
      "data": {
        "streetNumber": "4",
        "streetName": "Milburn",
        "streetType": "Place",
        "suburb": "St Ives Chase",
        "state": "NSW",
        "postcode": "2075",
        "latitude": -33.70131425995992,
        "longitude": 151.16600576829697
      },
      "confidence": 0.98
    }
  ]
}

# Address Validation
POST /api/address/validate
Request: {
  "address": "4 Milburn Place, St Ives Chase NSW 2075",
  "propertyId": "GNSW2075190"
}
Response: {
  "validated": true,
  "address": {...},
  "metadata": {...}
}
```

### Database Integration
```python
# ProfileAddress model (already implemented)
class ProfileAddress(Base):
    ProfileAddressID = Column(Integer, primary_key=True)
    ProfileID = Column(Integer, ForeignKey("Profile.ProfileID"))
    PropertyID = Column(Unicode(100))  # Geoscape identifier
    Latitude = Column(DECIMAL(10, 8))
    Longitude = Column(DECIMAL(11, 8))
    IsValidated = Column(Boolean, default=False)
    ValidationSource = Column(Unicode(50))  # 'geoscape', 'smarty_streets'
    ConfidenceScore = Column(DECIMAL(3, 2))
    # ... other fields
```

### API Configuration
```python
# backend/app/core/api_config.py (already configured)
GEOSCAPE_API_KEY: str = "9x4fpNyrr8VxVqWvPeKnuEWaH9vxgGxS"
GEOSCAPE_CONSUMER_SECRET: str = "8XkTgtu0Sz1D0aG9"
GEOSCAPE_BASE_URL: str = "https://api.geoscape.com.au/v1"
```

---

## Definition of Done

- [ ] Geoscape API endpoints implemented and tested
- [ ] Address data correctly stored in `ProfileAddress` table
- [ ] API usage tracking functional in `APIUsageTracking` table
- [ ] Frontend can successfully call backend address APIs
- [ ] Error handling and fallbacks implemented
- [ ] Performance monitoring and logging in place
- [ ] Security measures implemented (rate limiting, input validation)
- [ ] Documentation updated with API endpoints and usage

---

## Dependencies

- **EPC-8.1**: Database schema design (ProfileAddress table)
- **EPC-16.3**: API usage tracking dashboard
- **EPC-15.1**: Secure API key storage
- **Frontend**: BasicInfoStep.tsx address validation UI (completed)

---

## Notes

- **Current Status**: Frontend UI is complete and functional with mock data
- **Coordinates**: Verified with Google Maps for test addresses
- **API Keys**: Geoscape credentials already configured in `api_config.py`
- **Testing**: Use `frontend/address-test.html` for systematic testing
- **Regional Support**: Geoscape for Australia, SmartyStreets for US backup 