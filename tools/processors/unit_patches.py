"""Unit patches processor module."""

import logging
import copy

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_unit_patches(unit_data_list, templates):
    """
    Process unit data to create patches.
    
    Args:
        unit_data_list (list): List of unit data dictionaries
        templates (dict): Unit templates
        
    Returns:
        tuple: (patches, storage) - lists of patch operations and storage entries
    """
    patches = []
    storage = {}
    
    for unit_data in unit_data_list:
        patch, storage_entry = create_unit_patch(unit_data, templates)
        if patch and storage_entry:
            patches.append(patch)
            storage.update(storage_entry)
    
    return patches, storage

def create_unit_patch(unit_data, templates):
    """
    Create a patch for a single unit.
    
    Args:
        unit_data (dict): Unit data
        templates (dict): Unit templates
        
    Returns:
        tuple: (patch_operation, storage_entry) or (None, None) if failed
    """
    ITEM_ID = unit_data.get('id', '')
    ITEM_ASSET = unit_data.get('asset', '')
    ITEM_NAME = unit_data.get('name', '')
    ITEM_GROUP = unit_data.get('group', '')
    
    if ITEM_ASSET == "":
        logger.warning(f"{ITEM_NAME} Failed - Asset missing")
        return None, None

    if ITEM_GROUP not in templates:
        logger.warning(f"{ITEM_NAME} Failed - Template {ITEM_GROUP} not found")
        return None, None

    # Fetch from template
    template = templates[ITEM_GROUP]
    item = copy.deepcopy(template)

    # Update data (simplified - in reality you would update all fields)
    item["id"] = str(ITEM_ID)
    item["img_name"] = str(ITEM_ASSET)
    item["name"] = str(ITEM_NAME)

    # Create patch
    patch = {
        "op": "add",
        "path": "/items/-",
        "value": item
    }

    # Storage entry (unit ID -> quantity)
    storage_entry = {str(ITEM_ID): 1}

    logger.debug(f"Created patch for {ITEM_NAME}")
    return patch, storage_entry