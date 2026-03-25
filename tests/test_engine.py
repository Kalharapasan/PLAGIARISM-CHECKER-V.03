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
        required_stats = [
            'total_words', 'matched_words', 'unique_words',
            'unique_percentage', 'total_sources', 'high_risk_sources',
            'total_sequences', 'average_sequence_length', 'longest_sequence'
        ]
        
        for stat in required_stats:
            self.assertIn(stat, stats)
        
        self.assertEqual(stats['total_words'], 100)
        self.assertEqual(stats['matched_words'], 10 + 5 + 3 + 7 + 4) 
        self.assertEqual(stats['unique_words'], 100 - 29) 
        self.assertEqual(stats['total_sources'], 2)
        self.assertEqual(stats['total_sequences'], 5)

class TestUltimateEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not IMPORT_SUCCESS:
            raise unittest.SkipTest("Required imports not available")
        
        cls.config = {
            'detection.ultimate.algorithms': ['cosine_tfidf', 'semantic', 'lsi'],
            'detection.ultimate.enable_ml': True,
            'detection.ultimate.enable_nlp': True,
            'detection.ultimate.enable_readability': True
        }
        cls.engine = UltimatePlagiarismEngine(cls.config)
        
        cls.test_text = """
        Natural language processing (NLP) is a subfield of linguistics, 
        computer science, and artificial intelligence concerned with the 
        interactions between computers and human language.
        
        NLP techniques are used to analyze, understand, and derive meaning 
        from human language in a smart and useful way. Applications include 
        machine translation, sentiment analysis, and chatbots.
        """
        
        cls.paraphrased_text = """
        Natural language processing, a branch of linguistics, computer science, 
        and AI, focuses on computer-human language interactions.
        
        Methods in NLP help computers analyze, comprehend, and extract meaning 
        from human language intelligently. Uses encompass translation by machines, 
        analysis of sentiments, and conversational agents.
        """
    
    def test_01_cosine_similarity_tfidf(self):
        try:
            similarity = self.engine.calculate_cosine_similarity_tfidf(
                self.test_text,
                self.paraphrased_text
            )
            self.assertIsInstance(similarity, float)
            self.assertGreaterEqual(similarity, 0.0)
            self.assertLessEqual(similarity, 100.0)
        except Exception as e:
            print(f"Note: TF-IDF similarity test skipped: {e}")
    
    def test_02_semantic_similarity(self):
        try:
            similarity = self.engine.calculate_semantic_similarity(
                self.test_text,
                self.paraphrased_text
            )
            self.assertIsInstance(similarity, float)
            self.assertGreaterEqual(similarity, 0.0)
            self.assertLessEqual(similarity, 100.0)
        except Exception as e:
            print(f"Note: Semantic similarity test skipped: {e}")
    
    def test_03_levenshtein_distance(self):
        text1 = "kitten"
        text2 = "sitting"
        
        similarity = self.engine.calculate_levenshtein_distance(text1, text2)
        self.assertIsInstance(similarity, float)
        self.assertGreaterEqual(similarity, 0.0)
        self.assertLessEqual(similarity, 100.0)
        identical_similarity = self.engine.calculate_levenshtein_distance(
            self.test_text[:100],  
            self.test_text[:100]
        )
        self.assertAlmostEqual(identical_similarity, 100.0, delta=0.1)
    
    def test_04_readability_scores(self):
        scores = self.engine.calculate_readability_scores(self.test_text)
        
        if scores: 
            self.assertIsInstance(scores, dict)
            expected_metrics = [
                'flesch_reading_ease',
                'flesch_kincaid_grade', 
                'gunning_fog_index',
                'avg_sentence_length',
                'avg_syllables_per_word',
                'complex_word_percentage'
            ]
            
            for metric in expected_metrics:
                if metric in scores:
                    self.assertIsInstance(scores[metric], float)
    
    def test_05_extract_key_phrases(self):
        key_phrases = self.engine.extract_key_phrases(self.test_text, n=5)
        
        self.assertIsInstance(key_phrases, list)
        self.assertLessEqual(len(key_phrases), 5)
        
        if key_phrases:
            for phrase, freq in key_phrases:
                self.assertIsInstance(phrase, str)
                self.assertIsInstance(freq, int)
                self.assertGreater(freq, 0)
    
    def test_06_detect_advanced_citations(self):
        text_with_citations = """
        According to Smith (2020), natural language processing has advanced significantly.
        Recent studies (Johnson et al., 2021) show promising results.
        As noted by Brown (2019, p. 45), machine learning is crucial for NLP.
        Other researchers [1, 2, 3] have confirmed these findings.
        """
        
        citations = self.engine.detect_advanced_citations(text_with_citations)
        self.assertIsInstance(citations, list)
        
        if citations:
            for citation in citations:
                self.assertIn('text', citation)
                self.assertIn('position', citation)
                self.assertIn('type', citation)
                self.assertIn('name', citation)
                self.assertIsInstance(citation['text'], str)
    
    def test_07_analyze_comprehensive(self):
        database = [
            {
                'source': 'NLP Textbook',
                'url': 'https://example.com/nlp',
                'text': self.paraphrased_text
            }
        ]
        
        results = self.engine.analyze_comprehensive(
            self.test_text,
            database,
            selected_algorithms=['cosine', 'jaccard']
        )
        self.assertIsInstance(results, dict)
        self.assertIn('metadata', results)
        metadata = results['metadata']
        self.assertEqual(metadata['engine_version'], 'ultimate')
        self.assertIn('ml_enabled', metadata)
        self.assertIn('nlp_enabled', metadata)
        self.assertIn('readability_enabled', metadata)
        if metadata.get('readability_enabled'):
            self.assertIn('readability', results)
        
        if metadata.get('nlp_enabled'):
            self.assertIn('key_phrases', results)
            self.assertIn('advanced_citations', results)

class TestAdvancedTextAnalyzer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not IMPORT_SUCCESS:
            raise unittest.SkipTest("Required imports not available")
        
        cls.analyzer = AdvancedTextAnalyzer()
        
        cls.test_text = """
        The field of data science combines domain expertise, programming skills, 
        and knowledge of mathematics and statistics to extract meaningful insights 
        from data. Data scientists use machine learning algorithms to identify 
        patterns and make predictions.
        
        According to a recent study (Smith et al., 2022), organizations that 
        effectively use data science outperform their competitors. The researchers 
        found a 25% increase in productivity and a 30% reduction in costs.
        """
    
    def test_01_tokenize_advanced(self):
        tokens_without_stopwords = self.analyzer.tokenize_advanced(
            self.test_text, 
            remove_stopwords=True
        )
        self.assertIsInstance(tokens_without_stopwords, list)
        
        common_stopwords = {'the', 'a', 'an', 'and', 'of', 'to', 'in'}
        for stopword in common_stopwords:
            self.assertNotIn(stopword, tokens_without_stopwords)
        
        tokens_with_stopwords = self.analyzer.tokenize_advanced(
            self.test_text, 
            remove_stopwords=False
        )
        self.assertGreater(len(tokens_with_stopwords), len(tokens_without_stopwords))

    def test_02_extract_sentences(self):
        sentences = self.analyzer.extract_sentences(self.test_text)
        
        self.assertIsInstance(sentences, list)
        self.assertGreaterEqual(len(sentences), 2)
        
        for sentence in sentences:
            self.assertIsInstance(sentence, str)
            self.assertGreater(len(sentence.strip()), 20)

    
    def test_03_detect_citations(self):
                citations = self.analyzer.detect_citations(self.test_text)
        
        self.assertIsInstance(citations, list)
        self.assertGreaterEqual(len(citations), 1)
        
        if citations:
            citation = citations[0]
            self.assertIn('text', citation)
            self.assertIn('position', citation)
            self.assertIn('type', citation)
            self.assertIn('name', citation)
            self.assertIn('year', citation)
            self.assertEqual(citation['year'], 2022)
    
    def test_04_calculate_readability_scores(self):
        scores = self.analyzer.calculate_readability_scores(self.test_text)
        
        self.assertIsInstance(scores, dict)
        self.assertGreater(len(scores), 0)
        
        expected_metrics = [
            'flesch_reading_ease',
            'flesch_kincaid_grade',
            'gunning_fog_index',
            'smog_index',
            'coleman_liau_index',
            'automated_readability_index',
            'dale_chall_score'
        ]
        
        for metric in expected_metrics:
            if metric in scores:
                self.assertIsInstance(scores[metric], float)
    
    def test_05_extract_key_phrases(self):
        key_phrases = self.analyzer.extract_key_phrases(self.test_text, n=5)
        
        self.assertIsInstance(key_phrases, list)
        self.assertLessEqual(len(key_phrases), 5)
        
        if key_phrases:
            for phrase, freq, score in key_phrases:
                self.assertIsInstance(phrase, str)
                self.assertIsInstance(freq, int)
                self.assertIsInstance(score, float)
                self.assertGreater(freq, 0)
                self.assertGreater(score, 0.0)
    
    def test_06_detect_academic_structure(self):
        academic_text = """
        ABSTRACT
        This paper examines the impact of machine learning on business analytics.
        
        INTRODUCTION
        Machine learning has revolutionized data analysis in recent years.
        
        METHODOLOGY
        We conducted a survey of 500 companies using structured questionnaires.
        
        RESULTS
        Our findings indicate a 40% improvement in decision-making accuracy.
        
        CONCLUSION
        Machine learning significantly enhances business analytics capabilities.
        
        REFERENCES
        1. Smith, J. (2020). Machine Learning in Business. Journal of Analytics.
        2. Johnson, A. (2021). Data-Driven Decision Making. Business Review.
        """
        
        structure = self.analyzer.detect_academic_structure(academic_text)
        self.assertIsInstance(structure, dict)
        self.assertTrue(structure['abstract'])
        self.assertTrue(structure['introduction'])
        self.assertTrue(structure['methodology'])
        self.assertTrue(structure['results'])
        self.assertTrue(structure['conclusion'])
        self.assertTrue(structure['references'])
        
        self.assertIn('sections', structure)
        self.assertIn('section_count', structure)
        self.assertGreater(structure['section_count'], 0)
    
    def test_07_analyze_writing_style(self):
        style = self.analyzer.analyze_writing_style(self.test_text)
        
        self.assertIsInstance(style, dict)
        self.assertGreater(len(style), 0)
        
        expected_metrics = [
            'avg_sentence_length',
            'max_sentence_length',
            'min_sentence_length',
            'vocabulary_richness',
            'avg_word_length',
            'passive_voice_percentage',
            'academic_indicators'
        ]
        
        for metric in expected_metrics:
            self.assertIn(metric, style)
        self.assertIsInstance(style['academic_indicators'], dict)

    def test_08_detect_paraphrasing_patterns(self):
        patterns = self.analyzer.detect_paraphrasing_patterns(self.test_text)
        
        self.assertIsInstance(patterns, list)
        
        if patterns:
            for pattern in patterns:
                self.assertIn('name', pattern)
                self.assertIn('description', pattern)
                self.assertIn('count', pattern)
                self.assertIn('examples', pattern)
                self.assertIsInstance(pattern['count'], int)
                self.assertIsInstance(pattern['examples'], list)
    
    def test_09_generate_text_statistics(self):
        stats = self.analyzer.generate_text_statistics(self.test_text)
        
        self.assertIsInstance(stats, dict)
        for section in ['basic_statistics', 'averages', 'readability', 
                       'writing_style', 'citations', 'key_phrases',
                       'academic_structure', 'paraphrasing_patterns',
                       'analysis_timestamp']:
            self.assertIn(section, stats)
        
        basic_stats = stats['basic_statistics']
        self.assertIn('total_characters', basic_stats)
        self.assertIn('total_words', basic_stats)
        self.assertIn('total_sentences', basic_stats)
        self.assertIn('total_paragraphs', basic_stats)
        self.assertIn('character_distribution', basic_stats)
        char_dist = basic_stats['character_distribution']
        for char_type in ['alphabetic', 'numeric', 'spaces', 'punctuation', 'other']:
            self.assertIn(char_type, char_dist)
        
    
    def test_10_compare_texts(self):
        text1 = "Machine learning algorithms can identify patterns in data."
        text2 = "Patterns in data can be identified using machine learning algorithms."
        
        comparison = self.analyzer.compare_texts(text1, text2)
        
        self.assertIsInstance(comparison, dict)
        for section in ['similarity_metrics', 'readability_comparison',
                       'writing_style_comparison', 'text1_statistics',
                       'text2_statistics', 'key_differences']:
            self.assertIn(section, comparison)
        
        similarity_metrics = comparison['similarity_metrics']
        for metric in ['jaccard_similarity', 'overlap_coefficient', 
                      'dice_coefficient', 'shared_words']:
            self.assertIn(metric, similarity_metrics)

class TestDatabaseManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not IMPORT_SUCCESS:
            raise unittest.SkipTest("Required imports not available")

        cls.temp_dir = tempfile.mkdtemp()
        cls.db_path = Path(cls.temp_dir) / 'test_database.sqlite'
        
        cls.config = {
            'paths.database': str(cls.db_path)
        }
        
        cls.db_manager = DatabaseManager(cls.config)
        cls.sample_docs = [
            {
                'source': 'Test Document 1',
                'text': 'This is a test document about machine learning.',
                'url': 'https://example.com/doc1',
                'category': 'Technical'
            },
            {
                'source': 'Test Document 2',
                'text': 'Another test document about data science.',
                'url': 'https://example.com/doc2',
                'category': 'Academic'
            },
            {
                'source': 'Test Document 3',
                'text': 'Test document about artificial intelligence.',
                'url': 'https://example.com/doc3',
                'category': 'Technical'
            }
        ]
    
    def setUp(self):
        if self.db_path.exists():
            self.db_path.unlink()
        self.db_manager = DatabaseManager(self.config)
    
    def test_01_add_document(self):
        for doc in self.sample_docs:
            success = self.db_manager.add_document(
                source=doc['source'],
                text=doc['text'],
                url=doc['url'],
                category=doc['category']
            )
            self.assertTrue(success)
        
        success = self.db_manager.add_document(
            source=self.sample_docs[0]['source'],
            text=self.sample_docs[0]['text'],
            url=self.sample_docs[0]['url'],
            category=self.sample_docs[0]['category']
        )

        self.assertFalse(success)
    
    def test_02_get_all_documents(self):
        for doc in self.sample_docs:
            self.db_manager.add_document(
                doc['source'], doc['text'], doc['url'], doc['category']
            )
        docs = self.db_manager.get_all_documents()
        
        self.assertIsInstance(docs, list)
        self.assertEqual(len(docs), len(self.sample_docs))
        for doc in docs:
            self.assertIn('source', doc)
            self.assertIn('text', doc)
            self.assertIn('url', doc)
            self.assertIn('category', doc)
            self.assertIn('added_date', doc)
            self.assertIn('word_count', doc)
            self.assertIn('metadata', doc)
    
    def test_03_get_documents_by_category(self):
        for doc in self.sample_docs:
            self.db_manager.add_document(
                doc['source'], doc['text'], doc['url'], doc['category']
            )
        tech_docs = self.db_manager.get_all_documents(category='Technical')
        self.assertIsInstance(tech_docs, list)
        tech_count = sum(1 for doc in self.sample_docs if doc['category'] == 'Technical')
        self.assertEqual(len(tech_docs), tech_count)
        for doc in tech_docs:
            self.assertEqual(doc['category'], 'Technical')
    
    def test_04_search_documents(self):
        for doc in self.sample_docs:
            self.db_manager.add_document(
                doc['source'], doc['text'], doc['url'], doc['category']
            )
        results = self.db_manager.search_documents("machine learning")
        self.assertIsInstance(results, list)
        self.assertGreaterEqual(len(results), 1)
        results = self.db_manager.search_documents("data", category="Academic")
        self.assertIsInstance(results, list)