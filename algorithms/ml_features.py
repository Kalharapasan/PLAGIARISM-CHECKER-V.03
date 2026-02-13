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
        
        except ImportError as e:
            print(f"⚠ Some ML components not available: {e}")