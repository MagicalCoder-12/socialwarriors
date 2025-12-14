#!/usr/bin/env python3
"""
Unit Patch Generator Script

This script creates unit patches from CSV data:
- Reads unit data from CSV file
- Uses templates from unit_templates.json
- Generates JSON patches to add new units to the game
- Outputs patches to unit_patch.json
- Creates a storage file with unit IDs for save games
"""

import os
import json
import csv
import argparse
import logging
import sys
import copy

# Add the tools directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import config
import utils
import validators

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_templates():
    """
    Load unit templates from JSON file.
    
    Returns:
        dict: Unit templates
        
    Raises:
        Exception: If templates cannot be loaded or validated
    """
    try:
        templates = utils.load_json_file(config.UNIT_TEMPLATES_PATH)
        logger.info(f"Loaded templates from {config.UNIT_TEMPLATES_PATH}")
        
        # Validate each template
        for template_name, template in templates.items():
            validators.validate_template(template, template_name)
            
        return templates
    except Exception as e:
        logger.error(f"Failed to load templates: {str(e)}")
        raise

def load_csv_data():
    """
    Load unit data from CSV file.
    
    Returns:
        list: List of dictionaries representing unit data
    """
    units = []
    
    if not os.path.exists(config.INPUT_CSV_PATH):
        logger.warning(f"CSV file {config.INPUT_CSV_PATH} not found")
        return units
    
    try:
        with open(config.INPUT_CSV_PATH, "r", encoding='utf-8') as f:
            # Use DictReader for better readability
            reader = csv.DictReader(f, delimiter='\t')
            for row_num, row in enumerate(reader, start=1):
                try:
                    # Validate the row data
                    validators.validate_unit_data(row)
                    units.append(row)
                    logger.debug(f"Loaded unit data for {row['name']} from row {row_num}")
                except ValueError as e:
                    logger.warning(f"Skipping row {row_num} due to validation error: {str(e)}")
                    continue
                    
        logger.info(f"Loaded {len(units)} units from {config.INPUT_CSV_PATH}")
        return units
    except Exception as e:
        logger.error(f"Failed to load CSV data: {str(e)}")
        raise

def create_unit_patch(unit_data, templates):
    """
    Create a patch for a single unit.
    
    Args:
        unit_data (dict): Unit data from CSV
        templates (dict): Unit templates
        
    Returns:
        tuple: (patch_operation, storage_entry) or (None, None) if failed
    """
    ITEM_ID = unit_data['id']
    ITEM_ASSET = unit_data['asset']
    ITEM_NAME = unit_data['name']
    ITEM_HEALTH = unit_data['health']
    ITEM_ATTACK = unit_data['attack']
    ITEM_RANGE = unit_data['range']
    ITEM_SPEED = unit_data['speed']
    ITEM_INTERVAL = unit_data['interval']
    ITEM_POPULATION = unit_data['population']
    ITEM_SYRINGES = unit_data['syringes']
    ITEM_XP = unit_data['xp']
    ITEM_COST = utils.trim_quotes(unit_data['cost'])
    ITEM_GROUP = unit_data['group']
    ITEM_PROPERTIES = utils.trim_quotes(unit_data['properties'])
    
    if ITEM_ASSET == "":
        logger.warning(f"{ITEM_NAME} Failed - Asset missing")
        return None, None

    if ITEM_GROUP not in templates:
        logger.warning(f"{ITEM_NAME} Failed - Template {ITEM_GROUP} not found")
        return None, None

    # Fetch from template
    template = templates[ITEM_GROUP]
    item = copy.deepcopy(template)

    # Update data
    item["id"] = str(ITEM_ID)
    item["img_name"] = str(ITEM_ASSET)
    item["name"] = str(ITEM_NAME)
    item["life"] = str(ITEM_HEALTH)
    item["attack"] = str(ITEM_ATTACK)
    item["attack_range"] = str(ITEM_RANGE)
    item["velocity"] = str(ITEM_SPEED)
    item["attack_interval"] = str(ITEM_INTERVAL)
    item["population"] = str(ITEM_POPULATION)
    item["syringes"] = str(ITEM_SYRINGES)
    item["xp"] = str(ITEM_XP)
    item["costs"] = ITEM_COST.replace("\\", "")
    item["properties"] = ITEM_PROPERTIES.replace("\\", "")

    # Create patch
    patch = {
        "op": "add",
        "path": "/items/-",
        "value": item
    }

    # Storage entry (unit ID -> quantity)
    storage_entry = {str(ITEM_ID): 1}

    logger.info(f"Made patch for {ITEM_NAME}")
    return patch, storage_entry

def generate_patches(units, templates):
    """
    Generate patches for all units.
    
    Args:
        units (list): List of unit data dictionaries
        templates (dict): Unit templates
        
    Returns:
        tuple: (patches, storage) - lists of patch operations and storage entries
    """
    patches = []
    storage = {}
    
    for unit in units:
        patch, storage_entry = create_unit_patch(unit, templates)
        if patch and storage_entry:
            patches.append(patch)
            storage.update(storage_entry)
    
    return patches, storage

def save_results(patches, storage):
    """
    Save the generated patches and storage data.
    
    Args:
        patches (list): List of patch operations
        storage (dict): Storage data
    """
    if not patches:
        logger.warning("No patches to save")
        return
    
    try:
        # Save patches
        utils.save_json_file(config.UNIT_PATCH_PATH, patches)
        
        # Save storage
        utils.save_json_file(config.OUTPUT_STORAGE_PATH, storage)
        
        logger.info(f"Created patch for {len(patches)} items to {config.UNIT_PATCH_PATH}!")
    except Exception as e:
        logger.error(f"Failed to save results: {str(e)}")
        raise

def main():
    """Main function to run the unit patch generator."""
    parser = argparse.ArgumentParser(description='Generate unit patches from CSV data')
    parser.add_argument('--csv', default=config.INPUT_CSV_PATH, 
                       help='Input CSV file path')
    parser.add_argument('--templates', default=config.UNIT_TEMPLATES_PATH, 
                       help='Unit templates file path')
    parser.add_argument('--patch-output', default=config.UNIT_PATCH_PATH, 
                       help='Output patch file path')
    parser.add_argument('--storage-output', default=config.OUTPUT_STORAGE_PATH, 
                       help='Output storage file path')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Adjust logging level based on verbosity
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Load templates
        templates = load_templates()
        
        # Load CSV data
        units = load_csv_data()
        
        # Generate patches
        patches, storage = generate_patches(units, templates)
        
        # Save results
        save_results(patches, storage)
        
        logger.info(f"Successfully generated {len(patches)} patch operations")
        
    except Exception as e:
        logger.error(f"Failed to generate patches: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()