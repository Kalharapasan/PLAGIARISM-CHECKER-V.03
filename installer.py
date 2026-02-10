#!/usr/bin/env python3
import sys
import subprocess
import platform
from pathlib import Path
import json

class Installer:
    
    def check_python_version(self):
        if self.python_version.major < 3 or (self.python_version.major == 3 and self.python_version.minor < 8):
            print("❌ Python 3.8 or higher is required")
            return False
        print(f"✓ Python {self.python_version.major}.{self.python_version.minor} detected")
        return True
    
    def install_packages(self, packages):
        for package in packages:
            print(f"Installing {package}...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"✓ {package} installed successfully")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install {package}: {e}")
                return False
        return True
    
    def create_directories(self):
        directories = [
            'data',
            'data/sample_documents',
            'data/templates',
            'reports',
            'logs',
            'exports',
            'backups'
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            print(f"✓ Created directory: {directory}")