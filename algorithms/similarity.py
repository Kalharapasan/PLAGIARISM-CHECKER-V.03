import re
import math
import numpy as np
from typing import Dict, List, Tuple, Optional, Any, Set, Union
from collections import Counter, defaultdict
from dataclasses import dataclass, field
import hashlib
import heapq
from functools import lru_cache

@dataclass
class SimilarityConfig:
    use_cosine: bool = True
    use_jaccard: bool = True
    use_ngram: bool = True
    use_sequence: bool = True
    use_overlap: bool = False
    use_dice: bool = False
    use_levenshtein: bool = False
    use_tfidf: bool = False
    use_semantic: bool = False
    
    cosine_threshold: float = 0.1  
    jaccard_threshold: float = 0.1
    ngram_size: int = 3
    ngram_threshold: float = 0.1
    sequence_min_length: int = 5
    sequence_threshold: float = 0.05
    overlap_threshold: float = 0.1
    dice_threshold: float = 0.1
    
    levenshtein_threshold: float = 0.8  
    tfidf_threshold: float = 0.1
    semantic_threshold: float = 0.1
    
    remove_stopwords: bool = True
    normalize_text: bool = True
    min_word_length: int = 3
    language: str = 'english'
    
    weights: Dict[str, float] = field(default_factory=lambda: {
        'cosine': 0.25,
        'jaccard': 0.20,
        'ngram': 0.20,
        'sequence': 0.25,
        'overlap': 0.05,
        'dice': 0.05
    })
    
    enable_caching: bool = True
    cache_size: int = 1000
    parallel_processing: bool = False
    max_workers: int = 4
    
class TextPreprocessor:
    ENGLISH_STOPWORDS = {
        'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'as', 'is', 'was', 'are', 'were', 'be', 'been',
        'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that',
        'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me',
        'him', 'her', 'us', 'them', 'my', 'your', 'his', 'its', 'our', 'their',
        'mine', 'yours', 'hers', 'ours', 'theirs'
    }
    
    def __init__(self, config: SimilarityConfig = None):
        self.config = config or SimilarityConfig()
        self._setup_caches()
    
    def _setup_caches(self):
        if self.config.enable_caching:
            self._tokenize_cache = lru_cache(maxsize=self.config.cache_size)(self._tokenize_uncached)
            self._normalize_cache = lru_cache(maxsize=self.config.cache_size)(self._normalize_uncached)
        else:
            self._tokenize_cache = self._tokenize_uncached
            self._normalize_cache = self._normalize_uncached
    
    def preprocess(self, text: str) -> str:
        if self.config.normalize_text:
            text = self._normalize_cache(text)
        return text
    
    def _normalize_uncached(self, text: str) -> str:
        if not text:
            return ""
        text = text.lower()
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
        text = re.sub(r'[^\w\s\'-]', ' ', text)
        text = re.sub(r'\s+', ' ', text)       
        return text.strip()
    
    def tokenize(self, text: str, remove_stopwords: bool = None) -> List[str]:
        if remove_stopwords is None:
            remove_stopwords = self.config.remove_stopwords
        
        return self._tokenize_cache(text, remove_stopwords)
    
    def _tokenize_uncached(self, text: str, remove_stopwords: bool) -> List[str]:
        if not text:
            return []
        if self.config.normalize_text:
            text = self._normalize_uncached(text)
        words = re.findall(r'\b[a-z0-9][a-z0-9\'-]*\b', text.lower())
        if self.config.min_word_length > 1:
            words = [w for w in words if len(w) >= self.config.min_word_length]
        if remove_stopwords:
            words = [w for w in words if w not in self.ENGLISH_STOPWORDS]
        
        return words
    
    def get_ngrams(self, text: str, n: int = None) -> List[str]:
        if n is None:
            n = self.config.ngram_size
        
        words = self.tokenize(text)
        
        if len(words) < n:
            return []
        
        ngrams = []
        for i in range(len(words) - n + 1):
            ngram = ' '.join(words[i:i+n])
            ngrams.append(ngram)
        
        return ngrams
    
    def get_character_ngrams(self, text: str, n: int = 3) -> List[str]:
        if not text:
            return []
        text = self._normalize_uncached(text)
        text = text.replace(' ', '')
        
        if len(text) < n:
            return []
        
        ngrams = []
        for i in range(len(text) - n + 1):
            ngram = text[i:i+n]
            ngrams.append(ngram)
        
        return ngrams

class SimilarityCalculator:
    def __init__(self, config: SimilarityConfig = None):
        self.config = config or SimilarityConfig()
        self.preprocessor = TextPreprocessor(config)
        self.tfidf_vectorizer = None
        if self.config.use_tfidf:
            self._init_tfidf()
        self.semantic_model = None
        if self.config.use_semantic:
            self._init_semantic()
    
    def _init_tfidf(self):
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=10000,
                stop_words='english',
                ngram_range=(1, 2),
                analyzer='word'
            )
        except ImportError:
            print("Warning: scikit-learn not installed. TF-IDF disabled.")
            self.config.use_tfidf = False
    
    def _init_semantic(self):
        try:
            import spacy
            try:
                self.semantic_model = spacy.load('en_core_web_sm')
            except:
                import subprocess
                import sys
                subprocess.check_call([sys.executable, '-m', 'spacy', 'download', 'en_core_web_sm'])
                self.semantic_model = spacy.load('en_core_web_sm')
        except ImportError:
            print("Warning: spaCy not installed. Semantic similarity disabled.")
            self.config.use_semantic = False
    
    def calculate_cosine_similarity(self, text1: str, text2: str) -> float:
        words1 = self.preprocessor.tokenize(text1)
        words2 = self.preprocessor.tokenize(text2)
        
        if not words1 or not words2:
            return 0.0
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
        
        similarity = dot_product / (magnitude1 * magnitude2)
        
        return max(0.0, min(1.0, similarity))
    
    def calculate_jaccard_similarity(self, text1: str, text2: str) -> float: