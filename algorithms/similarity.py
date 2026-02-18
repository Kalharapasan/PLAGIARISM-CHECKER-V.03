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