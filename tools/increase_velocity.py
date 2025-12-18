#!/usr/bin/env python3
"""
Script to increase all unit velocity values by 7 in the game configuration.
"""

import json
import shutil
from datetime import datetime

def increase_velocity_values():
    """Increase all unit velocity values by 7."""
    config_path = "config/main.json"
    backup_path = f"config/main.json.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Create backup
    print(f"Creating backup: {backup_path}")
    shutil.copy2(config_path, backup_path)
    
    # Load the JSON data
    print("Loading configuration file...")
    with open(config_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Process all items
    items = data.get("items", [])
    print(f"Processing {len(items)} items...")
    
    velocity_updated_count = 0
    
    for item in items:
        # Check if item has a velocity field
        if "velocity" in item:
            try:
                # Get current velocity value
                current_velocity = int(item["velocity"])
                
                # Increase by 7
                new_velocity = current_velocity + 7
                
                # Update the velocity
                item["velocity"] = str(new_velocity)
                velocity_updated_count += 1
                
                # Print update for units (type "u") with non-zero velocity
                if item.get("type") == "u" and current_velocity > 0:
                    print(f"  Updated {item.get('name', 'Unknown')} ({item.get('id')}): {current_velocity} -> {new_velocity}")
                    
            except ValueError:
                # Handle case where velocity is not a valid integer
                print(f"  Warning: Invalid velocity value for item {item.get('id', 'Unknown')}: {item['velocity']}")
                continue
    
    # Save the modified data
    print(f"Saving updated configuration with {velocity_updated_count} velocity values modified...")
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
    
    print("Velocity update completed successfully!")
    print(f"Backup saved to: {backup_path}")

if __name__ == "__main__":
    increase_velocity_values()