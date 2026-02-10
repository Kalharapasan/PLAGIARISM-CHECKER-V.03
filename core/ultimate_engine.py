from typing import List, Dict, Tuple, Optional
import numpy as np
from .advanced_engine import AdvancedPlagiarismEngine

class UltimatePlagiarismEngine(AdvancedPlagiarismEngine):
    
    def _init_nlp_components(self):
        if self.enable_nlp:
            try:
                from sklearn.feature_extraction.text import TfidfVectorizer
                self.nlp_components['tfidf'] = TfidfVectorizer(
                    max_features=1000,
                    stop_words='english',
                    ngram_range=(1, 2)
                )
            except ImportError:
                pass
            
            try:
                from sklearn.decomposition import LatentDirichletAllocation
                from sklearn.metrics.pairwise import cosine_similarity
                self.nlp_components['lsi'] = {
                    'decomposition': LatentDirichletAllocation,
                    'similarity': cosine_similarity
                }
            except ImportError:
                pass
    
    def calculate_cosine_similarity_tfidf(self, text1: str, text2: str) -> float:
        if 'tfidf' not in self.nlp_components:
            return 0.0
        
        try:
            vectorizer = self.nlp_components['tfidf']
            tfidf_matrix = vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return similarity * 100
        except:
            return 0.0
    
    def calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        if 'lsi' not in self.nlp_components:
            return 0.0
        
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.decomposition import LatentDirichletAllocation
            from sklearn.metrics.pairwise import cosine_similarity
            
            vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
            tfidf_matrix = vectorizer.fit_transform([text1, text2])
            lsi = LatentDirichletAllocation(n_components=min(10, tfidf_matrix.shape[1]))
            lsi_matrix = lsi.fit_transform(tfidf_matrix)
            similarity = cosine_similarity(lsi_matrix[0:1], lsi_matrix[1:2])[0][0]
            return similarity * 100
        
        except:
            return 0.0
    
    def calculate_levenshtein_distance(self, text1: str, text2: str) -> float:
        if len(text1) < len(text2):
            return self.calculate_levenshtein_distance(text2, text1)
        if len(text2) == 0:
            return 100.0
        
        previous_row = range(len(text2) + 1)
        for i, c1 in enumerate(text1):
            current_row = [i + 1]
            for j, c2 in enumerate(text2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        distance = previous_row[-1]
        max_len = max(len(text1), len(text2))
        similarity = 100 - (distance / max_len * 100)
        return max(0, similarity)
    
    def calculate_readability_scores(self, text: str) -> Dict:
        sentences = self.get_sentences(text)
        words = self.tokenize(text)
        
        if not sentences or not words:
            return {}
        
        def count_syllables(word):
            word = word.lower()
            count = 0
            vowels = 'aeiou'
            previous_was_vowel = False
            
            for char in word:
                is_vowel = char in vowels
                if is_vowel and not previous_was_vowel:
                    count += 1
                previous_was_vowel = is_vowel
            
            if word.endswith('e'):
                count -= 1
            if count == 0:
                count = 1
                
            return count
        
        total_syllables = sum(count_syllables(word) for word in words)
        if len(sentences) > 0 and len(words) > 0:
            avg_sentence_length = len(words) / len(sentences)
            avg_syllables_per_word = total_syllables / len(words)
            
            flesch_reading_ease = 206.835 - 1.015 * avg_sentence_length - 84.6 * avg_syllables_per_word
            flesch_kincaid_grade = 0.39 * avg_sentence_length + 11.8 * avg_syllables_per_word - 15.59
            complex_words = sum(1 for word in words if count_syllables(word) >= 3)
            percent_complex = (complex_words / len(words)) * 100
            gunning_fog = 0.4 * (avg_sentence_length + percent_complex)
            
            return {
                'flesch_reading_ease': round(flesch_reading_ease, 2),
                'flesch_kincaid_grade': round(flesch_kincaid_grade, 2),
                'gunning_fog_index': round(gunning_fog, 2),
                'avg_sentence_length': round(avg_sentence_length, 2),
                'avg_syllables_per_word': round(avg_syllables_per_word, 2),
                'complex_word_percentage': round(percent_complex, 2)
            }
        
        return {}
    
    def extract_key_phrases(self, text: str, n: int = 10) -> List[Tuple[str, int]]:
        from collections import Counter
        
        words = self.tokenize(text)
        bigrams = [' '.join(words[i:i+2]) for i in range(len(words)-1)]
        trigrams = [' '.join(words[i:i+3]) for i in range(len(words)-2)]
        bigram_freq = Counter(bigrams)
        trigram_freq = Counter(trigrams)
        all_phrases = list(bigram_freq.items()) + list(trigram_freq.items())
        all_phrases.sort(key=lambda x: x[1], reverse=True)
        
        return all_phrases[:n]
    
    def detect_advanced_citations(self, text: str) -> List[Dict]:
        citation_patterns = [
            {'name': 'APA_inline', 'pattern': r'\(([A-Z][a-z]+(?:\s+(?:&|and)\s+[A-Z][a-z]+)?),\s*\d{4}\)', 'type': 'apa'},
            {'name': 'APA_narrative', 'pattern': r'([A-Z][a-z]+(?:\s+(?:&|and)\s+[A-Z][a-z]+)?)\s+\(\d{4}\)', 'type': 'apa'},
            {'name': 'MLA_inline', 'pattern': r'\(([A-Z][a-z]+)\s+\d+\)', 'type': 'mla'},
            {'name': 'Chicago_footnote', 'pattern': r'\[\d+\]', 'type': 'chicago'},
            {'name': 'Harvard', 'pattern': r'\(([A-Z][a-z]+)\s+\d{4}:\s*\d+\)', 'type': 'harvard'},
            {'name': 'IEEE', 'pattern': r'\[\d+(?:,\s*\d+)*\]', 'type': 'ieee'},
            {'name': 'Vancouver', 'pattern': r'\(\d+\)', 'type': 'vancouver'},
            {'name': 'Author_etal', 'pattern': r'([A-Z][a-z]+\s+et\s+al\.)', 'type': 'general'},
            {'name': 'According_to', 'pattern': r'(?:according to|as stated by|as noted by)\s+([A-Z][a-z]+)', 'type': 'narrative'}
        ]
        
        citations = []
        for pattern_info in citation_patterns:
            pattern = pattern_info['pattern']
            matches = re.finditer(pattern, text, re.IGNORECASE)
            
            for match in matches:
                citations.append({
                    'text': match.group(0),
                    'position': match.start(),
                    'type': pattern_info['type'],
                    'name': pattern_info['name'],
                    'author': match.group(1) if match.groups() else None
                })
        
        return citations
    
    def analyze_comprehensive(self, text: str, database: List[Dict], 
                            selected_algorithms: List[str] = None) -> Dict:
        if selected_algorithms is None:
            selected_algorithms = [k for k, v in self.algorithms.items() if v]
    