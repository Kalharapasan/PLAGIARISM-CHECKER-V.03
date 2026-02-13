import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional, Any, Union
from collections import Counter, defaultdict
import pickle
import json
import warnings
from pathlib import Path
import hashlib
from datetime import datetime

warnings.filterwarnings('ignore')

class MLFeatures:
    
    
    def _initialize_ml_components(self):
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
            from sklearn.preprocessing import StandardScaler, MinMaxScaler
            from sklearn.decomposition import PCA, TruncatedSVD, LatentDirichletAllocation
            from sklearn.cluster import KMeans, DBSCAN
            from sklearn.ensemble import IsolationForest
            from sklearn.neighbors import LocalOutlierFactor
            self.vectorizers['tfidf'] = TfidfVectorizer(
                max_features=5000,
                stop_words='english',
                ngram_range=(1, 3),
                min_df=2,
                max_df=0.95
            )
            
            self.vectorizers['count'] = CountVectorizer(
                max_features=3000,
                stop_words='english',
                ngram_range=(1, 2)
            )
            
            self.vectorizers['char'] = CountVectorizer(
                analyzer='char',
                ngram_range=(3, 5),
                max_features=2000
            )
            self.models['scaler'] = StandardScaler()
            self.models['minmax'] = MinMaxScaler()
            self.models['pca'] = PCA(n_components=50, random_state=42)
            self.models['svd'] = TruncatedSVD(n_components=100, random_state=42)
            self.models['lda'] = LatentDirichletAllocation(
                n_components=10,
                random_state=42,
                max_iter=10
            )
            self.models['kmeans'] = KMeans(n_clusters=5, random_state=42)
            self.models['dbscan'] = DBSCAN(eps=0.5, min_samples=5)
            self.models['isolation_forest'] = IsolationForest(
                contamination=0.1,
                random_state=42
            )
            self.models['lof'] = LocalOutlierFactor(
                contamination=0.1,
                novelty=True
            )
            
            print("✓ ML components initialized successfully")
        
        except ImportError as e:
            print(f"⚠ Some ML components not available: {e}")
    
    def extract_linguistic_features(self, text: str) -> Dict[str, float]:
        features['char_count'] = len(text)
        features['word_count'] = len(text.split())
        features['sentence_count'] = self._count_sentences(text)
        features['paragraph_count'] = self._count_paragraphs(text)
        words = text.split()
        if words:
            features['avg_word_length'] = sum(len(w) for w in words) / len(words)
            features['max_word_length'] = max(len(w) for w in words)
            features['unique_word_ratio'] = len(set(words)) / len(words)
            word_freq = Counter(words)
            features['vocabulary_richness'] = len(word_freq) / len(words)
            common_words = {'the', 'and', 'of', 'to', 'in', 'a', 'is', 'that', 'for', 'it'}
            common_word_count = sum(1 for w in words if w.lower() in common_words)
            features['common_word_ratio'] = common_word_count / len(words)
        if text:
            features['digit_ratio'] = sum(c.isdigit() for c in text) / len(text)
            features['letter_ratio'] = sum(c.isalpha() for c in text) / len(text)
            features['space_ratio'] = sum(c.isspace() for c in text) / len(text)
            features['punctuation_ratio'] = sum(c in '.,;:!?\'"()-[]{}' for c in text) / len(text)
            features['uppercase_ratio'] = sum(c.isupper() for c in text) / len(text)
        features['avg_sentence_length'] = features['word_count'] / max(features['sentence_count'], 1)
        features['avg_paragraph_length'] = features['sentence_count'] / max(features['paragraph_count'], 1)
        complex_words = [w for w in words if len(w) > 6]
        features['complex_word_ratio'] = len(complex_words) / max(len(words), 1)
        hapax_count = sum(1 for word, count in word_freq.items() if count == 1)
        features['hapax_legomena_ratio'] = hapax_count / max(len(word_freq), 1)
        
        return features
    
    def extract_stylometric_features(self, text: str) -> Dict[str, float]:
        features = {}
        function_words = {
            'the', 'and', 'to', 'of', 'a', 'in', 'that', 'is', 'was', 'he', 'for', 'it',
            'with', 'as', 'his', 'on', 'be', 'at', 'by', 'I', 'this', 'had', 'not', 'are',
            'but', 'from', 'or', 'have', 'an', 'they', 'which', 'one', 'you', 'were', 'her',
            'all', 'she', 'there', 'would', 'their', 'we', 'him', 'been', 'has', 'when',
            'who', 'will', 'more', 'no', 'if', 'out', 'so', 'said', 'what', 'up', 'its',
            'about', 'into', 'than', 'them', 'can', 'only', 'other', 'new', 'some', 'could',
            'time', 'these', 'two', 'may', 'then', 'do', 'first', 'any', 'my', 'now', 'such',
            'like', 'our', 'over', 'man', 'me', 'even', 'most', 'made', 'after', 'also',
            'did', 'many', 'before', 'must', 'through', 'back', 'years', 'where', 'much',
            'your', 'way', 'well', 'should', 'because', 'each', 'just', 'those', 'people',
            'how', 'too', 'little', 'state', 'good', 'very', 'make', 'world', 'still',
            'own', 'see', 'men', 'work', 'long', 'get', 'here', 'between', 'both', 'life',
            'being', 'under', 'never', 'day', 'same', 'another', 'know', 'while', 'last',
            'might', 'us', 'great', 'old', 'year', 'off', 'come', 'since', 'against',
            'go', 'came', 'right', 'used', 'take', 'three'
        }
        
        words = text.lower().split()
        if words:
            function_word_count = sum(1 for w in words if w in function_words)
            features['function_word_ratio'] = function_word_count / len(words)
        pos_tags = self._estimate_pos_tags(text)
        for pos, count in pos_tags.items():
            features[f'pos_{pos}_ratio'] = count / max(sum(pos_tags.values()), 1)
        sentences = self._extract_sentences(text)
        if sentences:
            sent_lengths = [len(s.split()) for s in sentences]
            features['sentence_length_mean'] = np.mean(sent_lengths)
            features['sentence_length_std'] = np.std(sent_lengths)
            features['sentence_length_cv'] = features['sentence_length_std'] / max(features['sentence_length_mean'], 1)
            sentence_beginnings = [s.split()[0].lower() if s.split() else '' for s in sentences[:50]]
            conjunction_beginnings = sum(1 for w in sentence_beginnings if w in {'and', 'but', 'or', 'however', 'therefore', 'thus', 'hence'})
            features['conjunction_sentence_start_ratio'] = conjunction_beginnings / len(sentences)
        sophisticated_words = self._identify_sophisticated_words(text)
        features['sophisticated_word_ratio'] = len(sophisticated_words) / max(len(words), 1)
        punctuation_counts = Counter(c for c in text if c in '.,;:!?\'"()-[]{}')
        for punct, count in punctuation_counts.items():
            features[f'punctuation_{punct}_ratio'] = count / max(len(text), 1)
        word_lengths = [len(w) for w in words]
        if word_lengths:
            features['word_length_mean'] = np.mean(word_lengths)
            features['word_length_std'] = np.std(word_lengths)
            features['word_length_skew'] = self._calculate_skewness(word_lengths)
        ttr_segments = self._calculate_ttr_segments(text)
        features['ttr_mean'] = np.mean(ttr_segments)
        features['ttr_std'] = np.std(ttr_segments)
        word_freq = Counter(words)
        dislegomena_count = sum(1 for count in word_freq.values() if count == 2)
        features['dislegomena_ratio'] = dislegomena_count / max(len(word_freq), 1)
        
        return features
    
    def extract_nlp_features(self, text: str) -> Dict[str, Any]:
        features = {}
        spacy_features = self._extract_spacy_features(text)
        features.update(spacy_features)