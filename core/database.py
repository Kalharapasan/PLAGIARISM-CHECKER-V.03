import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import hashlib

class DatabaseManager:
    
    def _initialize_db(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                url TEXT,
                text TEXT NOT NULL,
                category TEXT DEFAULT 'General',
                added_date TEXT,
                last_accessed TEXT,
                hash TEXT UNIQUE,
                metadata TEXT,
                word_count INTEGER DEFAULT 0
            )
        ''')