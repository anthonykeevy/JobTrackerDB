#!/usr/bin/env python3
"""
MCP (Model Context Protocol) Server Implementation
Provides database connectivity and operations with comprehensive logging.
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import hashlib
import secrets

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp_server.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class MCPServer:
    """MCP Server for database operations and connectivity"""
    
    def __init__(self):
        """Initialize MCP Server with database connection"""
        self.database_url = os.getenv("DATABASE_URL")
        if not self.database_url:
            logger.error("❌ DATABASE_URL not found in environment variables")
            raise ValueError("DATABASE_URL not configured")
        
        self.engine = create_engine(self.database_url, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        logger.info("🚀 MCP Server initialized")
        logger.info(f"📊 Database URL: {self.database_url}")
        
    def get_db_session(self):
        """Get database session"""
        return self.SessionLocal()
    
    def log_operation(self, operation: str, details: Dict[str, Any], success: bool = True):
        """Log MCP operations with details"""
        timestamp = datetime.utcnow().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "operation": operation,
            "success": success,
            "details": details
        }
        
        if success:
            logger.info(f"✅ MCP Operation: {operation} - {json.dumps(details, default=str)}")
        else:
            logger.error(f"❌ MCP Operation Failed: {operation} - {json.dumps(details, default=str)}")
        
        return log_entry
    
    async def execute_query(self, query: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Execute a SQL query and return results"""
        operation = "execute_query"
        details = {"query": query, "params": params}
        
        try:
            with self.get_db_session() as session:
                result = session.execute(text(query), params or {})
                
                if query.strip().upper().startswith('SELECT'):
                    # For SELECT queries, fetch results
                    rows = result.fetchall()
                    columns = result.keys()
                    data = [dict(zip(columns, row)) for row in rows]
                    
                    response = {
                        "success": True,
                        "data": data,
                        "row_count": len(data)
                    }
                else:
                    # For INSERT/UPDATE/DELETE queries
                    session.commit()
                    response = {
                        "success": True,
                        "affected_rows": result.rowcount
                    }
                
                self.log_operation(operation, details, True)
                return response
                
        except SQLAlchemyError as e:
            error_details = {"error": str(e), "error_type": type(e).__name__}
            self.log_operation(operation, {**details, **error_details}, False)
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def create_record(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new record in the specified table"""
        operation = "create_record"
        details = {"table": table, "data": data}
        
        try:
            # Build INSERT query
            columns = list(data.keys())
            values = list(data.values())
            placeholders = [f":{col}" for col in columns]
            
            query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
            
            with self.get_db_session() as session:
                result = session.execute(text(query), data)
                session.commit()
                
                # Get the inserted record ID (assuming auto-increment)
                if result.inserted_primary_key:
                    record_id = result.inserted_primary_key[0]
                else:
                    # Fallback: query for the latest record
                    result = session.execute(text(f"SELECT TOP 1 * FROM {table} ORDER BY 1 DESC"))
                    record = result.fetchone()
                    record_id = record[0] if record else None
                
                response = {
                    "success": True,
                    "record_id": record_id,
                    "table": table
                }
                
                self.log_operation(operation, details, True)
                return response
                
        except SQLAlchemyError as e:
            error_details = {"error": str(e), "error_type": type(e).__name__}
            self.log_operation(operation, {**details, **error_details}, False)
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def update_record(self, table: str, record_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a record in the specified table"""
        operation = "update_record"
        details = {"table": table, "record_id": record_id, "data": data}
        
        try:
            # Build UPDATE query
            set_clause = ", ".join([f"{col} = :{col}" for col in data.keys()])
            query = f"UPDATE {table} SET {set_clause} WHERE 1=1"
            
            # Add primary key condition (assuming first column is primary key)
            with self.get_db_session() as session:
                # Get table structure to find primary key
                result = session.execute(text(f"SELECT TOP 1 * FROM {table}"))
                columns = result.keys()
                primary_key = columns[0]  # Assume first column is primary key
                
                query += f" AND {primary_key} = :record_id"
                data["record_id"] = record_id
                
                result = session.execute(text(query), data)
                session.commit()
                
                response = {
                    "success": True,
                    "affected_rows": result.rowcount,
                    "table": table,
                    "record_id": record_id
                }
                
                self.log_operation(operation, details, True)
                return response
                
        except SQLAlchemyError as e:
            error_details = {"error": str(e), "error_type": type(e).__name__}
            self.log_operation(operation, {**details, **error_details}, False)
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def delete_record(self, table: str, record_id: int) -> Dict[str, Any]:
        """Delete a record from the specified table"""
        operation = "delete_record"
        details = {"table": table, "record_id": record_id}
        
        try:
            with self.get_db_session() as session:
                # Get table structure to find primary key
                result = session.execute(text(f"SELECT TOP 1 * FROM {table}"))
                columns = result.keys()
                primary_key = columns[0]  # Assume first column is primary key
                
                query = f"DELETE FROM {table} WHERE {primary_key} = :record_id"
                result = session.execute(text(query), {"record_id": record_id})
                session.commit()
                
                response = {
                    "success": True,
                    "affected_rows": result.rowcount,
                    "table": table,
                    "record_id": record_id
                }
                
                self.log_operation(operation, details, True)
                return response
                
        except SQLAlchemyError as e:
            error_details = {"error": str(e), "error_type": type(e).__name__}
            self.log_operation(operation, {**details, **error_details}, False)
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def get_table_info(self, table: str) -> Dict[str, Any]:
        """Get information about a table structure"""
        operation = "get_table_info"
        details = {"table": table}
        
        try:
            query = """
                SELECT 
                    COLUMN_NAME,
                    DATA_TYPE,
                    IS_NULLABLE,
                    COLUMN_DEFAULT,
                    CHARACTER_MAXIMUM_LENGTH
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = :table_name
                ORDER BY ORDINAL_POSITION
            """
            
            with self.get_db_session() as session:
                result = session.execute(text(query), {"table_name": table})
                columns = result.fetchall()
                
                table_info = {
                    "table_name": table,
                    "columns": [
                        {
                            "name": col[0],
                            "type": col[1],
                            "nullable": col[2] == "YES",
                            "default": col[3],
                            "max_length": col[4]
                        }
                        for col in columns
                    ]
                }
                
                response = {
                    "success": True,
                    "table_info": table_info
                }
                
                self.log_operation(operation, details, True)
                return response
                
        except SQLAlchemyError as e:
            error_details = {"error": str(e), "error_type": type(e).__name__}
            self.log_operation(operation, {**details, **error_details}, False)
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def list_tables(self) -> Dict[str, Any]:
        """List all tables in the database"""
        operation = "list_tables"
        details = {}
        
        try:
            query = """
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_TYPE = 'BASE TABLE'
                ORDER BY TABLE_NAME
            """
            
            with self.get_db_session() as session:
                result = session.execute(text(query))
                tables = [row[0] for row in result.fetchall()]
                
                response = {
                    "success": True,
                    "tables": tables,
                    "table_count": len(tables)
                }
                
                self.log_operation(operation, details, True)
                return response
                
        except SQLAlchemyError as e:
            error_details = {"error": str(e), "error_type": type(e).__name__}
            self.log_operation(operation, {**details, **error_details}, False)
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def health_check(self) -> Dict[str, Any]:
        """Check database connectivity and health"""
        operation = "health_check"
        details = {}
        
        try:
            with self.get_db_session() as session:
                result = session.execute(text("SELECT 1 as health_check"))
                health_result = result.fetchone()
                
                if health_result and health_result[0] == 1:
                    response = {
                        "success": True,
                        "status": "healthy",
                        "database": "connected",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                else:
                    response = {
                        "success": False,
                        "status": "unhealthy",
                        "error": "Health check failed"
                    }
                
                self.log_operation(operation, details, response["success"])
                return response
                
        except SQLAlchemyError as e:
            error_details = {"error": str(e), "error_type": type(e).__name__}
            self.log_operation(operation, {**details, **error_details}, False)
            return {
                "success": False,
                "status": "unhealthy",
                "error": str(e),
                "error_type": type(e).__name__
            }

# Global MCP Server instance
mcp_server = MCPServer()

# Export the server instance for use in other modules
__all__ = ['mcp_server', 'MCPServer'] 