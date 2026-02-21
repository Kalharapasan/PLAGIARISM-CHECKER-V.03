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
        words1 = set(self.preprocessor.tokenize(text1))
        words2 = set(self.preprocessor.tokenize(text2))
        if not words1 and not words2:
            return 1.0
        if not words1 or not words2:
            return 0.0
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def calculate_ngram_similarity(self, text1: str, text2: str, n: int = None) -> float:
        if n is None:
            n = self.config.ngram_size
        ngrams1 = set(self.preprocessor.get_ngrams(text1, n))
        ngrams2 = set(self.preprocessor.get_ngrams(text2, n))
        if not ngrams1 and not ngrams2:
            return 1.0
        if not ngrams1 or not ngrams2:
            return 0.0 
        intersection = len(ngrams1.intersection(ngrams2))
        union = len(ngrams1.union(ngrams2))
        
        return intersection / union if union > 0 else 0.0
    
    def calculate_character_ngram_similarity(self, text1: str, text2: str, n: int = 3) -> float:
        ngrams1 = set(self.preprocessor.get_character_ngrams(text1, n))
        ngrams2 = set(self.preprocessor.get_character_ngrams(text2, n))
        if not ngrams1 and not ngrams2:
            return 1.0
        if not ngrams1 or not ngrams2:
            return 0.0 
        intersection = len(ngrams1.intersection(ngrams2))
        union = len(ngrams1.union(ngrams2))
        
        return intersection / union if union > 0 else 0.0
    
    def find_common_sequences(self, text1: str, text2: str, min_length: int = None) -> List[Dict[str, Any]]:
        if min_length is None:
            min_length = self.config.sequence_min_length
        words1 = self.preprocessor.tokenize(text1)
        words2 = self.preprocessor.tokenize(text2)
        
        if not words1 or not words2:
            return []
        m, n = len(words1), len(words2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        max_length = 0
        end_pos = 0
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if words1[i-1] == words2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                    if dp[i][j] > max_length:
                        max_length = dp[i][j]
                        end_pos = i
                else:
                    dp[i][j] = 0
        sequences = []
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if dp[i][j] >= min_length:
                    if i == m or j == n or words1[i] != words2[j]:
                        length = dp[i][j]
                        start1 = i - length
                        start2 = j - length
                        
                        sequence_text = ' '.join(words1[start1:i])
                        
                        sequences.append({
                            'text': sequence_text,
                            'length': length,
                            'position1': start1,
                            'position2': start2,
                            'words1': words1[start1:i],
                            'words2': words2[start2:j]
                        })
        sequences.sort(key=lambda x: x['length'], reverse=True)
        filtered_sequences = []
        used_positions = set()
        for seq in sequences:
            overlap = False
            for pos in range(seq['position1'], seq['position1'] + seq['length']):
                if pos in used_positions:
                    overlap = True
                    break
            if not overlap:
                filtered_sequences.append(seq)
                for pos in range(seq['position1'], seq['position1'] + seq['length']):
                    used_positions.add(pos)
        
        return filtered_sequences
    
    def calculate_sequence_similarity(self, text1: str, text2: str) -> float:
        words1 = self.preprocessor.tokenize(text1)
        words2 = self.preprocessor.tokenize(text2)
        if not words1 or not words2:
            return 0.0
        sequences = self.find_common_sequences(text1, text2)
        
        if not sequences:
            return 0.0
        total_matched = sum(seq['length'] for seq in sequences)
        total_words = len(words1) + len(words2)
        similarity = (2 * total_matched) / total_words if total_words > 0 else 0.0     
        return min(1.0, similarity)
    
    def calculate_overlap_coefficient(self, text1: str, text2: str) -> float:
        words1 = set(self.preprocessor.tokenize(text1))
        words2 = set(self.preprocessor.tokenize(text2))
        if not words1 and not words2:
            return 1.0
        if not words1 or not words2:
            return 0.0
        intersection = len(words1.intersection(words2))
        min_size = min(len(words1), len(words2))
        
        return intersection / min_size if min_size > 0 else 0.0
    
    def calculate_dice_coefficient(self, text1: str, text2: str) -> float:
        words1 = set(self.preprocessor.tokenize(text1))
        words2 = set(self.preprocessor.tokenize(text2))
        if not words1 and not words2:
            return 1.0 
        if not words1 or not words2:
            return 0.0
        intersection = len(words1.intersection(words2))
        total = len(words1) + len(words2)
        
        return (2 * intersection) / total if total > 0 else 0.0
    
    def calculate_levenshtein_similarity(self, text1: str, text2: str) -> float:
        text1 = self.preprocessor.preprocess(text1)
        text2 = self.preprocessor.preprocess(text2)
        if len(text1) == 0 and len(text2) == 0:
            return 1.0
        if len(text1) == 0 or len(text2) == 0:
            return 0.0
        if len(text1) > len(text2):
            text1, text2 = text2, text1
        previous_row = list(range(len(text2) + 1))
        for i, c1 in enumerate(text1):
            current_row = [i + 1]
            for j, c2 in enumerate(text2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        distance = previous_row[-1]
        max_len = max(len(text1), len(text2))
        similarity = 1 - (distance / max_len) if max_len > 0 else 1.0
        
        return max(0.0, similarity)
    
    def calculate_tfidf_similarity(self, text1: str, text2: str) -> float:
        if self.tfidf_vectorizer is None:
            return 0.0
        try:
            from sklearn.metrics.pairwise import cosine_similarity
            tfidf_matrix = self.tfidf_vectorizer.fit_transform([text1, text2])
            similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            
            return float(similarity_matrix[0][0])
        except Exception as e:
            print(f"Warning: TF-IDF similarity calculation failed: {e}")
            return 0.0