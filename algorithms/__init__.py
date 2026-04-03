try:
    from .similarity import (
        SimilarityAlgorithms,
        normalize_score,
        calculate_confidence_interval,
        create_similarity_report
    )
    SIMILARITY_AVAILABLE = True
except ImportError as e:
    print(f"⚠ Warning: Similarity algorithms not available: {e}")
    SIMILARITY_AVAILABLE = False

try:
    from .nlp import (
        NLPProcessor,
        extract_nlp_features,
        analyze_text_complexity,
        detect_writing_patterns
    )
    NLP_AVAILABLE = True
except ImportError as e:
    print(f"⚠ Warning: NLP algorithms not available: {e}")
    NLP_AVAILABLE = False

try:
    from .citations import (
        CitationDetector,
        detect_citations,
        extract_citation_info,
        validate_citation_format,
        CitationPatterns
    )
    CITATIONS_AVAILABLE = True
except ImportError as e:
    print(f"⚠ Warning: Citation algorithms not available: {e}")
    CITATIONS_AVAILABLE = False

try:
    from .ml_features import (
        MLFeatures,
        create_ml_pipeline,
        validate_text_for_ml,
        batch_process_texts
    )
    ML_FEATURES_AVAILABLE = True
except ImportError as e:
    print(f"⚠ Warning: ML features not available: {e}")
    ML_FEATURES_AVAILABLE = False

# Define exports
__all__ = []

if SIMILARITY_AVAILABLE:
    __all__.extend([
        'SimilarityAlgorithms',
        'normalize_score',
        'calculate_confidence_interval',
        'create_similarity_report'
    ])

if NLP_AVAILABLE:
    __all__.extend([
        'NLPProcessor',
        'extract_nlp_features',
        'analyze_text_complexity',
        'detect_writing_patterns'
    ])

if CITATIONS_AVAILABLE:
    __all__.extend([
        'CitationDetector',
        'detect_citations',
        'extract_citation_info',
        'validate_citation_format',
        'CitationPatterns'
    ])

if ML_FEATURES_AVAILABLE:
    __all__.extend([
        'MLFeatures',
        'create_ml_pipeline',
        'validate_text_for_ml',
        'batch_process_texts'
    ])

# Package metadata
__version__ = '1.0.0'
__author__ = 'Plagiarism Checker Pro Team'
__description__ = 'Advanced text analysis and similarity algorithms for plagiarism detection'

# Algorithm categories
ALGORITHM_CATEGORIES = {
    'similarity': [
        'SimilarityAlgorithms',
        'normalize_score',
        'calculate_confidence_interval',
        'create_similarity_report'
    ],
    'nlp': [
        'NLPProcessor',
        'extract_nlp_features',
        'analyze_text_complexity',
        'detect_writing_patterns'
    ],
    'citations': [
        'CitationDetector',
        'detect_citations',
        'extract_citation_info',
        'validate_citation_format',
        'CitationPatterns'
    ],
    'machine_learning': [
        'MLFeatures',
        'create_ml_pipeline',
        'validate_text_for_ml',
        'batch_process_texts'
    ]
}

# Algorithm descriptions
ALGORITHM_DESCRIPTIONS = {
    'SimilarityAlgorithms': 'Multiple text similarity algorithms including cosine, Jaccard, n-gram, and semantic similarity',
    'normalize_score': 'Normalize similarity scores to a standard range',
    'calculate_confidence_interval': 'Calculate statistical confidence intervals for similarity scores',
    'create_similarity_report': 'Generate comprehensive similarity analysis reports',
    'NLPProcessor': 'Natural Language Processing features for text analysis',
    'extract_nlp_features': 'Extract NLP-based features from text',
    'analyze_text_complexity': 'Analyze text complexity and readability',
    'detect_writing_patterns': 'Detect writing patterns and styles',
    'CitationDetector': 'Detect and analyze citations in text',
    'detect_citations': 'Find citations using pattern matching',
    'extract_citation_info': 'Extract structured information from citations',
    'validate_citation_format': 'Validate citation formatting against style guides',
    'CitationPatterns': 'Predefined citation patterns for common styles',
    'MLFeatures': 'Machine learning features for advanced plagiarism detection',
    'create_ml_pipeline': 'Create ML pipeline configurations',
    'validate_text_for_ml': 'Validate text suitability for ML processing',
    'batch_process_texts': 'Process multiple texts with ML features'
}

# Algorithm dependencies
ALGORITHM_DEPENDENCIES = {
    'similarity': ['numpy', 'scikit-learn'],
    'nlp': ['nltk', 'spacy'],
    'citations': ['regex'],
    'machine_learning': ['scikit-learn', 'pandas', 'numpy']
}

# Utility functions
def get_available_algorithms():
    """
    Get list of available algorithms
    
    Returns:
        Dictionary mapping algorithm names to availability status
    """
    return {
        'similarity': SIMILARITY_AVAILABLE,
        'nlp': NLP_AVAILABLE,
        'citations': CITATIONS_AVAILABLE,
        'machine_learning': ML_FEATURES_AVAILABLE
    }

def check_algorithm_dependencies(algorithm_name):
    """
    Check if dependencies for an algorithm are available
    
    Args:
        algorithm_name: Name of the algorithm
        
    Returns:
        Tuple of (is_available, missing_dependencies)
    """
    import importlib
    
    if algorithm_name in ALGORITHM_DEPENDENCIES:
        dependencies = ALGORITHM_DEPENDENCIES[algorithm_name]
        missing = []
        
        for dep in dependencies:
            try:
                importlib.import_module(dep)
            except ImportError:
                missing.append(dep)
        
        return len(missing) == 0, missing
    else:
        return False, [f"Unknown algorithm: {algorithm_name}"]

def get_algorithm_description(algorithm_name):
    """
    Get description of an algorithm
    
    Args:
        algorithm_name: Name of the algorithm
        
    Returns:
        Description string or None if not found
    """
    return ALGORITHM_DESCRIPTIONS.get(algorithm_name)

def list_algorithms_by_category():
    """
    List all algorithms organized by category
    
    Returns:
        Dictionary mapping categories to algorithm lists
    """
    available = {}
    
    for category, algorithms in ALGORITHM_CATEGORIES.items():
        available_algorithms = []
        for algo in algorithms:
            if algo in globals() and globals()[algo] is not None:
                available_algorithms.append(algo)
        
        if available_algorithms:
            available[category] = available_algorithms
    
    return available

# Algorithm factory
class AlgorithmFactory:
    """
    Factory class for creating algorithm instances
    """
    
    @staticmethod
    def create_similarity_algorithm(config=None):
        """
        Create a similarity algorithm instance
        
        Args:
            config: Configuration dictionary
            
        Returns:
            SimilarityAlgorithms instance or None if unavailable
        """
        if not SIMILARITY_AVAILABLE:
            print("Error: Similarity algorithms not available")
            return None
        
        try:
            return SimilarityAlgorithms(config)
        except Exception as e:
            print(f"Error creating similarity algorithm: {e}")
            return None
    
    @staticmethod
    def create_nlp_processor(config=None):
        """
        Create an NLP processor instance
        
        Args:
            config: Configuration dictionary
            
        Returns:
            NLPProcessor instance or None if unavailable
        """
        if not NLP_AVAILABLE:
            print("Error: NLP algorithms not available")
            return None
        
        try:
            return NLPProcessor(config)
        except Exception as e:
            print(f"Error creating NLP processor: {e}")
            return None
    
    @staticmethod
    def create_citation_detector(config=None):
        """
        Create a citation detector instance
        
        Args:
            config: Configuration dictionary
            
        Returns:
            CitationDetector instance or None if unavailable
        """
        if not CITATIONS_AVAILABLE:
            print("Error: Citation algorithms not available")
            return None
        
        try:
            return CitationDetector(config)
        except Exception as e:
            print(f"Error creating citation detector: {e}")
            return None
    
    @staticmethod
    def create_ml_features(config=None):
        """
        Create ML features instance
        
        Args:
            config: Configuration dictionary
            
        Returns:
            MLFeatures instance or None if unavailable
        """
        if not ML_FEATURES_AVAILABLE:
            print("Error: ML features not available")
            return None
        
        try:
            return MLFeatures(config)
        except Exception as e:
            print(f"Error creating ML features: {e}")
            return None
    
    @staticmethod
    def create_all_available(config=None):
        """
        Create all available algorithm instances
        
        Args:
            config: Configuration dictionary
            
        Returns:
            Dictionary of algorithm instances
        """
        algorithms = {}
        
        if SIMILARITY_AVAILABLE:
            algorithms['similarity'] = AlgorithmFactory.create_similarity_algorithm(config)
        
        if NLP_AVAILABLE:
            algorithms['nlp'] = AlgorithmFactory.create_nlp_processor(config)
        
        if CITATIONS_AVAILABLE:
            algorithms['citations'] = AlgorithmFactory.create_citation_detector(config)
        
        if ML_FEATURES_AVAILABLE:
            algorithms['ml_features'] = AlgorithmFactory.create_ml_features(config)
        
        return algorithms

# Combined algorithm processor
class CombinedAlgorithmProcessor:
    """
    Combined processor for using multiple algorithms together
    """
    
    def __init__(self, config=None):
        self.config = config or {}
        self.algorithms = AlgorithmFactory.create_all_available(config)
        self.results_cache = {}
    
    def analyze_text(self, text, use_algorithms=None):
        """
        Analyze text using multiple algorithms
        
        Args:
            text: Text to analyze
            use_algorithms: List of algorithm names to use (None for all available)
            
        Returns:
            Dictionary with analysis results from all algorithms
        """
        import hashlib
        
        # Create cache key
        cache_key = hashlib.md5(text.encode()).hexdigest()
        if cache_key in self.results_cache:
            return self.results_cache[cache_key]
        
        results = {
            'text_hash': cache_key,
            'algorithms_used': [],
            'results': {}
        }
        
        if use_algorithms is None:
            use_algorithms = list(self.algorithms.keys())
        
        for algo_name in use_algorithms:
            if algo_name in self.algorithms and self.algorithms[algo_name]:
                try:
                    if algo_name == 'similarity':
                        # For similarity, we need two texts to compare
                        # Store processor for later comparison
                        results['results'][algo_name] = {
                            'processor': self.algorithms[algo_name],
                            'features': self.algorithms[algo_name].extract_all_features(text)
                        }
                    
                    elif algo_name == 'nlp':
                        nlp_results = self.algorithms[algo_name].analyze_text(text)
                        results['results'][algo_name] = nlp_results
                    
                    elif algo_name == 'citations':
                        citations = self.algorithms[algo_name].detect_citations(text)
                        results['results'][algo_name] = citations
                    
                    elif algo_name == 'ml_features':
                        features = self.algorithms[algo_name].extract_all_features(text)
                        results['results'][algo_name] = features
                    
                    results['algorithms_used'].append(algo_name)
                    
                except Exception as e:
                    results['results'][algo_name] = {'error': str(e)}
        
        # Cache results
        self.results_cache[cache_key] = results
        
        return results
    
    def compare_texts(self, text1, text2, use_algorithms=None):
        """
        Compare two texts using multiple algorithms
        
        Args:
            text1: First text
            text2: Second text
            use_algorithms: List of algorithm names to use
            
        Returns:
            Dictionary with comparison results
        """
        import hashlib
        
        # Create cache key
        cache_key = hashlib.md5((text1 + text2).encode()).hexdigest()
        if cache_key in self.results_cache:
            return self.results_cache[cache_key]
        
        comparison = {
            'text1_hash': hashlib.md5(text1.encode()).hexdigest(),
            'text2_hash': hashlib.md5(text2.encode()).hexdigest(),
            'algorithms_used': [],
            'similarity_scores': {},
            'detailed_comparison': {}
        }
        
        if use_algorithms is None:
            use_algorithms = list(self.algorithms.keys())
        
        for algo_name in use_algorithms:
            if algo_name in self.algorithms and self.algorithms[algo_name]:
                try:
                    if algo_name == 'similarity':
                        similarity_algo = self.algorithms[algo_name]
                        
                        # Calculate multiple similarity metrics
                        cosine = similarity_algo.calculate_cosine_similarity(text1, text2)
                        jaccard = similarity_algo.calculate_jaccard_similarity(text1, text2)
                        ngram = similarity_algo.calculate_ngram_similarity(text1, text2)
                        
                        comparison['similarity_scores'][algo_name] = {
                            'cosine': cosine,
                            'jaccard': jaccard,
                            'ngram': ngram,
                            'average': (cosine + jaccard + ngram) / 3
                        }
                        
                        # Get detailed comparison
                        detailed = similarity_algo.analyze_similarity_distribution(text1, text2)
                        comparison['detailed_comparison'][algo_name] = detailed
                    
                    elif algo_name == 'nlp':
                        nlp_processor = self.algorithms[algo_name]
                        features1 = nlp_processor.extract_features(text1)
                        features2 = nlp_processor.extract_features(text2)
                        
                        # Compare NLP features
                        comparison['detailed_comparison'][algo_name] = {
                            'text1_features': features1,
                            'text2_features': features2
                        }
                    
                    elif algo_name == 'ml_features':
                        ml_processor = self.algorithms[algo_name]
                        features1 = ml_processor.extract_all_features(text1)
                        features2 = ml_processor.extract_all_features(text2)
                        
                        # Calculate feature similarity
                        comparison['detailed_comparison'][algo_name] = {
                            'feature_comparison': 'ML feature comparison available'
                        }
                    
                    comparison['algorithms_used'].append(algo_name)
                    
                except Exception as e:
                    comparison['similarity_scores'][algo_name] = {'error': str(e)}
        
        # Calculate overall similarity
        if comparison['similarity_scores']:
            similarity_values = []
            for algo_results in comparison['similarity_scores'].values():
                if 'average' in algo_results:
                    similarity_values.append(algo_results['average'])
            
            if similarity_values:
                comparison['overall_similarity'] = sum(similarity_values) / len(similarity_values)
        
        # Cache results
        self.results_cache[cache_key] = comparison
        
        return comparison
    
    def clear_cache(self):
        """Clear the results cache"""
        self.results_cache.clear()

# Algorithm configuration
class AlgorithmConfig:
    """
    Configuration manager for algorithms
    """
    
    DEFAULT_CONFIG = {
        'similarity': {
            'algorithms': ['cosine', 'jaccard', 'ngram', 'levenshtein'],
            'weights': {
                'cosine': 1.0,
                'jaccard': 0.8,
                'ngram': 0.9,
                'levenshtein': 0.7
            },
            'min_sequence_length': 5,
            'ngram_size': 3
        },
        'nlp': {
            'use_spacy': True,
            'use_nltk': True,
            'extract_pos_tags': True,
            'extract_entities': True,
            'extract_dependencies': False
        },
        'citations': {
            'detection_methods': ['pattern', 'regex', 'ml'],
            'validate_formats': True,
            'extract_authors': True,
            'extract_years': True,
            'extract_pages': True
        },
        'ml_features': {
            'extract_linguistic': True,
            'extract_stylometric': True,
            'extract_nlp': True,
            'extract_embeddings': True,
            'embedding_methods': ['tfidf', 'count', 'char']
        }
    }
    
    def __init__(self, config_file=None):
        self.config = self.DEFAULT_CONFIG.copy()
        
        if config_file:
            self.load_config(config_file)
    
    def load_config(self, config_file):
        """
        Load configuration from file
        
        Args:
            config_file: Path to configuration file
        """
        import json
        from pathlib import Path
        
        config_path = Path(config_file)
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    loaded_config = json.load(f)
                
                # Merge with default config
                self._merge_configs(self.config, loaded_config)
                
            except Exception as e:
                print(f"Warning: Could not load config file: {e}")
    
    def save_config(self, config_file):
        """
        Save configuration to file
        
        Args:
            config_file: Path to configuration file
        """
        import json
        from pathlib import Path
        
        config_path = Path(config_file)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def _merge_configs(self, base, new):
        """Recursively merge configuration dictionaries"""
        for key, value in new.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_configs(base[key], value)
            else:
                base[key] = value
    
    def get_algorithm_config(self, algorithm_name):
        """
        Get configuration for a specific algorithm
        
        Args:
            algorithm_name: Name of the algorithm
            
        Returns:
            Configuration dictionary or empty dict if not found
        """
        return self.config.get(algorithm_name, {})
    
    def update_algorithm_config(self, algorithm_name, new_config):
        """
        Update configuration for a specific algorithm
        
        Args:
            algorithm_name: Name of the algorithm
            new_config: New configuration dictionary
        """
        if algorithm_name in self.config:
            self._merge_configs(self.config[algorithm_name], new_config)
        else:
            self.config[algorithm_name] = new_config

# Performance monitoring
class AlgorithmPerformanceMonitor:
    """
    Monitor algorithm performance and execution times
    """
    
    def __init__(self):
        self.execution_times = {}
        self.memory_usage = {}
        self.call_counts = {}
    
    def start_timing(self, algorithm_name, operation_name):
        """
        Start timing an operation
        
        Args:
            algorithm_name: Name of the algorithm
            operation_name: Name of the operation
        """
        import time
        key = f"{algorithm_name}.{operation_name}"
        self.execution_times[key] = {
            'start': time.time(),
            'end': None,
            'duration': None
        }
    
    def stop_timing(self, algorithm_name, operation_name):
        """
        Stop timing an operation
        
        Args:
            algorithm_name: Name of the algorithm
            operation_name: Name of the operation
        """
        import time
        key = f"{algorithm_name}.{operation_name}"
        if key in self.execution_times:
            self.execution_times[key]['end'] = time.time()
            self.execution_times[key]['duration'] = (
                self.execution_times[key]['end'] - self.execution_times[key]['start']
            )
    
    def record_memory_usage(self, algorithm_name, operation_name, memory_kb):
        """
        Record memory usage for an operation
        
        Args:
            algorithm_name: Name of the algorithm
            operation_name: Name of the operation
            memory_kb: Memory usage in kilobytes
        """
        key = f"{algorithm_name}.{operation_name}"
        if key not in self.memory_usage:
            self.memory_usage[key] = []
        self.memory_usage[key].append(memory_kb)
    
    def increment_call_count(self, algorithm_name, operation_name):
        """
        Increment call count for an operation
        
        Args:
            algorithm_name: Name of the algorithm
            operation_name: Name of the operation
        """
        key = f"{algorithm_name}.{operation_name}"
        self.call_counts[key] = self.call_counts.get(key, 0) + 1
    
    def get_performance_report(self):
        """
        Get performance report
        
        Returns:
            Dictionary with performance statistics
        """
        report = {
            'execution_times': {},
            'memory_usage': {},
            'call_counts': self.call_counts.copy()
        }
        
        # Calculate average execution times
        for key, data in self.execution_times.items():
            if data['duration'] is not None:
                report['execution_times'][key] = {
                    'duration_seconds': data['duration'],
                    'algorithm': key.split('.')[0],
                    'operation': key.split('.')[1]
                }
        
        # Calculate average memory usage
        for key, usage_list in self.memory_usage.items():
            if usage_list:
                report['memory_usage'][key] = {
                    'avg_kb': sum(usage_list) / len(usage_list),
                    'max_kb': max(usage_list),
                    'min_kb': min(usage_list),
                    'samples': len(usage_list)
                }
        
        return report
    
    def print_performance_summary(self):
        """Print formatted performance summary"""
        report = self.get_performance_report()
        
        print("\n" + "="*70)
        print("ALGORITHM PERFORMANCE SUMMARY")
        print("="*70)
        
        if report['execution_times']:
            print("\nExecution Times:")
            for key, data in sorted(report['execution_times'].items(), 
                                   key=lambda x: x[1]['duration_seconds'], 
                                   reverse=True):
                print(f"  {key:40}: {data['duration_seconds']:.4f} seconds")
        
        if report['memory_usage']:
            print("\nMemory Usage (average):")
            for key, data in sorted(report['memory_usage'].items(),
                                   key=lambda x: x[1]['avg_kb'],
                                   reverse=True):
                print(f"  {key:40}: {data['avg_kb']:.2f} KB")
        
        if report['call_counts']:
            print("\nCall Counts:")
            for key, count in sorted(report['call_counts'].items(),
                                    key=lambda x: x[1],
                                    reverse=True):
                print(f"  {key:40}: {count} calls")
        
        print("="*70)
    
    def reset(self):
        """Reset all performance counters"""
        self.execution_times.clear()
        self.memory_usage.clear()
        self.call_counts.clear()

# Algorithm registry
class AlgorithmRegistry:
    """
    Registry for managing and discovering algorithms
    """
    
    _registry = {}
    
    @classmethod
    def register(cls, algorithm_class, name=None, category=None, description=None):
        """
        Register an algorithm class
        
        Args:
            algorithm_class: The algorithm class to register
            name: Algorithm name (defaults to class name)
            category: Algorithm category
            description: Algorithm description
        """
        if name is None:
            name = algorithm_class.__name__
        
        cls._registry[name] = {
            'class': algorithm_class,
            'category': category,
            'description': description,
            'module': algorithm_class.__module__
        }
    
    @classmethod
    def get_algorithm(cls, name):
        """
        Get an algorithm class by name
        
        Args:
            name: Algorithm name
            
        Returns:
            Algorithm class or None if not found
        """
        entry = cls._registry.get(name)
        return entry['class'] if entry else None
    
    @classmethod
    def get_all_algorithms(cls):
        """
        Get all registered algorithms
        
        Returns:
            Dictionary of registered algorithms
        """
        return cls._registry.copy()
    
    @classmethod
    def get_algorithms_by_category(cls, category):
        """
        Get algorithms by category
        
        Args:
            category: Category name
            
        Returns:
            Dictionary of algorithms in the category
        """
        return {name: info for name, info in cls._registry.items() 
                if info['category'] == category}
    
    @classmethod
    def create_instance(cls, name, config=None):
        """
        Create an instance of a registered algorithm
        
        Args:
            name: Algorithm name
            config: Configuration dictionary
            
        Returns:
            Algorithm instance or None if not found
        """
        algorithm_class = cls.get_algorithm(name)
        if algorithm_class:
            try:
                return algorithm_class(config)
            except Exception as e:
                print(f"Error creating instance of {name}: {e}")
                return None
        return None

# Register available algorithms
if SIMILARITY_AVAILABLE:
    AlgorithmRegistry.register(
        SimilarityAlgorithms,
        name='SimilarityAlgorithms',
        category='similarity',
        description='Multiple text similarity algorithms'
    )

if NLP_AVAILABLE:
    AlgorithmRegistry.register(
        NLPProcessor,
        name='NLPProcessor',
        category='nlp',
        description='Natural Language Processing features'
    )

if CITATIONS_AVAILABLE:
    AlgorithmRegistry.register(
        CitationDetector,
        name='CitationDetector',
        category='citations',
        description='Citation detection and analysis'
    )

if ML_FEATURES_AVAILABLE:
    AlgorithmRegistry.register(
        MLFeatures,
        name='MLFeatures',
        category='machine_learning',
        description='Machine learning features for plagiarism detection'
    )

# Convenience functions
def get_algorithm(name):
    """
    Get an algorithm instance by name
    
    Args:
        name: Algorithm name
        
    Returns:
        Algorithm instance or None
    """
    return AlgorithmRegistry.create_instance(name)

def get_all_algorithm_instances(config=None):
    """
    Get instances of all available algorithms
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Dictionary of algorithm instances
    """
    return AlgorithmFactory.create_all_available(config)

def analyze_text_with_all_algorithms(text, config=None):
    """
    Analyze text with all available algorithms
    
    Args:
        text: Text to analyze
        config: Configuration dictionary
        
    Returns:
        Dictionary with analysis results
    """
    processor = CombinedAlgorithmProcessor(config)
    return processor.analyze_text(text)

def compare_texts_with_all_algorithms(text1, text2, config=None):
    """
    Compare two texts with all available algorithms
    
    Args:
        text1: First text
        text2: Second text
        config: Configuration dictionary
        
    Returns:
        Dictionary with comparison results
    """
    processor = CombinedAlgorithmProcessor(config)
    return processor.compare_texts(text1, text2)

# Export additional classes
__all__.extend([
    'AlgorithmFactory',
    'CombinedAlgorithmProcessor',
    'AlgorithmConfig',
    'AlgorithmPerformanceMonitor',
    'AlgorithmRegistry',
    'get_algorithm',
    'get_all_algorithm_instances',
    'analyze_text_with_all_algorithms',
    'compare_texts_with_all_algorithms'
])

# Main function for command-line usage
def main():
    """
    Main function for command-line usage
    """
    import sys
    import json
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'list':
            # List available algorithms
            algorithms = list_algorithms_by_category()
            print(json.dumps(algorithms, indent=2))
        
        elif command == 'check':
            # Check algorithm dependencies
            if len(sys.argv) > 2:
                algorithm = sys.argv[2]
                available, missing = check_algorithm_dependencies(algorithm)
                print(f"Algorithm: {algorithm}")
                print(f"Available: {available}")
                if missing:
                    print(f"Missing dependencies: {', '.join(missing)}")
            else:
                print("Usage: python -m algorithms check <algorithm_name>")
        
        elif command == 'info':
            # Get algorithm information
            if len(sys.argv) > 2:
                algorithm = sys.argv[2]
                description = get_algorithm_description(algorithm)
                if description:
                    print(f"{algorithm}: {description}")
                else:
                    print(f"Algorithm '{algorithm}' not found")
            else:
                print("Usage: python -m algorithms info <algorithm_name>")
        
        elif command == 'test':
            # Run a quick test
            test_text = "This is a test text for algorithm testing."
            print("Testing algorithm package...")
            
            # Test CombinedAlgorithmProcessor
            processor = CombinedAlgorithmProcessor()
            results = processor.analyze_text(test_text)
            
            print(f"Algorithms used: {results['algorithms_used']}")
            print("Test completed successfully!")
        
        else:
            print(f"Unknown command: {command}")
            print("\nAvailable commands:")
            print("  list    - List available algorithms")
            print("  check   - Check algorithm dependencies")
            print("  info    - Get algorithm information")
            print("  test    - Run a quick test")
    else:
        print("Algorithms Package for Plagiarism Checker Pro")
        print("\nUse 'python -m algorithms <command>' where command is:")
        print("  list, check, info, test")

if __name__ == '__main__':
    main()