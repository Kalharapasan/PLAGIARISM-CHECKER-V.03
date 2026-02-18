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