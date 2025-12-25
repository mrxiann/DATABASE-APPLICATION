import PyInstaller.__main__
import os
import sys

# Get current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the main script
main_script = os.path.join(current_dir, "main.py")

# PyInstaller options
options = [
    main_script,                    # Main script
    '--name=SK_Youth_Management_and_Information_System',       # Name of the executable
    '--onefile',                    # Create a single executable file
    '--windowed',                   # Don't show console window
    '--icon=icon.ico',              # Icon file (optional)
    '--add-data=database.py;.',     # Include database setup script
    '--hidden-import=mysql.connector',  # Hidden imports
    '--hidden-import=mysql.connector.plugins',
    '--hidden-import=pil',
    '--hidden-import=PIL',
    '--hidden-import=PIL._imaging',
    '--hidden-import=qrcode',
    '--hidden-import=qrcode.image.pil',
    '--collect-data=qrcode',        # Collect qrcode data files
    '--collect-data=PIL',           # Collect PIL data files
    '--exclude-module=tkinter',     # Don't exclude tkinter
    '--clean',                      # Clean PyInstaller cache
    '--noconfirm',                  # Don't ask for confirmation
]

# Add all Python files in the directory
for file in os.listdir(current_dir):
    if file.endswith('.py') and file != 'build_spec.py':
        options.append(f'--add-data={file};.')

print("Building executable with PyInstaller...")
print(f"Main script: {main_script}")
print(f"Options: {options}")

try:
    PyInstaller.__main__.run(options)
    print("\n Build completed successfully!")
    print(f"Executable should be in: {os.path.join(current_dir, 'dist')}")
except Exception as e:
    print(f"\n Build failed: {e}")
    print("Trying alternative approach...")