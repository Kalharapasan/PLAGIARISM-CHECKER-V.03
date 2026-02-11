import re
import string
import math
import json
from typing import Dict, List, Tuple, Optional, Any, Set, Union
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from enum import Enum
import hashlib
from datetime import datetime
import itertools
import numpy as np

class TextCategory(Enum):
    ACADEMIC = "academic"
    TECHNICAL = "technical"
    LITERARY = "literary"
    JOURNALISTIC = "journalistic"
    CASUAL = "casual"
    LEGAL = "legal"
    MEDICAL = "medical"
    SCIENTIFIC = "scientific"
    UNKNOWN = "unknown"

class Language(Enum):
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    ITALIAN = "it"
    PORTUGUESE = "pt"
    DUTCH = "nl"
    RUSSIAN = "ru"
    CHINESE = "zh"
    JAPANESE = "ja"
    KOREAN = "ko"
    ARABIC = "ar"
    HINDI = "hi"
    UNKNOWN = "unknown"
    

@dataclass
class NLPAnalysis:
    token_count: int = 0
    sentence_count: int = 0
    paragraph_count: int = 0
    character_count: int = 0
    word_count: int = 0
    vocabulary_size: int = 0
    type_token_ratio: float = 0.0
    hapax_legomena: int = 0 
    flesch_reading_ease: float = 0.0
    flesch_kincaid_grade: float = 0.0
    gunning_fog_index: float = 0.0
    smog_index: float = 0.0
    coleman_liau_index: float = 0.0
    automated_readability_index: float = 0.0
    dale_chall_score: float = 0.0
    avg_sentence_length: float = 0.0
    avg_word_length: float = 0.0
    avg_syllables_per_word: float = 0.0
    passive_voice_percentage: float = 0.0
    lexical_density: float = 0.0
