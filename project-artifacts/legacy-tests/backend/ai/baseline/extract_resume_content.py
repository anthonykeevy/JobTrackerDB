#!/usr/bin/env python3
"""
Extract Resume Content

This script extracts the text content from the actual resume file
so we can see what data we're working with for testing.
"""

import sys
import os
from pathlib import Path
from docx import Document

def extract_resume_content():
    """Extract text content from the resume file"""
    resume_file_path = Path("../Resume/Anthony Keevy Resume 202506.docx")
    
    if not resume_file_path.exists():
        print(f"Error: Resume file not found at {resume_file_path}")
        return None
    
    try:
        doc = Document(resume_file_path)
        content = []
        
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                content.append(paragraph.text)
        
        resume_text = '\n'.join(content)
        
        print("RESUME CONTENT EXTRACTED SUCCESSFULLY")
        print("=" * 50)
        print(f"File: {resume_file_path}")
        print(f"Content length: {len(resume_text)} characters")
        print(f"Lines: {len(content)}")
        print("\nRESUME CONTENT:")
        print("=" * 50)
        print(resume_text)
        print("=" * 50)
        
        # Save to file
        output_file = Path("resume_content.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(resume_text)
        
        print(f"\nContent saved to: {output_file}")
        return resume_text
        
    except Exception as e:
        print(f"Error extracting resume content: {e}")
        return None

def main():
    """Main function"""
    print("RESUME CONTENT EXTRACTOR")
    print("=" * 50)
    
    content = extract_resume_content()
    
    if content:
        print("\nExtraction completed successfully!")
        return True
    else:
        print("\nExtraction failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 