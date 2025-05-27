"""
NAICS Code Validator
Validates North American Industry Classification System codes using Census API
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NAICSValidator:
    """Validates NAICS codes using the Census API with caching"""
    
    CENSUS_API_BASE = "https://api.census.gov/data/2023/eeo"
    CACHE_FILE = "config/naics_cache.json"
    CACHE_EXPIRY_DAYS = 30
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize validator with optional API key
        
        Args:
            api_key: Census API key (or set CENSUS_API_KEY env var)
        """
        self.api_key = api_key or os.environ.get('CENSUS_API_KEY', '')
        self.cache = self._load_cache()
        
    def _load_cache(self) -> Dict:
        """Load cached NAICS validations"""
        if os.path.exists(self.CACHE_FILE):
            try:
                with open(self.CACHE_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load cache: {e}")
        return {}
    
    def _save_cache(self):
        """Save NAICS validation cache"""
        try:
            os.makedirs(os.path.dirname(self.CACHE_FILE), exist_ok=True)
            with open(self.CACHE_FILE, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save cache: {e}")
    
    def _is_cache_valid(self, cache_entry: Dict) -> bool:
        """Check if a cache entry is still valid"""
        if 'timestamp' not in cache_entry:
            return False
        
        cached_time = datetime.fromisoformat(cache_entry['timestamp'])
        expiry_time = cached_time + timedelta(days=self.CACHE_EXPIRY_DAYS)
        return datetime.now() < expiry_time
    
    def validate(self, code: str) -> Tuple[bool, Optional[str]]:
        """
        Validate a NAICS code
        
        Args:
            code: 6-digit NAICS code
            
        Returns:
            Tuple of (is_valid, description)
        """
        # Check format
        if not code or not code.isdigit() or len(code) != 6:
            return False, "Invalid format - must be 6 digits"
        
        # Check cache
        if code in self.cache and self._is_cache_valid(self.cache[code]):
            logger.info(f"Using cached result for NAICS {code}")
            return self.cache[code]['valid'], self.cache[code].get('description')
        
        # Query API
        try:
            if not self.api_key:
                logger.warning("No Census API key provided - using limited access")
            
            params = {
                'get': 'NAICS_TITLE',
                'for': 'industry:*',
                'NAICS_CODE': code
            }
            
            if self.api_key:
                params['key'] = self.api_key
                
            response = requests.get(self.CENSUS_API_BASE, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                # First row is header, valid if more than one row
                is_valid = len(data) > 1
                description = data[1][0] if is_valid and len(data[1]) > 0 else None
                
                # Cache result
                self.cache[code] = {
                    'valid': is_valid,
                    'description': description,
                    'timestamp': datetime.now().isoformat()
                }
                self._save_cache()
                
                return is_valid, description
            else:
                logger.error(f"Census API error: {response.status_code}")
                return False, f"API error: {response.status_code}"
                
        except requests.exceptions.Timeout:
            logger.error("Census API timeout")
            return False, "API timeout"
        except Exception as e:
            logger.error(f"Validation error: {e}")
            return False, str(e)
    
    def get_common_codes(self) -> Dict[str, str]:
        """Return dictionary of common NAICS codes for reference"""
        return {
            "541611": "Administrative Management and General Management Consulting Services",
            "541612": "Human Resources Consulting Services",
            "922140": "Correctional Institutions",
            "922150": "Parole Offices and Probation Offices",
            "922190": "Other Justice, Public Order, and Safety Activities",
            "923110": "Administration of Education Programs",
            "923120": "Administration of Public Health Programs",
            "923130": "Administration of Human Resource Programs",
            "923140": "Administration of Veterans' Affairs",
            "924110": "Administration of Air and Water Resource Programs",
            "924120": "Administration of Conservation Programs",
            "925110": "Administration of Housing Programs",
            "925120": "Administration of Urban Planning and Community Development",
            "926110": "Administration of General Economic Programs",
            "928110": "National Security"
        }


def check_workforce_snapshot(date_str: str) -> Tuple[bool, str]:
    """
    Validate workforce snapshot date for EEO-1 reporting
    
    Args:
        date_str: Date string in ISO format (YYYY-MM-DD)
        
    Returns:
        Tuple of (is_valid, message)
    """
    try:
        snapshot_date = datetime.fromisoformat(date_str).date()
        current_year = datetime.now().year
        
        # EEO-1 requires Q4 snapshot (Oct-Dec of prior year)
        required_year = current_year - 1
        required_start = datetime(required_year, 10, 1).date()
        required_end = datetime(required_year, 12, 31).date()
        
        if required_start <= snapshot_date <= required_end:
            return True, f"Valid Q4 {required_year} snapshot"
        else:
            return False, f"Must be Q4 {required_year} (Oct-Dec)"
            
    except ValueError:
        return False, "Invalid date format - use YYYY-MM-DD"


# Example usage and testing
if __name__ == "__main__":
    # Test NAICS validation
    validator = NAICSValidator()
    
    test_codes = ["541611", "999999", "12345", "922140"]
    
    print("Testing NAICS validation:")
    for code in test_codes:
        valid, desc = validator.validate(code)
        print(f"  {code}: {'Valid' if valid else 'Invalid'} - {desc}")
    
    print("\nCommon government NAICS codes:")
    for code, desc in validator.get_common_codes().items():
        print(f"  {code}: {desc}")
    
    # Test workforce snapshot
    print("\nTesting workforce snapshot dates:")
    test_dates = ["2024-12-31", "2024-06-30", "2023-11-15", "invalid-date"]
    
    for date in test_dates:
        valid, msg = check_workforce_snapshot(date)
        print(f"  {date}: {'Valid' if valid else 'Invalid'} - {msg}") 