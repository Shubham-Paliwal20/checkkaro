"""
Database-driven Ingredient Service
Replaces hardcoded patterns with database queries for better scalability
"""

from db.supabase_client import get_supabase_client
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class IngredientService:
    def __init__(self):
        self.supabase = get_supabase_client()
    
    def search_ingredient(self, ingredient_name: str) -> Optional[Dict]:
        """
        Search for a specific ingredient by name
        Returns detailed ingredient information
        """
        try:
            # First try exact match
            result = self.supabase.table('ingredient_rules').select('*').ilike('name', ingredient_name).execute()
            
            if result.data:
                return self._format_ingredient_data(result.data[0])
            
            # Try partial match
            result = self.supabase.table('ingredient_rules').select('*').ilike('name', f'%{ingredient_name}%').limit(1).execute()
            
            if result.data:
                return self._format_ingredient_data(result.data[0])
            
            # Try alias match
            result = self.supabase.table('ingredient_rules').select('*').contains('aliases', [ingredient_name]).limit(1).execute()
            
            if result.data:
                return self._format_ingredient_data(result.data[0])
            
            # If no match found, return None (will trigger fallback to hardcoded patterns)
            return None
            
        except Exception as e:
            logger.error(f"Error searching ingredient {ingredient_name}: {str(e)}")
            return None
    
    def get_ingredient_suggestions(self, search_term: str, limit: int = 10) -> List[Dict]:
        """
        Get ingredient suggestions for auto-complete
        Returns list of matching ingredients with basic info
        """
        try:
            if len(search_term) < 2:
                return []
            
            # Use the custom search function for better results
            result = self.supabase.rpc('search_ingredients_with_suggestions', {
                'search_term': search_term,
                'limit_count': limit
            }).execute()
            
            if result.data:
                return [
                    {
                        'id': item['id'],
                        'name': item['name'],
                        'classification': item['classification'],
                        'what_it_is': item['what_it_is'],
                        'aliases': item['aliases'] or []
                    }
                    for item in result.data
                ]
            
            # Fallback to simple search if RPC function not available
            result = self.supabase.table('ingredient_rules').select(
                'id, name, classification, what_it_is, aliases'
            ).ilike('name', f'{search_term}%').limit(limit).execute()
            
            return [
                {
                    'id': item['id'],
                    'name': item['name'],
                    'classification': item['classification'],
                    'what_it_is': item['what_it_is'],
                    'aliases': item['aliases'] or []
                }
                for item in result.data
            ]
            
        except Exception as e:
            logger.error(f"Error getting ingredient suggestions for '{search_term}': {str(e)}")
            return []
    
    def get_popular_ingredients(self, limit: int = 20) -> List[Dict]:
        """
        Get popular/commonly searched ingredients
        """
        try:
            # Get commonly questioned ingredients first (most interesting)
            result = self.supabase.table('ingredient_rules').select(
                'id, name, classification, what_it_is'
            ).eq('classification', 'commonly_questioned').limit(limit // 2).execute()
            
            popular = result.data or []
            
            # Add some worth knowing ingredients
            if len(popular) < limit:
                remaining = limit - len(popular)
                result = self.supabase.table('ingredient_rules').select(
                    'id, name, classification, what_it_is'
                ).eq('classification', 'worth_knowing').limit(remaining).execute()
                
                popular.extend(result.data or [])
            
            return popular
            
        except Exception as e:
            logger.error(f"Error getting popular ingredients: {str(e)}")
            return []
    
    def _format_ingredient_data(self, raw_data: Dict) -> Dict:
        """
        Format raw database data into the expected response format
        """
        return {
            'id': raw_data.get('id'),
            'name': raw_data.get('name'),
            'classification': raw_data.get('classification'),
            'what_it_is': raw_data.get('what_it_is'),
            'commonly_found_in': raw_data.get('commonly_found_in'),
            'one_line_note': raw_data.get('one_line_note'),
            'regulatory_note': raw_data.get('fssai_position'),  # Map fssai_position to regulatory_note
            'countries_restricted': raw_data.get('countries_restricted', []),
            'fssai_position': raw_data.get('fssai_position'),
            'applies_to': raw_data.get('applies_to', 'both'),
            'aliases': raw_data.get('aliases', [])
        }

# Global instance
ingredient_service = IngredientService()
