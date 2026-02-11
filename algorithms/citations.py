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
    text_category: TextCategory = TextCategory.UNKNOWN
    detected_language: Language = Language.UNKNOWN
    topics: List[str] = field(default_factory=list)
    key_phrases: List[Dict[str, Any]] = field(default_factory=list)
    named_entities: List[Dict[str, Any]] = field(default_factory=list)
    
    citation_count: int = 0
    reference_count: int = 0
    has_abstract: bool = False
    has_introduction: bool = False
    has_conclusion: bool = False
    has_references: bool = False
    
    sentiment_score: float = 0.0 
    subjectivity_score: float = 0.0 
    formality_score: float = 0.0 
    
    coherence_score: float = 0.0 
    cohesion_score: float = 0.0  
    transition_word_density: float = 0.0
    
    processing_time: float = 0.0
    timestamp: str = ""
    text_hash: str = ""
    
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'basic_statistics': {
                'token_count': self.token_count,
                'sentence_count': self.sentence_count,
                'paragraph_count': self.paragraph_count,
                'character_count': self.character_count,
                'word_count': self.word_count
            },
            'vocabulary_analysis': {
                'vocabulary_size': self.vocabulary_size,
                'type_token_ratio': self.type_token_ratio,
                'hapax_legomena': self.hapax_legomena
            },
            'readability_scores': {
                'flesch_reading_ease': self.flesch_reading_ease,
                'flesch_kincaid_grade': self.flesch_kincaid_grade,
                'gunning_fog_index': self.gunning_fog_index,
                'smog_index': self.smog_index,
                'coleman_liau_index': self.coleman_liau_index,
                'automated_readability_index': self.automated_readability_index,
                'dale_chall_score': self.dale_chall_score
            },
            'style_analysis': {
                'avg_sentence_length': self.avg_sentence_length,
                'avg_word_length': self.avg_word_length,
                'avg_syllables_per_word': self.avg_syllables_per_word,
                'passive_voice_percentage': self.passive_voice_percentage,
                'lexical_density': self.lexical_density
            },
            'content_analysis': {
                'text_category': self.text_category.value,
                'detected_language': self.detected_language.value,
                'topics': self.topics,
                'key_phrases': self.key_phrases,
                'named_entities': self.named_entities
            },
            'academic_indicators': {
                'citation_count': self.citation_count,
                'reference_count': self.reference_count,
                'has_abstract': self.has_abstract,
                'has_introduction': self.has_introduction,
                'has_conclusion': self.has_conclusion,
                'has_references': self.has_references
            },
            'sentiment_tone': {
                'sentiment_score': self.sentiment_score,
                'subjectivity_score': self.subjectivity_score,
                'formality_score': self.formality_score
            },
            'coherence_cohesion': {
                'coherence_score': self.coherence_score,
                'cohesion_score': self.cohesion_score,
                'transition_word_density': self.transition_word_density
            },
            'metadata': {
                'processing_time': self.processing_time,
                'timestamp': self.timestamp,
                'text_hash': self.text_hash
            }
        }

class TextProcessor:
