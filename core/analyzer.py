import re
import math
from typing import List, Dict, Tuple, Set, Optional
from collections import Counter
from datetime import datetime

class AdvancedTextAnalyzer:
    
    def _load_comprehensive_stopwords(self) -> Set[str]:
        basic_stops = {
            'a', 'about', 'above', 'across', 'after', 'afterwards', 'again', 'against', 'all', 
            'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 
            'amongst', 'amoungst', 'amount', 'an', 'and', 'another', 'any', 'anyhow', 'anyone', 
            'anything', 'anyway', 'anywhere', 'are', 'around', 'as', 'at', 'back', 'be', 'became', 
            'because', 'become', 'becomes', 'becoming', 'been', 'before', 'beforehand', 'behind', 
            'being', 'below', 'beside', 'besides', 'between', 'beyond', 'bill', 'both', 'bottom', 
            'but', 'by', 'call', 'can', 'cannot', 'cant', 'co', 'computer', 'con', 'could', 
            'couldnt', 'cry', 'de', 'describe', 'detail', 'do', 'done', 'down', 'due', 'during', 
            'each', 'eg', 'eight', 'either', 'eleven', 'else', 'elsewhere', 'empty', 'enough', 
            'etc', 'even', 'ever', 'every', 'everyone', 'everything', 'everywhere', 'except', 
            'few', 'fifteen', 'fify', 'fill', 'find', 'fire', 'first', 'five', 'for', 'former', 
            'formerly', 'forty', 'found', 'four', 'from', 'front', 'full', 'further', 'get', 
            'give', 'go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her', 'here', 'hereafter', 
            'hereby', 'herein', 'hereupon', 'hers', 'herself', 'him', 'himself', 'his', 'how', 
            'however', 'hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed', 'interest', 'into', 
            'is', 'it', 'its', 'itself', 'keep', 'last', 'latter', 'latterly', 'least', 'less', 
            'ltd', 'made', 'many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine', 'more', 
            'moreover', 'most', 'mostly', 'move', 'much', 'must', 'my', 'myself', 'name', 
            'namely', 'neither', 'never', 'nevertheless', 'next', 'nine', 'no', 'nobody', 
            'none', 'noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of', 'off', 'often', 
            'on', 'once', 'one', 'only', 'onto', 'or', 'other', 'others', 'otherwise', 'our', 
            'ours', 'ourselves', 'out', 'over', 'own', 'part', 'per', 'perhaps', 'please', 
            'put', 'rather', 're', 'same', 'see', 'seem', 'seemed', 'seeming', 'seems', 'serious', 
            'several', 'she', 'should', 'show', 'side', 'since', 'sincere', 'six', 'sixty', 
            'so', 'some', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhere', 
            'still', 'such', 'system', 'take', 'ten', 'than', 'that', 'the', 'their', 'them', 
            'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', 'therefore', 
            'therein', 'thereupon', 'these', 'they', 'thick', 'thin', 'third', 'this', 'those', 
            'though', 'three', 'through', 'throughout', 'thru', 'thus', 'to', 'together', 'too', 
            'top', 'toward', 'towards', 'twelve', 'twenty', 'two', 'un', 'under', 'until', 'up', 
            'upon', 'us', 'very', 'via', 'was', 'we', 'well', 'were', 'what', 'whatever', 
            'when', 'whence', 'whenever', 'where', 'whereafter', 'whereas', 'whereby', 
            'wherein', 'whereupon', 'wherever', 'whether', 'which', 'while', 'whither', 'who', 
            'whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with', 'within', 'without', 
            'would', 'yet', 'you', 'your', 'yours', 'yourself', 'yourselves'
        }
        return basic_stops
    
    def _load_common_phrases(self) -> List[str]:
        return [
            'in conclusion', 'in summary', 'for example', 'for instance',
            'according to', 'as shown in', 'it is important to note',
            'in other words', 'on the other hand', 'as a result',
            'in addition', 'furthermore', 'moreover', 'however',
            'therefore', 'consequently', 'nevertheless', 'nonetheless',
            'as stated', 'as mentioned', 'based on', 'due to',
            'in terms of', 'with regard to', 'with respect to',
            'it should be noted', 'it is clear that', 'the fact that',
            'in order to', 'as well as', 'such as', 'so that',
            'even though', 'as if', 'as though', 'as soon as',
            'as long as', 'so as to', 'in case', 'provided that',
            'assuming that', 'given that', 'in light of'
        ]
    
    def _load_citation_patterns(self) -> List[Dict]:
        return [
            {'name': 'APA_inline', 'pattern': r'\(([A-Z][a-z]+(?:\s+(?:&|and)\s+[A-Z][a-z]+)?),\s*\d{4}\)', 'type': 'apa'},
            {'name': 'APA_narrative', 'pattern': r'([A-Z][a-z]+(?:\s+(?:&|and)\s+[A-Z][a-z]+)?)\s+\(\d{4}\)', 'type': 'apa'},
            {'name': 'MLA_inline', 'pattern': r'\(([A-Z][a-z]+)\s+\d+\)', 'type': 'mla'},
            {'name': 'Chicago_footnote', 'pattern': r'\[\d+\]', 'type': 'chicago'},
            {'name': 'Harvard', 'pattern': r'\(([A-Z][a-z]+)\s+\d{4}:\s*\d+\)', 'type': 'harvard'},
            {'name': 'IEEE', 'pattern': r'\[\d+(?:,\s*\d+)*\]', 'type': 'ieee'},
            {'name': 'Vancouver', 'pattern': r'\(\d+\)', 'type': 'vancouver'},
            {'name': 'Author_etal', 'pattern': r'([A-Z][a-z]+\s+et\s+al\.)', 'type': 'general'},
            {'name': 'According_to', 'pattern': r'(?:according to|as stated by|as noted by)\s+([A-Z][a-z]+)', 'type': 'narrative'},
            {'name': 'Multiple_authors', 'pattern': r'\(([A-Z][a-z]+(?:\s+(?:&|and|et al\.)\s+[A-Z][a-z]+)+)\)', 'type': 'general'},
            {'name': 'Year_only', 'pattern': r'\(\d{4}\)', 'type': 'general'},
            {'name': 'Page_reference', 'pattern': r'pp?\.\s*\d+(?:-\d+)?', 'type': 'page'},
            {'name': 'URL_reference', 'pattern': r'Retrieved from https?://[^\s]+', 'type': 'url'}
        ]
    
    def _load_academic_terms(self) -> Set[str]:
        return {
            'analysis', 'approach', 'area', 'assessment', 'assume', 'authority', 'available',
            'benefit', 'concept', 'consistent', 'constitutional', 'context', 'contract', 'create',
            'data', 'definition', 'derived', 'distribution', 'economic', 'environment', 'established',
            'estimate', 'evidence', 'export', 'factors', 'financial', 'formula', 'function',
            'identified', 'income', 'indicate', 'individual', 'interpretation', 'involved', 'issues',
            'labour', 'legal', 'legislation', 'major', 'method', 'occur', 'percent', 'period',
            'policy', 'principle', 'procedure', 'process', 'required', 'research', 'response',
            'role', 'section', 'sector', 'significant', 'similar', 'source', 'specific', 'structure',
            'theory', 'variables', 'achieve', 'acquisition', 'administration', 'affect', 'appropriate',
            'aspects', 'assistance', 'categories', 'chapter', 'commission', 'community', 'complex',
            'computer', 'conclusion', 'conduct', 'consequences', 'construction', 'consumer', 'credit',
            'cultural', 'design', 'distinction', 'elements', 'equation', 'evaluation', 'features',
            'final', 'focus', 'impact', 'injury', 'institute', 'investment', 'items', 'journal',
            'maintenance', 'normal', 'obtained', 'participation', 'perceived', 'positive', 'potential',
            'previous', 'primary', 'purchase', 'range', 'region', 'regulations', 'relevant', 'resident',
            'resources', 'restricted', 'security', 'sought', 'select', 'site', 'strategies', 'survey',
            'text', 'traditional', 'transfer', 'alternative', 'circumstances', 'comments', 'compensation',
            'components', 'consent', 'considerable', 'constant', 'constraints', 'contribution', 'convention',
            'coordination', 'core', 'corporate', 'corresponding', 'criteria', 'deduction', 'demonstrate',
            'document', 'dominant', 'emphasis', 'ensure', 'excluded', 'framework', 'funds', 'illustrated',
            'immigration', 'implies', 'initial', 'instance', 'interaction', 'justification', 'layer',
            'link', 'location', 'maximum', 'minorities', 'negative', 'outcomes', 'partnership', 'philosophy',
            'physical', 'proportion', 'published', 'reaction', 'registered', 'reliance', 'removed', 'scheme',
            'sequence', 'sex', 'shift', 'specified', 'sufficient', 'task', 'technical', 'techniques',
            'technology', 'validity', 'volume', 'access', 'adequate', 'annual', 'apparent', 'approximated',
            'attitudes', 'attributed', 'civil', 'code', 'commitment', 'communication', 'concentration',
            'conference', 'contrast', 'cycle', 'debate', 'despite', 'dimensions', 'domestic', 'emerged',
            'error', 'ethnic', 'goals', 'granted', 'hence', 'hypothesis', 'implementation', 'implications',
            'imposed', 'integration', 'internal', 'investigation', 'job', 'label', 'mechanism', 'obvious',
            'occupational', 'option', 'output', 'overall', 'parallel', 'parameters', 'phase', 'predicted',
            'principal', 'prior', 'professional', 'project', 'promote', 'regime', 'resolution', 'retained',
            'series', 'statistics', 'status', 'stress', 'subsequent', 'sum', 'summary', 'undertaken',
            'academic', 'argument', 'citation', 'plagiarism', 'reference', 'bibliography', 'footnote',
            'endnote', 'paraphrase', 'quotation', 'attribution', 'originality', 'integrity', 'ethics'
        }
        
    def tokenize_advanced(self, text: str, remove_stopwords: bool = True) -> List[str]:
        if not text:
            return []
        text = text.lower()
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
        text = re.sub(r'[^\w\s\'-]', ' ', text)
        tokens = re.findall(r'\b[a-z0-9][a-z0-9\'-]+\b', text)
        if remove_stopwords:
            tokens = [t for t in tokens if t not in self.stop_words and len(t) > 2]
        
        return tokens
    
    def extract_sentences(self, text: str) -> List[str]:
        if not text:
            return []
        abbreviations = [
            'Dr.', 'Mr.', 'Mrs.', 'Ms.', 'Prof.', 'Dr', 'Mr', 'Mrs', 'Ms', 'Prof',
            'i.e.', 'e.g.', 'etc.', 'viz.', 'cf.', 'c.f.', 'et al.', 'et al',
            'vs.', 'v.', 'Vol.', 'vol.', 'No.', 'no.', 'pp.', 'p.', 'ch.',
            'chap.', 'ed.', 'trans.', 'approx.', 'appx.', 'fig.', 'ref.',
            'Jan.', 'Feb.', 'Mar.', 'Apr.', 'Jun.', 'Jul.', 'Aug.', 'Sep.',
            'Sept.', 'Oct.', 'Nov.', 'Dec.', 'Mon.', 'Tue.', 'Wed.', 'Thu.',
            'Thur.', 'Fri.', 'Sat.', 'Sun.'
        ]
        for abbr in abbreviations:
            text = text.replace(abbr, abbr.replace('.', '@ABBR@'))
        sentences = re.split(r'[.!?]+\s+', text)
        sentences = [s.replace('@ABBR@', '.') for s in sentences]
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        return sentences
    
    def detect_citations(self, text: str) -> List[Dict]:
        citations = []
        
        for pattern_info in self.citation_patterns:
            pattern = pattern_info['pattern']
            matches = re.finditer(pattern, text, re.IGNORECASE)
            
            for match in matches:
                citation_info = {
                    'text': match.group(0),
                    'position': match.start(),
                    'type': pattern_info['type'],
                    'name': pattern_info['name'],
                    'author': match.group(1) if match.groups() else None,
                    'full_match': match.group()
                }
                year_match = re.search(r'\d{4}', match.group(0))
                if year_match:
                    citation_info['year'] = int(year_match.group())
                page_match = re.search(r'pp?\.\s*(\d+(?:-\d+)?)', match.group(0))
                if page_match:
                    citation_info['pages'] = page_match.group(1)
                
                citations.append(citation_info)
                citations.sort(key=lambda x: x['position'])
        
        return citations
    
    def calculate_readability_scores(self, text: str) -> Dict:
        sentences = self.extract_sentences(text)
        words = self.tokenize_advanced(text, remove_stopwords=False)
        
        if not sentences or not words:
            return {}
        def count_syllables(word):
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