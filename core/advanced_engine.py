from typing import List, Dict, Optional
from .base_engine import BasePlagiarismEngine
from collections import Counter
import math

class AdvancedPlagiarismEngine(BasePlagiarismEngine):
    
    def calculate_ngram_similarity(self, text1: str, text2: str, n: int = 3) -> float:
        words1 = self.tokenize(text1)
        words2 = self.tokenize(text2)
        
        if len(words1) < n or len(words2) < n:
            return 0.0
        
        ngrams1 = set(' '.join(words1[i:i+n]) for i in range(len(words1) - n + 1))
        ngrams2 = set(' '.join(words2[i:i+n]) for i in range(len(words2) - n + 1))
        
        if not ngrams1 or not ngrams2:
            return 0.0
        
        intersection = len(ngrams1.intersection(ngrams2))
        union = len(ngrams1.union(ngrams2))
        
        return (intersection / union) * 100 if union > 0 else 0.0
    
    def calculate_overlap_coefficient(self, text1: str, text2: str) -> float:
        words1 = set(self.tokenize(text1))
        words2 = set(self.tokenize(text2))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        min_size = min(len(words1), len(words2))
        
        return (intersection / min_size) * 100 if min_size > 0 else 0.0