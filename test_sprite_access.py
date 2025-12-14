#!/usr/bin/env python3
"""
Test script to verify sprite file access for troubleshooting sprite loading issues.
"""

import os
from bundle import ASSETS_DIR

def test_sprite_access():
    """Test if sprite files can be accessed properly."""
    sprites_dir = os.path.join(ASSETS_DIR, "sprites")
    
    print(f"Assets directory: {ASSETS_DIR}")
    print(f"Sprites directory: {sprites_dir}")
    
    # Check if assets directory exists
    if not os.path.exists(ASSETS_DIR):
        print("ERROR: Assets directory does not exist!")
        return False
        
    # Check if sprites directory exists
    if not os.path.exists(sprites_dir):
        print("ERROR: Sprites directory does not exist!")
        return False
    
    # List some sample sprite files
    try:
        sprite_files = os.listdir(sprites_dir)
        print(f"Found {len(sprite_files)} sprite files")
        
        # Check for house sprite files specifically
        house_sprites = [f for f in sprite_files if "house" in f.lower()]
        print(f"Found {len(house_sprites)} house sprite files:")
        for sprite in house_sprites[:5]:  # Show first 5
            print(f"  - {sprite}")
            
        # Try to access a specific sprite file
        test_sprite = "0001_house_1_m.swf"
        test_sprite_path = os.path.join(sprites_dir, test_sprite)
        
        if os.path.exists(test_sprite_path):
            file_size = os.path.getsize(test_sprite_path)
            print(f"SUCCESS: Test sprite {test_sprite} found, size: {file_size} bytes")
            return True
        else:
            print(f"ERROR: Test sprite {test_sprite} not found!")
            return False
            
    except Exception as e:
        print(f"ERROR: Failed to list sprite files: {e}")
        return False

if __name__ == "__main__":
    print("Testing sprite file access...")
    success = test_sprite_access()
    if success:
        print("\nSprite access test PASSED")
    else:
        print("\nSprite access test FAILED")