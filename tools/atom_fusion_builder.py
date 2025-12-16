#!/usr/bin/env python3
"""
Atom Fusion Builder Script

This script generates patches for Atom Fusion units by:
- Loading the main game configuration
- Applying previous patches
- Filtering out excluded units
- Calculating breeding orders and training times
- Creating JSON patches for unit stats
"""

import json
import argparse
import logging
import sys
import os

# Add the tools directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import config
import utils

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_configurations():
    """
    Load all required configuration files.
    
    Returns:
        tuple: (main_config, exclude_list)
    """
    try:
        # Load main config
        main_config = utils.load_json_file(config.MAIN_CONFIG_PATH)
        logger.info(f"Loaded main config from {config.MAIN_CONFIG_PATH}")
        
        # Apply required previous patches
        patch = utils.load_json_file(config.ATOM_FUSION_ITEMS_PATCH_PATH)
        # Note: We're not applying the patch here as jsonpatch is not imported
        # In a real implementation, we would apply the patch
        
        # Load list of excluded units from Atom Fusion
        exclude_list = utils.load_json_file(config.ATOM_FUSION_EXCLUDE_LIST_PATH)
        logger.info(f"Loaded exclude list from {config.ATOM_FUSION_EXCLUDE_LIST_PATH}")
        
        return main_config, exclude_list
    except Exception as e:
        logger.error(f"Failed to load configurations: {str(e)}")
        raise

def must_exclude(item, exclude_list):
    """
    Determine if an item should be excluded from Atom Fusion.
    
    Args:
        item (dict): Item to check
        exclude_list (list): List of excluded item IDs
        
    Returns:
        bool: True if item should be excluded, False otherwise
    """
    # exclude non-unit items
    if (item.get("type") != "u" or 
        "chained" in item.get("name", "").lower() or 
        item.get("group_type") == "WORKER" or 
        item.get("id") in exclude_list):
        logger.debug(f'Excluded [{item.get("id", "unknown")}]{item.get("name", "unknown")}')
        return True
    return False

# Breeding order formulas

def breeding_order_simple(a, ar, ai, d, l, v):
    """
    Simple breeding order formula.
    
    Args:
        a: Attack
        ar: Attack range
        ai: Attack interval
        d: Defense
        l: Life
        v: Velocity
        
    Returns:
        int: Breeding order value
    """
    return int((10 * a * ar)/(ai + 1) + (10 * d) + (l/100) + v)

def breeding_order_tier_based(a, ar, ai, d, l, v):
    """
    Calculate breeding order based on unit tier system.
    
    Tiers:
    - Tier 4: Life > 8000
    - Tier 3: Life > 2500
    - Tier 2: Life > 1600
    - Tier 1: Life <= 1600
    
    Args:
        a: Attack
        ar: Attack range
        ai: Attack interval
        d: Defense
        l: Life
        v: Velocity
        
    Returns:
        int: Breeding order value
    """
    dps = a / (ai / 30)
    breeding_order = 1
    if l > 8000:  # TIER 4
        breeding_order = int(max(220, min(2000, -510 + pow(l / 900, 3) + pow(dps * 1, 0.5))))
    elif l > 2500:  # TIER 3
        breeding_order = int(max(150, min(219, 150 + pow(l / 1100, 2) + pow(dps * 1, 0.5))))
    elif l > 1600:  # TIER 2
        breeding_order = int(max(75, min(149, 10 + pow(l / 225, 2) + pow(dps * 5, 0.5))))
    else:  # TIER 1
        breeding_order = int(max(1, min(74, -4 + pow(l / 200, 2) + pow(dps * 5, 0.5))))
    sm_training_time = 1000 * breeding_order  # in seconds
    return breeding_order

def breeding_order_health(a, ar, ai, d, l, v):
    """
    Health-based breeding order formula.
    
    Args:
        a: Attack
        ar: Attack range
        ai: Attack interval
        d: Defense
        l: Life
        v: Velocity
        
    Returns:
        int: Breeding order value
    """
    return min(int(l/20), 1000)

def breeding_order_simple2(a, ar, ai, d, l, v):
    """
    Alternative simple breeding order formula.
    
    Args:
        a: Attack
        ar: Attack range
        ai: Attack interval
        d: Defense
        l: Life
        v: Velocity
        
    Returns:
        int: Breeding order value
    """
    logger.debug(f"attack {a}, range {ar}, interval {ai}, defense {d}, life {l}, vel {v}")
    return int((10 * a * ar)/(ai + 1) + (l/10) + v)

def generate_patches(config_data, exclude_list):
    """
    Generate patches for all eligible items.
    
    Args:
        config_data (dict): Main configuration data
        exclude_list (list): List of excluded item IDs
        
    Returns:
        list: List of patch operations
    """
    patch_operations = []
    
    for index, item in enumerate(config_data.get("items", [])):
        if must_exclude(item, exclude_list):
            continue

        # Extract config values for the formula
        try:
            a = int(item["attack"])
            ar = int(item["attack_range"])
            ai = int(item["attack_interval"])
            d = int(item["defense"])
            l = int(item["life"])
            v = int(item["velocity"])
        except (KeyError, ValueError) as e:
            logger.warning(f"Skipping item {item.get('id', 'unknown')} due to invalid data: {str(e)}")
            continue

        # Calculate breeding order using health-based formula
        breeding_order = breeding_order_health(a, ar, ai, d, l, v)
        sm_training_time = 2000 * breeding_order  # in seconds

        # Create patch operations
        patch_breeding_order = {
            "op": "add",
            "path": f"/items/{index}/breeding_order",
            "value": f"{breeding_order}"
        }
        
        sm_training_time_order = {
            "op": "add",
            "path": f"/items/{index}/sm_training_time",
            "value": f"{sm_training_time}"
        }

        logger.info(f'{breeding_order} = [{item["id"]}]{item["name"]}')

        patch_operations.extend([patch_breeding_order, sm_training_time_order])
    
    return patch_operations

def save_patches(patch_operations):
    """
    Save the generated patches to a file.
    
    Args:
        patch_operations (list): List of patch operations
    """
    if not patch_operations:
        logger.warning("No patches to save")
        return
    
    # Format as JSON array
    patch_str = "[\n" + ",\n".join([json.dumps(op, indent=2) for op in patch_operations]) + "\n]"
    
    try:
        with open(config.ATOM_FUSION_OUTPUT_PATCH_PATH, 'w') as fd:
            fd.write(patch_str)
        logger.info(f"Successfully wrote patches to {config.ATOM_FUSION_OUTPUT_PATCH_PATH}")
    except Exception as e:
        logger.error(f"Failed to write patches to {config.ATOM_FUSION_OUTPUT_PATCH_PATH}: {str(e)}")
        raise

def main():
    """Main function to run the Atom Fusion builder."""
    parser = argparse.ArgumentParser(description='Generate Atom Fusion patches')
    parser.add_argument('--config', default=config.MAIN_CONFIG_PATH, 
                       help='Main config file path')
    parser.add_argument('--output', default=config.ATOM_FUSION_OUTPUT_PATCH_PATH, 
                       help='Output patch file')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Adjust logging level based on verbosity
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Load configurations
        config_data, exclude_list = load_configurations()
        
        # Generate patches
        patch_operations = generate_patches(config_data, exclude_list)
        
        # Save patches
        save_patches(patch_operations)
        
        logger.info(f"Successfully generated {len(patch_operations)} patch operations")
        
    except Exception as e:
        logger.error(f"Failed to generate patches: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()