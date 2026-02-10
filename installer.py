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
            
    
    def create_sample_config(self):
        config = {
            "application": {
                "name": "Plagiarism Checker Pro",
                "version": "3.0",
                "default_mode": "basic"
            },
            "database": {
                "path": "data/database.sqlite",
                "backup_enabled": True
            }
        }
        
        config_path = Path("config.json")
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        
        print("✓ Created sample configuration")
    
    def create_sample_database(self):
        from core.database import DatabaseManager
        from config import Config
        
        config = Config()
        db_manager = DatabaseManager(config.config)
        sample_docs = [
            {
                'source': 'Wikipedia - Academic Integrity',
                'url': 'https://en.wikipedia.org/wiki/Academic_integrity',
                'text': '''Academic integrity is the moral code or ethical policy of academia. 
                It includes values such as avoidance of cheating or plagiarism, maintenance of 
                academic standards, and honesty and rigor in research and academic publishing.''',
                'category': 'Academic'
            },
            {
                'source': 'Educational Research Journal',
                'url': 'https://example.com/research',
                'text': '''Plagiarism is the representation of another author's language, thoughts, 
                ideas, or expressions as one's own original work. In educational contexts, proper 
                attribution is essential.''',
                'category': 'Academic'
            }
        ]
        
        for doc in sample_docs:
            db_manager.add_document(
                doc['source'],
                doc['text'],
                doc['url'],
                doc['category']
            )
        
        print("✓ Created sample database")
    
    def create_shortcuts(self):
        if self.system == "Windows":
            self._create_windows_shortcut()
        elif self.system == "Linux":
            self._create_linux_shortcut()
        elif self.system == "Darwin":
            self._create_mac_shortcut()
    
    def _create_windows_shortcut(self):
        try:
            import win32com.client
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(str(Path.home() / "Desktop" / "Plagiarism Checker.lnk"))
            shortcut.TargetPath = sys.executable
            shortcut.Arguments = "main.py --mode basic"
            shortcut.WorkingDirectory = str(Path.cwd())
            shortcut.IconLocation = sys.executable
            shortcut.save()
            print("✓ Created desktop shortcut for Windows")
        except:
            print("ℹ️ Could not create Windows shortcut (pywin32 not installed)")
    
    def _create_linux_shortcut(self):
        desktop_entry = """[Desktop Entry]
Type=Application
Name=Plagiarism Checker Pro
Comment=Advanced plagiarism detection tool
Exec=python3 {}/main.py --mode basic
Path={}
Icon={}/icon.png
Terminal=false
Categories=Education;Office;
""".format(Path.cwd(), Path.cwd(), Path.cwd())
        
        desktop_file = Path.home() / ".local" / "share" / "applications" / "plagiarism-checker.desktop"
        desktop_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(desktop_file, 'w') as f:
            f.write(desktop_entry)
        import os
        os.chmod(desktop_file, 0o755)
        
        print("✓ Created desktop entry for Linux")
    
    def _create_mac_shortcut(self):
        print("ℹ️ macOS shortcut creation requires manual setup")
    
    def run(self, install_type="basic"):
        print("=" * 60)
        print("Plagiarism Checker Pro - Installation")
        print("=" * 60)
        if not self.check_python_version():
            return False
        self.create_directories()
        packages = self.requirements['core']
        if install_type == "advanced":
            packages.extend(self.requirements['advanced'])
        elif install_type == "ultimate":
            packages.extend(self.requirements['advanced'])
            packages.extend(self.requirements['ultimate'])
        
        if not self.install_packages(packages):
            return False
        self.create_sample_config()
        self.create_sample_database()
        self.create_shortcuts()
    