# API Configuration for External Services
# This file stores API keys and configuration for external services

import os
from typing import Optional

class APIConfig:
    """Configuration class for external API services"""
    
    # Geoscape Predictive API Configuration
    GEOSCAPE_API_KEY: str = "9x4fpNyrr8VxVqWvPeKnuEWaH9vxgGxS"
    GEOSCAPE_CONSUMER_SECRET: str = "8XkTgtu0Sz1D0aG9"
    GEOSCAPE_BASE_URL: str = "https://api.geoscape.com.au/v1"
    GEOSCAPE_TIMEOUT: int = 30  # seconds
    
    # Geoscape API Products (per your subscription)
    GEOSCAPE_ADDRESSES_API: bool = True
    GEOSCAPE_PREDICTIVE_API: bool = True
    
    # Regional API Configuration (Future expansion)
    REGIONAL_API_PROVIDERS = {
        'AU': 'geoscape',      # Australia - Geoscape
        'US': 'smarty_streets', # United States - SmartyStreets  
        'UK': 'postcodes_io',   # United Kingdom - Postcodes.io
        'CA': 'canada_post',    # Canada - Canada Post
        'EU': 'here_api',       # Europe - HERE API
        # TODO: Add more regions as needed for global expansion
    }
    
    # Smarty Streets API Configuration (backup address validation)
    SMARTY_STREETS_API_KEY: Optional[str] = os.getenv('SMARTY_STREETS_API_KEY')
    SMARTY_STREETS_AUTH_TOKEN: Optional[str] = os.getenv('SMARTY_STREETS_AUTH_TOKEN')
    SMARTY_STREETS_BASE_URL: str = "https://us-street.api.smartystreets.com/street-address"
    
    # OpenAI API Configuration (for resume parsing)
    OPENAI_API_KEY: Optional[str] = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    
    @classmethod
    def validate_geoscape_config(cls) -> bool:
        """Validate that Geoscape API is properly configured"""
        return bool(cls.GEOSCAPE_API_KEY)
    
    @classmethod
    def validate_smarty_streets_config(cls) -> bool:
        """Validate that Smarty Streets API is properly configured"""
        return bool(cls.SMARTY_STREETS_API_KEY and cls.SMARTY_STREETS_AUTH_TOKEN)
    
    @classmethod
    def validate_openai_config(cls) -> bool:
        """Validate that OpenAI API is properly configured"""
        return bool(cls.OPENAI_API_KEY)

# Geoscape API Endpoints and Data Structures
class GeoscapeEndpoints:
    """Geoscape API endpoint definitions"""
    
    # Address validation and geocoding
    ADDRESS_VALIDATION = "/address/validate"
    ADDRESS_GEOCODE = "/address/geocode"
    ADDRESS_REVERSE_GEOCODE = "/address/reverse-geocode"
    
    # Property and location data
    PROPERTY_DETAILS = "/property/details"
    LOCATION_DETAILS = "/location/details"
    
    # Demographic and market data
    DEMOGRAPHICS = "/demographics"
    MARKET_DATA = "/market-data"

# Geoscape API Response Types
class GeoscapeAddressData:
    """Data structure for Geoscape address validation response"""
    
    def __init__(self, api_response: dict):
        self.raw_response = api_response
        self.is_valid = api_response.get('valid', False)
        self.confidence_score = api_response.get('confidence_score', 0.0)
        self.suggestions = api_response.get('suggestions', [])
        
        # Standardized address components
        self.street_number = api_response.get('street_number')
        self.street_name = api_response.get('street_name')
        self.street_type = api_response.get('street_type')
        self.suburb = api_response.get('suburb')
        self.state = api_response.get('state')
        self.postcode = api_response.get('postcode')
        self.country = api_response.get('country', 'Australia')
        
        # Additional Geoscape-specific data
        self.property_id = api_response.get('property_id')
        self.latitude = api_response.get('latitude')
        self.longitude = api_response.get('longitude')
        self.property_type = api_response.get('property_type')
        self.land_area = api_response.get('land_area')
        self.floor_area = api_response.get('floor_area')
        
        # Demographic data
        self.demographics = api_response.get('demographics', {})
        self.market_data = api_response.get('market_data', {})
    
    def to_address_dict(self) -> dict:
        """Convert to standardized address format for database storage"""
        return {
            'street_number': self.street_number,
            'street_name': self.street_name,
            'street_type': self.street_type,
            'suburb': self.suburb,
            'state': self.state,
            'postcode': self.postcode,
            'country': self.country,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'property_id': self.property_id,
            'property_type': self.property_type,
            'land_area': self.land_area,
            'floor_area': self.floor_area,
            'confidence_score': self.confidence_score,
            'is_validated': self.is_valid
        } 