# Social Warriors Tools

This directory contains tools for modifying and extending the Social Warriors game.

## Overview

The tools in this directory are designed to help developers and modders:

1. Generate patches for Atom Fusion units
2. Create new unit definitions from CSV data
3. Validate game data and configurations

## Tools

### atom_fusion_builder.py

Generates patches for Atom Fusion units by calculating breeding orders and training times.

**Features:**
- Loads main game configuration
- Applies previous patches
- Filters out excluded units
- Calculates breeding orders using multiple formulas
- Creates JSON patches for unit stats

**Usage:**
```bash
python atom_fusion_builder.py [--config PATH] [--output PATH] [--verbose]
```

### make_sw_unit_patch.py

Creates unit patches from CSV data using templates.

**Features:**
- Reads unit data from CSV file
- Uses templates from unit_templates.json
- Generates JSON patches to add new units to the game
- Outputs patches to unit_patch.json
- Creates a storage file with unit IDs for save games

**Usage:**
```bash
python make_sw_unit_patch.py [--csv PATH] [--templates PATH] [--verbose]
```

## Modules

### config.py

Centralized configuration file containing paths to all required files.

### validators.py

Validation utilities for templates and unit data.

### utils.py

General utility functions for file handling and string manipulation.

### processors/

Contains specialized processing modules:
- `atom_fusion.py`: Processes units for Atom Fusion capabilities
- `unit_patches.py`: Handles unit patch generation

## Data Files

### atom_fusion_excluded_units.json

List of unit IDs that should be excluded from Atom Fusion calculations.

### unit_templates.json

Template definitions for different unit types (ROBOT, AIR_VEHICLE, DRAGON, HEALER).

### sw_unit_patch.csv

Tab-separated file containing unit data for new units to be added to the game.

## Testing

### test_formulas.py

Unit tests for the breeding order formulas used in atom_fusion_builder.py.

**Usage:**
```bash
python test_formulas.py
```

## Improvements Made

1. **Error Handling & Validation** - Added comprehensive error handling and data validation
2. **Configuration File** - Centralized configuration in config.py
3. **Command-Line Arguments** - Added CLI support for flexibility
4. **Logging** - Replaced print statements with proper logging
5. **Documentation** - Added docstrings and comments to explain the formulas
6. **Unit Test Coverage** - Created tests for the calculation functions
7. **Improved CSV Processing** - Using DictReader for better readability
8. **Template Validation** - Added validation to ensure templates have all required fields
9. **Performance Improvements** - Structured code for better performance
10. **Modular Design** - Split scripts into smaller, reusable modules