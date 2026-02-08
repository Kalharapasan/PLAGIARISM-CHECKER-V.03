import json
import hashlib
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
import threading
import queue
import sys

class ProgressTracker:
    def __init__(self, total: int = 100):
        self.total = total
        self.current = 0
        self.message = ""
        self.callback = None
        self.lock = threading.Lock()
    
    def update(self, increment: int = 1, message: str = None):
        with self.lock:
            self.current += increment
            if message:
                self.message = message
            
            if self.callback:
                self.callback(self.current, self.total, self.message)
    
    def set_callback(self, callback):
        self.callback = callback

class FileProcessor:
    @staticmethod
    def get_file_hash(filepath: str) -> str:
        hash_md5 = hashlib.md5()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    @staticmethod
    def get_file_info(filepath: str) -> Dict:
        path = Path(filepath)
        
        return {
            'name': path.name,
            'stem': path.stem,
            'suffix': path.suffix,
            'size': path.stat().st_size,
            'created': datetime.fromtimestamp(path.stat().st_ctime).isoformat(),
            'modified': datetime.fromtimestamp(path.stat().st_mtime).isoformat(),
            'hash': FileProcessor.get_file_hash(filepath)
        }
    
    @staticmethod
    def is_supported_format(filepath: str, supported_formats: List[str]) -> bool:
        ext = Path(filepath).suffix.lower()
        return ext in supported_formats

class TextNormalizer:
    @staticmethod
    def normalize(text: str) -> str:
        text = ' '.join(text.split())
        text = ' '.join(text.splitlines())
        text = text.replace('"', "'")
        import re
        text = re.sub(r'[^\w\s.,;:!?\'"-]', ' ', text)
        
        return text.strip()
    
    @staticmethod
    def remove_formatting(text: str) -> str:
        import re
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'[*_`#\[\]]', ' ', text)
        text = re.sub(r'http[s]?://\S+', ' ', text)
        text = re.sub(r'\S+@\S+', ' ', text)
        
        return TextNormalizer.normalize(text)

class CacheManager:
    
    def get(self, key: str):