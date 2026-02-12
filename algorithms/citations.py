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
    
    def __init__(self, language: str = 'en'):
        self.language = language
        self.stopwords = self.STOPWORDS.get(language, self.STOPWORDS['en'])
    
    def clean_text(self, text: str) -> str:
        if not text:
            return ""
        text = text.lower()
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
        text = re.sub(r'[^\w\s\'-]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def tokenize(self, text: str, remove_stopwords: bool = True) -> List[str]:
        text = self.clean_text(text)
        words = re.findall(r'\b[a-z0-9][a-z0-9\'-]*\b', text)
        if remove_stopwords:
            words = [w for w in words if w not in self.stopwords and len(w) > 2]
        return words
    
    def extract_sentences(self, text: str) -> List[str]:
        if not text:
            return []
        abbreviations = [
            'dr.', 'mr.', 'mrs.', 'ms.', 'prof.', 'dr', 'mr', 'mrs', 'ms', 'prof',
            'i.e.', 'e.g.', 'etc.', 'viz.', 'cf.', 'c.f.', 'et al.', 'et al',
            'vs.', 'v.', 'vol.', 'no.', 'pp.', 'p.', 'ch.', 'chap.', 'ed.',
            'trans.', 'approx.', 'appx.', 'fig.', 'ref.', 'jan.', 'feb.', 'mar.',
            'apr.', 'jun.', 'jul.', 'aug.', 'sep.', 'sept.', 'oct.', 'nov.', 'dec.'
        ]
        
        for abbr in abbreviations:
            text = text.replace(abbr, abbr.replace('.', '@ABBR@'))
            
        sentences = re.split(r'[.!?]+\s+', text)
        sentences = [s.replace('@ABBR@', '.') for s in sentences]
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        return sentences
    
    def extract_paragraphs(self, text: str) -> List[str]:
        if not text:
            return []
        paragraphs = re.split(r'\n\s*\n', text)
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        return paragraphs
    
    def count_syllables(self, word: str) -> int:
        word = word.lower()
        if word.endswith('es') or word.endswith('ed'):
            word = word[:-2]
        vowels = 'aeiouy'
        count = 0
        previous_was_vowel = False
        
        for i, char in enumerate(word):
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                if char == 'y' and i == 0:
                    continue
                count += 1
            
            previous_was_vowel = is_vowel
        if word.endswith('e'):
            count -= 1
        if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
            count += 1
        if count == 0:
            count = 1
        
        return count
    
    def detect_passive_voice(self, text: str) -> int:
        patterns = [
            r'\b(?:is|are|was|were|be|been|being)\s+\w+ed\b',
            r'\b(?:has|have|had)\s+been\s+\w+ed\b',
            r'\b(?:will|would|shall|should|can|could|may|might|must)\s+be\s+\w+ed\b'
        ]
        
        passive_count = 0
        for pattern in patterns:
            passive_count += len(re.findall(pattern, text, re.IGNORECASE))
        
        return passive_count
    
    def extract_named_entities(self, text: str) -> List[Dict[str, Any]]:
        entities = []
        person_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b'
        persons = re.findall(person_pattern, text)
        for person in persons:
            entities.append({
                'text': person,
                'type': 'PERSON',
                'start': text.find(person),
                'end': text.find(person) + len(person)
            })
        org_patterns = [
            r'\b([A-Z][A-Za-z]+\s+(?:Corp|Corporation|Inc|Co|Company|Ltd|LLC))\b',
            r'\b([A-Z][A-Za-z]+\s+(?:University|College|Institute|Academy))\b',
            r'\b([A-Z][A-Za-z]+\s+(?:Hospital|Clinic|Center|Laboratory))\b'
        ]
        
        for pattern in org_patterns:
            orgs = re.findall(pattern, text)
            for org in orgs:
                entities.append({
                    'text': org,
                    'type': 'ORGANIZATION',
                    'start': text.find(org),
                    'end': text.find(org) + len(org)
                })
        location_patterns = [
            r'\b([A-Z][a-z]+\s+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr))\b',
            r'\b([A-Z][a-z]+\s+(?:City|Town|Village|County|State|Province|Country))\b',
            r'\b(\d+\s+[A-Z][a-z]+\s+(?:Street|St|Avenue|Ave|Road|Rd))\b'
        ]
        
        for pattern in location_patterns:
            locations = re.findall(pattern, text)
            for location in locations:
                entities.append({
                    'text': location,
                    'type': 'LOCATION',
                    'start': text.find(location),
                    'end': text.find(location) + len(location)
                })
        date_patterns = [
            r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b',
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
            r'\b\d{4}\b'
        ]
        
        for pattern in date_patterns:
            dates = re.findall(pattern, text, re.IGNORECASE)
            for date in dates:
                entities.append({
                    'text': date,
                    'type': 'DATE',
                    'start': text.find(date),
                    'end': text.find(date) + len(date)
                })
        
        return entities
    
    def extract_key_phrases(self, text: str, top_n: int = 10) -> List[Dict[str, Any]]:
        words = self.tokenize(text, remove_stopwords=True)
        
        if len(words) < 3:
            return []
        all_phrases = []
        phrase_frequencies = {}
        
        for ngram_size in range(2, 5):
            for i in range(len(words) - ngram_size + 1):
                phrase = ' '.join(words[i:i+ngram_size])
                if all(word in self.stopwords for word in phrase.split()):
                    continue
                
                if phrase in phrase_frequencies:
                    phrase_frequencies[phrase] += 1
                else:
                    phrase_frequencies[phrase] = 1
        key_phrases = []
        total_phrases = len(phrase_frequencies)
        for phrase, freq in phrase_frequencies.items():
            tf = freq / total_phrases if total_phrases > 0 else 0
            words_in_phrase = len(phrase.split())
            length_bonus = 1.0 + (0.1 * (words_in_phrase - 2))
            academic_terms = sum(1 for word in phrase.split() if word in self.ACADEMIC_WORDS)
            academic_bonus = 1.0 + (0.15 * academic_terms)
            score = tf * length_bonus * academic_bonus * 100
            
            key_phrases.append({
                'phrase': phrase,
                'frequency': freq,
                'score': round(score, 2),
                'length': words_in_phrase
            })
        key_phrases.sort(key=lambda x: x['score'], reverse=True)
        return key_phrases[:top_n]
    
    def detect_academic_structure(self, text: str) -> Dict[str, Any]:
        structure = {
            'has_abstract': False,
            'has_introduction': False,
            'has_literature_review': False,
            'has_methodology': False,
            'has_results': False,
            'has_discussion': False,
            'has_conclusion': False,
            'has_references': False,
            'sections': [],
            'section_count': 0
        }
        
        section_patterns = {
            'abstract': r'\b(?:abstract|summary|executive\s+summary)\b',
            'introduction': r'\b(?:introduction|background|context)\b',
            'literature_review': r'\b(?:literature\s+review|related\s+work|previous\s+research)\b',
            'methodology': r'\b(?:methodology|methods|research\s+design|procedure)\b',
            'results': r'\b(?:results|findings|analysis|data\s+analysis)\b',
            'discussion': r'\b(?:discussion|interpretation|implications)\b',
            'conclusion': r'\b(?:conclusion|conclusions|summary\s+and\s+conclusions)\b',
            'references': r'\b(?:references|bibliography|works\s+cited|sources)\b'
        }
        paragraphs = self.extract_paragraphs(text)
        
        for para in paragraphs:
            para_lower = para.lower().strip()
            if len(para_lower) < 100:  
                for section_name, pattern in section_patterns.items():
                    if re.search(pattern, para_lower, re.IGNORECASE):
                        structure[f'has_{section_name}'] = True
                        lines = para.split('\n')
                        if lines:
                            title = lines[0].strip()
                            if title and title not in structure['sections']:
                                structure['sections'].append(title)
        structure['section_count'] = len(structure['sections'])
        
        return structure

    def detect_citations(self, text: str) -> List[Dict[str, Any]]:
        citation_patterns = [
            {
                'name': 'APA_inline',
                'pattern': r'\(([A-Z][a-z]+(?:\s+(?:&|and)\s+[A-Z][a-z]+)?),\s*\d{4}\)',
                'type': 'apa'
            },
            {
                'name': 'APA_narrative',
                'pattern': r'([A-Z][a-z]+(?:\s+(?:&|and)\s+[A-Z][a-z]+)?)\s+\(\d{4}\)',
                'type': 'apa'
            },
            {
                'name': 'MLA_inline',
                'pattern': r'\(([A-Z][a-z]+)\s+\d+\)',
                'type': 'mla'
            },
            {
                'name': 'Chicago_footnote',
                'pattern': r'\[\d+\]',
                'type': 'chicago'
            },
            {
                'name': 'Harvard',
                'pattern': r'\(([A-Z][a-z]+)\s+\d{4}:\s*\d+\)',
                'type': 'harvard'
            },
            {
                'name': 'IEEE',
                'pattern': r'\[\d+(?:,\s*\d+)*\]',
                'type': 'ieee'
            },
            {
                'name': 'Vancouver',
                'pattern': r'\(\d+\)',
                'type': 'vancouver'
            },
            {
                'name': 'Author_etal',
                'pattern': r'([A-Z][a-z]+\s+et\s+al\.)',
                'type': 'general'
            }
        ]
        
        citations = []
        
        for pattern_info in citation_patterns:
            pattern = pattern_info['pattern']
            matches = re.finditer(pattern, text, re.IGNORECASE)
            
            for match in matches:
                citation_info = {
                    'text': match.group(0),
                    'position': match.start(),
                    'type': pattern_info['type'],
                    'name': pattern_info['name'],
                    'author': match.group(1) if match.groups() else None
                }
                year_match = re.search(r'\d{4}', match.group(0))
                if year_match:
                    citation_info['year'] = int(year_match.group())
                
                citations.append(citation_info)
        citations.sort(key=lambda x: x['position'])
        
        return citations

class ReadabilityAnalyzer:
    
    
    def calculate_flesch_reading_ease(self, text: str) -> float:
        sentences = self.processor.extract_sentences(text)
        words = self.processor.tokenize(text, remove_stopwords=False)
        
        if not sentences or not words:
            return 0.0
        
        total_syllables = sum(self.processor.count_syllables(word) for word in words)
        
        avg_sentence_length = len(words) / len(sentences)
        avg_syllables_per_word = total_syllables / len(words)
        score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        
        return round(max(0, min(100, score)), 2)
    
    def calculate_flesch_kincaid_grade(self, text: str) -> float:
        sentences = self.processor.extract_sentences(text)
        words = self.processor.tokenize(text, remove_stopwords=False)
        
        if not sentences or not words:
            return 0.0
        
        total_syllables = sum(self.processor.count_syllables(word) for word in words)
        
        avg_sentence_length = len(words) / len(sentences)
        avg_syllables_per_word = total_syllables / len(words)
        grade = (0.39 * avg_sentence_length) + (11.8 * avg_syllables_per_word) - 15.59
        
        return round(max(0, grade), 2)
    
    def calculate_gunning_fog_index(self, text: str) -> float:
        sentences = self.processor.extract_sentences(text)
        words = self.processor.tokenize(text, remove_stopwords=False)
        
        if not sentences or not words:
            return 0.0
        complex_words = sum(1 for word in words if self.processor.count_syllables(word) >= 3)
        
        avg_sentence_length = len(words) / len(sentences)
        percent_complex = (complex_words / len(words)) * 100
        fog_index = 0.4 * (avg_sentence_length + percent_complex)
        
        return round(max(0, fog_index), 2)
    
    def calculate_smog_index(self, text: str) -> float:
        sentences = self.processor.extract_sentences(text)
        words = self.processor.tokenize(text, remove_stopwords=False)
        
        if len(sentences) < 3:
            return 0.0
        polysyllabic_words = sum(1 for word in words if self.processor.count_syllables(word) >= 3)
        smog = 1.043 * math.sqrt(polysyllabic_words * (30 / len(sentences))) + 3.1291
        
        return round(max(0, smog), 2)
    
    def calculate_coleman_liau_index(self, text: str) -> float:
        sentences = self.processor.extract_sentences(text)
        words = self.processor.tokenize(text, remove_stopwords=False)
        
        if not sentences or not words:
            return 0.0
        chars = sum(len(word) for word in words)
        
        avg_letters_per_word = chars / len(words)
        avg_sentences_per_word = len(sentences) / len(words)
        grade = (0.0588 * avg_letters_per_word * 100) - (0.296 * avg_sentences_per_word * 100) - 15.8
        return round(max(0, grade), 2)
    
    def calculate_automated_readability_index(self, text: str) -> float:
        sentences = self.processor.extract_sentences(text)
        words = self.processor.tokenize(text, remove_stopwords=False)
        
        if not sentences or not words:
            return 0.0
    

def detect_language(text: str) -> str:
    analyzer = TextAnalyzer()
    language = analyzer._detect_language(text)
    return language.value


def calculate_readability(text: str) -> Dict[str, float]:
    analyzer = ReadabilityAnalyzer()
    return analyzer.analyze_readability(text)

__all__ = [
    'TextCategory',
    'Language',
    'NLPAnalysis',
    'TextProcessor',
    'ReadabilityAnalyzer',
    'TextAnalyzer',
    'summarize_text',
    'extract_keywords',
    'detect_language',
    'calculate_readability'
]