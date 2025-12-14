# Social Wars Build Instructions

## Prerequisites
- Python 3.x installed
- PyInstaller installed (`pip install pyinstaller`)

## Automated Build Process
1. Navigate to the `build` directory
2. Run `build.bat`
3. The script will automatically:
   - Use PyInstaller to create a distributable version
   - Create necessary directories (work, dist, bundle)
   - Package all required files

## Manual Bundle Creation (if automated build fails)
If the automated build process fails, you can manually create the bundle using the following steps:

1. Create the directory structure:
   ```
   build/bundle/social-warriors_0.03a/bundle/
   ```

2. Copy all Python files (*.py) from the root directory to the bundle folder

3. Copy all Markdown documentation files (*.md) from the root directory to the bundle folder

4. Copy the LICENSE file and requirements.txt to the bundle folder

5. Copy the following directories and their contents to the bundle folder:
   - config/
   - mods/
   - stub/
   - templates/
   - tools/

## Files Included in Bundle
The bundle includes all project files except:
- Game data folders (villages/)
- Base Python library files (base_library.zip, python3X.dll)
- Build artifacts (work/, dist/ directories)

## Distribution
The final bundle can be found at:
```
build/bundle/social-warriors_0.03a/bundle/
```

This directory contains everything needed to run the Social Wars preservation project on a machine without Python installed.