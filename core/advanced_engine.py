from typing import List, Dict, Optional
from .base_engine import BasePlagiarismEngine
from collections import Counter
import math

class AdvancedPlagiarismEngine(BasePlagiarismEngine):
    
    def calculate_ngram_similarity(self, text1: str, text2: str, n: int = 3) -> float: