"""
Address Validation API Endpoints

This module provides REST API endpoints for address validation and search functionality
using the Geoscape API for Australian addresses and SmartyStreets as a fallback for US addresses.

Endpoints:
- GET /api/address/search - Address autocomplete/search
- POST /api/address/validate - Address validation and geocoding
"""

from fastapi import APIRouter, HTTPException, Depends, Request, Query
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import httpx
import json
import logging
import os
from datetime import datetime
from sqlalchemy.orm import Session
import time

# Create log directory if it doesn't exist
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'log')
os.makedirs(log_dir, exist_ok=True)

# Configure file logging for API calls
api_logger = logging.getLogger('api_calls')
api_logger.setLevel(logging.INFO)
api_handler = logging.FileHandler(os.path.join(log_dir, 'api_calls.log'))
api_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
api_logger.addHandler(api_handler)
api_logger.propagate = False

def log_api_call(endpoint: str, method: str, request_data: Dict, response_data: Dict, status_code: int, response_time: float):
    """Log API call details to file"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'endpoint': endpoint,
        'method': method,
        'request_data': request_data,
        'response_data': response_data,
        'status_code': status_code,
        'response_time_ms': round(response_time * 1000, 2)
    }
    api_logger.info(f"API_CALL: {json.dumps(log_entry, indent=2)}")

from ..core.api_config import APIConfig, GeoscapeEndpoints, GeoscapeAddressData
from ..models import ProfileAddress, APIUsageTracking
from ..services.geoscape_service import GeoscapeService
from ..services.address_validation_service import AddressValidationService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/address", tags=["address"])

# Pydantic models for request/response
class AddressSearchRequest(BaseModel):
    query: str = Field(..., min_length=3, description="Address search query")
    country: str = Field(default="AU", description="Country code (AU, US, etc.)")
    limit: int = Field(default=10, ge=1, le=50, description="Maximum number of suggestions")

class AddressSearchResponse(BaseModel):
    suggestions: List[Dict[str, Any]]
    total_count: int
    query: str
    country: str
    error: Optional[str] = None

class AddressValidationRequest(BaseModel):
    address: str = Field(..., description="Full address to validate")
    property_id: Optional[str] = Field(None, description="Geoscape property ID for precise validation")
    country: str = Field(default="AU", description="Country code")

class AddressValidationResponse(BaseModel):
    validated: bool
    address: Dict[str, Any]
    metadata: Dict[str, Any]
    confidence_score: float
    property_id: Optional[str] = None

class AddressCoordinatesRequest(BaseModel):
    address: str = Field(..., description="Full address to get coordinates for")
    property_id: Optional[str] = Field(None, description="Geoscape property ID for precise coordinates")
    country: str = Field(default="AU", description="Country code")

class AddressCoordinatesResponse(BaseModel):
    success: bool
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[Dict[str, Any]] = None
    property_id: Optional[str] = None
    confidence_score: Optional[float] = None
    error: Optional[str] = None

class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None

# Import database session
from mcp.db.session import get_db

# Dependency for database session
def get_db_session():
    """Get database session using the existing session configuration"""
    return next(get_db())

@router.get("/search", response_model=AddressSearchResponse)
async def search_addresses(
    q: str = Query(..., min_length=3, description="Address search query"),
    country: str = Query(default="AU", description="Country code"),
    limit: int = Query(default=10, ge=1, le=50, description="Maximum suggestions"),
    request: Request = None,
    db: Session = Depends(get_db_session)
):
    """
    Search for addresses using autocomplete functionality.
    
    This endpoint provides address suggestions based on partial input,
    using Geoscape API for Australian addresses and SmartyStreets for US addresses.
    """
    start_time = datetime.now()
    request_data = {"query": q, "country": country, "limit": limit}
    
    try:
        # Initialize address validation service
        address_service = AddressValidationService()
        
        # Perform address search
        try:
            suggestions = await address_service.search_addresses(
                query=q,
                country=country,
                limit=limit
            )
        except Exception as e:
            # Log the error
            response_time = (datetime.now() - start_time).total_seconds() * 1000
            error_response = {
                "error": "Address lookup service is not available",
                "message": str(e),
                "suggestions": [],
                "total_count": 0,
                "query": q,
                "country": country
            }
            
            # Log error API call
            log_api_call(
                endpoint="/api/address/search",
                method="GET",
                request_data={"query": q, "country": country, "limit": limit},
                response_data=error_response,
                status_code=503,
                response_time=response_time
            )
            
            # Return error response
            return AddressSearchResponse(
                suggestions=[],
                total_count=0,
                query=q,
                country=country,
                error="Address lookup service is not available. Please use manual address entry below."
            )
        
        # Prepare response
        response_data = {
            "suggestions": suggestions,
            "total_count": len(suggestions),
            "query": q,
            "country": country
        }
        
        # Log successful API call
        response_time = (datetime.now() - start_time).total_seconds()
        log_api_call(
            endpoint="/api/address/search",
            method="GET",
            request_data=request_data,
            response_data=response_data,
            status_code=200,
            response_time=response_time
        )
        
        # Log API usage for billing
        if db:
            await log_api_usage(
                db=db,
                api_provider="geoscape" if country == "AU" else "smarty_streets",
                endpoint="/address/search",
                request_data={"query": q, "country": country, "limit": limit},
                response_status="success",
                response_time=(datetime.now() - start_time).total_seconds() * 1000,
                user_id=None,  # TODO: Get from authentication
                request=request
            )
        
        return AddressSearchResponse(
            suggestions=suggestions,
            total_count=len(suggestions),
            query=q,
            country=country
        )
        
    except Exception as e:
        # Log error API call
        response_time = (datetime.now() - start_time).total_seconds()
        error_response = {"error": "Address search failed", "message": str(e)}
        log_api_call(
            endpoint="/api/address/search",
            method="GET",
            request_data=request_data,
            response_data=error_response,
            status_code=500,
            response_time=response_time
        )
        
        logger.error(f"Address search error: {str(e)}")
        
        # Log failed API usage
        if db:
            await log_api_usage(
                db=db,
                api_provider="geoscape" if country == "AU" else "smarty_streets",
                endpoint="/address/search",
                request_data={"query": q, "country": country, "limit": limit},
                response_status="error",
                response_time=0,
                error_message=str(e),
                user_id=None,
                request=request
            )
        
        raise HTTPException(
            status_code=500,
            detail=f"Address search failed: {str(e)}"
        )

@router.post("/validate", response_model=AddressValidationResponse)
async def validate_address(
    request_data: AddressValidationRequest,
    request: Request = None,
    db: Session = Depends(get_db_session)
):
    """
    Validate and geocode an address.
    
    This endpoint validates the provided address and returns standardized
    address components with coordinates and confidence scores.
    """
    start_time = datetime.now()
    request_data_dict = request_data.dict()
    
    try:
        # Initialize address validation service
        address_service = AddressValidationService()
        
        # Validate address
        validation_result = await address_service.validate_address(
            address=request_data.address,
            property_id=request_data.property_id,
            country=request_data.country
        )
        
        # Prepare response
        response_data = {
            "validated": validation_result.get("validated", False),
            "address": validation_result.get("address", {}),
            "metadata": validation_result.get("metadata", {}),
            "confidence_score": validation_result.get("confidence_score", 0.0),
            "property_id": validation_result.get("property_id")
        }
        
        # Log successful API call
        response_time = (datetime.now() - start_time).total_seconds()
        log_api_call(
            endpoint="/api/address/validate",
            method="POST",
            request_data=request_data_dict,
            response_data=response_data,
            status_code=200,
            response_time=response_time
        )
        
        # Log API usage for billing
        if db:
            await log_api_usage(
                db=db,
                api_provider="geoscape" if request_data.country == "AU" else "smarty_streets",
                endpoint="/address/validate",
                request_data=request_data.dict(),
                response_status="success",
                response_time=(datetime.now() - start_time).total_seconds() * 1000,
                user_id=None,  # TODO: Get from authentication
                request=request
            )
        
        # Save validated address to database if validation was successful
        profile_address_id = None
        if validation_result.get("validated", False) and db:
            address_data = validation_result.get("address", {})
            address_data.update({
                "property_id": validation_result.get("property_id"),
                "validation_source": "geoscape" if request_data.country == "AU" else "smarty_streets",
                "confidence_score": validation_result.get("confidence_score", 0.0)
            })
            
            profile_address_id = await save_validated_address(
                db=db,
                address_data=address_data,
                user_id=None,  # TODO: Get from authentication
                profile_id=None  # TODO: Get from user context
            )
        
        return AddressValidationResponse(
            validated=validation_result.get("validated", False),
            address=validation_result.get("address", {}),
            metadata=validation_result.get("metadata", {}),
            confidence_score=validation_result.get("confidence_score", 0.0),
            property_id=validation_result.get("property_id")
        )
        
    except Exception as e:
        # Log error API call
        response_time = (datetime.now() - start_time).total_seconds()
        error_response = {"error": "Address validation failed", "message": str(e)}
        log_api_call(
            endpoint="/api/address/validate",
            method="POST",
            request_data=request_data_dict,
            response_data=error_response,
            status_code=500,
            response_time=response_time
        )
        
        logger.error(f"Address validation error: {str(e)}")
        
        # Log failed API usage
        if db:
            await log_api_usage(
                db=db,
                api_provider="geoscape" if request_data.country == "AU" else "smarty_streets",
                endpoint="/address/validate",
                request_data=request_data.dict(),
                response_status="error",
                response_time=0,
                error_message=str(e),
                user_id=None,
                request=request
            )
        
        raise HTTPException(
            status_code=500,
            detail=f"Address validation failed: {str(e)}"
        )

@router.post("/coordinates", response_model=AddressCoordinatesResponse)
async def get_address_coordinates(
    request_data: AddressCoordinatesRequest,
    request: Request = None,
    db: Session = Depends(get_db_session)
):
    """
    Get precise coordinates for a selected address.
    
    This endpoint uses the validation service to get accurate coordinates
    with 15 decimal precision for mapping and geocoding purposes.
    """
    start_time = time.time()
    
    try:
        # Log the request
        request_data_dict = {
            "address": request_data.address,
            "property_id": request_data.property_id,
            "country": request_data.country
        }
        
        logger.info(f"🔍 COORDINATES REQUEST: {request_data.address}")
        
        # Initialize address validation service
        address_service = AddressValidationService()
        
        # Get coordinates
        result = await address_service.get_address_coordinates(
            address=request_data.address,
            property_id=request_data.property_id,
            country=request_data.country
        )
        
        response_time = time.time() - start_time
        
        # Log the response
        log_api_call(
            endpoint="/api/address/coordinates",
            method="POST",
            request_data=request_data_dict,
            response_data=result,
            status_code=200 if result.get("success") else 400,
            response_time=response_time
        )
        
        # Log API usage
        await log_api_usage(
            db=db,
            api_provider="geoscape" if request_data.country == "AU" else "unknown",
            endpoint="coordinates",
            request_data=request_data_dict,
            response_status="success" if result.get("success") else "error",
            response_time=response_time,
            request=request,
            error_message=result.get("error")
        )
        
        if result.get("success"):
            logger.info(f"✅ COORDINATES SUCCESS: {request_data.address} -> {result.get('latitude')}, {result.get('longitude')}")
            # Ensure address field is a dictionary or None
            response_data = {
                "success": result.get("success", False),
                "latitude": result.get("latitude"),
                "longitude": result.get("longitude"),
                "address": result.get("address") if isinstance(result.get("address"), dict) else None,
                "property_id": result.get("property_id"),
                "confidence_score": result.get("confidence_score"),
                "error": result.get("error")
            }
            return AddressCoordinatesResponse(**response_data)
        else:
            logger.warning(f"❌ COORDINATES FAILED: {request_data.address} - {result.get('error')}")
            # Ensure address field is a dictionary or None
            response_data = {
                "success": result.get("success", False),
                "latitude": result.get("latitude"),
                "longitude": result.get("longitude"),
                "address": result.get("address") if isinstance(result.get("address"), dict) else None,
                "property_id": result.get("property_id"),
                "confidence_score": result.get("confidence_score"),
                "error": result.get("error")
            }
            return AddressCoordinatesResponse(**response_data)
            
    except Exception as e:
        response_time = time.time() - start_time
        error_msg = f"Failed to get coordinates: {str(e)}"
        
        logger.error(f"❌ COORDINATES ERROR: {error_msg}")
        
        # Log the error
        log_api_call(
            endpoint="/api/address/coordinates",
            method="POST",
            request_data=request_data_dict if 'request_data_dict' in locals() else {},
            response_data={"error": error_msg},
            status_code=503,
            response_time=response_time
        )
        
        # Log API usage error
        await log_api_usage(
            db=db,
            api_provider="geoscape" if request_data.country == "AU" else "unknown",
            endpoint="coordinates",
            request_data=request_data_dict if 'request_data_dict' in locals() else {},
            response_status="error",
            response_time=response_time,
            request=request,
            error_message=error_msg
        )
        
        return AddressCoordinatesResponse(
            success=False,
            address={},
            error=error_msg
        )

async def log_api_usage(
    db: Session,
    api_provider: str,
    endpoint: str,
    request_data: Dict[str, Any],
    response_status: str,
    response_time: float,
    user_id: Optional[int] = None,
    request: Request = None,
    error_message: Optional[str] = None
):
    """
    Log API usage for billing and monitoring purposes.
    
    This function records API calls in the APIUsageTracking table for
    cost tracking, quota management, and performance monitoring.
    """
    try:
        # Create API usage tracking record
        usage_record = APIUsageTracking(
            UserID=user_id,
            APIProvider=api_provider,
            APIEndpoint=endpoint,
            CallCount=1,
            CreditCost=0.001,  # TODO: Calculate actual cost based on provider
            ResponseTime=response_time,
            RequestData=json.dumps(request_data),
            ResponseStatus=response_status,
            ResponseData=json.dumps({"status": response_status}),
            ErrorMessage=error_message,
            BillingPeriod=datetime.now().strftime("%Y-%m"),
            IsBillable=True,
            IPAddress=request.client.host if request else None,
            UserAgent=request.headers.get("user-agent") if request else None
        )
        
        # Add to database session
        db.add(usage_record)
        db.commit()
        
    except Exception as e:
        logger.error(f"Failed to log API usage: {str(e)}")
        # Don't raise exception as this is not critical to the main functionality

async def save_validated_address(
    db: Session,
    address_data: Dict[str, Any],
    user_id: Optional[int] = None,
    profile_id: Optional[int] = None
) -> Optional[int]:
    """
    Save a validated address to the ProfileAddress table.
    
    Args:
        db: Database session
        address_data: Address data from validation
        user_id: User ID (optional)
        profile_id: Profile ID (optional)
    
    Returns:
        ProfileAddressID if successful, None otherwise
    """
    try:
        # Create ProfileAddress record
        profile_address = ProfileAddress(
            ProfileID=profile_id,
            PropertyID=address_data.get("property_id"),
            StreetNumber=address_data.get("street_number"),
            StreetName=address_data.get("street_name"),
            StreetType=address_data.get("street_type"),
            Suburb=address_data.get("suburb"),
            State=address_data.get("state"),
            Postcode=address_data.get("postcode"),
            Country=address_data.get("country"),
            Latitude=address_data.get("latitude"),
            Longitude=address_data.get("longitude"),
            IsValidated=True,
            ValidationSource=address_data.get("validation_source", "geoscape"),
            ConfidenceScore=address_data.get("confidence_score", 0.0),
            ValidationDate=datetime.now(),
            AddressType="primary",  # Default to primary address
            IsActive=True,
            CreatedDate=datetime.now(),
            LastModifiedDate=datetime.now()
        )
        
        # Add to database session
        db.add(profile_address)
        db.commit()
        db.refresh(profile_address)
        
        logger.info(f"Saved validated address with ProfileAddressID: {profile_address.ProfileAddressID}")
        return profile_address.ProfileAddressID
        
    except Exception as e:
        logger.error(f"Failed to save validated address: {str(e)}")
        db.rollback()
        return None

@router.get("/health")
async def health_check():
    """
    Health check endpoint for address validation services.
    
    Returns the status of configured API providers.
    """
    return {
        "status": "healthy",
        "services": {
            "geoscape": {
                "configured": APIConfig.validate_geoscape_config(),
                "base_url": APIConfig.GEOSCAPE_BASE_URL
            },
            "smarty_streets": {
                "configured": APIConfig.validate_smarty_streets_config(),
                "base_url": APIConfig.SMARTY_STREETS_BASE_URL
            }
        },
        "timestamp": datetime.now().isoformat()
    } 