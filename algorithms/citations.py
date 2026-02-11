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
    STOPWORDS = {
        'en': {
            'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'as', 'is', 'was', 'are', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'must', 'can', 'shall', 'ought',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 
            'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 
            'her', 'its', 'our', 'their', 'mine', 'yours', 'hers', 'ours', 'theirs',
            'myself', 'yourself', 'himself', 'herself', 'itself', 'ourselves',
            'yourselves', 'themselves', 'what', 'which', 'who', 'whom', 'whose',
            'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few',
            'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
            'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will',
            'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y',
            'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven',
            'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn',
            'weren', 'won', 'wouldn'
        },
        'es': {
            'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las',
            'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al', 'lo', 'como',
            'más', 'pero', 'sus', 'le', 'ya', 'o', 'este', 'sí', 'porque',
            'esta', 'entre', 'cuando', 'muy', 'sin', 'sobre', 'también', 'me',
            'hasta', 'hay', 'donde', 'quien', 'desde', 'todo', 'nos', 'durante',
            'todos', 'uno', 'les', 'ni', 'contra', 'otros', 'ese', 'eso', 'ante',
            'ellos', 'e', 'esto', 'mí', 'antes', 'algunos', 'qué', 'unos', 'yo',
            'otro', 'otras', 'otra', 'él', 'tanto', 'esa', 'estos', 'mucho',
            'quienes', 'nada', 'muchos', 'cual', 'poco', 'ella', 'estar', 'estas',
            'algunas', 'algo', 'nosotros', 'mi', 'mis', 'tú', 'te', 'ti', 'tu',
            'tus', 'ellas', 'nosotras', 'vosotros', 'vosotras', 'os', 'mío',
            'mía', 'míos', 'mías', 'tuyo', 'tuya', 'tuyos', 'tuyas', 'suyo',
            'suya', 'suyos', 'suyas', 'nuestro', 'nuestra', 'nuestros',
            'nuestras', 'vuestro', 'vuestra', 'vuestros', 'vuestras', 'esos',
            'esas', 'estoy', 'estás', 'está', 'estamos', 'estáis', 'están',
            'esté', 'estés', 'estemos', 'estéis', 'estén', 'estaré', 'estarás',
            'estará', 'estaremos', 'estaréis', 'estarán', 'estaría', 'estarías',
            'estaríamos', 'estaríais', 'estarían', 'estaba', 'estabas', 'estábamos',
            'estabais', 'estaban', 'estuve', 'estuviste', 'estuvo', 'estuvimos',
            'estuvisteis', 'estuvieron', 'estuviera', 'estuvieras', 'estuviéramos',
            'estuvierais', 'estuvieran', 'estuviese', 'estuvieses', 'estuviésemos',
            'estuvieseis', 'estuviesen', 'estando', 'estado', 'estada', 'estados',
            'estadas', 'estad', 'he', 'has', 'ha', 'hemos', 'habéis', 'han',
            'haya', 'hayas', 'hayamos', 'hayáis', 'hayan', 'habré', 'habrás',
            'habrá', 'habremos', 'habréis', 'habrán', 'habría', 'habrías',
            'habríamos', 'habríais', 'habrían', 'había', 'habías', 'habíamos',
            'habíais', 'habían', 'hube', 'hubiste', 'hubo', 'hubimos', 'hubisteis',
            'hubieron', 'hubiera', 'hubieras', 'hubiéramos', 'hubierais',
            'hubieran', 'hubiese', 'hubieses', 'hubiésemos', 'hubieseis',
            'hubiesen', 'habiendo', 'habido', 'habida', 'habidos', 'habidas'
        }
    }
    
    ACADEMIC_WORDS = {
        'analysis', 'approach', 'area', 'assessment', 'assume', 'authority',
        'available', 'benefit', 'concept', 'consistent', 'constitutional',
        'context', 'contract', 'create', 'data', 'definition', 'derived',
        'distribution', 'economic', 'environment', 'established', 'estimate',
        'evidence', 'export', 'factors', 'financial', 'formula', 'function',
        'identified', 'income', 'indicate', 'individual', 'interpretation',
        'involved', 'issues', 'labour', 'legal', 'legislation', 'major',
        'method', 'occur', 'percent', 'period', 'policy', 'principle',
        'procedure', 'process', 'required', 'research', 'response', 'role',
        'section', 'sector', 'significant', 'similar', 'source', 'specific',
        'structure', 'theory', 'variables', 'achieve', 'acquisition',
        'administration', 'affect', 'appropriate', 'aspects', 'assistance',
        'categories', 'chapter', 'commission', 'community', 'complex',
        'computer', 'conclusion', 'conduct', 'consequences', 'construction',
        'consumer', 'credit', 'cultural', 'design', 'distinction', 'elements',
        'equation', 'evaluation', 'features', 'final', 'focus', 'impact',
        'injury', 'institute', 'investment', 'items', 'journal', 'maintenance',
        'normal', 'obtained', 'participation', 'perceived', 'positive',
        'potential', 'previous', 'primary', 'purchase', 'range', 'region',
        'regulations', 'relevant', 'resident', 'resources', 'restricted',
        'security', 'sought', 'select', 'site', 'strategies', 'survey', 'text',
        'traditional', 'transfer', 'alternative', 'circumstances', 'comments',
        'compensation', 'components', 'consent', 'considerable', 'constant',
        'constraints', 'contribution', 'convention', 'coordination', 'core',
        'corporate', 'corresponding', 'criteria', 'deduction', 'demonstrate',
        'document', 'dominant', 'emphasis', 'ensure', 'excluded', 'framework',
        'funds', 'illustrated', 'immigration', 'implies', 'initial', 'instance',
        'interaction', 'justification', 'layer', 'link', 'location', 'maximum',
        'minorities', 'negative', 'outcomes', 'partnership', 'philosophy',
        'physical', 'proportion', 'published', 'reaction', 'registered',
        'reliance', 'removed', 'scheme', 'sequence', 'sex', 'shift', 'specified',
        'sufficient', 'task', 'technical', 'techniques', 'technology', 'validity',
        'volume', 'access', 'adequate', 'annual', 'apparent', 'approximated',
        'attitudes', 'attributed', 'civil', 'code', 'commitment', 'communication',
        'concentration', 'conference', 'contrast', 'cycle', 'debate', 'despite',
        'dimensions', 'domestic', 'emerged', 'error', 'ethnic', 'goals', 'granted',
        'hence', 'hypothesis', 'implementation', 'implications', 'imposed',
        'integration', 'internal', 'investigation', 'job', 'label', 'mechanism',
        'obvious', 'occupational', 'option', 'output', 'overall', 'parallel',
        'parameters', 'phase', 'predicted', 'principal', 'prior', 'professional',
        'project', 'promote', 'regime', 'resolution', 'retained', 'series',
        'statistics', 'status', 'stress', 'subsequent', 'sum', 'summary',
        'undertaken', 'academic', 'argument', 'citation', 'plagiarism',
        'reference', 'bibliography', 'footnote', 'endnote', 'paraphrase',
        'quotation', 'attribution', 'originality', 'integrity', 'ethics'
    }
    
    TRANSITION_WORDS = {
        'addition': {'furthermore', 'moreover', 'additionally', 'also', 'besides', 
                    'in addition', 'likewise', 'similarly'},
        'contrast': {'however', 'nevertheless', 'nonetheless', 'on the other hand', 
                    'in contrast', 'conversely', 'although', 'though', 'whereas', 
                    'while', 'despite', 'in spite of'},
        'cause_effect': {'therefore', 'thus', 'consequently', 'as a result', 
                        'hence', 'accordingly', 'so', 'because', 'since', 
                        'due to', 'owing to'},
        'example': {'for example', 'for instance', 'such as', 'namely', 
                   'specifically', 'to illustrate', 'in particular'},
        'time': {'meanwhile', 'subsequently', 'afterward', 'then', 'next', 
                'previously', 'finally', 'eventually', 'simultaneously'},
        'conclusion': {'in conclusion', 'to conclude', 'to summarize', 
                      'in summary', 'overall', 'all in all', 'in brief'}
    }
    
    def clean_text(self, text: str) -> str:
        if not text:
            return ""
        text = text.lower()
