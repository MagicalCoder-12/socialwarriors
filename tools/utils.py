"""Utility functions for the tools scripts."""

import json
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_json_file(file_path):
    """
    Safely load a JSON file.
    
    Args:
        file_path (str): Path to the JSON file
        
    Returns:
        dict: Loaded JSON data
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file contains invalid JSON
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in {file_path}: {str(e)}", e.doc, e.pos)

def save_json_file(file_path, data):
    """
    Safely save data to a JSON file.
    
    Args:
        file_path (str): Path to the JSON file
        data: Data to save (must be JSON serializable)
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Successfully saved data to {file_path}")
    except Exception as e:
        logger.error(f"Failed to save data to {file_path}: {str(e)}")
        raise

def trim_quotes(input_str):
    """
    Trim leading and trailing quotes from a string.
    
    Args:
        input_str (str): String to trim
        
    Returns:
        str: Trimmed string
    """
    new_str = input_str
    while new_str.startswith('"') or new_str.startswith("'"):
        new_str = new_str[1:]
    while new_str.endswith('"') or new_str.endswith("'"):
        new_str = new_str[:-1]
    return new_str