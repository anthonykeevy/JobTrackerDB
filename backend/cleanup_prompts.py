#!/usr/bin/env python3
"""
Cleanup Prompt Management System

This script cleans up the prompt management system by:
1. Removing the address validation prompt (not needed since we use Geoscape API)
2. Keeping only the resume parsing prompt
"""

import sys
import os
import logging

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp.db.session import get_db
from app.models import PromptManagement

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def cleanup_prompts():
    """Clean up the prompt management system"""
    try:
        logger.info("🧹 Cleaning up Prompt Management System...")
        
        # Get database session
        db = next(get_db())
        
        # Remove address validation prompts
        logger.info("🗑️ Removing address validation prompts...")
        address_prompts = db.query(PromptManagement).filter(
            PromptManagement.PromptType == 'address_validation'
        ).all()
        
        for prompt in address_prompts:
            logger.info(f"   Removing: {prompt.PromptName} (v{prompt.PromptVersion})")
            db.delete(prompt)
        
        db.commit()
        logger.info(f"✅ Removed {len(address_prompts)} address validation prompts")
        
        # Show remaining prompts
        remaining_prompts = db.query(PromptManagement).all()
        logger.info(f"📊 Remaining prompts in database: {len(remaining_prompts)}")
        
        for prompt in remaining_prompts:
            logger.info(f"   - {prompt.PromptName} (v{prompt.PromptVersion}) - {prompt.PromptType}")
            logger.info(f"     Status: {'Active' if prompt.IsActive else 'Inactive'}, Default: {'Yes' if prompt.IsDefault else 'No'}")
        
        logger.info("🎉 Prompt cleanup completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error cleaning up prompts: {e}")
        return False
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    success = cleanup_prompts()
    sys.exit(0 if success else 1) 