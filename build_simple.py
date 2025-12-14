import os
import sys
import subprocess

# Change to the project directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Run PyInstaller with the required parameters
cmd = [
    sys.executable, '-m', 'PyInstaller',
    '--onedir',
    '--console',
    '--noupx',
    '--noconfirm',
    '--runtime-hook=build/path_bundle.py',
    '--add-data', 'assets;assets',
    '--add-data', 'config;config',
    '--add-data', 'stub;stub',
    '--add-data', 'templates;templates',
    '--add-data', 'villages;villages',
    '--paths', '.',
    '--workpath', 'build/work',
    '--distpath', 'build/dist',
    '--specpath', 'build/bundle',
    '--icon=build/icon.ico',
    '--name', 'social-warriors_0.02a',
    'server.py'
]

print("Running build command:")
print(' '.join(cmd))

try:
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    print("Build completed successfully!")
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print("Build failed with error:")
    print(e.stderr)
    sys.exit(1)