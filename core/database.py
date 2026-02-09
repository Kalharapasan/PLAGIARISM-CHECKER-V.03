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
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_documents_category ON documents(category)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_documents_hash ON documents(hash)')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS check_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                check_date TEXT,
                similarity_score REAL,
                total_words INTEGER,
                matched_sources INTEGER,
                report_path TEXT,
                analysis_data TEXT
            )
        ''')
        
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_history_date ON check_history(check_date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_history_score ON check_history(similarity_score)')