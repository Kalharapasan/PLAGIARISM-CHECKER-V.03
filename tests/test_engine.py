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