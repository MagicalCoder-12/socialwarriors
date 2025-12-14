import os
import sys
import subprocess

# Change to the project directory
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Run PyInstaller with the required parameters
cmd = [
    sys.executable, '-m', 'PyInstaller',
    '--onefile',
    '--console',
    '--add-data', 'assets;assets',
    '--add-data', 'stub;stub',
    '--add-data', 'templates;templates',
    '--add-data', 'villages;villages',
    '--add-data', 'config;config',
    '--paths', '.',
    '--noconfirm',
    '--icon=build/icon.ico',
    '--noupx',
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