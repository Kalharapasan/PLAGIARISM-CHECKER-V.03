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
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                color TEXT DEFAULT '#667eea',
                document_count INTEGER DEFAULT 0
            )
        ''')
        
        default_categories = [
            ('General', 'General reference documents', '#667eea'),
            ('Academic', 'Academic papers and articles', '#4299e1'),
            ('Technical', 'Technical documentation', '#48bb78'),
            ('Literature', 'Literary works', '#ed8936'),
            ('News', 'News articles', '#f56565'),
            ('Research', 'Research papers', '#9f7aea'),
            ('Legal', 'Legal documents', '#ed64a6'),
            ('Business', 'Business documents', '#38b2ac')
        ]
        
        for name, desc, color in default_categories:
            cursor.execute('''
                INSERT OR IGNORE INTO categories (name, description, color)
                VALUES (?, ?, ?)
            ''', (name, desc, color))