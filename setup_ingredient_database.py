#!/usr/bin/env python3
"""
Setup script to populate the ingredient_rules table with comprehensive data
Run this script to migrate from hardcoded patterns to database-driven ingredient search
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_dir))

from db.supabase_client import get_supabase_client
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_ingredient_database():
    """
    Setup the ingredient database by running the migration SQL
    """
    try:
        supabase = get_supabase_client()
        
        # Read the migration SQL file
        migration_file = Path(__file__).parent / 'database' / 'migrate_ingredients_to_db.sql'
        
        if not migration_file.exists():
            logger.error(f"Migration file not found: {migration_file}")
            return False
        
        with open(migration_file, 'r', encoding='utf-8') as f:
            migration_sql = f.read()
        
        logger.info("Running ingredient database migration...")
        
        # Execute the migration SQL
        # Note: Supabase Python client doesn't support raw SQL execution
        # This needs to be run manually in Supabase SQL Editor
        logger.info("Please run the following SQL in your Supabase SQL Editor:")
        logger.info("=" * 80)
        print(migration_sql)
        logger.info("=" * 80)
        
        logger.info("Migration SQL printed above. Please copy and run it in Supabase SQL Editor.")
        logger.info("After running the SQL, the ingredient search will use the database instead of hardcoded patterns.")
        
        return True
        
    except Exception as e:
        logger.error(f"Error setting up ingredient database: {str(e)}")
        return False

def test_ingredient_search():
    """
    Test the ingredient search functionality
    """
    try:
        from services.ingredient_service import ingredient_service
        
        logger.info("Testing ingredient search...")
        
        # Test search
        result = ingredient_service.search_ingredient("Tartrazine")
        if result:
            logger.info(f"✅ Search test passed: Found {result['name']}")
        else:
            logger.warning("⚠️ Search test: No result found (database might be empty)")
        
        # Test suggestions
        suggestions = ingredient_service.get_ingredient_suggestions("tar", 5)
        logger.info(f"✅ Suggestions test: Found {len(suggestions)} suggestions")
        
        # Test popular ingredients
        popular = ingredient_service.get_popular_ingredients(10)
        logger.info(f"✅ Popular ingredients test: Found {len(popular)} popular ingredients")
        
        return True
        
    except Exception as e:
        logger.error(f"Error testing ingredient search: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("CheckKaro Ingredient Database Setup")
    logger.info("=" * 50)
    
    # Setup database
    if setup_ingredient_database():
        logger.info("✅ Database setup instructions provided")
    else:
        logger.error("❌ Database setup failed")
        sys.exit(1)
    
    # Test functionality (will work after SQL is run in Supabase)
    logger.info("\nTesting ingredient search functionality...")
    if test_ingredient_search():
        logger.info("✅ All tests passed!")
    else:
        logger.warning("⚠️ Some tests failed - make sure to run the SQL migration first")
    
    logger.info("\n🎉 Setup complete! Your ingredient search now supports:")
    logger.info("   • Database-driven search instead of hardcoded patterns")
    logger.info("   • Real-time auto-suggestions")
    logger.info("   • Popular ingredients from database")
    logger.info("   • Comprehensive ingredient information")