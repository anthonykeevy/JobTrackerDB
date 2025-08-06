#!/usr/bin/env python3
"""
Check Prompts

Simple script to check the current state of prompts in the database.
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp.db.session import get_db
from app.models import PromptManagement

def main():
    """Check prompts"""
    try:
        db = next(get_db())
        
        # Check all prompts
        prompts = db.query(PromptManagement).all()
        print(f"Total prompts: {len(prompts)}")
        
        for prompt in prompts:
            print(f"- {prompt.PromptName} v{prompt.PromptVersion} (Active: {prompt.IsActive})")
        
        # Check active prompt
        active = db.query(PromptManagement).filter(PromptManagement.IsActive == True).first()
        if active:
            print(f"\n✅ Active prompt: {active.PromptName} v{active.PromptVersion}")
        else:
            print("\n❌ No active prompt found")
            
            # Try to activate the first prompt
            first_prompt = db.query(PromptManagement).first()
            if first_prompt:
                first_prompt.IsActive = True
                db.commit()
                print(f"✅ Activated: {first_prompt.PromptName} v{first_prompt.PromptVersion}")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 