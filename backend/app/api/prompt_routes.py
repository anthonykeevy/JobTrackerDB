"""
Prompt Management API Routes

This module provides API endpoints for managing AI prompts including:
- CRUD operations for prompts
- Prompt versioning
- Performance tracking
- Admin interface endpoints
"""

import logging
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from mcp.db.session import get_db
from app.services.prompt_service import PromptService
from app.models import PromptManagement

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/prompts",
    tags=["Prompt Management"]
)

# Pydantic models for request/response
class PromptCreateRequest(BaseModel):
    PromptName: str
    PromptType: str
    PromptVersion: str = "1.0"
    SystemPrompt: str
    UserPrompt: str
    Description: Optional[str] = None
    ExpectedOutput: Optional[str] = None
    ValidationRules: Optional[str] = None
    IsActive: bool = True
    IsDefault: bool = False
    PerformanceMetrics: Optional[str] = None

class PromptUpdateRequest(BaseModel):
    PromptName: Optional[str] = None
    SystemPrompt: Optional[str] = None
    UserPrompt: Optional[str] = None
    Description: Optional[str] = None
    ExpectedOutput: Optional[str] = None
    ValidationRules: Optional[str] = None
    IsActive: Optional[bool] = None
    IsDefault: Optional[bool] = None
    PerformanceMetrics: Optional[str] = None

class PromptResponse(BaseModel):
    PromptID: int
    PromptName: str
    PromptType: str
    PromptVersion: str
    SystemPrompt: str
    UserPrompt: str
    Description: Optional[str]
    ExpectedOutput: Optional[str]
    ValidationRules: Optional[str]
    IsActive: bool
    IsDefault: bool
    PerformanceMetrics: Optional[str]
    createdDate: str
    createdBy: Optional[str]
    lastUpdated: Optional[str]
    updatedBy: Optional[str]

@router.get("/", response_model=List[PromptResponse])
async def get_all_prompts(
    prompt_type: Optional[str] = Query(None, description="Filter by prompt type"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db)
):
    """Get all prompts with optional filtering"""
    try:
        prompt_service = PromptService(db)
        
        if prompt_type:
            prompts = prompt_service.get_prompt_history(prompt_type)
        else:
            prompts = db.query(PromptManagement).all()
        
        if is_active is not None:
            prompts = [p for p in prompts if p.IsActive == is_active]
        
        return [
            PromptResponse(
                PromptID=p.PromptID,
                PromptName=p.PromptName,
                PromptType=p.PromptType,
                PromptVersion=p.PromptVersion,
                SystemPrompt=p.SystemPrompt,
                UserPrompt=p.UserPrompt,
                Description=p.Description,
                ExpectedOutput=p.ExpectedOutput,
                ValidationRules=p.ValidationRules,
                IsActive=p.IsActive,
                IsDefault=p.IsDefault,
                PerformanceMetrics=p.PerformanceMetrics,
                createdDate=p.createdDate.isoformat() if p.createdDate else None,
                createdBy=p.createdBy,
                lastUpdated=p.lastUpdated.isoformat() if p.lastUpdated else None,
                updatedBy=p.updatedBy
            )
            for p in prompts
        ]
    except Exception as e:
        logger.error(f"Error getting prompts: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get prompts: {str(e)}")

@router.get("/types")
async def get_prompt_types(db: Session = Depends(get_db)):
    """Get all available prompt types"""
    try:
        types = db.query(PromptManagement.PromptType).distinct().all()
        return {"prompt_types": [t[0] for t in types]}
    except Exception as e:
        logger.error(f"Error getting prompt types: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get prompt types: {str(e)}")

@router.get("/{prompt_id}", response_model=PromptResponse)
async def get_prompt_by_id(prompt_id: int, db: Session = Depends(get_db)):
    """Get a specific prompt by ID"""
    try:
        prompt = db.query(PromptManagement).filter(PromptManagement.PromptID == prompt_id).first()
        if not prompt:
            raise HTTPException(status_code=404, detail="Prompt not found")
        
        return PromptResponse(
            PromptID=prompt.PromptID,
            PromptName=prompt.PromptName,
            PromptType=prompt.PromptType,
            PromptVersion=prompt.PromptVersion,
            SystemPrompt=prompt.SystemPrompt,
            UserPrompt=prompt.UserPrompt,
            Description=prompt.Description,
            ExpectedOutput=prompt.ExpectedOutput,
            ValidationRules=prompt.ValidationRules,
            IsActive=prompt.IsActive,
            IsDefault=prompt.IsDefault,
            PerformanceMetrics=prompt.PerformanceMetrics,
            createdDate=prompt.createdDate.isoformat() if prompt.createdDate else None,
            createdBy=prompt.createdBy,
            lastUpdated=prompt.lastUpdated.isoformat() if prompt.lastUpdated else None,
            updatedBy=prompt.updatedBy
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting prompt {prompt_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get prompt: {str(e)}")

@router.post("/", response_model=PromptResponse)
async def create_prompt(
    request: PromptCreateRequest,
    db: Session = Depends(get_db)
):
    """Create a new prompt"""
    try:
        prompt_service = PromptService(db)
        
        # Check if prompt with same name already exists
        existing = db.query(PromptManagement).filter(
            PromptManagement.PromptName == request.PromptName
        ).first()
        
        if existing:
            raise HTTPException(status_code=400, detail="Prompt with this name already exists")
        
        prompt_data = request.dict()
        prompt_data["createdBy"] = "admin"  # TODO: Get from authentication
        
        prompt = prompt_service.create_prompt(prompt_data)
        if not prompt:
            raise HTTPException(status_code=500, detail="Failed to create prompt")
        
        return PromptResponse(
            PromptID=prompt.PromptID,
            PromptName=prompt.PromptName,
            PromptType=prompt.PromptType,
            PromptVersion=prompt.PromptVersion,
            SystemPrompt=prompt.SystemPrompt,
            UserPrompt=prompt.UserPrompt,
            Description=prompt.Description,
            ExpectedOutput=prompt.ExpectedOutput,
            ValidationRules=prompt.ValidationRules,
            IsActive=prompt.IsActive,
            IsDefault=prompt.IsDefault,
            PerformanceMetrics=prompt.PerformanceMetrics,
            createdDate=prompt.createdDate.isoformat() if prompt.createdDate else None,
            createdBy=prompt.createdBy,
            lastUpdated=prompt.lastUpdated.isoformat() if prompt.lastUpdated else None,
            updatedBy=prompt.updatedBy
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating prompt: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create prompt: {str(e)}")

@router.put("/{prompt_id}", response_model=PromptResponse)
async def update_prompt(
    prompt_id: int,
    request: PromptUpdateRequest,
    db: Session = Depends(get_db)
):
    """Update an existing prompt"""
    try:
        prompt_service = PromptService(db)
        
        updates = request.dict(exclude_unset=True)
        updates["updatedBy"] = "admin"  # TODO: Get from authentication
        
        prompt = prompt_service.update_prompt(prompt_id, updates)
        if not prompt:
            raise HTTPException(status_code=404, detail="Prompt not found")
        
        return PromptResponse(
            PromptID=prompt.PromptID,
            PromptName=prompt.PromptName,
            PromptType=prompt.PromptType,
            PromptVersion=prompt.PromptVersion,
            SystemPrompt=prompt.SystemPrompt,
            UserPrompt=prompt.UserPrompt,
            Description=prompt.Description,
            ExpectedOutput=prompt.ExpectedOutput,
            ValidationRules=prompt.ValidationRules,
            IsActive=prompt.IsActive,
            IsDefault=prompt.IsDefault,
            PerformanceMetrics=prompt.PerformanceMetrics,
            createdDate=prompt.createdDate.isoformat() if prompt.createdDate else None,
            createdBy=prompt.createdBy,
            lastUpdated=prompt.lastUpdated.isoformat() if prompt.lastUpdated else None,
            updatedBy=prompt.updatedBy
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating prompt {prompt_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update prompt: {str(e)}")

@router.delete("/{prompt_id}")
async def delete_prompt(prompt_id: int, db: Session = Depends(get_db)):
    """Delete a prompt (soft delete by setting IsActive to False)"""
    try:
        prompt = db.query(PromptManagement).filter(PromptManagement.PromptID == prompt_id).first()
        if not prompt:
            raise HTTPException(status_code=404, detail="Prompt not found")
        
        prompt.IsActive = False
        prompt.updatedBy = "admin"  # TODO: Get from authentication
        db.commit()
        
        return {"message": "Prompt deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting prompt {prompt_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete prompt: {str(e)}")

@router.post("/initialize")
async def initialize_default_prompts(db: Session = Depends(get_db)):
    """Initialize default prompts for the system"""
    try:
        prompt_service = PromptService(db)
        success = prompt_service.initialize_default_prompts()
        
        if success:
            return {"message": "Default prompts initialized successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to initialize default prompts")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error initializing default prompts: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to initialize default prompts: {str(e)}")

@router.get("/active/{prompt_type}")
async def get_active_prompt(prompt_type: str, db: Session = Depends(get_db)):
    """Get the active prompt for a specific type"""
    try:
        prompt_service = PromptService(db)
        prompt = prompt_service.get_active_prompt(prompt_type)
        
        if not prompt:
            raise HTTPException(status_code=404, detail=f"No active prompt found for type: {prompt_type}")
        
        return PromptResponse(
            PromptID=prompt.PromptID,
            PromptName=prompt.PromptName,
            PromptType=prompt.PromptType,
            PromptVersion=prompt.PromptVersion,
            SystemPrompt=prompt.SystemPrompt,
            UserPrompt=prompt.UserPrompt,
            Description=prompt.Description,
            ExpectedOutput=prompt.ExpectedOutput,
            ValidationRules=prompt.ValidationRules,
            IsActive=prompt.IsActive,
            IsDefault=prompt.IsDefault,
            PerformanceMetrics=prompt.PerformanceMetrics,
            createdDate=prompt.createdDate.isoformat() if prompt.createdDate else None,
            createdBy=prompt.createdBy,
            lastUpdated=prompt.lastUpdated.isoformat() if prompt.lastUpdated else None,
            updatedBy=prompt.updatedBy
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting active prompt for type {prompt_type}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get active prompt: {str(e)}") 