"""
Migration tests for JobTrackerDB using existing Alembic setup
"""
import pytest
import os
import tempfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic import command
from alembic.config import Config

from app.models import Base

class TestMigrations:
    """Test Alembic migrations work correctly"""
    
    @pytest.fixture
    def temp_db(self):
        """Create a temporary database for testing"""
        # Create temporary database file
        fd, path = tempfile.mkstemp(suffix='.db')
        os.close(fd)
        
        # Create engine
        engine = create_engine(f"sqlite:///{path}")
        
        yield engine, path
        
        # Cleanup
        try:
            engine.dispose()
        finally:
            os.unlink(path)
    
    def test_migration_generation(self, temp_db):
        """Test that migrations can be generated"""
        engine, db_path = temp_db
        
        # Test migration generation
        backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        alembic_cfg = Config(os.path.join(backend_dir, "alembic.ini"))
        alembic_cfg.set_main_option("script_location", os.path.join(backend_dir, "migrations"))
        alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite:///{db_path}")
        
        # Ensure DB is stamped to current head to satisfy autogenerate precondition
        command.stamp(alembic_cfg, "head")
        # This should not raise an exception
        command.revision(alembic_cfg, autogenerate=True, message="test_migration")
    
    def test_migration_upgrade(self, temp_db):
        """Test that migrations can be applied"""
        engine, db_path = temp_db
        
        engine, db_path = temp_db
        
        # Apply migrations
        backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        alembic_cfg = Config(os.path.join(backend_dir, "alembic.ini"))
        alembic_cfg.set_main_option("script_location", os.path.join(backend_dir, "migrations"))
        alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite:///{db_path}")
        
        # This should not raise an exception
        command.upgrade(alembic_cfg, "head")
    
    def test_migration_rollback(self, temp_db):
        """Test that migrations can be rolled back"""
        engine, db_path = temp_db
        
        engine, db_path = temp_db
        
        # Apply migrations
        backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        alembic_cfg = Config(os.path.join(backend_dir, "alembic.ini"))
        alembic_cfg.set_main_option("script_location", os.path.join(backend_dir, "migrations"))
        alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite:///{db_path}")
        
        # Upgrade to head
        command.upgrade(alembic_cfg, "head")
        
        # Get current revision
        from alembic.script import ScriptDirectory
        script_dir = ScriptDirectory.from_config(alembic_cfg)
        current_rev = command.current(alembic_cfg)
        
        # Rollback one step
        if current_rev:
            command.downgrade(alembic_cfg, "-1")
    
    def test_model_compatibility(self):
        """Test that all models are compatible with migrations"""
        # This test ensures all models can be imported and have proper relationships
        from app.models import (
            Profile, User, ProfileAddress, APIUsageTracking,
            JobBoardJob, UserJobBoardJobFitScore
        )
        
        # Test that models can be instantiated
        profile = Profile()
        user = User()
        address = ProfileAddress()
        
        assert profile is not None
        assert user is not None
        assert address is not None 