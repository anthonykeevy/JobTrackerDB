#!/usr/bin/env python3
"""
Initialize Resume Parsing Prompt Management System

This script initializes the resume parsing prompt management system by:
1. Creating the PromptManagement table
2. Initializing default resume parsing prompt
3. Setting up the prompt management infrastructure
"""

import sys
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models import Base, PromptManagement
from app.services.prompt_service import PromptService
from mcp.db.session import get_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_prompt_management():
    """Initialize the prompt management system"""
    try:
        logger.info("🚀 Initializing Prompt Management System...")
        
        # Get database session
        db = next(get_db())
        
        # Create PromptManagement table
        logger.info("📋 Creating PromptManagement table...")
        engine = create_engine(os.getenv("DATABASE_URL"))
        Base.metadata.create_all(engine, tables=[PromptManagement.__table__])
        logger.info("✅ PromptManagement table created successfully")
        
        # Initialize default prompts
        logger.info("📝 Initializing default prompts...")
        prompt_service = PromptService(db)
        success = prompt_service.initialize_default_prompts()
        
        if success:
            logger.info("✅ Default prompts initialized successfully")
            
            # Display initialized prompts
            prompts = db.query(PromptManagement).all()
            logger.info(f"📊 Total prompts in database: {len(prompts)}")
            
            for prompt in prompts:
                logger.info(f"  - {prompt.PromptName} (v{prompt.PromptVersion}) - {prompt.PromptType}")
                logger.info(f"    Status: {'Active' if prompt.IsActive else 'Inactive'}, Default: {'Yes' if prompt.IsDefault else 'No'}")
        else:
            logger.error("❌ Failed to initialize default prompts")
            return False
        
        logger.info("🎉 Prompt Management System initialization completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error initializing prompt management system: {e}")
        return False
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    success = initialize_prompt_management()
    sys.exit(0 if success else 1) 