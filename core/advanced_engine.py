from typing import List, Dict, Optional
from .base_engine import BasePlagiarismEngine
from collections import Counter
import math

class AdvancedPlagiarismEngine(BasePlagiarismEngine):
    
    def calculate_ngram_similarity(self, text1: str, text2: str, n: int = 3) -> float:
        words1 = self.tokenize(text1)
        words2 = self.tokenize(text2)
        
        if len(words1) < n or len(words2) < n:
            return 0.0
        
        ngrams1 = set(' '.join(words1[i:i+n]) for i in range(len(words1) - n + 1))
        ngrams2 = set(' '.join(words2[i:i+n]) for i in range(len(words2) - n + 1))
        
        if not ngrams1 or not ngrams2:
            return 0.0
        
        intersection = len(ngrams1.intersection(ngrams2))
        union = len(ngrams1.union(ngrams2))
        
        return (intersection / union) * 100 if union > 0 else 0.0
    
    def calculate_overlap_coefficient(self, text1: str, text2: str) -> float:
        words1 = set(self.tokenize(text1))
        words2 = set(self.tokenize(text2))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        min_size = min(len(words1), len(words2))
        
        return (intersection / min_size) * 100 if min_size > 0 else 0.0
    
    def calculate_dice_coefficient(self, text1: str, text2: str) -> float:
        words1 = set(self.tokenize(text1))
        words2 = set(self.tokenize(text2))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        total = len(words1) + len(words2)
        
        return (2 * intersection / total) * 100 if total > 0 else 0.0

    def analyze_text(self, text: str, database: List[Dict], 
                    algorithms: List[str] = None) -> Dict:
        
        if algorithms is None:
            algorithms = [k for k, v in self.algorithms.items() if v]
        
        results = {
            'overall_similarity': 0,
            'total_words': len(self.tokenize(text)),
            'total_sentences': len(self.get_sentences(text)),
            'citations_found': len(self.detect_citations(text)),
            'matches': [],
            'algorithm_scores': {},
            'statistics': {},
            'metadata': {
                'algorithms_used': algorithms,
                'database_size': len(database)
            }
        }
        
        all_similarities = []
        
        for doc in database:
            doc_text = doc.get('text', '')
            doc_similarities = {}
        
            if 'cosine' in algorithms:
                doc_similarities['cosine'] = self.calculate_cosine_similarity(text, doc_text)
            
            if 'jaccard' in algorithms:
                doc_similarities['jaccard'] = self.calculate_jaccard_similarity(text, doc_text)
            
            if 'ngram' in algorithms:
                doc_similarities['ngram'] = self.calculate_ngram_similarity(text, doc_text, 3)
            
            if 'overlap' in algorithms:
                doc_similarities['overlap'] = self.calculate_overlap_coefficient(text, doc_text)
            
            if 'dice' in algorithms:
                doc_similarities['dice'] = self.calculate_dice_coefficient(text, doc_text)
            
            if 'sequence' in algorithms:
                sequences = self.find_common_sequences(text, doc_text)
                if sequences:
                    total_seq_words = sum(s['length'] for s in sequences)
                    doc_similarities['sequence'] = (total_seq_words / results['total_words']) * 100 if results['total_words'] > 0 else 0
                else:
                    doc_similarities['sequence'] = 0
            if doc_similarities:
                avg_similarity = sum(doc_similarities.values()) / len(doc_similarities)
            else:
                avg_similarity = 0
            
            threshold = self.config.get('detection.advanced.threshold', 10.0)
            if avg_similarity > threshold:
                sequences = self.find_common_sequences(text, doc_text)
                
                match_info = {
                    'source': doc.get('source', 'Unknown'),
                    'url': doc.get('url', ''),
                    'category': doc.get('category', 'General'),
                    'similarity': round(avg_similarity, 2),
                    'algorithm_scores': {k: round(v, 2) for k, v in doc_similarities.items()},
                    'confidence': self._calculate_confidence(doc_similarities),
                    'matched_sequences': sequences[:5],
                    'total_sequences': len(sequences),
                    'risk_level': self._calculate_risk_level(avg_similarity)
                }
                
                results['matches'].append(match_info)
                all_similarities.append(avg_similarity)
                
            if all_similarities:
                weights = []
            for match in results['matches']:
                if match['confidence'] == 'High':
                    weights.append(1.5)
                elif match['confidence'] == 'Medium':
                    weights.append(1.0)
                else:
                    weights.append(0.5)
            
            total_weight = sum(w for w in weights)
            weighted_sum = sum(s * w for s, w in zip(all_similarities, weights))
            
            results['overall_similarity'] = round(
                weighted_sum / total_weight if total_weight > 0 else 0, 2
            )
        results['matches'].sort(key=lambda x: x['similarity'], reverse=True)
        results['statistics'] = self._calculate_statistics(results, text)
        results['algorithm_scores'] = self._calculate_algorithm_scores(results)
        
        return results
    
    def _calculate_confidence(self, algorithm_scores: Dict[str, float]) -> str:
        if not algorithm_scores or len(algorithm_scores) < 2:
            return "Low"
        
        scores = list(algorithm_scores.values())
        avg = sum(scores) / len(scores)
        variance = sum((s - avg) ** 2 for s in scores) / len(scores)
        std_dev = math.sqrt(variance)
        cv = (std_dev / avg) * 100 if avg > 0 else 100
        
        if cv < 15:
            return "High"
        elif cv < 30:
            return "Medium"
        else:
            return "Low"
    
    def _calculate_risk_level(self, similarity: float) -> str:
        if similarity >= 40:
            return "Critical"
        elif similarity >= 30:
            return "High"
        elif similafrity >= 15:
            return "Medium"
        elif similarity >= 5:
            return "Low"
        else:
            return "Minimal"
    
    def _calculate_statistics(self, results: Dict, text: str) -> Dict:
        total_words = results['total_words']
        matched_words = sum(
            sum(seq['length'] for seq in match['matched_sequences'])
            for match in results['matches']
        )
        
        all_sequences = [seq for match in results['matches'] for seq in match['matched_sequences']]
        
        stats = {
            'total_words': total_words,
            'matched_words': matched_words,
            'unique_words': total_words - matched_words,
            'unique_percentage': round((1 - matched_words / total_words) * 100, 2) if total_words > 0 else 100,
            'total_sources': len(results['matches']),
            'high_risk_sources': sum(1 for m in results['matches'] if m['risk_level'] in ['High', 'Critical']),
            'total_sequences': len(all_sequences),
            'average_sequence_length': round(sum(s['length'] for s in all_sequences) / len(all_sequences), 2) if all_sequences else 0,
            'longest_sequence': max((s['length'] for s in all_sequences), default=0)
        }
        
        return stats
    
    def _calculate_algorithm_scores(self, results: Dict) -> Dict:
        if not results['matches']:
            return {}
        
        dralgo_scores = {}
        or match in results['matches']:
            for algo, score in match.get('algorithm_scores', {}).items():
                if algo not in algo_scores:
                    algo_scores[algo] = []
                algo_scores[algo].append(score)
        
        performance = {}
        for algo, scores in algo_scores.items():
            performance[algo] = {
                'average': round(sum(scores) / len(scores), 2),
                'max': round(max(scores), 2),
                'min': round(min(scores), 2)
            }
        
        return performance
        
            
            
        
        
        
        
        