import json
import hashlib
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
import threading
import queue
import sys

class ProgressTracker:
    
    def update(self, increment: int = 1, message: str = None):
        with self.lock:
            self.current += increment
            if message:
                self.message = message
            
            if self.callback:
                self.callback(self.current, self.total, self.message)
    
    def set_callback(self, callback):
        self.callback = callback