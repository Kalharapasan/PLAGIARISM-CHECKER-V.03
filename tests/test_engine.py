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