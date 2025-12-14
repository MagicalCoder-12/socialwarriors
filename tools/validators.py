"""Validation utilities for the tools scripts."""

import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Required fields for different template types
REQUIRED_FIELDS = {
    'common': ['attack', 'defense', 'life', 'velocity', 'attack_range', 'attack_interval'],
    'ROBOT': ['mechanic', 'seeStealthUnits', 'resurrectable'],
    'AIR_VEHICLE': ['ft_flying', 'bulldozable'],
    'DRAGON': ['bulldozable', 'seeStealthUnits'],
    'HEALER': ['healer', 'seeStealthUnits']
}

def validate_template(template, template_name):
    """
    Validate that a template has all required fields.
    
    Args:
        template (dict): The template to validate
        template_name (str): Name of the template for error reporting
        
    Raises:
        ValueError: If template is missing required fields
    """
    # Check common required fields
    missing_fields = [field for field in REQUIRED_FIELDS['common'] if field not in template]
    if missing_fields:
        raise ValueError(f"Template {template_name} missing common fields: {missing_fields}")
    
    # Check template-type specific fields
    group_type = template.get('group_type', '')
    if group_type in REQUIRED_FIELDS:
        missing_fields = [field for field in REQUIRED_FIELDS[group_type] if field not in template]
        if missing_fields:
            raise ValueError(f"Template {template_name} missing {group_type} specific fields: {missing_fields}")
    
    logger.debug(f"Template {template_name} passed validation")

def validate_unit_data(unit_data):
    """
    Validate unit data from CSV.
    
    Args:
        unit_data (dict): Unit data to validate
        
    Raises:
        ValueError: If unit data is invalid
    """
    required_keys = ['id', 'asset', 'name', 'health', 'attack', 'range', 'speed', 'interval', 'population', 'syringes', 'xp', 'cost', 'group', 'properties']
    
    missing_keys = [key for key in required_keys if not unit_data.get(key)]
    if missing_keys:
        raise ValueError(f"Unit data missing required keys: {missing_keys}")
    
    # Validate numeric fields
    numeric_fields = ['health', 'attack', 'range', 'speed', 'interval', 'population', 'syringes', 'xp']
    for field in numeric_fields:
        try:
            float(unit_data[field])
        except ValueError:
            raise ValueError(f"Invalid numeric value for {field}: {unit_data[field]}")
    
    # Validate JSON fields
    json_fields = ['cost', 'properties']
    for field in json_fields:
        try:
            json.loads(unit_data[field])
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in {field}: {unit_data[field]}")
    
    logger.debug(f"Unit data for {unit_data['name']} passed validation")