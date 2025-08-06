#!/usr/bin/env python3
"""
JobTrackerDB Project File Organization Script

This script scans the entire project structure and organizes all test files
into a comprehensive testing framework. It runs from the project root and
creates the complete organized structure.

Features:
- Scans entire project for test files
- Creates organized directory structure
- Moves files to appropriate locations
- Provides detailed logging and verification
- Includes test mode for safety
"""

import os
import shutil
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('file_organization.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ProjectFileOrganizer:
    """Organizes project files into a comprehensive testing structure"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.test_root = self.project_root / "tests"
        
        # Define the target directory structure
        self.target_structure = {
            "tests/backend/ai/baseline": [],
            "tests/backend/ai/performance": [],
            "tests/backend/ai/prompts": [],
            "tests/backend/api": [],
            "tests/backend/database": [],
            "tests/backend/integration": [],
            "tests/frontend/components": [],
            "tests/frontend/pages": [],
            "tests/frontend/integration": [],
            "tests/general/performance": [],
            "tests/general/security": [],
            "tests/general/e2e": [],
            "tests/data/resumes": [],
            "tests/data/baseline": [],
            "tests/data/exports": []
        }
        
        # Define file mappings (source -> target)
        self.file_mappings = {
            # AI/Resume Parsing Tests
            "backend/test_resume_parser_performance.py": "tests/backend/ai/performance/",
            "backend/test_prompt_management.py": "tests/backend/ai/prompts/",
            "backend/compare_prompt_versions.py": "tests/backend/ai/prompts/",
            "backend/improve_resume_prompt.py": "tests/backend/ai/prompts/",
            "backend/activate_prompt.py": "tests/backend/ai/prompts/",
            "backend/check_prompts.py": "tests/backend/ai/prompts/",
            "backend/cleanup_prompts.py": "tests/backend/ai/prompts/",
            "backend/initialize_prompts.py": "tests/backend/ai/prompts/",
            
            # API Tests
            "test_resume_upload.py": "tests/backend/api/",
            "backend/test_resume_upload.py": "tests/backend/api/",
            "backend/test_address_api.py": "tests/backend/api/",
            "backend/test_geoscape_api.py": "tests/backend/api/",
            "backend/test_geoscape_api_v2.py": "tests/backend/api/",
            "backend/test_geoscape_raw_response.py": "tests/backend/api/",
            "test_coordinates.py": "tests/backend/api/",
            "backend/test_coordinates.py": "tests/backend/api/",
            
            # Database Tests
            "check_resume_data_saved.py": "tests/backend/database/",
            "backend/check_resume_data_saved.py": "tests/backend/database/",
            "backend/check_resume_data.py": "tests/backend/database/",
            "backend/schema_comparison.py": "tests/backend/database/",
            "backend/create_smart_migration.py": "tests/backend/database/",
            "backend/safe_migration_template.py": "tests/backend/database/",
            "backend/setup_database.py": "tests/backend/database/",
            "backend/reset_password.py": "tests/backend/database/",
            
            # Integration Tests
            "backend/mcp_server.py": "tests/backend/integration/",
            
            # Performance Tests
            "backend/test_results_test_20250805_192953.json": "tests/general/performance/",
            "backend/test_results_test_20250805_192752.json": "tests/general/performance/",
            "backend/test_results_test_20250805_185426.json": "tests/general/performance/",
            "backend/test_results_test_20250805_185104.json": "tests/general/performance/",
            "backend/test_results_test_20250805_185009.json": "tests/general/performance/",
            
            # Data/Exports
            "backend/JobTrackerDB_API.postman_collection.json": "tests/data/exports/",
            "backend/JobTrackerDB_API.postman_environment.json": "tests/data/exports/",
            "backend/README_Postman_Testing.md": "tests/data/exports/",
            
            # SQL Files
            "query_prompt_benefits.sql": "tests/data/exports/",
            "profile_tables_queries.sql": "tests/data/exports/",
            
            # Documentation
            "RESUME_PARSER_TESTING_FRAMEWORK.md": "tests/data/exports/",
        }
        
        # Files to exclude from moving
        self.exclude_files = {
            "organize_project_files.py",
            "organize_test_files.ps1",
            ".gitignore",
            "README.md",
            "package.json",
            "package-lock.json",
            "requirements.txt",
            "requirements-test.txt",
            "env.example",
            "alembic.ini",
            "alembic_production.ini",
            "alembic_staging.ini",
            "__init__.py",
            "mcp_server.log"
        }
        
        # Track moved files for verification
        self.moved_files = []
        self.failed_moves = []
        
    def scan_project_structure(self) -> Dict[str, List[str]]:
        """Scan the entire project and find all files"""
        logger.info("Scanning project structure...")
        
        project_files = {}
        
        for root, dirs, files in os.walk(self.project_root):
            # Skip certain directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'venv', '__pycache__', '.git']]
            
            for file in files:
                if file not in self.exclude_files:
                    rel_path = os.path.relpath(os.path.join(root, file), self.project_root)
                    project_files[rel_path] = os.path.join(root, file)
        
        logger.info(f"Found {len(project_files)} files in project")
        return project_files
    
    def create_directory_structure(self) -> bool:
        """Create the target directory structure"""
        logger.info("Creating directory structure...")
        
        try:
            for target_dir in self.target_structure.keys():
                full_path = self.project_root / target_dir
                full_path.mkdir(parents=True, exist_ok=True)
                logger.info(f"  Created: {target_dir}")
            
            return True
        except Exception as e:
            logger.error(f"Error creating directory structure: {e}")
            return False
    
    def find_files_to_move(self, project_files: Dict[str, str]) -> List[Tuple[str, str, str]]:
        """Find files that need to be moved"""
        moves = []
        
        for source_path, target_dir in self.file_mappings.items():
            if source_path in project_files:
                source_file = project_files[source_path]
                target_file = self.project_root / target_dir / Path(source_path).name
                
                # Only move if source exists and target doesn't exist or is different
                if os.path.exists(source_file):
                    if not os.path.exists(target_file) or os.path.getmtime(source_file) > os.path.getmtime(target_file):
                        moves.append((source_file, str(target_file), target_dir))
                    else:
                        logger.info(f"  Skipping {source_path} - target exists and is newer")
                else:
                    logger.warning(f"  Source file not found: {source_path}")
        
        return moves
    
    def test_move_operation(self, source: str, target: str) -> bool:
        """Test a move operation without actually moving"""
        try:
            if not os.path.exists(source):
                logger.error(f"Test failed: Source file does not exist: {source}")
                return False
            
            target_dir = os.path.dirname(target)
            if not os.path.exists(target_dir):
                logger.error(f"Test failed: Target directory does not exist: {target_dir}")
                return False
            
            logger.info(f"Test passed: {source} -> {target}")
            return True
            
        except Exception as e:
            logger.error(f"Test failed: {e}")
            return False
    
    def move_file(self, source: str, target: str, target_dir: str, test_mode: bool = False) -> bool:
        """Move a file from source to target"""
        try:
            if test_mode:
                return self.test_move_operation(source, target)
            
            # Create backup of target if it exists
            if os.path.exists(target):
                backup_path = f"{target}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                shutil.copy2(target, backup_path)
                logger.info(f"  Created backup: {backup_path}")
            
            # Move the file
            shutil.move(source, target)
            self.moved_files.append((source, target, target_dir))
            logger.info(f"  Moved: {os.path.basename(source)} -> {target_dir}")
            return True
            
        except Exception as e:
            self.failed_moves.append((source, target, str(e)))
            logger.error(f"  Failed to move {source}: {e}")
            return False
    
    def verify_moves(self) -> Dict[str, int]:
        """Verify that all moves were successful"""
        logger.info("Verifying file moves...")
        
        verification_results = {}
        
        for source, target, target_dir in self.moved_files:
            if os.path.exists(target):
                verification_results[target_dir] = verification_results.get(target_dir, 0) + 1
                logger.info(f"  Verified: {os.path.basename(target)} in {target_dir}")
            else:
                logger.error(f"  Verification failed: {target} not found")
        
        return verification_results
    
    def generate_summary(self, verification_results: Dict[str, int]):
        """Generate a summary of the organization"""
        logger.info("\nORGANIZATION SUMMARY")
        logger.info("=" * 50)
        
        total_moved = len(self.moved_files)
        total_failed = len(self.failed_moves)
        
        logger.info(f"Total files moved: {total_moved}")
        logger.info(f"Total failed moves: {total_failed}")
        
        if verification_results:
            logger.info("\nFiles by category:")
            for category, count in verification_results.items():
                logger.info(f"  {category}: {count} files")
        
        if self.failed_moves:
            logger.info("\nFailed moves:")
            for source, target, error in self.failed_moves:
                logger.info(f"  {source}: {error}")
        
        logger.info("\nFile organization completed!")
    
    def run_organization(self, test_mode: bool = True) -> bool:
        """Run the complete file organization process"""
        logger.info("Starting JobTrackerDB Project File Organization")
        logger.info("=" * 60)
        
        if test_mode:
            logger.info("RUNNING IN TEST MODE - No files will be moved")
        else:
            logger.info("RUNNING IN EXECUTION MODE - Files will be moved")
        
        # Step 1: Scan project structure
        project_files = self.scan_project_structure()
        
        # Step 2: Create directory structure
        if not self.create_directory_structure():
            return False
        
        # Step 3: Find files to move
        moves = self.find_files_to_move(project_files)
        logger.info(f"Found {len(moves)} files to move")
        
        if not moves:
            logger.info("No files need to be moved")
            return True
        
        # Step 4: Test or execute moves
        successful_moves = 0
        for source, target, target_dir in moves:
            if self.move_file(source, target, target_dir, test_mode):
                successful_moves += 1
        
        # Step 5: Verify moves (only in execution mode)
        if not test_mode and successful_moves > 0:
            verification_results = self.verify_moves()
            self.generate_summary(verification_results)
        
        # Step 6: Generate test summary
        if test_mode:
            logger.info(f"\nTEST SUMMARY:")
            logger.info(f"  Files that would be moved: {len(moves)}")
            logger.info(f"  Successful test moves: {successful_moves}")
            logger.info(f"  Failed test moves: {len(moves) - successful_moves}")
            
            if successful_moves == len(moves):
                logger.info("All test moves passed! Ready for execution.")
                return True
            else:
                logger.error("Some test moves failed. Please review before execution.")
                return False
        
        return successful_moves == len(moves)

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Organize JobTrackerDB project files")
    parser.add_argument("--execute", action="store_true", help="Execute the moves (default is test mode)")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    
    args = parser.parse_args()
    
    organizer = ProjectFileOrganizer(args.project_root)
    success = organizer.run_organization(test_mode=not args.execute)
    
    if success:
        if args.execute:
            logger.info("File organization completed successfully!")
        else:
            logger.info("Test completed successfully! Run with --execute to perform the moves.")
    else:
        logger.error("File organization failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 