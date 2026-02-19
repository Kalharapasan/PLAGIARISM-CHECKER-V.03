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