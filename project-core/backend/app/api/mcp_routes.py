"""
MCP (Model Context Protocol) FastAPI Routes
Exposes database operations through REST API endpoints with comprehensive logging.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import logging
from mcp_server import mcp_server

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/mcp",
    tags=["MCP Database Operations"]
)

# Pydantic models for request/response
class QueryRequest(BaseModel):
    query: str
    params: Optional[Dict[str, Any]] = None

class RecordCreateRequest(BaseModel):
    table: str
    data: Dict[str, Any]

class RecordUpdateRequest(BaseModel):
    table: str
    record_id: int
    data: Dict[str, Any]

class RecordDeleteRequest(BaseModel):
    table: str
    record_id: int

class TableInfoRequest(BaseModel):
    table: str

@router.get("/health")
async def mcp_health_check():
    """Check MCP server health and database connectivity"""
    logger.info("🔍 MCP Health Check Requested")
    
    try:
        result = await mcp_server.health_check()
        logger.info(f"✅ MCP Health Check Result: {result}")
        return result
    except Exception as e:
        logger.error(f"❌ MCP Health Check Failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@router.post("/query")
async def execute_query(request: QueryRequest):
    """Execute a custom SQL query"""
    logger.info(f"🔍 MCP Query Request: {request.query}")
    
    try:
        result = await mcp_server.execute_query(request.query, request.params)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        logger.info(f"✅ MCP Query Executed Successfully: {result.get('row_count', 'N/A')} rows")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ MCP Query Failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Query execution failed: {str(e)}")

@router.post("/create")
async def create_record(request: RecordCreateRequest):
    """Create a new record in the specified table"""
    logger.info(f"🔍 MCP Create Record Request: {request.table}")
    
    try:
        result = await mcp_server.create_record(request.table, request.data)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        logger.info(f"✅ MCP Record Created Successfully: ID {result.get('record_id', 'N/A')}")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ MCP Create Record Failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Record creation failed: {str(e)}")

@router.put("/update")
async def update_record(request: RecordUpdateRequest):
    """Update an existing record in the specified table"""
    logger.info(f"🔍 MCP Update Record Request: {request.table} ID {request.record_id}")
    
    try:
        result = await mcp_server.update_record(request.table, request.record_id, request.data)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        logger.info(f"✅ MCP Record Updated Successfully: {result.get('affected_rows', 0)} rows affected")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ MCP Update Record Failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Record update failed: {str(e)}")

@router.delete("/delete")
async def delete_record(request: RecordDeleteRequest):
    """Delete a record from the specified table"""
    logger.info(f"🔍 MCP Delete Record Request: {request.table} ID {request.record_id}")
    
    try:
        result = await mcp_server.delete_record(request.table, request.record_id)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        logger.info(f"✅ MCP Record Deleted Successfully: {result.get('affected_rows', 0)} rows affected")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ MCP Delete Record Failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Record deletion failed: {str(e)}")

@router.get("/tables")
async def list_tables():
    """List all tables in the database"""
    logger.info("🔍 MCP List Tables Request")
    
    try:
        result = await mcp_server.list_tables()
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        logger.info(f"✅ MCP Tables Listed Successfully: {result.get('table_count', 0)} tables found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ MCP List Tables Failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"List tables failed: {str(e)}")

@router.post("/table-info")
async def get_table_info(request: TableInfoRequest):
    """Get detailed information about a table structure"""
    logger.info(f"🔍 MCP Table Info Request: {request.table}")
    
    try:
        result = await mcp_server.get_table_info(request.table)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        logger.info(f"✅ MCP Table Info Retrieved Successfully: {len(result.get('table_info', {}).get('columns', []))} columns")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ MCP Table Info Failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Table info failed: {str(e)}")

@router.get("/capabilities")
async def get_mcp_capabilities():
    """Get MCP server capabilities and available operations"""
    logger.info("🔍 MCP Capabilities Request")
    
    capabilities = {
        "server": "MCP Database Server",
        "version": "1.0.0",
        "capabilities": [
            {
                "name": "health_check",
                "description": "Check database connectivity and server health",
                "endpoint": "GET /api/v1/mcp/health"
            },
            {
                "name": "execute_query",
                "description": "Execute custom SQL queries",
                "endpoint": "POST /api/v1/mcp/query"
            },
            {
                "name": "create_record",
                "description": "Create new records in any table",
                "endpoint": "POST /api/v1/mcp/create"
            },
            {
                "name": "update_record",
                "description": "Update existing records in any table",
                "endpoint": "PUT /api/v1/mcp/update"
            },
            {
                "name": "delete_record",
                "description": "Delete records from any table",
                "endpoint": "DELETE /api/v1/mcp/delete"
            },
            {
                "name": "list_tables",
                "description": "List all tables in the database",
                "endpoint": "GET /api/v1/mcp/tables"
            },
            {
                "name": "get_table_info",
                "description": "Get detailed table structure information",
                "endpoint": "POST /api/v1/mcp/table-info"
            }
        ],
        "features": [
            "Comprehensive logging of all operations",
            "Error handling and detailed error messages",
            "Database connection management",
            "Transaction support",
            "Parameterized query support",
            "Health monitoring"
        ]
    }
    
    logger.info("✅ MCP Capabilities Retrieved Successfully")
    return capabilities 