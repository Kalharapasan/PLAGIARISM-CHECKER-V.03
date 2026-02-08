import re
import math
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Set
from collections import Counter
import difflib
import hashlib

class BasePlagiarismEngine:
    
    def _load_stop_words(self) -> Set[str]:
        return {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }
    
    def _load_citation_patterns(self) -> List[Dict]:
        return [
            {'pattern': r'\(([^)]+),\s*\d{4}\)', 'type': 'apa'},
            {'pattern': r'\[(\d+)\]', 'type': 'numerical'},
            {'pattern': r'according to ([^,\.]+)', 'type': 'narrative'},
            {'pattern': r'([A-Z][a-z]+ et al\.)', 'type': 'author_etal'}
        ]
    
    def extract_text(self, filepath: str) -> str:
        ext = Path(filepath).suffix.lower()
        
        if ext == '.txt':
            return self._extract_txt(filepath)
        elif ext == '.docx':
            return self._extract_docx(filepath)
        elif ext == '.pdf':
            return self._extract_pdf(filepath)
        else:
            raise ValueError(f"Unsupported format: {ext}")
    
    def _extract_txt(self, filepath: str) -> str:
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        for encoding in encodings:
            try:
                with open(filepath, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    
    def _extract_docx(self, filepath: str) -> str:
        try:
            from docx import Document
            doc = Document(filepath)
            text = []
            for para in doc.paragraphs:
                if para.text.strip():
                    text.append(para.text)
            return '\n'.join(text)
        except ImportError:
            import zipfile
            with zipfile.ZipFile(filepath) as docx:
                xml_content = docx.read('word/document.xml').decode('utf-8')
                text = re.sub(r'<[^>]+>', ' ', xml_content)
                return ' '.join(text.split())
    
    def _extract_pdf(self, filepath: str) -> str:
        text = []
        try:
            import pdfplumber
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text.append(page_text)
            if text:
                return '\n'.join(text)
        except ImportError:
            pass
        try:
            from pypdf import PdfReader
            reader = PdfReader(filepath)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
            return '\n'.join(text)
        except ImportError:
            raise Exception("PDF support requires pdfplumber or pypdf")
    
    def tokenize(self, text: str) -> List[str]:
        words = re.findall(r'\b[a-z0-9]+\b', text.lower())
        return [w for w in words if w not in self.stop_words and len(w) > 2]

    def get_sentences(self, text: str) -> List[str]:
        sentences = re.split(r'[.!?]+\s+', text)
        return [s.strip() for s in sentences if len(s.strip()) > 10]
    
    def detect_citations(self, text: str) -> List[Dict]: