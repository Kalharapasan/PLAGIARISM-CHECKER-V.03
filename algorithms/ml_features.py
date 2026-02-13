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
        
        except ImportError as e:
            print(f"⚠ Some ML components not available: {e}")