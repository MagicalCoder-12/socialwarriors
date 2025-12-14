#!/usr/bin/env python3
"""
Diagnostic tool to identify and troubleshoot sprite loading issues in Social Wars Flash game.
"""

import os
import sys
from flask import Flask, jsonify, send_from_directory
from bundle import ASSETS_DIR

def check_asset_structure():
    """Check the asset directory structure."""
    print("=== ASSET STRUCTURE DIAGNOSTIC ===")
    
    # Check main directories
    required_dirs = ["assets", "assets/sprites", "assets/flash"]
    for dir_name in required_dirs:
        dir_path = os.path.join(".", dir_name)
        if os.path.exists(dir_path):
            print(f"✓ {dir_name} directory exists")
        else:
            print(f"✗ {dir_name} directory missing")
    
    # Check key files
    key_files = [
        "assets/sprites/0001_house_1_m.swf",
        "assets/flash/SWLoader.swf",
        "stub/crossdomain.xml"
    ]
    
    for file_path in key_files:
        full_path = os.path.join(".", file_path)
        if os.path.exists(full_path):
            size = os.path.getsize(full_path)
            print(f"✓ {file_path} exists ({size} bytes)")
        else:
            print(f"✗ {file_path} missing")

def check_flash_parameters():
    """Check Flash embedding parameters."""
    print("\n=== FLASH PARAMETERS DIAGNOSTIC ===")
    
    # These are the key parameters that affect sprite loading
    flash_params = {
        "staticUrl": "Should point to http://127.0.0.1:5055/static/socialwars/",
        "swf loader": "SWLoader.swf should load game SWF files",
        "crossdomain": "crossdomain.xml should allow all access"
    }
    
    for param, description in flash_params.items():
        print(f"- {param}: {description}")

def check_server_routes():
    """Check server route configuration."""
    print("\n=== SERVER ROUTES DIAGNOSTIC ===")
    
    # Expected routes for sprite loading
    expected_routes = {
        "/static/socialwars/<path:path>": "Serve static assets including sprites",
        "/crossdomain.xml": "Flash security policy file",
        "/static/socialwars/flash/SWLoader.swf": "Main game loader"
    }
    
    for route, purpose in expected_routes.items():
        print(f"- {route}: {purpose}")

def check_permissions():
    """Check file permissions."""
    print("\n=== PERMISSIONS DIAGNOSTIC ===")
    
    # Check if we can read sprite files
    sprites_dir = os.path.join(ASSETS_DIR, "sprites")
    try:
        if os.access(sprites_dir, os.R_OK):
            print("✓ Sprite directory is readable")
        else:
            print("✗ Sprite directory is not readable")
            
        # Try to read a specific file
        test_file = os.path.join(sprites_dir, "0001_house_1_m.swf")
        if os.access(test_file, os.R_OK):
            print("✓ Individual sprite files are readable")
        else:
            print("✗ Individual sprite files are not readable")
            
    except Exception as e:
        print(f"✗ Permission check failed: {e}")

def suggest_fixes():
    """Suggest fixes for common sprite loading issues."""
    print("\n=== RECOMMENDED FIXES ===")
    
    fixes = [
        "1. Ensure you're using a Flash-enabled browser (FlashBrowser recommended)",
        "2. Check that Flash is enabled in your browser settings",
        "3. Verify that all asset files are present in the assets directory",
        "4. Make sure the server is running on http://127.0.0.1:5055",
        "5. Check that crossdomain.xml is properly configured",
        "6. Clear your browser cache and restart the game",
        "7. Try accessing sprites directly: http://127.0.0.1:5055/static/socialwars/sprites/0001_house_1_m.swf"
    ]
    
    for fix in fixes:
        print(fix)

def main():
    """Main diagnostic function."""
    print("Social Wars Sprite Loading Diagnostic Tool")
    print("=" * 50)
    
    check_asset_structure()
    check_flash_parameters()
    check_server_routes()
    check_permissions()
    suggest_fixes()
    
    print("\n=== ADDITIONAL TROUBLESHOOTING ===")
    print("If sprites still don't load:")
    print("- Check browser console for Flash security errors")
    print("- Verify that SWLoader.swf is loading correctly")
    print("- Ensure that the game version in login matches available SWF files")
    print("- Try different Flash versions if available")

if __name__ == "__main__":
    main()