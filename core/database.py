import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import hashlib

class DatabaseManager:
    
    def _initialize_db(self):