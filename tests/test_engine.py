import unittest
import tempfile
import os
import sys
from pathlib import Path
import json
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from core.base_engine import BasePlagiarismEngine
    from core.advanced_engine import AdvancedPlagiarismEngine
    from core.ultimate_engine import UltimatePlagiarismEngine
    from core.analyzer import AdvancedTextAnalyzer
    from core.database import DatabaseManager
    from core.utils import (
        ProgressTracker, 
        FileProcessor, 
        TextNormalizer,
        CacheManager, 
        ErrorHandler,
        load_config, 
        save_config,
        format_file_size,
        format_percentage
    )
    try:
        from file_handlers.text_extractor import TextExtractor
        from file_handlers.docx_handler import DOCXHandler
        TEXT_EXTRACTOR_AVAILABLE = True
    except ImportError:
        TEXT_EXTRACTOR_AVAILABLE = False
    
    try:
        from algorithms.similarity import SimilarityAlgorithms
        SIMILARITY_AVAILABLE = True
    except ImportError:
        SIMILARITY_AVAILABLE = False

    try:
        from algorithms.ml_features import MLFeatures
        ML_FEATURES_AVAILABLE = True
    except ImportError:
        ML_FEATURES_AVAILABLE = False
        
    IMPORT_SUCCESS = True
except ImportError as e:
    print(f"⚠ Warning: Some imports failed: {e}")
    IMPORT_SUCCESS = False

class TestBaseEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not IMPORT_SUCCESS:
            raise unittest.SkipTest("Required imports not available")
        
        cls.config = {
            'detection.basic.min_match_length': 5,
            'detection.basic.threshold': 5.0
        }
        cls.engine = BasePlagiarismEngine(cls.config)
        cls.test_text = """
        Plagiarism is the representation of another author's language, thoughts, 
        ideas, or expressions as one's own original work. In educational contexts, 
        there are differing definitions of plagiarism depending on the institution.
        
        Academic integrity is the moral code or ethical policy of academia. 
        This includes values such as avoidance of cheating or plagiarism.
        """
        
        cls.similar_text = """
        Plagiarism involves using another author's language, thoughts, ideas, 
        or expressions as one's own original work. Different educational 
        institutions have varying definitions of plagiarism.
        
        The moral code of academia, known as academic integrity, encompasses 
        values like avoiding cheating or plagiarism.
        """
        
        cls.different_text = """
        The quick brown fox jumps over the lazy dog. This sentence contains 
        all letters of the English alphabet. It is often used for typing 
        practice and testing keyboards.
        """

    def test_01_tokenize(self):
        tokens = self.engine.tokenize(self.test_text)
        self.assertIsInstance(tokens, list)
        self.assertGreater(len(tokens), 10)
        self.assertNotIn('the', tokens)
        self.assertNotIn('is', tokens)
        self.assertIn('plagiarism', tokens)
        self.assertIn('academic', tokens)

    def test_02_get_sentences(self):
        sentences = self.engine.get_sentences(self.test_text)
        self.assertIsInstance(sentences, list)
        self.assertGreaterEqual(len(sentences), 2)
        for sentence in sentences:
            self.assertGreater(len(sentence), 10)
    
    def test_03_detect_citations(self):
        text_with_citations = """
        According to Smith (2020), plagiarism is a serious offense.
        Other researchers (Johnson & Lee, 2019) have noted similar findings.
        Recent studies [1] have confirmed these results.
        """
        
        citations = self.engine.detect_citations(text_with_citations)
        self.assertIsInstance(citations, list)
        self.assertGreaterEqual(len(citations), 2)
        for citation in citations:
            self.assertIn('text', citation)
            self.assertIn('position', citation)
            self.assertIn('type', citation)
            self.assertIsInstance(citation['text'], str)
            self.assertIsInstance(citation['position'], int)
        
    def test_04_calculate_cosine_similarity(self):
        high_similarity = self.engine.calculate_cosine_similarity(
            self.test_text, 
            self.similar_text
        )
        self.assertIsInstance(high_similarity, float)
        self.assertGreater(high_similarity, 10.0)
        low_similarity = self.engine.calculate_cosine_similarity(
            self.test_text, 
            self.different_text
        )
        self.assertLess(low_similarity, 50.0)
    
    def test_05_find_common_sequences(self):
        sequences = self.engine.find_common_sequences(
            self.test_text, 
            self.similar_text,
            min_length=3
        )
        self.assertIsInstance(sequences, list)
        
        if sequences:
            for seq in sequences:
                self.assertIn('text', seq)
                self.assertIn('length', seq)
                self.assertIn('position', seq)
                self.assertIn('similarity', seq)
                self.assertGreaterEqual(seq['length'], 3)
    
    def test_06_calculate_jaccard_similarity(self):
        similarity = self.engine.calculate_jaccard_similarity(
            self.test_text, 
            self.similar_text
        )
        self.assertIsInstance(similarity, float)
        self.assertGreaterEqual(similarity, 0.0)
        self.assertLessEqual(similarity, 100.0)
    
    def test_07_generate_document_hash(self):
        hash1 = self.engine.generate_document_hash(self.test_text)
        hash2 = self.engine.generate_document_hash(self.similar_text)
        hash3 = self.engine.generate_document_hash(self.test_text)
        
        self.assertIsInstance(hash1, str)
        self.assertEqual(len(hash1), 32)
        self.assertEqual(hash1, hash3)
        self.assertNotEqual(hash1, hash2)

    def test_08_analyze_basic(self):
        database = [
            {
                'source': 'Wikipedia - Plagiarism',
                'url': 'https://en.wikipedia.org/wiki/Plagiarism',
                'text': self.similar_text
            },
            {
                'source': 'Academic Integrity Guide',
                'url': 'https://example.com/integrity',
                'text': self.different_text
            }
        ]
        
        results = self.engine.analyze_basic(self.test_text, database)
        self.assertIsInstance(results, dict)
        required_keys = ['overall_similarity', 'total_words', 'total_sentences', 
                        'citations_found', 'matches']
        for key in required_keys:
            self.assertIn(key, results)
        self.assertIsInstance(results['overall_similarity'], float)
        self.assertIsInstance(results['total_words'], int)
        self.assertIsInstance(results['total_sentences'], int)
        self.assertIsInstance(results['citations_found'], int)
        self.assertIsInstance(results['matches'], list)
        self.assertGreaterEqual(len(results['matches']), 0)

class TestAdvancedEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not IMPORT_SUCCESS:
            raise unittest.SkipTest("Required imports not available")
        
        cls.config = {
            'detection.advanced.algorithms': ['cosine', 'jaccard', 'ngram', 'sequence'],
            'detection.advanced.threshold': 10.0
        }
        cls.engine = AdvancedPlagiarismEngine(cls.config)
        
        cls.test_text = """
        Machine learning is a subset of artificial intelligence that provides 
        systems the ability to automatically learn and improve from experience 
        without being explicitly programmed. It focuses on the development of 
        computer programs that can access data and use it to learn for themselves.
        
        The process of learning begins with observations or data, such as examples, 
        direct experience, or instruction, in order to look for patterns in data 
        and make better decisions in the future based on the examples that we provide.
        """
        
        cls.plagiarized_text = """
        Machine learning is a branch of artificial intelligence that gives 
        systems the capability to automatically learn and improve from experience 
        without being explicitly programmed. It concentrates on the creation of 
        computer programs that can access data and use it to learn independently.
        
        The learning process starts with observations or data, like examples, 
        direct experience, or instruction, to search for patterns in data and 
        make improved decisions later based on the examples we provide.
        """
    def test_01_ngram_similarity(self):
        similarity = self.engine.calculate_ngram_similarity(
            self.test_text, 
            self.plagiarized_text,
            n=3
        )
        self.assertIsInstance(similarity, float)
        self.assertGreaterEqual(similarity, 0.0)
        self.assertLessEqual(similarity, 100.0)
        self.assertGreater(similarity, 20.0)
    
    def test_02_overlap_coefficient(self):
        similarity = self.engine.calculate_overlap_coefficient(
            self.test_text, 
            self.plagiarized_text
        )
        self.assertIsInstance(similarity, float)
        self.assertGreaterEqual(similarity, 0.0)
        self.assertLessEqual(similarity, 100.0)
    
    def test_03_dice_coefficient(self):
        similarity = self.engine.calculate_dice_coefficient(
            self.test_text, 
            self.plagiarized_text
        )
        self.assertIsInstance(similarity, float)
        self.assertGreaterEqual(similarity, 0.0)
        self.assertLessEqual(similarity, 100.0)
    

    def test_04_analyze_text(self):
        database = [
            {
                'source': 'ML Textbook',
                'url': 'https://example.com/ml',
                'category': 'Technical',
                'text': self.plagiarized_text
            },
            {
                'source': 'AI Research Paper',
                'url': 'https://example.com/ai',
                'category': 'Academic',
                'text': 'Artificial intelligence is the simulation of human intelligence processes by machines.'
            }
        ]
        
        results = self.engine.analyze_text(
            self.test_text, 
            database,
            algorithms=['cosine', 'jaccard', 'ngram']
        )
    
    self.assertIsInstance(results, dict)
        required_keys = [
            'overall_similarity', 'total_words', 'total_sentences',
            'citations_found', 'matches', 'algorithm_scores',
            'statistics', 'metadata'
        ]
        for key in required_keys:
            self.assertIn(key, results)
    
    self.assertIn('algorithms_used', results['metadata'])
    self.assertIn('database_size', results['metadata'])
    if results['matches']:
            match = results['matches'][0]
            self.assertIn('source', match)
            self.assertIn('similarity', match)
            self.assertIn('algorithm_scores', match)
            self.assertIn('confidence', match)
            self.assertIn('risk_level', match)
            self.assertIn(match['confidence'], ['High', 'Medium', 'Low'])
            self.assertIn(match['risk_level'], ['Critical', 'High', 'Medium', 'Low', 'Minimal'])
    
    def test_05_confidence_calculation(self):
        consistent_scores = {'cosine': 75.0, 'jaccard': 72.0, 'ngram': 78.0}
        confidence = self.engine._calculate_confidence(consistent_scores)
        self.assertIn(confidence, ['High', 'Medium', 'Low'])
        inconsistent_scores = {'cosine': 20.0, 'jaccard': 75.0, 'ngram': 10.0}
        confidence = self.engine._calculate_confidence(inconsistent_scores)
        self.assertIn(confidence, ['High', 'Medium', 'Low'])
    
    def test_06_risk_level_calculation(self):
        test_cases = [
            (45.0, 'Critical'),
            (35.0, 'High'),
            (20.0, 'Medium'),
            (10.0, 'Low'),
            (2.0, 'Minimal'),
            (0.0, 'Minimal')
        ]
        
        for similarity, expected_risk in test_cases:
            risk_level = self.engine._calculate_risk_level(similarity)
            self.assertEqual(risk_level, expected_risk)

    def test_07_statistics_calculation(self):
        mock_results = {
            'total_words': 100,
            'matches': [
                {
                    'matched_sequences': [
                        {'length': 10},
                        {'length': 5},
                        {'length': 3}
                    ]
                },
                {
                    'matched_sequences': [
                        {'length': 7},
                        {'length': 4}
                    ]
                }
            ]
        }
        
        mock_text = "Sample text for testing statistics calculation."
        
        stats = self.engine._calculate_statistics(mock_results, mock_text)
