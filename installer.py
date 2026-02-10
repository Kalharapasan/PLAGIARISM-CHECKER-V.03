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