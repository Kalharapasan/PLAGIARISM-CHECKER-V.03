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