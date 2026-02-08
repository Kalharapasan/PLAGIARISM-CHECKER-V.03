import re
import math
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Set
from collections import Counter
import difflib
import hashlib

class BasePlagiarismEngine:
    def __init__(self, config=None):
        self.config = config or {}
        self.min_match_length = self.config.get('detection.basic.min_match_length', 5)
        self.stop_words = self._load_stop_words()
        self.citation_patterns = self._load_citation_patterns()
    
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
        citations = []
        for pattern_info in self.citation_patterns:
            pattern = pattern_info['pattern']
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                citations.append({
                    'text': match.group(0),
                    'position': match.start(),
                    'type': pattern_info['type']
                })
        return citations
    
    def calculate_cosine_similarity(self, text1: str, text2: str) -> float:
        words1 = self.tokenize(text1)
        words2 = self.tokenize(text2)
        
        freq1 = Counter(words1)
        freq2 = Counter(words2)
        
        all_words = set(freq1.keys()).union(set(freq2.keys()))
        vec1 = [freq1.get(word, 0) for word in all_words]
        vec2 = [freq2.get(word, 0) for word in all_words]
        
        dot_product = sum(v1 * v2 for v1, v2 in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(v ** 2 for v in vec1))
        magnitude2 = math.sqrt(sum(v ** 2 for v in vec2))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return (dot_product / (magnitude1 * magnitude2)) * 100
    
    def find_common_sequences(self, text1: str, text2: str, min_length: int = None) -> List[Dict]:
        if min_length is None:
            min_length = self.min_match_length
        
        words1 = self.tokenize(text1)
        words2 = self.tokenize(text2)
        
        matcher = difflib.SequenceMatcher(None, words1, words2)
        matches = []
        
        for match in matcher.get_matching_blocks():
            if match.size >= min_length:
                matched_text = ' '.join(words1[match.a:match.a + match.size])
                matches.append({
                    'text': matched_text,
                    'length': match.size,
                    'position': match.a,
                    'similarity': (match.size / len(words1)) * 100 if words1 else 0
                })
        
        return sorted(matches, key=lambda x: x['length'], reverse=True)
    
    def calculate_jaccard_similarity(self, text1: str, text2: str) -> float:
        words1 = set(self.tokenize(text1))
        words2 = set(self.tokenize(text2))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return (intersection / union) * 100 if union > 0 else 0.0
    
    def generate_document_hash(self, text: str) -> str:
        return hashlib.md5(text.encode()).hexdigest()
    
    def analyze_basic(self, text: str, database: List[Dict]) -> Dict:
        results = {
            'overall_similarity': 0,
            'total_words': len(self.tokenize(text)),
            'total_sentences': len(self.get_sentences(text)),
            'citations_found': len(self.detect_citations(text)),
            'matches': []
        }
        
        for doc in database:
            doc_text = doc.get('text', '')
            similarity = self.calculate_cosine_similarity(text, doc_text)
            
            if similarity > self.config.get('detection.basic.threshold', 5):
                sequences = self.find_common_sequences(text, doc_text)
                match_info = {
                    'source': doc.get('source', 'Unknown'),
                    'url': doc.get('url', ''),
                    'similarity': round(similarity, 2),
                    'matched_sequences': sequences[:3]
                }
                results['matches'].append(match_info)
        
        if results['matches']:
            results['overall_similarity'] = round(
                sum(m['similarity'] for m in results['matches']) / len(results['matches']), 2
            )
        
        results['matches'].sort(key=lambda x: x['similarity'], reverse=True)
        return results