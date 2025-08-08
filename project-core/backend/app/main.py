import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from mcp.endpoints.routes import router
from app.api.address import router as address_router
from app.api.resume import router as resume_router
from app.api.mcp_routes import router as mcp_router
from app.api.prompt_routes import router as prompt_router
from app.monitoring import get_health_status, is_healthy
from mcp.db.session import get_db

app = FastAPI(
    title="JobTrackerDB API",
    description="Comprehensive job tracking and career management platform API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:5174", "http://127.0.0.1:5174"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router)  # MCP endpoints (users, auth)
app.include_router(address_router)  # Address endpoints
app.include_router(resume_router)  # Resume parsing endpoints
app.include_router(mcp_router)  # MCP database operations
app.include_router(prompt_router)  # Prompt management endpoints

@app.get("/health")
async def health_check(db=Depends(get_db)):
    """Health check endpoint"""
    return get_health_status(db)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "JobTrackerDB API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "users": "/api/v1/users",
            "auth": "/api/v1/auth/login",
            "mcp": "/api/v1/mcp/capabilities",
            "resume": "/api/v1/resume/parse"
        }
    }
