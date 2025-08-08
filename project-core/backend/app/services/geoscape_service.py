"""
Geoscape API Service

This module provides a service layer for interacting with the Geoscape Predictive API
for Australian address validation, geocoding, and property data retrieval.

Features:
- Address search and autocomplete
- Address validation and geocoding
- Property details retrieval
- Demographic and market data access
- Support for simple API key authentication
"""

import httpx
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import time

from ..core.api_config import APIConfig, GeoscapeEndpoints, GeoscapeAddressData


# Configure logging
logger = logging.getLogger(__name__)

class GeoscapeService:
    """
    Service class for interacting with Geoscape Predictive API.
    
    This service handles all communication with the Geoscape API for
    address validation, geocoding, and property data retrieval.
    Supports simple API key authentication.
    """
    
    def __init__(self):
        """Initialize the Geoscape service with API configuration."""
        self.api_key = APIConfig.GEOSCAPE_API_KEY
        self.consumer_secret = APIConfig.GEOSCAPE_CONSUMER_SECRET
        self.base_url = APIConfig.GEOSCAPE_BASE_URL
        self.timeout = APIConfig.GEOSCAPE_TIMEOUT
        

        
        # Validate configuration
        if not self._validate_config():
            raise ValueError("Geoscape API configuration is invalid")
    
    def _validate_config(self) -> bool:
        """Validate that the Geoscape API is properly configured."""
        return bool(self.api_key and self.consumer_secret and self.base_url)
    
    def _get_headers_simple_auth(self) -> Dict[str, str]:
        """Get authentication headers for simple API key authentication."""
        return {
            "Authorization": self.api_key,  # Direct API key, no "Bearer" prefix
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    async def _get_headers(self) -> Dict[str, str]:
        """
        Get authentication headers using simple API key authentication.
        
        Returns:
            Authentication headers
        """
        return self._get_headers_simple_auth()
    
    async def _make_request(
        self, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        method: str = "GET"
    ) -> Dict[str, Any]:
        """
        Make a request to the Geoscape API with authentication fallback.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters or request body
            method: HTTP method (GET, POST, etc.)
            
        Returns:
            API response as dictionary
            
        Raises:
            Exception: If the API request fails
        """
        try:
            url = f"{self.base_url}{endpoint}"
            headers = await self._get_headers()
            
            logger.info(f"Making {method} request to Geoscape API: {url}")
            logger.info(f"Request params: {params}")
            logger.info(f"Using authentication: Simple API Key")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                if method.upper() == "GET":
                    response = await client.get(url, headers=headers, params=params)
                elif method.upper() == "POST":
                    response = await client.post(url, headers=headers, json=params)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                logger.info(f"Geoscape API response status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    logger.info(f"Geoscape API response: {data}")
                    return data
                
                else:
                    logger.error(f"Geoscape API request failed: {response.status_code}")
                    logger.error(f"Response: {response.text}")
                    raise Exception(f"API request failed with status {response.status_code}: {response.text}")
                    
        except httpx.TimeoutException:
            logger.error("Geoscape API request timed out")
            raise Exception("Address validation service is temporarily unavailable. Please enter your address manually.")
        except httpx.RequestError as e:
            logger.error(f"Geoscape API request error: {e}")
            raise Exception("Address validation service is temporarily unavailable. Please enter your address manually.")
        except Exception as e:
            logger.error(f"Unexpected error in Geoscape API request: {e}")
            raise Exception("Address validation service is temporarily unavailable. Please enter your address manually.")
    
    def _get_mock_response(self, endpoint: str, params: Optional[Dict[str, Any]] = None, method: str = "GET") -> Dict[str, Any]:
        """
        Get mock response for testing purposes.
        
        This method provides realistic mock data that matches the expected
        Geoscape API response format for testing and development.
        """
        query = params.get("q", "") if params else ""
        address = params.get("address", "") if params else ""
        
        # Mock data for test addresses
        mock_data = {
            "4 Milburn Place, St Ives Chase NSW 2075": {
                "street_number": "4",
                "street_name": "Milburn",
                "street_type": "Place",
                "suburb": "St Ives Chase",
                "state": "NSW",
                "postcode": "2075",
                "latitude": -33.70131425995992,
                "longitude": 151.16600576829697,
                "property_id": "GNSW2075190",
                "property_type": "Residential",
                "land_area": 650.0,
                "floor_area": 180.0
            },
            "14 Milburn Place, St Ives Chase NSW 2075": {
                "street_number": "14",
                "street_name": "Milburn",
                "street_type": "Place",
                "suburb": "St Ives Chase",
                "state": "NSW",
                "postcode": "2075",
                "latitude": -33.70131425995992,
                "longitude": 151.16600576829697,
                "property_id": "GNSW2075191",
                "property_type": "Residential",
                "land_area": 650.0,
                "floor_area": 180.0
            },
            "123 Main Street, Sydney NSW 2000": {
                "street_number": "123",
                "street_name": "Main",
                "street_type": "Street",
                "suburb": "Sydney",
                "state": "NSW",
                "postcode": "2000",
                "latitude": -33.8688,
                "longitude": 151.2093,
                "property_id": "GNSW2000123",
                "property_type": "Commercial",
                "land_area": 200.0,
                "floor_area": 500.0
            }
        }
        
        if "/address/search" in endpoint:
            # Mock search response
            suggestions = []
            for addr, data in mock_data.items():
                if query.lower() in addr.lower():
                    suggestions.append({
                        "formatted_address": addr,
                        "id": data["property_id"],
                        "address": {
                            "street_number": data["street_number"],
                            "street_name": data["street_name"],
                            "street_type": data["street_type"],
                            "suburb": data["suburb"],
                            "state": data["state"],
                            "postcode": data["postcode"]
                        },
                        "property": {
                            "id": data["property_id"],
                            "type": data["property_type"],
                            "land_area": data["land_area"],
                            "floor_area": data["floor_area"]
                        },
                        "location": {
                            "latitude": data["latitude"],
                            "longitude": data["longitude"]
                        },
                        "confidence_score": 0.98
                    })
            
            return {
                "suggestions": suggestions[:5]  # Limit to 5 suggestions
            }
        
        elif "/address/validate" in endpoint:
            # Mock validation response
            for addr, data in mock_data.items():
                if address.lower() in addr.lower() or addr.lower() in address.lower():
                    return {
                        "result": {
                            "valid": True,
                            "confidence_score": 0.98,
                            "formatted_address": addr,
                            "address": {
                                "street_number": data["street_number"],
                                "street_name": data["street_name"],
                                "street_type": data["street_type"],
                                "suburb": data["suburb"],
                                "state": data["state"],
                                "postcode": data["postcode"]
                            },
                            "property": {
                                "id": data["property_id"],
                                "type": data["property_type"],
                                "land_area": data["land_area"],
                                "floor_area": data["floor_area"]
                            },
                            "location": {
                                "latitude": data["latitude"],
                                "longitude": data["longitude"]
                            },
                            "demographics": {
                                "population": 15000,
                                "median_age": 35,
                                "median_income": 85000
                            }
                        }
                    }
            
            # Default response for unknown addresses
            return {
                "result": {
                    "valid": False,
                    "confidence_score": 0.0,
                    "formatted_address": address,
                    "address": {},
                    "property": {},
                    "location": {},
                    "demographics": {}
                }
            }
        
        elif "/health" in endpoint:
            return {
                "status": "healthy",
                "timestamp": datetime.now().isoformat()
            }
        
        # Default response
        return {"error": "Mock endpoint not implemented"}
    
    async def search_addresses(
        self, 
        query: str, 
        limit: int = 10,
        state: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for addresses using Geoscape autocomplete.
        
        Args:
            query: Address search query
            limit: Maximum number of suggestions
            state: Filter by state (optional)
            
        Returns:
            List of address suggestions with standardized format
        """
        try:
            # Prepare request parameters
            params = {
                "query": query,  # Use "query" parameter as per their API
                "limit": limit
            }
            
            if state:
                params["state"] = state
            
            # Make API request
            logger.info(f"Searching addresses with query: '{query}', limit: {limit}, state: {state}")
            response = await self._make_request(
                endpoint="/predictive/address",  # Correct working endpoint
                params=params
            )
            logger.info(f"Geoscape search response: {response}")
            
            # Process and standardize response
            suggestions = []
            for item in response.get("suggest", []):  # Use "suggest" key as per their API
                suggestion = self._standardize_address_suggestion(item)
                if suggestion:
                    suggestions.append(suggestion)
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Address search failed: {str(e)}")
            raise
    
    async def validate_address(
        self, 
        address: str,
        property_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Validate and geocode an address.
        
        Args:
            address: Full address to validate
            property_id: Geoscape property ID for precise validation (optional)
            
        Returns:
            Validation result with standardized address data
        """
        try:
            # Prepare request parameters
            params = {
                "address": address,
                "include": "property,location,demographics,market"
            }
            
            if property_id:
                params["property_id"] = property_id
            
            # Make API request
            response = await self._make_request(
                endpoint="/predictive/address/validate",
                params=params,
                method="POST"
            )
            
            # Process and standardize response
            validation_result = self._standardize_validation_response(response)
            return validation_result
            
        except Exception as e:
            logger.error(f"Address validation failed: {str(e)}")
            raise
    
    async def get_address_coordinates(self, address: str, property_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get precise coordinates for a selected address.
        
        Args:
            address: Full address string
            property_id: Geoscape property ID (optional)
            
        Returns:
            Dictionary with coordinates and address details
        """
        try:
            # First try to get coordinates from the property details endpoint if we have a property_id
            if property_id:
                try:
                    property_details = await self.get_property_details(property_id)
                    if property_details.get("success") and property_details.get("coordinates"):
                        return {
                            "success": True,
                            "latitude": property_details["coordinates"]["latitude"],
                            "longitude": property_details["coordinates"]["longitude"],
                            "address": property_details.get("address", {}),
                            "property_id": property_id,
                            "confidence_score": 0.9
                        }
                except Exception as e:
                    logger.warning(f"Failed to get property details for {property_id}: {e}")
            
            # Fallback to search endpoint
            search_results = await self.search_addresses(address, limit=5)
            
            if search_results:
                # Find the best match
                best_match = None
                for result in search_results:
                    if result.get("address", "").lower() == address.lower():
                        best_match = result
                        break
                
                # If no exact match, use the first result
                if not best_match and search_results:
                    best_match = search_results[0]
                
                if best_match:
                    # Try to get coordinates from the search result data
                    address_data = best_match.get("data", {})
                    latitude = address_data.get("latitude")
                    longitude = address_data.get("longitude")
                    
                    # If we have actual coordinates from the search, use them
                    if latitude is not None and longitude is not None:
                        address_data.update({
                            "latitude": latitude,
                            "longitude": longitude
                        })
                        
                        return {
                            "success": True,
                            "latitude": latitude,
                            "longitude": longitude,
                            "address": address_data,
                            "property_id": best_match.get("id"),
                            "confidence_score": 0.8
                        }
                    
                    # If no coordinates in search result, try to get them from property details
                    property_id = best_match.get("id")
                    if property_id:
                        try:
                            property_details = await self.get_property_details(property_id)
                            if property_details.get("success") and property_details.get("coordinates"):
                                return {
                                    "success": True,
                                    "latitude": property_details["coordinates"]["latitude"],
                                    "longitude": property_details["coordinates"]["longitude"],
                                    "address": address_data,
                                    "property_id": property_id,
                                    "confidence_score": 0.7
                                }
                        except Exception as e:
                            logger.warning(f"Failed to get property details for {property_id}: {e}")
                    
                    # Last resort: use default coordinates based on state
                    state = address_data.get("state", "NSW")
                    
                    # Get default coordinates for the state
                    state_coords = {
                        'NSW': [-33.8688, 151.2093], # Sydney
                        'VIC': [-37.8136, 144.9631], # Melbourne
                        'QLD': [-27.4698, 153.0251], # Brisbane
                        'WA': [-31.9505, 115.8605],  # Perth
                        'SA': [-34.9285, 138.6007],  # Adelaide
                        'TAS': [-42.8821, 147.3272], # Hobart
                        'NT': [-12.4634, 130.8456],  # Darwin
                        'ACT': [-35.2809, 149.1300]  # Canberra
                    }
                    
                    default_lat, default_lng = state_coords.get(state, [-33.8688, 151.2093])
                    
                    # Include coordinates in the address object as well
                    address_data.update({
                        "latitude": default_lat,
                        "longitude": default_lng
                    })
                    
                    return {
                        "success": True,
                        "latitude": default_lat,
                        "longitude": default_lng,
                        "address": address_data,
                        "property_id": property_id,
                        "confidence_score": 0.5  # Lower confidence for default coordinates
                    }
            
            logger.warning(f"No address match found for: {address}")
            return {
                "success": False,
                "error": "No address match found",
                "address": address
            }
                
        except Exception as e:
            logger.error(f"Failed to get coordinates for address {address}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "address": address
            }

    async def get_property_details(self, property_id: str) -> Dict[str, Any]:
        """
        Get detailed property information.
        
        Args:
            property_id: Geoscape property identifier
            
        Returns:
            Property details including type, area, demographics, etc.
        """
        try:
            response = await self._make_request(
                endpoint=f"/property/{property_id}",
                params={"include": "demographics,market,location"}
            )
            
            return self._standardize_property_response(response)
            
        except Exception as e:
            logger.error(f"Property details retrieval failed: {str(e)}")
            raise
    
    def _standardize_address_suggestion(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Standardize address suggestion from Geoscape API response.
        
        Args:
            item: Raw suggestion item from API
            
        Returns:
            Standardized suggestion dictionary
        """
        try:
            # Extract address components from their format
            address = item.get("address", "")
            suggestion_id = item.get("id", "")
            rank = item.get("rank", 0)
            
            # Parse the address string to extract components
            # Example: "4 MILBURN CCT, BOOLAROO NSW 2284"
            address_parts = address.split(", ")
            if len(address_parts) >= 2:
                street_part = address_parts[0]
                location_part = address_parts[1]
                
                # Parse street part (e.g., "4 MILBURN CCT")
                street_words = street_part.split()
                if len(street_words) >= 3:
                    street_number = street_words[0]
                    # Join all words except first (number) and last (type) as street name
                    street_name = " ".join(street_words[1:-1])
                    street_type = street_words[-1]
                elif len(street_words) == 2:
                    # Handle cases like "4 MILBURN" (no street type)
                    street_number = street_words[0]
                    street_name = street_words[1]
                    street_type = ""
                else:
                    street_number = ""
                    street_name = street_part
                    street_type = ""
                
                # Parse location part (e.g., "BOOLAROO NSW 2284")
                location_words = location_part.split()
                if len(location_words) >= 3:
                    # Last two words are state and postcode
                    suburb = " ".join(location_words[:-2])
                    state = location_words[-2]
                    postcode = location_words[-1]
                elif len(location_words) == 2:
                    # Handle cases with just suburb and state
                    suburb = location_words[0]
                    state = location_words[1]
                    postcode = ""
                else:
                    suburb = location_part
                    state = ""
                    postcode = ""
            else:
                # Fallback for addresses without comma separation
                street_number = ""
                street_name = ""
                street_type = ""
                suburb = ""
                state = ""
                postcode = ""
            
            # Build standardized suggestion
            suggestion = {
                "address": address,
                "id": suggestion_id,
                "data": {
                    "streetNumber": street_number,
                    "streetName": street_name,
                    "streetType": street_type,
                    "suburb": suburb,
                    "state": state,
                    "postcode": postcode,
                    "latitude": None,  # Not provided in this response
                    "longitude": None,  # Not provided in this response
                    "propertyType": None,  # Not provided in this response
                    "landArea": None,  # Not provided in this response
                    "floorArea": None  # Not provided in this response
                },
                "confidence": 1.0 - (rank * 0.1)  # Convert rank to confidence score
            }
            
            return suggestion
            
        except Exception as e:
            logger.error(f"Failed to standardize address suggestion: {str(e)}")
            return None
    
    def _standardize_validation_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Standardize address validation response.
        
        Args:
            response: Raw validation response from API
            
        Returns:
            Standardized validation result
        """
        try:
            # Extract main result
            result = response.get("result", {})
            address_data = result.get("address", {})
            property_data = result.get("property", {})
            location_data = result.get("location", {})
            demographics_data = result.get("demographics", {})
            
            # Get coordinates with 15 decimal precision
            latitude = location_data.get("latitude")
            longitude = location_data.get("longitude")
            
            # Format coordinates to 15 decimal places if they exist
            if latitude is not None:
                latitude = round(float(latitude), 15)
            if longitude is not None:
                longitude = round(float(longitude), 15)
            
            # Build standardized validation result
            validation_result = {
                "validated": result.get("valid", False),
                "confidence_score": result.get("confidence_score", 0.0),
                "property_id": property_data.get("id"),
                "address": {
                    "streetNumber": address_data.get("street_number"),
                    "streetName": address_data.get("street_name"),
                    "streetType": address_data.get("street_type"),
                    "suburb": address_data.get("suburb"),
                    "state": address_data.get("state"),
                    "postcode": address_data.get("postcode"),
                    "country": "Australia",
                    "latitude": latitude,
                    "longitude": longitude,
                    "formattedAddress": result.get("formatted_address", "")
                },
                "metadata": {
                    "propertyType": property_data.get("type"),
                    "landArea": property_data.get("land_area"),
                    "floorArea": property_data.get("floor_area"),
                    "demographics": demographics_data,
                    "validationDate": datetime.now().isoformat(),
                    "validationSource": "geoscape"
                }
            }
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Failed to standardize validation response: {str(e)}")
            return {
                "validated": False,
                "confidence_score": 0.0,
                "address": {},
                "metadata": {},
                "error": str(e)
            }
    
    def _standardize_property_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Standardize property details response.
        
        Args:
            response: Raw property response from API
            
        Returns:
            Standardized property details
        """
        try:
            property_data = response.get("property", {})
            location_data = response.get("location", {})
            demographics_data = response.get("demographics", {})
            market_data = response.get("market", {})
            
            return {
                "property_id": property_data.get("id"),
                "property_type": property_data.get("type"),
                "land_area": property_data.get("land_area"),
                "floor_area": property_data.get("floor_area"),
                "latitude": location_data.get("latitude"),
                "longitude": location_data.get("longitude"),
                "demographics": demographics_data,
                "market_data": market_data,
                "last_updated": response.get("last_updated")
            }
            
        except Exception as e:
            logger.error(f"Failed to standardize property response: {str(e)}")
            return {"error": str(e)}
    
    async def test_connection(self) -> bool:
        """
        Test the connection to Geoscape API.
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            # Make a simple health check request
            response = await self._make_request("/health")
            return response.get("status") == "healthy"
        except Exception as e:
            logger.error(f"Geoscape API connection test failed: {str(e)}")
            return False 