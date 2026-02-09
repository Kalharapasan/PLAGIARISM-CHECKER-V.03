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
    def __init__(self, max_size: int = 100):
        self.cache = {}
        self.max_size = max_size
        self.access_order = []
    
    def get(self, key: str):
        if key in self.cache:
            self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache[key]
        return None
    
    def set(self, key: str, value):
        if len(self.cache) >= self.max_size:
            lru_key = self.access_order.pop(0)
            del self.cache[lru_key]
        
        self.cache[key] = value
        self.access_order.append(key)
    
    def clear(self):
        self.cache.clear()
        self.access_order.clear()

class ErrorHandler:
    
    @staticmethod
    def handle_error(error: Exception, context: str = "") -> Dict:
        error_info = {
            'error': str(error),
            'type': type(error).__name__,
            'context': context,
            'timestamp': datetime.now().isoformat()
        }
        ErrorHandler.log_error(error_info)
        
        return error_info
    
    @staticmethod
    def log_error(error_info: Dict):
        log_file = Path("logs/errors.log")
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(error_info) + '\n')
    
def load_config(config_file: str = "config.json") -> Dict:
    config_path = Path(config_file)
    
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
    from config import Config
    return Config().default_config

def save_config(config: Dict, config_file: str = "config.json"):
    config_path = Path(config_file)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def format_file_size(size_bytes: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def format_percentage(value: float) -> str:
    return f"{value:.2f}%"

def format_timestamp(timestamp: str) -> str:
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return timestamp
    
def safe_get(dictionary: Dict, keys: List, default: Any = None) -> Any:
