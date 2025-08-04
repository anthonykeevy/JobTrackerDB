import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from mcp.endpoints.routes import router
from app.api.address import router as address_router
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

# Health check endpoint for CI/CD monitoring
@app.get("/health")
async def health_check():
    """Basic health check endpoint for monitoring and CI/CD."""
    return {"status": "healthy", "service": "JobTrackerDB API"}

# Comprehensive health check endpoint
@app.get("/health/detailed")
async def detailed_health_check(db=Depends(get_db)):
    """Detailed health check with database and external service status."""
    return get_health_status(db)

# Readiness check for Kubernetes
@app.get("/ready")
async def readiness_check(db=Depends(get_db)):
    """Readiness check for Kubernetes deployments."""
    if is_healthy(db):
        return {"status": "ready"}
    else:
        return {"status": "not_ready"}, 503

# Liveness check for Kubernetes
@app.get("/live")
async def liveness_check():
    """Liveness check for Kubernetes deployments."""
    return {"status": "alive"}

# Include routers
app.include_router(router)  # MCP endpoints
app.include_router(address_router)  # Address validation endpoints
