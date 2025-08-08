# 🌍 Geoscape API Integration Guide

## 📋 Overview

This document outlines the integration of Geoscape's Predictive API for address validation and property data enrichment in the JobTrackerDB application.

## 🎯 API Configuration

### **API Key Setup**
- **API Key**: [Your Geoscape API Key] (stored securely in environment variables)
- **Base URL**: `https://api.geoscape.com.au/v1`
- **Timeout**: 30 seconds
- **Rate Limits**: As per Geoscape subscription plan

### **Environment Variables**
```bash
# Add to your .env file
GEOSCAPE_API_KEY=your_api_key_here
```

## 🏗️ Database Schema

### **ProfileAddress Table**
The new `ProfileAddress` table stores comprehensive address data with Geoscape integration:

```sql
CREATE TABLE ProfileAddress (
    ProfileAddressID INT PRIMARY KEY IDENTITY(1,1),
    ProfileID INT NOT NULL,
    
    -- Standard address components
    StreetNumber NVARCHAR(20),
    StreetName NVARCHAR(255) NOT NULL,
    StreetType NVARCHAR(50),
    UnitNumber NVARCHAR(20),
    UnitType NVARCHAR(50),
    Suburb NVARCHAR(100) NOT NULL,
    State NVARCHAR(50) NOT NULL,
    Postcode NVARCHAR(20) NOT NULL,
    Country NVARCHAR(100) NOT NULL DEFAULT 'Australia',
    
    -- Geoscape API data
    PropertyID NVARCHAR(100),
    Latitude DECIMAL(10, 8),
    Longitude DECIMAL(11, 8),
    PropertyType NVARCHAR(100),
    LandArea DECIMAL(10, 2),
    FloorArea DECIMAL(10, 2),
    
    -- Validation and confidence
    IsValidated BIT DEFAULT 0,
    ValidationSource NVARCHAR(50),
    ConfidenceScore DECIMAL(3, 2),
    ValidationDate DATETIME,
    
    -- Address status
    IsActive BIT DEFAULT 1,
    IsPrimary BIT DEFAULT 0,
    AddressType NVARCHAR(50),
    
    -- Metadata
    createdDate DATETIME DEFAULT GETDATE(),
    createdBy NVARCHAR(100),
    lastUpdated DATETIME,
    updatedBy NVARCHAR(100),
    
    FOREIGN KEY (ProfileID) REFERENCES Profile(ProfileID)
);
```

## 🔧 Frontend Integration

### **Enhanced Address Form**
The Basic Info step now includes:

1. **Granular Address Fields**:
   - Street Number (optional)
   - Street Name (required)
   - Street Type dropdown (Street, Road, Avenue, etc.)
   - Unit Number (optional)
   - Unit Type dropdown (Unit, Apartment, Suite, etc.)
   - Suburb/City (required)
   - State/Province (required)
   - Postcode (required)
   - Country (required)

2. **Address Validation**:
   - Real-time validation via Geoscape API
   - Confidence score display
   - Property ID tracking
   - Validation source tracking

3. **Visual Feedback**:
   - Validation status indicators
   - Confidence score display
   - Property details (when available)

### **TypeScript Interfaces**
```typescript
interface AddressData {
  // Standard address components
  streetNumber?: string;
  streetName: string;
  streetType?: string;
  unitNumber?: string;
  unitType?: string;
  suburb: string;
  state: string;
  postcode: string;
  country: string;
  
  // Geoscape API data
  propertyId?: string;
  latitude?: number;
  longitude?: number;
  propertyType?: string;
  landArea?: number;
  floorArea?: number;
  
  // Validation data
  isValidated?: boolean;
  validationSource?: 'geoscape' | 'smarty_streets' | 'manual';
  confidenceScore?: number;
  validationDate?: string;
  
  // Address metadata
  isPrimary?: boolean;
  addressType?: 'residential' | 'work' | 'mailing' | 'temporary';
}
```

## 🚀 API Endpoints

### **Address Validation**
```python
POST /api/address/validate
{
  "streetNumber": "123",
  "streetName": "Main Street",
  "streetType": "Street",
  "unitNumber": "4B",
  "unitType": "Unit",
  "suburb": "Sydney",
  "state": "NSW",
  "postcode": "2000",
  "country": "Australia"
}
```

**Response**:
```json
{
  "valid": true,
  "confidence_score": 0.95,
  "property_id": "PROP_ABC123",
  "latitude": -33.8688,
  "longitude": 151.2093,
  "property_type": "Residential",
  "land_area": 450.5,
  "floor_area": 180.2,
  "suggestions": [],
  "demographics": {},
  "market_data": {}
}
```

### **Address Geocoding**
```python
POST /api/address/geocode
{
  "address": "123 Main Street, Sydney NSW 2000"
}
```

### **Reverse Geocoding**
```python
POST /api/address/reverse-geocode
{
  "latitude": -33.8688,
  "longitude": 151.2093
}
```

## 🔄 Implementation Workflow

### **1. Address Entry**
1. User enters address details in granular form
2. Form validates required fields
3. User clicks "Validate Address" button

### **2. API Validation**
1. Frontend sends address data to backend
2. Backend calls Geoscape API
3. API returns validation result with confidence score
4. Backend stores validated address data

### **3. Data Storage**
1. Address data saved to `ProfileAddress` table
2. Property details stored for future reference
3. Validation metadata tracked

### **4. User Feedback**
1. Validation status displayed to user
2. Confidence score shown
3. Property details displayed (if available)
4. User can proceed or edit address

## 🛡️ Error Handling

### **API Failures**
- Graceful degradation to manual entry
- User-friendly error messages
- Retry mechanisms for temporary failures

### **Validation Issues**
- Clear feedback on validation problems
- Suggestions for address corrections
- Manual override options

### **Data Integrity**
- Validation of all address components
- Proper error handling for missing data
- Backup validation sources (Smarty Streets)

## 📊 Benefits

### **For Users**
- **Accurate Address Data**: Real-time validation ensures correct addresses
- **Property Insights**: Access to property details and demographics
- **Professional Presentation**: Validated addresses enhance profile credibility
- **Time Savings**: Auto-completion and validation reduce manual entry

### **For Platform**
- **Data Quality**: Consistent, validated address data
- **Analytics**: Geographic insights for job matching
- **Compliance**: Proper address formatting for international users
- **Scalability**: API-based validation supports global expansion

## 🔮 Future Enhancements

### **Planned Features**
1. **Demographic Integration**: Use property demographics for job matching
2. **Commute Analysis**: Calculate commute times from validated addresses
3. **Market Data**: Integrate property market data for relocation insights
4. **International Expansion**: Support for multiple address validation services

### **Advanced Analytics**
1. **Geographic Job Matching**: Match users to jobs based on location
2. **Commute Optimization**: Suggest jobs within preferred commute times
3. **Relocation Planning**: Provide insights for job-related moves
4. **Market Analysis**: Salary insights based on geographic location

## 🔧 Development Notes

### **Testing**
- Mock Geoscape API responses for development
- Comprehensive test cases for validation scenarios
- Error handling test cases

### **Performance**
- API response caching for repeated addresses
- Batch validation for bulk operations
- Rate limiting to respect API quotas

### **Security**
- API keys stored securely in environment variables
- Address data encrypted in transit
- User consent for address validation

---

## 📞 Support

For questions about Geoscape API integration:
- **Technical Issues**: Check API documentation and error logs
- **Configuration**: Verify API keys and endpoint URLs
- **Rate Limits**: Monitor API usage and upgrade plans as needed

**Last Updated**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss") 