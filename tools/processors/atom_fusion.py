"""Atom Fusion processor module."""

import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_atom_fusion_units(config_data, exclude_list):
    """
    Process units for Atom Fusion capabilities.
    
    Args:
        config_data (dict): Main configuration data
        exclude_list (list): List of excluded unit IDs
        
    Returns:
        list: List of processed units
    """
    processed_units = []
    
    for unit in config_data.get("items", []):
        # Skip excluded units
        if unit.get("id") in exclude_list:
            continue
            
        # Process unit for Atom Fusion
        # This is a simplified example - in reality, you would implement
        # the specific logic needed for Atom Fusion processing
        processed_unit = {
            "id": unit.get("id"),
            "name": unit.get("name"),
            "fusion_eligible": is_fusion_eligible(unit),
            "fusion_tier": calculate_fusion_tier(unit)
        }
        
        processed_units.append(processed_unit)
    
    logger.info(f"Processed {len(processed_units)} units for Atom Fusion")
    return processed_units

def is_fusion_eligible(unit):
    """
    Determine if a unit is eligible for Atom Fusion.
    
    Args:
        unit (dict): Unit data
        
    Returns:
        bool: True if eligible, False otherwise
    """
    # Simplified eligibility check
    return (
        unit.get("type") == "u" and
        "chained" not in unit.get("name", "").lower() and
        unit.get("group_type") != "WORKER"
    )

def calculate_fusion_tier(unit):
    """
    Calculate the fusion tier for a unit.
    
    Args:
        unit (dict): Unit data
        
    Returns:
        int: Fusion tier (1-5)
    """
    life = int(unit.get("life", 0))
    
    if life > 8000:
        return 5
    elif life > 5000:
        return 4
    elif life > 2500:
        return 3
    elif life > 1000:
        return 2
    else:
        return 1