from .test_engine import (
    TestBaseEngine,
    TestAdvancedEngine,
    TestUltimateEngine,
    TestAdvancedTextAnalyzer,
    TestDatabaseManager,
    TestUtils,
    TestTextExtractor,
    TestSimilarityAlgorithms,
    TestMLFeatures,
    TestIntegration,
    run_tests
)

__all__ = [
    'TestBaseEngine',
    'TestAdvancedEngine', 
    'TestUltimateEngine',
    'TestAdvancedTextAnalyzer',
    'TestDatabaseManager',
    'TestUtils',
    'TestTextExtractor',
    'TestSimilarityAlgorithms',
    'TestMLFeatures',
    'TestIntegration',
    'run_tests'
]

# Version information
__version__ = '1.0.0'
__author__ = 'Plagiarism Checker Pro Team'
__description__ = 'Comprehensive test suite for Plagiarism Checker Pro'

# Test categories for organization
TEST_CATEGORIES = {
    'core': [
        'TestBaseEngine',
        'TestAdvancedEngine',
        'TestUltimateEngine',
        'TestAdvancedTextAnalyzer',
        'TestDatabaseManager',
        'TestUtils'
    ],
    'algorithms': [
        'TestSimilarityAlgorithms',
        'TestMLFeatures'
    ],
    'integration': [
        'TestIntegration'
    ],
    'file_handlers': [
        'TestTextExtractor'
    ]
}

# Test dependencies
TEST_DEPENDENCIES = {
    'core': ['core'],
    'algorithms': ['algorithms'],
    'file_handlers': ['file_handlers'],
    'integration': ['core', 'algorithms', 'file_handlers']
}

def get_test_category(test_class_name):
    """
    Get the category of a test class
    
    Args:
        test_class_name: Name of the test class
        
    Returns:
        Category name or None if not found
    """
    for category, tests in TEST_CATEGORIES.items():
        if test_class_name in tests:
            return category
    return None

def get_tests_by_category(category):
    """
    Get all test classes in a category
    
    Args:
        category: Category name
        
    Returns:
        List of test class names in the category
    """
    return TEST_CATEGORIES.get(category, [])

def get_all_test_classes():
    """
    Get all available test classes
    
    Returns:
        List of all test class names
    """
    all_tests = []
    for tests in TEST_CATEGORIES.values():
        all_tests.extend(tests)
    return all_tests

def check_test_dependencies(test_class_name):
    """
    Check if dependencies for a test are available
    
    Args:
        test_class_name: Name of the test class
        
    Returns:
        Tuple of (is_available, missing_dependencies)
    """
    category = get_test_category(test_class_name)
    if not category:
        return False, [f"Unknown test category for {test_class_name}"]
    
    dependencies = TEST_DEPENDENCIES.get(category, [])
    missing = []
    
    for dependency in dependencies:
        try:
            if dependency == 'core':
                from core.base_engine import BasePlagiarismEngine
            elif dependency == 'algorithms':
                from algorithms.similarity import SimilarityAlgorithms
            elif dependency == 'file_handlers':
                from file_handlers.text_extractor import TextExtractor
        except ImportError as e:
            missing.append(f"{dependency}: {e}")
    
    return len(missing) == 0, missing

def create_test_suite(categories=None, test_names=None):
    """
    Create a test suite with selected tests
    
    Args:
        categories: List of category names to include (None for all)
        test_names: List of specific test names to include (None for all)
        
    Returns:
        unittest.TestSuite object
    """
    import unittest
    
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    
    # Map test class names to actual classes
    test_class_map = {
        'TestBaseEngine': TestBaseEngine,
        'TestAdvancedEngine': TestAdvancedEngine,
        'TestUltimateEngine': TestUltimateEngine,
        'TestAdvancedTextAnalyzer': TestAdvancedTextAnalyzer,
        'TestDatabaseManager': TestDatabaseManager,
        'TestUtils': TestUtils,
        'TestTextExtractor': TestTextExtractor,
        'TestSimilarityAlgorithms': TestSimilarityAlgorithms,
        'TestMLFeatures': TestMLFeatures,
        'TestIntegration': TestIntegration
    }
    
    # Determine which tests to include
    test_classes_to_run = []
    
    if test_names:
        # Specific test names provided
        for test_name in test_names:
            if test_name in test_class_map:
                test_classes_to_run.append(test_name)
            else:
                print(f"Warning: Test class '{test_name}' not found")
    elif categories:
        # Categories provided
        for category in categories:
            if category in TEST_CATEGORIES:
                test_classes_to_run.extend(TEST_CATEGORIES[category])
            else:
                print(f"Warning: Test category '{category}' not found")
    else:
        # All tests
        test_classes_to_run = list(test_class_map.keys())
    
    # Add tests to suite
    for test_class_name in test_classes_to_run:
        test_class = test_class_map.get(test_class_name)
        if test_class:
            # Check dependencies
            available, missing = check_test_dependencies(test_class_name)
            if available:
                try:
                    suite.addTest(loader.loadTestsFromTestCase(test_class))
                except Exception as e:
                    print(f"Warning: Failed to load tests from {test_class_name}: {e}")
            else:
                print(f"Warning: Skipping {test_class_name} - missing dependencies: {missing}")
        else:
            print(f"Warning: Test class '{test_class_name}' not found in test_class_map")
    
    return suite

def run_category_tests(categories, verbosity=2):
    """
    Run tests from specific categories
    
    Args:
        categories: List of category names
        verbosity: Test output verbosity
        
    Returns:
        unittest.TestResult object
    """
    suite = create_test_suite(categories=categories)
    runner = unittest.TextTestRunner(verbosity=verbosity)
    return runner.run(suite)

def run_specific_tests(test_names, verbosity=2):
    """
    Run specific tests by name
    
    Args:
        test_names: List of test class names
        verbosity: Test output verbosity
        
    Returns:
        unittest.TestResult object
    """
    suite = create_test_suite(test_names=test_names)
    runner = unittest.TextTestRunner(verbosity=verbosity)
    return runner.run(suite)

# Convenience functions for common test scenarios
def run_core_tests(verbosity=2):
    """Run only core functionality tests"""
    return run_category_tests(['core'], verbosity)

def run_algorithm_tests(verbosity=2):
    """Run only algorithm tests"""
    return run_category_tests(['algorithms'], verbosity)

def run_integration_tests(verbosity=2):
    """Run only integration tests"""
    return run_category_tests(['integration'], verbosity)

def run_file_handler_tests(verbosity=2):
    """Run only file handler tests"""
    return run_category_tests(['file_handlers'], verbosity)

# Test statistics and reporting
class TestStatistics:
    """Collect and report test statistics"""
    
    def __init__(self):
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.skipped_tests = 0
        self.errors = 0
        self.test_times = {}
        self.category_results = {}
    
    def update_from_result(self, result):
        """Update statistics from test result"""
        self.total_tests = result.testsRun
        self.failed_tests = len(result.failures)
        self.errors = len(result.errors)
        self.skipped_tests = len(result.skipped)
        self.passed_tests = self.total_tests - self.failed_tests - self.errors - self.skipped_tests
    
    def get_summary(self):
        """Get summary statistics"""
        return {
            'total_tests': self.total_tests,
            'passed_tests': self.passed_tests,
            'failed_tests': self.failed_tests,
            'skipped_tests': self.skipped_tests,
            'errors': self.errors,
            'success_rate': (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        }
    
    def print_report(self):
        """Print a formatted test report"""
        summary = self.get_summary()
        
        print("\n" + "="*70)
        print("TEST REPORT SUMMARY")
        print("="*70)
        print(f"Total Tests Run:    {summary['total_tests']}")
        print(f"Tests Passed:       {summary['passed_tests']}")
        print(f"Tests Failed:       {summary['failed_tests']}")
        print(f"Tests Skipped:      {summary['skipped_tests']}")
        print(f"Errors:             {summary['errors']}")
        print(f"Success Rate:       {summary['success_rate']:.2f}%")
        print("="*70)
        
        if summary['success_rate'] == 100:
            print("\n✅ All tests passed successfully!")
        elif summary['success_rate'] >= 90:
            print("\n⚠️  Most tests passed, but some issues need attention.")
        elif summary['success_rate'] >= 70:
            print("\n⚠️  Significant test failures detected.")
        else:
            print("\n❌ Major test failures detected. Immediate attention required.")

# Test utilities
def create_test_data():
    """
    Create sample test data for manual testing
    
    Returns:
        Dictionary with sample test data
    """
    return {
        'sample_texts': {
            'original': "Machine learning is a branch of artificial intelligence that focuses on the development of algorithms that can learn from and make predictions on data.",
            'paraphrased': "As a subset of AI, machine learning concentrates on creating algorithms capable of learning from data and making predictions.",
            'different': "The quick brown fox jumps over the lazy dog. This sentence contains all letters of the English alphabet."
        },
        'sample_documents': [
            {
                'source': 'AI Textbook',
                'text': 'Artificial intelligence encompasses various technologies including machine learning, natural language processing, and computer vision.',
                'category': 'Academic'
            },
            {
                'source': 'Research Paper',
                'text': 'Deep learning models have achieved state-of-the-art results in image recognition and natural language processing tasks.',
                'category': 'Research'
            }
        ],
        'test_config': {
            'detection.basic.min_match_length': 5,
            'detection.advanced.algorithms': ['cosine', 'jaccard', 'ngram'],
            'paths.database': ':memory:'
        }
    }

def validate_test_environment():
    """
    Validate that the test environment is properly set up
    
    Returns:
        Dictionary with validation results
    """
    import sys
    import importlib
    
    validation = {
        'python_version': sys.version,
        'platform': sys.platform,
        'modules': {},
        'status': 'PASS'
    }
    
    # Check required modules
    required_modules = [
        'unittest',
        'json',
        'tempfile',
        'pathlib',
        'datetime'
    ]
    
    # Check core modules
    core_modules = [
        'core.base_engine',
        'core.advanced_engine',
        'core.analyzer',
        'core.database',
        'core.utils'
    ]
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            validation['modules'][module] = 'AVAILABLE'
        except ImportError:
            validation['modules'][module] = 'MISSING'
            validation['status'] = 'FAIL'
    
    for module in core_modules:
        try:
            importlib.import_module(module)
            validation['modules'][module] = 'AVAILABLE'
        except ImportError:
            validation['modules'][module] = 'MISSING'
            # Core modules are required
            validation['status'] = 'FAIL'
    
    # Check optional modules
    optional_modules = [
        'algorithms.similarity',
        'algorithms.ml_features',
        'file_handlers.text_extractor',
        'file_handlers.docx_handler',
        'file_handlers.pdf_handler'
    ]
    
    for module in optional_modules:
        try:
            importlib.import_module(module)
            validation['modules'][module] = 'AVAILABLE'
        except ImportError:
            validation['modules'][module] = 'MISSING (optional)'
    
    return validation

# Quick test runner for development
def quick_test():
    """
    Run a quick subset of tests for development
    
    Returns:
        Test results
    """
    print("Running quick test suite...")
    
    # Run only core tests for speed
    result = run_core_tests(verbosity=1)
    
    stats = TestStatistics()
    stats.update_from_result(result)
    stats.print_report()
    
    return result

# Performance testing utilities
class PerformanceTimer:
    """Timer for performance testing"""
    
    def __init__(self):
        self.times = {}
    
    def start(self, name):
        """Start timer for a named operation"""
        import time
        self.times[name] = {
            'start': time.time(),
            'end': None,
            'duration': None
        }
    
    def stop(self, name):
        """Stop timer for a named operation"""
        import time
        if name in self.times:
            self.times[name]['end'] = time.time()
            self.times[name]['duration'] = (
                self.times[name]['end'] - self.times[name]['start']
            )
    
    def get_duration(self, name):
        """Get duration for a named operation"""
        return self.times.get(name, {}).get('duration')
    
    def print_summary(self):
        """Print timing summary"""
        print("\n" + "="*70)
        print("PERFORMANCE TIMING SUMMARY")
        print("="*70)
        
        for name, data in self.times.items():
            if data['duration'] is not None:
                print(f"{name:30}: {data['duration']:.4f} seconds")
        
        total_time = sum(data['duration'] for data in self.times.values() 
                        if data['duration'] is not None)
        print(f"\n{'Total time':30}: {total_time:.4f} seconds")
        print("="*70)

# Test fixtures and utilities
def setup_test_database(db_manager):
    """
    Set up a test database with sample data
    
    Args:
        db_manager: DatabaseManager instance
        
    Returns:
        List of added document IDs
    """
    test_documents = [
        {
            'source': 'Academic Integrity Guide',
            'text': 'Academic integrity involves honesty, trust, fairness, respect, and responsibility in academic work.',
            'url': 'https://example.com/integrity',
            'category': 'Academic'
        },
        {
            'source': 'Plagiarism Definition',
            'text': 'Plagiarism is using someone else\'s work or ideas without proper attribution.',
            'url': 'https://example.com/plagiarism',
            'category': 'General'
        },
        {
            'source': 'Citation Styles',
            'text': 'Common citation styles include APA, MLA, Chicago, and Harvard formats.',
            'url': 'https://example.com/citations',
            'category': 'Academic'
        }
    ]
    
    added_docs = []
    for doc in test_documents:
        success = db_manager.add_document(
            doc['source'], doc['text'], doc['url'], doc['category']
        )
        if success:
            added_docs.append(doc['source'])
    
    return added_docs

def cleanup_test_database(db_manager):
    """
    Clean up test database
    
    Args:
        db_manager: DatabaseManager instance
    """
    # Delete all documents
    docs = db_manager.get_all_documents()
    for doc in docs:
        db_manager.delete_document(doc['source'])
    
    # Clear history
    db_manager.clear_history()

# Test discovery and auto-import
def discover_tests():
    """
    Discover all test modules in the tests directory
    
    Returns:
        List of discovered test module names
    """
    import os
    import glob
    
    test_dir = os.path.dirname(__file__)
    test_modules = []
    
    for file in glob.glob(os.path.join(test_dir, "test_*.py")):
        module_name = os.path.basename(file)[:-3]  # Remove .py extension
        test_modules.append(module_name)
    
    return test_modules

# Main test execution function
def main():
    """
    Main function to run tests from command line
    
    This provides a simple way to run tests directly from this module
    """
    import sys
    
    if len(sys.argv) > 1:
        # Parse command line arguments
        if sys.argv[1] == '--quick':
            quick_test()
        elif sys.argv[1] == '--core':
            run_core_tests()
        elif sys.argv[1] == '--all':
            run_tests()
        elif sys.argv[1] == '--validate':
            results = validate_test_environment()
            import json
            print(json.dumps(results, indent=2))
        elif sys.argv[1] == '--help':
            print("""
Test Runner Options:
  --quick     Run quick test suite
  --core      Run core functionality tests
  --all       Run all tests
  --validate  Validate test environment
  --help      Show this help message
            """)
        else:
            print(f"Unknown option: {sys.argv[1]}")
            print("Use --help for available options")
    else:
        # Default: run all tests
        run_tests()

if __name__ == '__main__':
    main()