import os
import sys
from pathlib import Path

# Try to import available file handlers
try:
    from .text_extractor import (
        TextExtractor,
        guess_file_format,
        validate_file_for_extraction,
        create_sample_files
    )
    TEXT_EXTRACTOR_AVAILABLE = True
except ImportError as e:
    print(f"⚠ Warning: TextExtractor not available: {e}")
    TEXT_EXTRACTOR_AVAILABLE = False

try:
    from .docx_handler import (
        DOCXHandler,
        extract_docx_as_zip,
        get_docx_word_count,
        get_docx_character_count,
        is_docx_password_protected
    )
    DOCX_HANDLER_AVAILABLE = True
except ImportError as e:
    print(f"⚠ Warning: DOCXHandler not available: {e}")
    DOCX_HANDLER_AVAILABLE = False

try:
    from .pdf_handler import PDFHandler
    PDF_HANDLER_AVAILABLE = True
except ImportError as e:
    print(f"⚠ Warning: PDFHandler not available: {e}")
    PDF_HANDLER_AVAILABLE = False

# Define exports
__all__ = []

if TEXT_EXTRACTOR_AVAILABLE:
    __all__.extend([
        'TextExtractor',
        'guess_file_format',
        'validate_file_for_extraction',
        'create_sample_files'
    ])

if DOCX_HANDLER_AVAILABLE:
    __all__.extend([
        'DOCXHandler',
        'extract_docx_as_zip',
        'get_docx_word_count',
        'get_docx_character_count',
        'is_docx_password_protected'
    ])

if PDF_HANDLER_AVAILABLE:
    __all__.extend([
        'PDFHandler'
    ])

# Package metadata
__version__ = '1.0.0'
__author__ = 'Plagiarism Checker Pro Team'
__description__ = 'File format handlers for text extraction in plagiarism detection'

# Supported file formats
SUPPORTED_FORMATS = {
    # Document formats
    '.txt': 'Plain Text',
    '.docx': 'Microsoft Word (DOCX)',
    '.doc': 'Microsoft Word (DOC)',
    '.pdf': 'Portable Document Format',
    '.rtf': 'Rich Text Format',
    '.odt': 'OpenDocument Text',
    '.html': 'HTML Document',
    '.htm': 'HTML Document',
    '.xml': 'XML Document',
    
    # Presentation formats
    '.pptx': 'Microsoft PowerPoint (PPTX)',
    '.ppt': 'Microsoft PowerPoint (PPT)',
    '.odp': 'OpenDocument Presentation',
    
    # Spreadsheet formats
    '.xlsx': 'Microsoft Excel (XLSX)',
    '.xls': 'Microsoft Excel (XLS)',
    '.ods': 'OpenDocument Spreadsheet',
    '.csv': 'Comma Separated Values',
    
    # Code formats
    '.py': 'Python Source Code',
    '.java': 'Java Source Code',
    '.cpp': 'C++ Source Code',
    '.c': 'C Source Code',
    '.js': 'JavaScript Source Code',
    '.ts': 'TypeScript Source Code',
    '.css': 'Cascading Style Sheets',
    '.json': 'JSON Data',
    '.md': 'Markdown',
    '.sql': 'SQL Script',
    
    # Other formats
    '.tex': 'LaTeX Document',
    '.epub': 'EPUB eBook',
    '.mobi': 'Mobipocket eBook',
    '.azw': 'Amazon Kindle eBook'
}

# Format categories
FORMAT_CATEGORIES = {
    'documents': ['.txt', '.docx', '.doc', '.pdf', '.rtf', '.odt', '.html', '.htm', '.xml', '.tex', '.md'],
    'presentations': ['.pptx', '.ppt', '.odp'],
    'spreadsheets': ['.xlsx', '.xls', '.ods', '.csv'],
    'code': ['.py', '.java', '.cpp', '.c', '.js', '.ts', '.css', '.json', '.sql'],
    'ebooks': ['.epub', '.mobi', '.azw']
}

# Handler availability
HANDLER_AVAILABILITY = {
    'TextExtractor': TEXT_EXTRACTOR_AVAILABLE,
    'DOCXHandler': DOCX_HANDLER_AVAILABLE,
    'PDFHandler': PDF_HANDLER_AVAILABLE
}

# Handler dependencies
HANDLER_DEPENDENCIES = {
    'TextExtractor': ['python-docx', 'pypdf', 'pdfplumber', 'beautifulsoup4', 'pandas'],
    'DOCXHandler': ['python-docx'],
    'PDFHandler': ['pypdf', 'pdfplumber']
}

# Utility functions
def get_supported_formats():
    """
    Get all supported file formats
    
    Returns:
        Dictionary of supported formats
    """
    return SUPPORTED_FORMATS.copy()

def get_formats_by_category(category=None):
    """
    Get file formats by category
    
    Args:
        category: Category name (None for all categories)
        
    Returns:
        Dictionary of formats in the category
    """
    if category:
        return FORMAT_CATEGORIES.get(category, [])
    return FORMAT_CATEGORIES.copy()

def is_format_supported(filepath):
    """
    Check if a file format is supported
    
    Args:
        filepath: Path to the file
        
    Returns:
        Tuple of (is_supported, format_description)
    """
    path = Path(filepath)
    ext = path.suffix.lower()
    
    if ext in SUPPORTED_FORMATS:
        return True, SUPPORTED_FORMATS[ext]
    else:
        return False, f"Unsupported format: {ext}"

def get_format_category(filepath):
    """
    Get the category of a file format
    
    Args:
        filepath: Path to the file
        
    Returns:
        Category name or None
    """
    path = Path(filepath)
    ext = path.suffix.lower()
    
    for category, formats in FORMAT_CATEGORIES.items():
        if ext in formats:
            return category
    return None

def get_available_handlers():
    """
    Get list of available file handlers
    
    Returns:
        Dictionary of handler availability
    """
    return HANDLER_AVAILABILITY.copy()

def check_handler_dependencies(handler_name):
    """
    Check if dependencies for a handler are available
    
    Args:
        handler_name: Name of the handler
        
    Returns:
        Tuple of (is_available, missing_dependencies)
    """
    import importlib
    
    if handler_name in HANDLER_DEPENDENCIES:
        dependencies = HANDLER_DEPENDENCIES[handler_name]
        missing = []
        
        for dep in dependencies:
            try:
                importlib.import_module(dep)
            except ImportError:
                missing.append(dep)
        
        return len(missing) == 0, missing
    else:
        return False, [f"Unknown handler: {handler_name}"]

# Unified file handler
class UnifiedFileHandler:
    """
    Unified interface for all file handlers
    """
    
    def __init__(self, config=None):
        self.config = config or {}
        self.handlers = {}
        self.extraction_cache = {}
        
        # Initialize available handlers
        self._initialize_handlers()
    
    def _initialize_handlers(self):
        """Initialize all available file handlers"""
        if TEXT_EXTRACTOR_AVAILABLE:
            self.handlers['TextExtractor'] = TextExtractor(self.config)
        
        if DOCX_HANDLER_AVAILABLE:
            self.handlers['DOCXHandler'] = DOCXHandler(self.config)
        
        if PDF_HANDLER_AVAILABLE:
            self.handlers['PDFHandler'] = PDFHandler(self.config)
    
    def extract_text(self, filepath, format_hint=None, use_cache=True):
        """
        Extract text from a file using the appropriate handler
        
        Args:
            filepath: Path to the file
            format_hint: Optional format hint if auto-detection fails
            use_cache: Whether to use extraction cache
            
        Returns:
            Extracted text as string
        """
        import hashlib
        
        # Create cache key
        cache_key = hashlib.md5(str(filepath).encode()).hexdigest()
        if use_cache and cache_key in self.extraction_cache:
            return self.extraction_cache[cache_key]
        
        # Check if file exists
        if not Path(filepath).exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        # Get file info
        file_info = self.get_file_info(filepath)
        
        if not file_info['is_supported']:
            raise ValueError(f"Unsupported file format: {file_info['extension']}")
        
        # Try TextExtractor first if available
        if 'TextExtractor' in self.handlers:
            try:
                text = self.handlers['TextExtractor'].extract_text(filepath, format_hint)
                if use_cache:
                    self.extraction_cache[cache_key] = text
                return text
            except Exception as e:
                print(f"TextExtractor failed for {filepath}: {e}")
        
        # Try format-specific handlers
        extension = file_info['extension'].lower()
        
        if extension == '.docx' and 'DOCXHandler' in self.handlers:
            try:
                text = self.handlers['DOCXHandler'].extract_text(filepath)
                if use_cache:
                    self.extraction_cache[cache_key] = text
                return text
            except Exception as e:
                print(f"DOCXHandler failed for {filepath}: {e}")
        
        elif extension == '.pdf' and 'PDFHandler' in self.handlers:
            try:
                text = self.handlers['PDFHandler'].extract_text(filepath)
                if use_cache:
                    self.extraction_cache[cache_key] = text
                return text
            except Exception as e:
                print(f"PDFHandler failed for {filepath}: {e}")
        
        # Fallback to basic text extraction
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            if use_cache:
                self.extraction_cache[cache_key] = text
            return text
        except UnicodeDecodeError:
            # Try binary reading
            with open(filepath, 'rb') as f:
                data = f.read()
                text = data.decode('utf-8', errors='ignore')
                if use_cache:
                    self.extraction_cache[cache_key] = text
                return text
    
    def extract_with_metadata(self, filepath):
        """
        Extract text with metadata
        
        Args:
            filepath: Path to the file
            
        Returns:
            Dictionary with text and metadata
        """
        if 'TextExtractor' in self.handlers:
            try:
                return self.handlers['TextExtractor'].extract_with_metadata(filepath)
            except Exception as e:
                print(f"TextExtractor metadata extraction failed: {e}")
        
        # Fallback to basic extraction
        try:
            text = self.extract_text(filepath, use_cache=False)
            file_info = self.get_file_info(filepath)
            
            return {
                'success': True,
                'text': text,
                'metadata': file_info,
                'text_metrics': {
                    'characters': len(text),
                    'words': len(text.split()),
                    'lines': text.count('\n') + 1,
                    'paragraphs': len([p for p in text.split('\n\n') if p.strip()])
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'filepath': filepath
            }
    
    def batch_extract(self, filepaths, progress_callback=None):
        """
        Extract text from multiple files
        
        Args:
            filepaths: List of file paths
            progress_callback: Callback function for progress updates
            
        Returns:
            List of extraction results
        """
        if 'TextExtractor' in self.handlers:
            return self.handlers['TextExtractor'].batch_extract(filepaths, progress_callback)
        
        # Manual batch extraction
        results = []
        total_files = len(filepaths)
        
        for i, filepath in enumerate(filepaths):
            try:
                result = self.extract_with_metadata(filepath)
                results.append(result)
                
                if progress_callback:
                    progress = (i + 1) / total_files * 100
                    progress_callback(progress, filepath, result.get('success', False))
                    
            except Exception as e:
                results.append({
                    'success': False,
                    'error': str(e),
                    'filepath': filepath
                })
                
                if progress_callback:
                    progress = (i + 1) / total_files * 100
                    progress_callback(progress, filepath, False)
        
        return results
    
    def get_file_info(self, filepath):
        """
        Get information about a file
        
        Args:
            filepath: Path to the file
            
        Returns:
            Dictionary with file information
        """
        if 'TextExtractor' in self.handlers:
            try:
                return self.handlers['TextExtractor'].get_file_info(filepath)
            except Exception as e:
                print(f"TextExtractor file info failed: {e}")
        
        # Manual file info extraction
        path = Path(filepath)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        # Get MIME type
        import mimetypes
        mime_type, _ = mimetypes.guess_type(filepath)
        
        # Check if format is supported
        is_supported, _ = is_format_supported(filepath)
        
        return {
            'filename': path.name,
            'extension': path.suffix.lower(),
            'filepath': str(path.absolute()),
            'file_size': path.stat().st_size,
            'created': path.stat().st_ctime,
            'modified': path.stat().st_mtime,
            'mime_type': mime_type or 'application/octet-stream',
            'is_supported': is_supported,
            'is_readable': os.access(filepath, os.R_OK)
        }
    
    def validate_file(self, filepath):
        """
        Validate if a file can be processed
        
        Args:
            filepath: Path to the file
            
        Returns:
            Dictionary with validation results
        """
        if 'TextExtractor' in self.handlers:
            try:
                return validate_file_for_extraction(filepath)
            except Exception as e:
                print(f"TextExtractor validation failed: {e}")
        
        # Manual validation
        validation = {
            'is_valid': False,
            'errors': [],
            'warnings': [],
            'file_info': {}
        }
        
        try:
            path = Path(filepath)
            
            if not path.exists():
                validation['errors'].append('File does not exist')
                return validation
            
            if not path.is_file():
                validation['errors'].append('Path is not a file')
                return validation
            
            # Check file size
            file_size = path.stat().st_size
            validation['file_info']['size_bytes'] = file_size
            
            if file_size == 0:
                validation['errors'].append('File is empty')
                return validation
            
            # Check if readable
            if not os.access(filepath, os.R_OK):
                validation['errors'].append('File is not readable')
                return validation
            
            # Check format support
            is_supported, description = is_format_supported(filepath)
            validation['file_info']['format_supported'] = is_supported
            validation['file_info']['format_description'] = description
            
            if not is_supported:
                validation['warnings'].append(f'Format may not be fully supported: {description}')
            
            validation['is_valid'] = True
            
        except Exception as e:
            validation['errors'].append(f'Validation failed: {str(e)}')
        
        return validation
    
    def clear_cache(self):
        """Clear the extraction cache"""
        self.extraction_cache.clear()
    
    def get_handler_statistics(self):
        """
        Get statistics about handler usage
        
        Returns:
            Dictionary with handler statistics
        """
        stats = {
            'total_extractions': len(self.extraction_cache),
            'available_handlers': list(self.handlers.keys()),
            'cache_size_mb': sum(len(text) for text in self.extraction_cache.values()) / (1024 * 1024)
        }
        return stats

# File format detector
class FileFormatDetector:
    """
    Advanced file format detection
    """
    
    # File signatures (magic numbers)
    FILE_SIGNATURES = {
        b'%PDF': '.pdf',
        b'PK\x03\x04': '.zip',  # ZIP-based formats (DOCX, PPTX, XLSX, etc.)
        b'\xD0\xCF\x11\xE0': '.doc',  # OLE2 compound documents
        b'\xEF\xBB\xBF': '.txt',  # UTF-8 BOM
        b'{\\rtf': '.rtf',
        b'\x89PNG\r\n\x1a\n': '.png',
        b'\xFF\xD8\xFF': '.jpg',
        b'GIF87a': '.gif',
        b'GIF89a': '.gif',
        b'BM': '.bmp',
        b'<!DOCTYPE': '.html',
        b'<?xml': '.xml',
        b'#!': '.script'  # Shell script
    }
    
    def __init__(self):
        pass
    
    def detect_by_signature(self, filepath, max_bytes=1024):
        """
        Detect file format by file signature
        
        Args:
            filepath: Path to the file
            max_bytes: Maximum bytes to read for signature detection
            
        Returns:
            Detected format (extension) or None
        """
        try:
            with open(filepath, 'rb') as f:
                header = f.read(max_bytes)
            
            for signature, format_ext in self.FILE_SIGNATURES.items():
                if header.startswith(signature):
                    return format_ext
            
            return None
            
        except Exception as e:
            print(f"Signature detection failed: {e}")
            return None
    
    def detect_by_extension(self, filepath):
        """
        Detect file format by extension
        
        Args:
            filepath: Path to the file
            
        Returns:
            Detected format (extension)
        """
        path = Path(filepath)
        ext = path.suffix.lower()
        return ext if ext else '.txt'  # Default to text
    
    def detect_by_content(self, filepath, sample_size=4096):
        """
        Detect file format by content analysis
        
        Args:
            filepath: Path to the file
            sample_size: Number of bytes to sample
            
        Returns:
            Tuple of (format, confidence)
        """
        try:
            with open(filepath, 'rb') as f:
                sample = f.read(sample_size)
            
            # Try to decode as text
            try:
                text_sample = sample.decode('utf-8', errors='ignore')
                
                # Check for common patterns
                if '<!DOCTYPE' in text_sample or '<html' in text_sample:
                    return '.html', 0.9
                elif '<?xml' in text_sample:
                    return '.xml', 0.9
                elif '{\\rtf' in text_sample:
                    return '.rtf', 0.9
                elif any(keyword in text_sample.lower() for keyword in 
                        ['function', 'var ', 'def ', 'class ', 'import ', '#include']):
                    return '.code', 0.7
                elif all(32 <= byte <= 126 or byte in (9, 10, 13) for byte in sample[:100]):
                    return '.txt', 0.8
                    
            except UnicodeDecodeError:
                # Binary file
                return '.bin', 0.5
            
            return '.unknown', 0.0
            
        except Exception as e:
            print(f"Content detection failed: {e}")
            return '.unknown', 0.0
    
    def detect_format(self, filepath):
        """
        Detect file format using multiple methods
        
        Args:
            filepath: Path to the file
            
        Returns:
            Dictionary with detection results
        """
        results = {
            'by_signature': self.detect_by_signature(filepath),
            'by_extension': self.detect_by_extension(filepath),
            'by_content': self.detect_by_content(filepath),
            'final_decision': None,
            'confidence': 0.0
        }
        
        # Make final decision
        if results['by_signature']:
            results['final_decision'] = results['by_signature']
            results['confidence'] = 0.95
        elif results['by_extension'] in SUPPORTED_FORMATS:
            results['final_decision'] = results['by_extension']
            results['confidence'] = 0.85
        elif results['by_content'][0] != '.unknown':
            results['final_decision'] = results['by_content'][0]
            results['confidence'] = results['by_content'][1]
        else:
            results['final_decision'] = '.txt'  # Default
            results['confidence'] = 0.5
        
        return results

# Batch file processor
class BatchFileProcessor:
    """
    Process batches of files efficiently
    """
    
    def __init__(self, config=None):
        self.config = config or {}
        self.handler = UnifiedFileHandler(config)
        self.results = []
        self.statistics = {
            'total_files': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'total_bytes': 0,
            'total_text_chars': 0
        }
    
    def process_directory(self, directory, recursive=False, extensions=None, 
                         max_files=None, skip_unsupported=True):
        """
        Process all files in a directory
        
        Args:
            directory: Directory path
            recursive: Whether to search recursively
            extensions: List of extensions to include (None for all supported)
            max_files: Maximum number of files to process
            skip_unsupported: Whether to skip unsupported formats
            
        Returns:
            List of processing results
        """
        import glob
        
        dir_path = Path(directory)
        if not dir_path.exists() or not dir_path.is_dir():
            raise ValueError(f"Directory not found: {directory}")
        
        # Determine file patterns
        if extensions:
            patterns = [f"*{ext}" for ext in extensions]
        else:
            patterns = [f"*{ext}" for ext in SUPPORTED_FORMATS.keys()]
        
        # Collect files
        files = []
        for pattern in patterns:
            if recursive:
                files.extend(dir_path.rglob(pattern))
            else:
                files.extend(dir_path.glob(pattern))
        
        # Remove duplicates and sort
        files = sorted(set(files))
        
        # Apply max_files limit
        if max_files:
            files = files[:max_files]
        
        self.statistics['total_files'] = len(files)
        
        # Process files
        self.results = []
        for i, file_path in enumerate(files):
            if file_path.is_file():
                try:
                    # Validate file
                    validation = self.handler.validate_file(str(file_path))
                    
                    if not validation['is_valid'] and skip_unsupported:
                        self.statistics['skipped'] += 1
                        continue
                    
                    # Extract text
                    result = self.handler.extract_with_metadata(str(file_path))
                    
                    if result['success']:
                        self.statistics['successful'] += 1
                        self.statistics['total_bytes'] += result['metadata']['file_size']
                        self.statistics['total_text_chars'] += len(result['text'])
                    else:
                        self.statistics['failed'] += 1
                    
                    self.results.append(result)
                    
                except Exception as e:
                    self.statistics['failed'] += 1
                    self.results.append({
                        'success': False,
                        'error': str(e),
                        'filepath': str(file_path)
                    })
        
        return self.results
    
    def get_statistics(self):
        """
        Get processing statistics
        
        Returns:
            Dictionary with statistics
        """
        stats = self.statistics.copy()
        
        if stats['total_files'] > 0:
            stats['success_rate'] = (stats['successful'] / stats['total_files']) * 100
            stats['failure_rate'] = (stats['failed'] / stats['total_files']) * 100
            stats['skip_rate'] = (stats['skipped'] / stats['total_files']) * 100
            stats['avg_file_size_kb'] = stats['total_bytes'] / stats['total_files'] / 1024
            if stats['successful'] > 0:
                stats['avg_text_chars'] = stats['total_text_chars'] / stats['successful']
            else:
                stats['avg_text_chars'] = 0
        else:
            stats.update({
                'success_rate': 0.0,
                'failure_rate': 0.0,
                'skip_rate': 0.0,
                'avg_file_size_kb': 0.0,
                'avg_text_chars': 0.0
            })
        
        return stats
    
    def export_results(self, output_format='json', output_file=None):
        """
        Export processing results
        
        Args:
            output_format: Export format ('json', 'csv', 'txt')
            output_file: Output file path (None for return as string)
            
        Returns:
            Exported data or writes to file
        """
        import json
        import csv
        from datetime import datetime
        
        if output_format == 'json':
            data = {
                'metadata': {
                    'export_date': datetime.now().isoformat(),
                    'total_results': len(self.results),
                    'statistics': self.get_statistics()
                },
                'results': self.results
            }
            
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                return True
            else:
                return json.dumps(data, indent=2, ensure_ascii=False)
        
        elif output_format == 'csv':
            if not output_file:
                raise ValueError("Output file required for CSV export")
            
            # Prepare CSV data
            csv_data = []
            for result in self.results:
                row = {
                    'filepath': result.get('filepath', ''),
                    'success': result.get('success', False),
                    'error': result.get('error', ''),
                    'text_length': len(result.get('text', '')),
                    'file_size': result.get('metadata', {}).get('file_size', 0),
                    'format': result.get('metadata', {}).get('extension', '')
                }
                csv_data.append(row)
            
            # Write CSV
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['filepath', 'success', 'error', 'text_length', 'file_size', 'format']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(csv_data)
            
            return True
        
        elif output_format == 'txt':
            if not output_file:
                output = []
                for result in self.results:
                    output.append(f"File: {result.get('filepath', '')}")
                    output.append(f"Success: {result.get('success', False)}")
                    if not result.get('success'):
                        output.append(f"Error: {result.get('error', '')}")
                    output.append("")
                return '\n'.join(output)
            else:
                with open(output_file, 'w', encoding='utf-8') as f:
                    for result in self.results:
                        f.write(f"File: {result.get('filepath', '')}\n")
                        f.write(f"Success: {result.get('success', False)}\n")
                        if not result.get('success'):
                            f.write(f"Error: {result.get('error', '')}\n")
                        f.write("\n")
                return True
        
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
    
    def clear_results(self):
        """Clear processing results"""
        self.results.clear()
        self.statistics = {
            'total_files': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'total_bytes': 0,
            'total_text_chars': 0
        }

# File handler factory
class FileHandlerFactory:
    """
    Factory for creating file handlers
    """
    
    @staticmethod
    def create_handler(handler_type, config=None):
        """
        Create a file handler
        
        Args:
            handler_type: Type of handler ('unified', 'text', 'docx', 'pdf')
            config: Configuration dictionary
            
        Returns:
            Handler instance or None
        """
        if handler_type == 'unified':
            return UnifiedFileHandler(config)
        
        elif handler_type == 'text' and TEXT_EXTRACTOR_AVAILABLE:
            return TextExtractor(config)
        
        elif handler_type == 'docx' and DOCX_HANDLER_AVAILABLE:
            return DOCXHandler(config)
        
        elif handler_type == 'pdf' and PDF_HANDLER_AVAILABLE:
            return PDFHandler(config)
        
        else:
            print(f"Warning: Handler type '{handler_type}' not available")
            return None
    
    @staticmethod
    def create_batch_processor(config=None):
        """
        Create a batch file processor
        
        Args:
            config: Configuration dictionary
            
        Returns:
            BatchFileProcessor instance
        """
        return BatchFileProcessor(config)
    
    @staticmethod
    def create_format_detector():
        """
        Create a file format detector
        
        Returns:
            FileFormatDetector instance
        """
        return FileFormatDetector()
    
    @staticmethod
    def create_all_handlers(config=None):
        """
        Create all available handlers
        
        Args:
            config: Configuration dictionary
            
        Returns:
            Dictionary of handler instances
        """
        handlers = {}
        
        handlers['unified'] = UnifiedFileHandler(config)
        
        if TEXT_EXTRACTOR_AVAILABLE:
            handlers['text'] = TextExtractor(config)
        
        if DOCX_HANDLER_AVAILABLE:
            handlers['docx'] = DOCXHandler(config)
        
        if PDF_HANDLER_AVAILABLE:
            handlers['pdf'] = PDFHandler(config)
        
        handlers['batch'] = BatchFileProcessor(config)
        handlers['detector'] = FileFormatDetector()
        
        return handlers

# Export additional classes
__all__.extend([
    'UnifiedFileHandler',
    'FileFormatDetector',
    'BatchFileProcessor',
    'FileHandlerFactory',
    'SUPPORTED_FORMATS',
    'FORMAT_CATEGORIES',
    'get_supported_formats',
    'get_formats_by_category',
    'is_format_supported',
    'get_format_category',
    'get_available_handlers',
    'check_handler_dependencies'
])

# Convenience functions
def extract_text(filepath, handler_type='unified', config=None):
    """
    Convenience function to extract text from a file
    
    Args:
        filepath: Path to the file
        handler_type: Type of handler to use
        config: Configuration dictionary
        
    Returns:
        Extracted text
    """
    handler = FileHandlerFactory.create_handler(handler_type, config)
    if handler:
        return handler.extract_text(filepath)
    else:
        raise ValueError(f"Handler type '{handler_type}' not available")

def batch_process(directory, config=None, **kwargs):
    """
    Convenience function for batch processing
    
    Args:
        directory: Directory to process
        config: Configuration dictionary
        **kwargs: Additional arguments for process_directory
        
    Returns:
        BatchFileProcessor instance with results
    """
    processor = BatchFileProcessor(config)
    processor.process_directory(directory, **kwargs)
    return processor

def detect_file_format(filepath):
    """
    Convenience function to detect file format
    
    Args:
        filepath: Path to the file
        
    Returns:
        Format detection results
    """
    detector = FileFormatDetector()
    return detector.detect_format(filepath)

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
            # List supported formats
            formats = get_supported_formats()
            print("Supported File Formats:")
            for ext, desc in sorted(formats.items()):
                print(f"  {ext:10} - {desc}")
        
        elif command == 'info':
            # Get file information
            if len(sys.argv) > 2:
                filepath = sys.argv[2]
                handler = UnifiedFileHandler()
                try:
                    info = handler.get_file_info(filepath)
                    print(json.dumps(info, indent=2, default=str))
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print("Usage: python -m file_handlers info <filepath>")
        
        elif command == 'extract':
            # Extract text from file
            if len(sys.argv) > 2:
                filepath = sys.argv[2]
                handler = UnifiedFileHandler()
                try:
                    text = handler.extract_text(filepath)
                    print(f"Extracted text ({len(text)} characters):")
                    print("-" * 50)
                    print(text[:500] + "..." if len(text) > 500 else text)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print("Usage: python -m file_handlers extract <filepath>")
        
        elif command == 'detect':
            # Detect file format
            if len(sys.argv) > 2:
                filepath = sys.argv[2]
                result = detect_file_format(filepath)
                print(json.dumps(result, indent=2))
            else:
                print("Usage: python -m file_handlers detect <filepath>")
        
        elif command == 'test':
            # Run a quick test
            print("Testing file handlers package...")
            
            # Create a test file
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write("This is a test file for file handlers.")
                test_file = f.name
            
            try:
                # Test format detection
                print(f"Test file: {test_file}")
                
                # Detect format
                detector = FileFormatDetector()
                detection = detector.detect_format(test_file)
                print(f"Format detection: {detection['final_decision']} (confidence: {detection['confidence']})")
                
                # Extract text
                handler = UnifiedFileHandler()
                text = handler.extract_text(test_file)
                print(f"Text extraction successful: {len(text)} characters")
                
                print("Test completed successfully!")
                
            finally:
                # Clean up
                import os
                os.unlink(test_file)
        
        elif command == 'handlers':
            # List available handlers
            handlers = get_available_handlers()
            print("Available File Handlers:")
            for name, available in handlers.items():
                status = "✓ Available" if available else "✗ Not available"
                print(f"  {name:20} - {status}")
        
        else:
            print(f"Unknown command: {command}")
            print("\nAvailable commands:")
            print("  list     - List supported file formats")
            print("  info     - Get file information")
            print("  extract  - Extract text from file")
            print("  detect   - Detect file format")
            print("  test     - Run a quick test")
            print("  handlers - List available handlers")
    else:
        print("File Handlers Package for Plagiarism Checker Pro")
        print("\nUse 'python -m file_handlers <command>' where command is:")
        print("  list, info, extract, detect, test, handlers")

if __name__ == '__main__':
    main()