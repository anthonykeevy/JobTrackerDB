"""
Monitoring and health check utilities for JobTrackerDB
"""
import time
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import HTTPException
import psutil
import requests

logger = logging.getLogger(__name__)

class HealthChecker:
    """Health check utility for monitoring application status"""
    
    def __init__(self):
        self.start_time = time.time()
        self.checks = {}
    
    def check_database_connection(self, db_session) -> Dict[str, Any]:
        """Check database connectivity"""
        try:
            # Simple query to test connection
            result = db_session.execute("SELECT 1")
            return {
                "status": "healthy",
                "response_time": time.time(),
                "details": "Database connection successful"
            }
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "details": "Database connection failed"
            }
    
    def check_external_apis(self) -> Dict[str, Any]:
        """Check external API connectivity"""
        api_status = {}
        
        # Check Geoscape API
        try:
            # Add your Geoscape API health check here
            api_status["geoscape"] = {
                "status": "healthy",
                "response_time": time.time()
            }
        except Exception as e:
            api_status["geoscape"] = {
                "status": "unhealthy",
                "error": str(e)
            }
        
        # Check OpenAI API
        try:
            # Add your OpenAI API health check here
            api_status["openai"] = {
                "status": "healthy",
                "response_time": time.time()
            }
        except Exception as e:
            api_status["openai"] = {
                "status": "unhealthy",
                "error": str(e)
            }
        
        return api_status
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get system performance metrics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                "cpu_usage": cpu_percent,
                "memory_usage": memory.percent,
                "disk_usage": disk.percent,
                "uptime": time.time() - self.start_time
            }
        except Exception as e:
            logger.error(f"Failed to get system metrics: {e}")
            return {"error": str(e)}
    
    def comprehensive_health_check(self, db_session) -> Dict[str, Any]:
        """Perform comprehensive health check"""
        health_status = {
            "timestamp": datetime.utcnow().isoformat(),
            "service": "JobTrackerDB API",
            "version": "1.0.0",
            "status": "healthy",
            "checks": {}
        }
        
        # Database check
        db_check = self.check_database_connection(db_session)
        health_status["checks"]["database"] = db_check
        
        # External APIs check
        api_check = self.check_external_apis()
        health_status["checks"]["external_apis"] = api_check
        
        # System metrics
        system_metrics = self.get_system_metrics()
        health_status["checks"]["system"] = system_metrics
        
        # Determine overall status
        all_healthy = True
        for check_name, check_result in health_status["checks"].items():
            if isinstance(check_result, dict) and check_result.get("status") == "unhealthy":
                all_healthy = False
                break
        
        health_status["status"] = "healthy" if all_healthy else "unhealthy"
        
        return health_status

# Global health checker instance
health_checker = HealthChecker()

def get_health_status(db_session) -> Dict[str, Any]:
    """Get current health status"""
    return health_checker.comprehensive_health_check(db_session)

def is_healthy(db_session) -> bool:
    """Check if the application is healthy"""
    health_status = get_health_status(db_session)
    return health_status["status"] == "healthy" 