#!/usr/bin/env python3
"""
Test Resume Truncation

This script tests the resume truncation function to see what's happening.
"""

import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app'))

try:
    from app.api.resume import truncate_resume_content
except ImportError as e:
    print(f"Error importing required modules: {e}")
    sys.exit(1)

def test_truncation():
    """Test the truncation function"""
    
    try:
        # Read resume content
        resume_file_path = Path("../Resume/Anthony Keevy Resume 202506.docx")
        if not resume_file_path.exists():
            print(f"❌ Resume file not found: {resume_file_path}")
            return False
        
        with open(resume_file_path, 'rb') as f:
            resume_content = f.read()
        
        print(f"✅ Resume file loaded: {len(resume_content)} bytes")
        
        # Extract text from DOCX
        from app.api.resume import extract_text_from_docx
        resume_text = extract_text_from_docx(resume_content)
        
        print(f"✅ Resume text extracted: {len(resume_text)} characters")
        print(f"   First 200 chars: {resume_text[:200]}...")
        
        # Test truncation
        print("\n🔄 Testing truncation...")
        truncated_text = truncate_resume_content(resume_text, max_tokens=8000)  # More aggressive truncation
        
        print(f"✅ Truncation completed:")
        print(f"   Original length: {len(resume_text)} characters")
        print(f"   Truncated length: {len(truncated_text)} characters")
        print(f"   Reduction: {((len(resume_text) - len(truncated_text)) / len(resume_text) * 100):.1f}%")
        
        print(f"\nTruncated text preview:")
        print("=" * 50)
        print(truncated_text[:500] + "..." if len(truncated_text) > 500 else truncated_text)
        print("=" * 50)
        
        # Estimate tokens (rough calculation)
        estimated_tokens = len(truncated_text) / 4
        print(f"\nEstimated tokens: {estimated_tokens:.0f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during truncation test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    print("TEST RESUME TRUNCATION")
    print("=" * 50)
    
    success = test_truncation()
    
    if success:
        print("\n✅ Truncation test completed successfully!")
    else:
        print("\n❌ Truncation test failed")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 