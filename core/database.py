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
            
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                total_checks INTEGER DEFAULT 0,
                total_documents INTEGER DEFAULT 0,
                avg_similarity REAL DEFAULT 0,
                checks_today INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _get_connection(self):
        return sqlite3.connect(str(self.db_path))
    
    def add_document(self, source: str, text: str, url: str = '', 
                    category: str = 'General', metadata: Dict = None) -> bool:
        
        try:
            text_hash = hashlib.sha256(text.encode()).hexdigest()
            words = text.split()
            word_count = len(words)
            metadata_json = json.dumps(metadata) if metadata else '{}'
            
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO documents 
                (source, url, text, category, added_date, hash, metadata, word_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                source,
                url,
                text,
                category,
                datetime.now().isoformat(),
                text_hash,
                metadata_json,
                word_count
            ))
            cursor.execute('''
                UPDATE categories 
                SET document_count = document_count + 1 
                WHERE name = ?
            ''', (category,))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            print(f"Error adding document: {e}")
            return False
    
    def get_all_documents(self, category: str = None) -> List[Dict]:
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if category:
            cursor.execute('''
                SELECT source, url, text, category, added_date, word_count, metadata
                FROM documents 
                WHERE category = ?
                ORDER BY added_date DESC
            ''', (category,))
        else:
            cursor.execute('''
                SELECT source, url, text, category, added_date, word_count, metadata
                FROM documents 
                ORDER BY added_date DESC
            ''')
        
        docs = []
        for row in cursor.fetchall():
            try:
                metadata = json.loads(row[6]) if row[6] else {}
            except:
                metadata = {}
            
            docs.append({
                'source': row[0],
                'url': row[1],
                'text': row[2],
                'category': row[3],
                'added_date': row[4],
                'word_count': row[5],
                'metadata': metadata
            })
        for doc in docs:
            cursor.execute('''
                UPDATE documents 
                SET last_accessed = ?
                WHERE source = ?
            ''', (datetime.now().isoformat(), doc['source']))
        
        conn.commit()
        conn.close()
        return docs
    
    def search_documents(self, query: str, category: str = None) -> List[Dict]:
        


        