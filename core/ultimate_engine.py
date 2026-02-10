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
    