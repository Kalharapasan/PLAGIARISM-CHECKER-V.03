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
            if word.endswith('e'):
                count -= 1
            if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
                count += 1
            if count == 0:
                count = 1
                
            return count
        total_syllables = sum(count_syllables(word) for word in words)
        total_sentences = len(sentences)
        total_words = len(words)
    
    if total_sentences > 0 and total_words > 0:
            avg_sentence_length = total_words / total_sentences
            avg_syllables_per_word = total_syllables / total_words
            
            flesch_reading_ease = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
            flesch_kincaid_grade = (0.39 * avg_sentence_length) + (11.8 * avg_syllables_per_word) - 15.59
            complex_words = sum(1 for word in words if count_syllables(word) >= 3)
            percent_complex = (complex_words / total_words) * 100
            gunning_fog = 0.4 * (avg_sentence_length + percent_complex)
            if total_sentences >= 3:
                smog = 1.043 * math.sqrt(complex_words * (30 / total_sentences)) + 3.1291
            else:
                smog = 0
            avg_letters_per_word = sum(len(word) for word in words) / total_words
            coleman_liau = (0.0588 * avg_letters_per_word * 100) - (0.296 * (100 / total_sentences)) - 15.8
            ari = (4.71 * (sum(len(word) for word in words) / total_words)) + (0.5 * avg_sentence_length) - 21.43
            easy_words = sum(1 for word in words if word not in self.academic_terms)
            percent_difficult = ((total_words - easy_words) / total_words) * 100
            dale_chall = (0.1579 * percent_difficult) + (0.0496 * avg_sentence_length)
            if percent_difficult > 5:
                dale_chall += 3.6365
            
            return {
                'flesch_reading_ease': round(flesch_reading_ease, 2),
                'flesch_kincaid_grade': round(flesch_kincaid_grade, 2),
                'gunning_fog_index': round(gunning_fog, 2),
                'smog_index': round(smog, 2),
                'coleman_liau_index': round(coleman_liau, 2),
                'automated_readability_index': round(ari, 2),
                'dale_chall_score': round(dale_chall, 2),
                'avg_sentence_length': round(avg_sentence_length, 2),
                'avg_syllables_per_word': round(avg_syllables_per_word, 2),
                'avg_letters_per_word': round(avg_letters_per_word, 2),
                'complex_word_percentage': round(percent_complex, 2),
                'difficult_word_percentage': round(percent_difficult, 2),
                'total_syllables': total_syllables,
                'total_sentences': total_sentences,
                'total_words': total_words
            }
        
        return {}
    
    def extract_key_phrases(self, text: str, n: int = 10, min_length: int = 2) -> List[Tuple[str, int, float]]:
        words = self.tokenize_advanced(text, remove_stopwords=True)
        
        if len(words) < min_length:
            return []
        all_phrases = []
        phrase_frequencies = {}
        for ngram_size in range(2, 5):  
            for i in range(len(words) - ngram_size + 1):
                phrase = ' '.join(words[i:i+ngram_size])
                if all(word in self.stop_words for word in phrase.split()):
                    continue
                if phrase in self.common_phrases:
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
            academic_terms_in_phrase = sum(1 for word in phrase.split() if word in self.academic_terms)
            academic_bonus = 1.0 + (0.15 * academic_terms_in_phrase)
            score = tf * length_bonus * academic_bonus * 100
            key_phrases.append((phrase, freq, round(score, 2)))
            key_phrases.sort(key=lambda x: x[2], reverse=True)
        return key_phrases[:n]
    
    def detect_academic_structure(self, text: str) -> Dict:
        structure = {
            'abstract': False,
            'introduction': False,
            'literature_review': False,
            'methodology': False,
            'results': False,
            'discussion': False,
            'conclusion': False,
            'references': False,
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
        paragraphs = text.split('\n\n')
        for para in paragraphs:
            para_lower = para.lower().strip()
            if len(para_lower) < 100:
                 for section_name, pattern in section_patterns.items():
                    if re.search(pattern, para_lower, re.IGNORECASE):
                        structure[section_name] = True
                        lines = para.split('\n')
                        if lines:
                            title = lines[0].strip()
                            if title and title not in structure['sections']:
                                structure['sections'].append(title)
        
        structure['section_count'] = len(structure['sections'])
        
        return structure 
    
    def analyze_writing_style(self, text: str) -> Dict:
        sentences = self.extract_sentences(text)
        words = self.tokenize_advanced(text, remove_stopwords=False)
        
        if not sentences or not words:
            return {}
        
        total_sentences = len(sentences)
        total_words = len(words)
        sentence_lengths = [len(self.tokenize_advanced(s, remove_stopwords=False)) for s in sentences]
        avg_sentence_length = sum(sentence_lengths) / total_sentences if total_sentences > 0 else 0
        max_sentence_length = max(sentence_lengths) if sentence_lengths else 0
        min_sentence_length = min(sentence_lengths) if sentence_lengths else 0
        paragraphs = [p for p in text.split('\n\n') if p.strip()]
        avg_paragraph_length = sum(len(self.tokenize_advanced(p, remove_stopwords=False)) for p in paragraphs) / len(paragraphs) if paragraphs else 0
        unique_words = set(words)
        vocabulary_richness = len(unique_words) / total_words if total_words > 0 else 0
        avg_word_length = sum(len(word) for word in words) / total_words if total_words > 0 else 0
        passive_patterns = [
            r'\b(?:is|are|was|were|be|been|being)\s+\w+ed\b',
            r'\b(?:has|have|had)\s+been\s+\w+ed\b',
            r'\b(?:will|would|shall|should|can|could|may|might|must)\s+be\s+\w+ed\b'
        ]
        
        passive_count = 0
        for pattern in passive_patterns:
            passive_count += len(re.findall(pattern, text, re.IGNORECASE))
        
        passive_percentage = (passive_count / total_sentences) * 100 if total_sentences > 0 else 0
        academic_indicators = {
            'hedging': len(re.findall(r'\b(?:may|might|could|would|possibly|perhaps|likely|seems|appears)\b', text, re.IGNORECASE)),
            'certainty': len(re.findall(r'\b(?:certainly|definitely|undoubtedly|clearly|obviously|evidently)\b', text, re.IGNORECASE)),
            'contrast': len(re.findall(r'\b(?:however|nevertheless|nonetheless|although|though|whereas|while)\b', text, re.IGNORECASE)),
            'addition': len(re.findall(r'\b(?:furthermore|moreover|additionally|also|besides|in addition)\b', text, re.IGNORECASE)),
            'consequence': len(re.findall(r'\b(?:therefore|thus|hence|consequently|accordingly|as a result)\b', text, re.IGNORECASE)),
            'exemplification': len(re.findall(r'\b(?:for example|for instance|such as|including|namely|specifically)\b', text, re.IGNORECASE))
        }
        
        return {
            'avg_sentence_length': round(avg_sentence_length, 2),
            'max_sentence_length': max_sentence_length,
            'min_sentence_length': min_sentence_length,
            'sentence_length_variation': round(max(sentence_lengths) - min(sentence_lengths), 2) if sentence_lengths else 0,
            'avg_paragraph_length': round(avg_paragraph_length, 2),
            'vocabulary_richness': round(vocabulary_richness, 4),
            'avg_word_length': round(avg_word_length, 2),
            'passive_voice_percentage': round(passive_percentage, 2),
            'academic_indicators': academic_indicators,
            'total_paragraphs': len(paragraphs),
            'unique_words': len(unique_words),
            'type_token_ratio': round(len(unique_words) / total_words, 4) if total_words > 0 else 0
        }
        
    def detect_paraphrasing_patterns(self, text: str) -> List[Dict]:
        patterns = []
        paraphrase_indicators = [
            {
                'name': 'synonym_replacement',
                'pattern': r'\b(?:said|stated|mentioned|noted|explained|described|argued)\b',
                'description': 'Reporting verb patterns often used in paraphrasing'
            },
            {
                'name': 'in_other_words',
                'pattern': r'\b(?:in other words|that is|i\.e\.|namely|specifically)\b',
                'description': 'Phrases indicating reformulation'
            },
            {
                'name': 'according_to',
                'pattern': r'\b(?:according to|as stated by|as noted by|as argued by)\b',
                'description': 'Attribution phrases'
            },
            {
                'name': 'paraphrase_intro',
                'pattern': r'\b(?:this means that|this suggests that|this indicates that|this shows that)\b',
                'description': 'Paraphrase introduction phrases'
            },
            {
                'name': 'quotation_markers',
                'pattern': r'\b(?:quotes|states|writes|observes|comments|remarks)\b',
                'description': 'Verbs introducing quoted or paraphrased material'
            }
        ]
        
        for indicator in paraphrase_indicators:
            matches = list(re.finditer(indicator['pattern'], text, re.IGNORECASE))
            if matches:
                patterns.append({
                    'name': indicator['name'],
                    'description': indicator['description'],
                    'count': len(matches),
                    'examples': [m.group(0) for m in matches[:3]]  
                })
        
        return patterns
    
    def generate_text_statistics(self, text: str) -> Dict:
        words = self.tokenize_advanced(text, remove_stopwords=False)
        sentences = self.extract_sentences(text)
        paragraphs = [p for p in text.split('\n\n') if p.strip()]
        
        total_chars = len(text)
        total_words = len(words)
        total_sentences = len(sentences)
        total_paragraphs = len(paragraphs)
        alphabetic_chars = sum(1 for c in text if c.isalpha())
        numeric_chars = sum(1 for c in text if c.isdigit())
        space_chars = sum(1 for c in text if c.isspace())
        punctuation_chars = sum(1 for c in text if c in '.,;:!?\'"()-[]{}')
        unique_words = set(words)
        avg_word_length = sum(len(word) for word in words) / total_words if total_words > 0 else 0
        avg_sentence_length = total_words / total_sentences if total_sentences > 0 else 0
        avg_paragraph_length = total_words / total_paragraphs if total_paragraphs > 0 else 0
        readability = self.calculate_readability_scores(text)
        writing_style = self.analyze_writing_style(text)
        citations = self.detect_citations(text)
        key_phrases = self.extract_key_phrases(text, n=5)