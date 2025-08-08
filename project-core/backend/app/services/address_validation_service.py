"""
Address Validation Service

This module provides a unified service for address validation across multiple
API providers, with automatic fallback and regional routing.

Supported Providers:
- Geoscape (Australia) - Primary provider for AU addresses
- SmartyStreets (US) - Primary provider for US addresses
- Future: Regional providers for global expansion
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from .geoscape_service import GeoscapeService
from ..core.api_config import APIConfig

# Configure logging
logger = logging.getLogger(__name__)

class AddressValidationService:
    """
    Unified address validation service with multi-provider support.
    
    This service automatically routes address validation requests to the
    appropriate API provider based on country and provides fallback options.
    """
    
    def __init__(self):
        """Initialize the address validation service with configured providers."""
        self.providers = {}
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize available API providers based on configuration."""
        try:
            # Initialize Geoscape for Australia
            if APIConfig.validate_geoscape_config():
                self.providers['geoscape'] = GeoscapeService()
                logger.info("Geoscape service initialized for Australia")
            else:
                logger.warning("Geoscape API not configured - Australian addresses will not be supported")
        
        except Exception as e:
            logger.error(f"Failed to initialize Geoscape service: {str(e)}")
        
        # TODO: Initialize SmartyStreets for US addresses
        # if APIConfig.validate_smarty_streets_config():
        #     self.providers['smarty_streets'] = SmartyStreetsService()
        #     logger.info("SmartyStreets service initialized for US")
        
        if not self.providers:
            logger.warning("No address validation providers configured")
    
    def _get_provider_for_country(self, country: str) -> Optional[str]:
        """
        Get the appropriate provider for a given country.
        
        Args:
            country: Country code (AU, US, etc.)
            
        Returns:
            Provider name or None if no provider available
        """
        provider_mapping = {
            'AU': 'geoscape',
            'US': 'smarty_streets',
            # Add more mappings as providers are added
        }
        
        return provider_mapping.get(country.upper())
    
    async def search_addresses(
        self, 
        query: str, 
        country: str = "AU",
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for addresses using autocomplete functionality.
        
        Args:
            query: Address search query
            country: Country code (AU, US, etc.)
            limit: Maximum number of suggestions
            
        Returns:
            List of address suggestions in standardized format
        """
        try:
            # Get appropriate provider
            provider_name = self._get_provider_for_country(country)
            if not provider_name or provider_name not in self.providers:
                logger.warning(f"No provider available for country: {country}")
                return []
            
            provider = self.providers[provider_name]
            
            # Perform search based on provider
            if provider_name == 'geoscape':
                suggestions = await provider.search_addresses(query, limit)
            elif provider_name == 'smarty_streets':
                # TODO: Implement SmartyStreets search
                suggestions = []
            else:
                logger.error(f"Unknown provider: {provider_name}")
                return []
            
            # Standardize suggestions
            standardized_suggestions = []
            for suggestion in suggestions:
                standardized = self._standardize_suggestion(suggestion, country)
                if standardized:
                    standardized_suggestions.append(standardized)
            
            return standardized_suggestions
            
        except Exception as e:
            logger.error(f"Address search failed: {str(e)}")
            raise e
    
    async def get_address_coordinates(
        self, 
        address: str, 
        property_id: Optional[str] = None,
        country: str = "AU"
    ) -> Dict[str, Any]:
        """
        Get precise coordinates for a selected address.
        
        Args:
            address: Full address string
            property_id: Property ID from the provider (optional)
            country: Country code (AU, US, etc.)
            
        Returns:
            Dictionary with coordinates and address details
        """
        try:
            # Get appropriate provider
            provider_name = self._get_provider_for_country(country)
            if not provider_name or provider_name not in self.providers:
                logger.warning(f"No provider available for country: {country}")
                return {
                    "success": False,
                    "error": f"No provider available for country: {country}",
                    "address": address
                }
            
            provider = self.providers[provider_name]
            
            # Get coordinates from provider
            if provider_name == 'geoscape':
                result = await provider.get_address_coordinates(address, property_id)
            else:
                # For other providers, use validation endpoint
                validation_result = await provider.validate_address(address, property_id)
                if validation_result.get("validated", False):
                    address_data = validation_result.get("address", {})
                    result = {
                        "success": True,
                        "latitude": address_data.get("latitude"),
                        "longitude": address_data.get("longitude"),
                        "address": address_data,
                        "property_id": validation_result.get("property_id"),
                        "confidence_score": validation_result.get("confidence_score", 0.0)
                    }
                else:
                    result = {
                        "success": False,
                        "error": "Address validation failed",
                        "address": address
                    }
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to get coordinates for address {address}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "address": address
            }

    async def validate_address(
        self, 
        address: str,
        property_id: Optional[str] = None,
        country: str = "AU"
    ) -> Dict[str, Any]:
        """
        Validate and geocode an address.
        
        Args:
            address: Full address to validate
            property_id: Property ID for precise validation (optional)
            country: Country code (AU, US, etc.)
            
        Returns:
            Validation result with standardized address data
        """
        try:
            # Get appropriate provider
            provider_name = self._get_provider_for_country(country)
            if not provider_name or provider_name not in self.providers:
                logger.warning(f"No provider available for country: {country}")
                return self._create_fallback_response(address, country)
            
            provider = self.providers[provider_name]
            
            # Perform validation based on provider
            if provider_name == 'geoscape':
                validation_result = await provider.validate_address(address, property_id)
            elif provider_name == 'smarty_streets':
                # TODO: Implement SmartyStreets validation
                validation_result = self._create_fallback_response(address, country)
            else:
                logger.error(f"Unknown provider: {provider_name}")
                return self._create_fallback_response(address, country)
            
            # Standardize validation result
            standardized_result = self._standardize_validation_result(validation_result, country)
            return standardized_result
            
        except Exception as e:
            logger.error(f"Address validation failed: {str(e)}")
            return self._create_fallback_response(address, country, error=str(e))
    
    def _standardize_suggestion(self, suggestion: Dict[str, Any], country: str) -> Optional[Dict[str, Any]]:
        """
        Standardize address suggestion across providers.
        
        Args:
            suggestion: Raw suggestion from provider
            country: Country code for context
            
        Returns:
            Standardized suggestion or None if invalid
        """
        try:
            # Extract common fields
            data = suggestion.get('data', {})
            
            standardized = {
                "address": suggestion.get('address', ''),
                "id": suggestion.get('id', ''),
                "data": {
                    "streetNumber": data.get('streetNumber'),
                    "streetName": data.get('streetName'),
                    "streetType": data.get('streetType'),
                    "suburb": data.get('suburb'),
                    "state": data.get('state'),
                    "postcode": data.get('postcode'),
                    "country": country,
                    "latitude": data.get('latitude'),
                    "longitude": data.get('longitude'),
                    "propertyType": data.get('propertyType'),
                    "landArea": data.get('landArea'),
                    "floorArea": data.get('floorArea')
                },
                "confidence": suggestion.get('confidence', 0.0)
            }
            
            return standardized
            
        except Exception as e:
            logger.error(f"Failed to standardize suggestion: {str(e)}")
            return None
    
    def _standardize_validation_result(self, result: Dict[str, Any], country: str) -> Dict[str, Any]:
        """
        Standardize validation result across providers.
        
        Args:
            result: Raw validation result from provider
            country: Country code for context
            
        Returns:
            Standardized validation result
        """
        try:
            address_data = result.get('address', {})
            metadata = result.get('metadata', {})
            
            standardized = {
                "validated": result.get('validated', False),
                "confidence_score": result.get('confidence_score', 0.0),
                "property_id": result.get('property_id'),
                "address": {
                    "streetNumber": address_data.get('streetNumber'),
                    "streetName": address_data.get('streetName'),
                    "streetType": address_data.get('streetType'),
                    "suburb": address_data.get('suburb'),
                    "state": address_data.get('state'),
                    "postcode": address_data.get('postcode'),
                    "country": country,
                    "latitude": address_data.get('latitude'),
                    "longitude": address_data.get('longitude'),
                    "formattedAddress": address_data.get('formattedAddress', '')
                },
                "metadata": {
                    "propertyType": metadata.get('propertyType'),
                    "landArea": metadata.get('landArea'),
                    "floorArea": metadata.get('floorArea'),
                    "demographics": metadata.get('demographics', {}),
                    "validationDate": metadata.get('validationDate', datetime.now().isoformat()),
                    "validationSource": metadata.get('validationSource', 'unknown')
                }
            }
            
            return standardized
            
        except Exception as e:
            logger.error(f"Failed to standardize validation result: {str(e)}")
            return self._create_fallback_response("", country, error=str(e))
    
    def _create_fallback_response(
        self, 
        address: str, 
        country: str, 
        error: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a fallback response when validation fails.
        
        Args:
            address: Original address
            country: Country code
            error: Error message (optional)
            
        Returns:
            Fallback validation result
        """
        return {
            "validated": False,
            "confidence_score": 0.0,
            "property_id": None,
            "address": {
                "streetNumber": None,
                "streetName": None,
                "streetType": None,
                "suburb": None,
                "state": None,
                "postcode": None,
                "country": country,
                "latitude": None,
                "longitude": None,
                "formattedAddress": address
            },
            "metadata": {
                "propertyType": None,
                "landArea": None,
                "floorArea": None,
                "demographics": {},
                "validationDate": datetime.now().isoformat(),
                "validationSource": "fallback",
                "error": error
            }
        }
    
    async def test_providers(self) -> Dict[str, bool]:
        """
        Test all configured providers.
        
        Returns:
            Dictionary mapping provider names to connection status
        """
        results = {}
        
        for provider_name, provider in self.providers.items():
            try:
                if hasattr(provider, 'test_connection'):
                    results[provider_name] = await provider.test_connection()
                else:
                    results[provider_name] = True  # Assume working if no test method
            except Exception as e:
                logger.error(f"Provider {provider_name} test failed: {str(e)}")
                results[provider_name] = False
        
        return results
    
    def get_available_countries(self) -> List[str]:
        """
        Get list of countries with available providers.
        
        Returns:
            List of country codes with available validation services
        """
        available_countries = []
        
        if 'geoscape' in self.providers:
            available_countries.append('AU')
        
        if 'smarty_streets' in self.providers:
            available_countries.append('US')
        
        return available_countries 