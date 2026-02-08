import re
import math
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Set
from collections import Counter
import difflib
import hashlib

class BasePlagiarismEngine:
    
    def _load_stop_words(self) -> Set[str]:
        return {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }
    
    def _load_citation_patterns(self) -> List[Dict]:
        return [
            {'pattern': r'\(([^)]+),\s*\d{4}\)', 'type': 'apa'},
            {'pattern': r'\[(\d+)\]', 'type': 'numerical'},
            {'pattern': r'according to ([^,\.]+)', 'type': 'narrative'},
            {'pattern': r'([A-Z][a-z]+ et al\.)', 'type': 'author_etal'}
        ]