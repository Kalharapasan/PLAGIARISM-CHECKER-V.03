import os
import sys
from pathlib import Path
from datetime import datetime

# Try to import available report modules
try:
    from .basic_report import generate_basic_report
    BASIC_REPORT_AVAILABLE = True
except ImportError as e:
    print(f"⚠ Warning: Basic report module not available: {e}")
    BASIC_REPORT_AVAILABLE = False

try:
    from .advanced_report import (
        generate_advanced_report,
        generate_html_report,
        generate_json_report
    )
    ADVANCED_REPORT_AVAILABLE = True
except ImportError as e:
    print(f"⚠ Warning: Advanced report module not available: {e}")
    ADVANCED_REPORT_AVAILABLE = False

try:
    from .html_report import (
        generate_interactive_html_report,
        generate_pdf_report,
        generate_word_report
    )
    HTML_REPORT_AVAILABLE = True
except ImportError as e:
    print(f"⚠ Warning: HTML report module not available: {e}")
    HTML_REPORT_AVAILABLE = False

# Define exports
__all__ = []

if BASIC_REPORT_AVAILABLE:
    __all__.extend([
        'generate_basic_report'
    ])

if ADVANCED_REPORT_AVAILABLE:
    __all__.extend([
        'generate_advanced_report',
        'generate_html_report',
        'generate_json_report'
    ])

if HTML_REPORT_AVAILABLE:
    __all__.extend([
        'generate_interactive_html_report',
        'generate_pdf_report',
        'generate_word_report'
    ])

# Package metadata
__version__ = '1.0.0'
__author__ = 'Plagiarism Checker Pro Team'
__description__ = 'Report generation for plagiarism detection results'

# Report types
REPORT_TYPES = {
    'basic': {
        'name': 'Basic Text Report',
        'description': 'Simple text-based report with basic statistics',
        'format': 'text',
        'available': BASIC_REPORT_AVAILABLE
    },
    'advanced': {
        'name': 'Advanced Text Report',
        'description': 'Detailed text report with comprehensive analysis',
        'format': 'text',
        'available': ADVANCED_REPORT_AVAILABLE
    },
    'html': {
        'name': 'HTML Report',
        'description': 'Formatted HTML report with styling',
        'format': 'html',
        'available': ADVANCED_REPORT_AVAILABLE
    },
    'json': {
        'name': 'JSON Report',
        'description': 'Structured JSON data for programmatic use',
        'format': 'json',
        'available': ADVANCED_REPORT_AVAILABLE
    },
    'interactive_html': {
        'name': 'Interactive HTML Report',
        'description': 'Interactive HTML report with charts and filters',
        'format': 'html',
        'available': HTML_REPORT_AVAILABLE
    },
    'pdf': {
        'name': 'PDF Report',
        'description': 'Printable PDF document',
        'format': 'pdf',
        'available': HTML_REPORT_AVAILABLE
    },
    'word': {
        'name': 'Word Document',
        'description': 'Microsoft Word document report',
        'format': 'docx',
        'available': HTML_REPORT_AVAILABLE
    }
}

# Report templates
REPORT_TEMPLATES = {
    'academic': {
        'name': 'Academic Report',
        'description': 'Formal report suitable for academic use',
        'sections': ['title', 'executive_summary', 'methodology', 'results', 'analysis', 'recommendations', 'references'],
        'style': 'formal'
    },
    'executive': {
        'name': 'Executive Summary',
        'description': 'Concise summary for decision makers',
        'sections': ['title', 'summary', 'key_findings', 'risk_assessment', 'recommendations'],
        'style': 'concise'
    },
    'detailed': {
        'name': 'Detailed Analysis',
        'description': 'Comprehensive technical analysis',
        'sections': ['title', 'introduction', 'methodology', 'detailed_results', 'statistical_analysis', 'patterns_detected', 'conclusions', 'appendix'],
        'style': 'technical'
    },
    'simple': {
        'name': 'Simple Report',
        'description': 'Basic report for quick overview',
        'sections': ['title', 'summary', 'similarity_score', 'matches', 'recommendations'],
        'style': 'simple'
    }
}

# Utility functions
def get_available_report_types():
    """
    Get list of available report types
    
    Returns:
        Dictionary of available report types
    """
    available = {}
    for report_type, info in REPORT_TYPES.items():
        if info['available']:
            available[report_type] = info
    return available

def get_report_template(template_name):
    """
    Get a report template
    
    Args:
        template_name: Name of the template
        
    Returns:
        Template dictionary or None if not found
    """
    return REPORT_TEMPLATES.get(template_name)

def list_report_templates():
    """
    List all available report templates
    
    Returns:
        Dictionary of report templates
    """
    return REPORT_TEMPLATES.copy()

# Unified report generator
class ReportGenerator:
    """
    Unified interface for generating all types of reports
    """
    
    def __init__(self, config=None):
        self.config = config or {}
        self.report_cache = {}
        self.generated_reports = []
        
    def generate_report(self, results, filename, report_type='advanced', 
                       template='academic', algorithms=None, **kwargs):
        """
        Generate a report of specified type
        
        Args:
            results: Plagiarism detection results
            filename: Original filename
            report_type: Type of report to generate
            template: Report template to use
            algorithms: List of algorithms used
            **kwargs: Additional arguments
            
        Returns:
            Generated report as string or bytes
        """
        import hashlib
        
        # Create cache key
        cache_data = f"{filename}_{report_type}_{template}_{hash(str(results))}"
        cache_key = hashlib.md5(cache_data.encode()).hexdigest()
        
        if cache_key in self.report_cache:
            return self.report_cache[cache_key]
        
        # Check if report type is available
        if report_type not in REPORT_TYPES or not REPORT_TYPES[report_type]['available']:
            # Fall back to available report type
            available_types = get_available_report_types()
            if available_types:
                report_type = list(available_types.keys())[0]
                print(f"Warning: Requested report type not available. Using {report_type} instead.")
            else:
                raise ValueError("No report types available")
        
        # Generate report based on type
        if algorithms is None:
            algorithms = results.get('metadata', {}).get('algorithms_used', [])
        
        if report_type == 'basic' and BASIC_REPORT_AVAILABLE:
            report = generate_basic_report(results, filename, algorithms)
        
        elif report_type == 'advanced' and ADVANCED_REPORT_AVAILABLE:
            report = generate_advanced_report(results, filename, algorithms)
        
        elif report_type == 'html' and ADVANCED_REPORT_AVAILABLE:
            report = generate_html_report(results, filename, algorithms)
        
        elif report_type == 'json' and ADVANCED_REPORT_AVAILABLE:
            report = generate_json_report(results, filename, algorithms)
        
        elif report_type == 'interactive_html' and HTML_REPORT_AVAILABLE:
            report = generate_interactive_html_report(results, filename, algorithms, **kwargs)
        
        elif report_type == 'pdf' and HTML_REPORT_AVAILABLE:
            report = generate_pdf_report(results, filename, algorithms, **kwargs)
        
        elif report_type == 'word' and HTML_REPORT_AVAILABLE:
            report = generate_word_report(results, filename, algorithms, **kwargs)
        
        else:
            # Fallback to text report
            report = self._generate_fallback_report(results, filename, algorithms)
        
        # Apply template if applicable
        report = self._apply_template(report, template, report_type)
        
        # Track generated report
        self.generated_reports.append({
            'filename': filename,
            'report_type': report_type,
            'template': template,
            'timestamp': datetime.now().isoformat(),
            'cache_key': cache_key
        })
        
        # Cache the report
        self.report_cache[cache_key] = report
        
        return report
    
    def _generate_fallback_report(self, results, filename, algorithms):
        """
        Generate a fallback text report
        
        Args:
            results: Plagiarism detection results
            filename: Original filename
            algorithms: List of algorithms used
            
        Returns:
            Fallback report as string
        """
        report_lines = []
        
        # Header
        report_lines.append("=" * 80)
        report_lines.append("PLAGIARISM DETECTION REPORT")
        report_lines.append("=" * 80)
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"Document: {filename}")
        report_lines.append(f"Algorithms: {', '.join(algorithms)}")
        report_lines.append("")
        
        # Summary
        report_lines.append("SUMMARY")
        report_lines.append("-" * 80)
        report_lines.append(f"Overall Similarity: {results.get('overall_similarity', 0):.2f}%")
        report_lines.append(f"Total Words: {results.get('total_words', 0)}")
        report_lines.append(f"Total Sentences: {results.get('total_sentences', 0)}")
        report_lines.append(f"Sources Matched: {len(results.get('matches', []))}")
        report_lines.append("")
        
        # Matches
        matches = results.get('matches', [])
        if matches:
            report_lines.append("DETECTED MATCHES")
            report_lines.append("-" * 80)
            for i, match in enumerate(matches, 1):
                report_lines.append(f"Match #{i}:")
                report_lines.append(f"  Source: {match.get('source', 'Unknown')}")
                report_lines.append(f"  Similarity: {match.get('similarity', 0):.2f}%")
                report_lines.append(f"  Risk Level: {match.get('risk_level', 'Unknown')}")
                
                if match.get('url'):
                    report_lines.append(f"  URL: {match.get('url')}")
                report_lines.append("")
        
        # Recommendations
        report_lines.append("RECOMMENDATIONS")
        report_lines.append("-" * 80)
        similarity = results.get('overall_similarity', 0)
        
        if similarity < 15:
            report_lines.append("✓ Document shows minimal similarity to reference sources.")
            report_lines.append("✓ Generally acceptable for academic submissions.")
            report_lines.append("• Double-check all citations are properly formatted.")
        elif similarity < 30:
            report_lines.append("⚠ Document shows moderate similarity.")
            report_lines.append("⚠ Review matched sections and ensure proper attribution.")
            report_lines.append("• Consider paraphrasing highly similar sections.")
            report_lines.append("• Verify all borrowed content has appropriate citations.")
        else:
            report_lines.append("✗ Document shows substantial similarity.")
            report_lines.append("✗ Comprehensive revision required before submission.")
            report_lines.append("• Review all matched sections with source material.")
            report_lines.append("• Ensure proper citation for all borrowed content.")
            report_lines.append("• Rewrite highly similar sections in your own words.")
        
        report_lines.append("")
        report_lines.append("=" * 80)
        report_lines.append("DISCLAIMER: This is an automated analysis. Results should be")
        report_lines.append("reviewed by a human. Always follow institutional guidelines.")
        report_lines.append("=" * 80)
        
        return '\n'.join(report_lines)
    
    def _apply_template(self, report, template_name, report_type):
        """
        Apply a template to a report
        
        Args:
            report: The generated report
            template_name: Name of the template to apply
            report_type: Type of report
            
        Returns:
            Report with template applied
        """
        template = REPORT_TEMPLATES.get(template_name)
        if not template or report_type not in ['text', 'html']:
            return report
        
        # For now, just add template metadata
        # In a full implementation, this would apply formatting
        if isinstance(report, str):
            if report_type == 'text':
                return f"Template: {template['name']}\n\n{report}"
            elif report_type == 'html':
                # Add template info as comment
                return f"<!-- Template: {template['name']} -->\n{report}"
        
        return report
    
    def save_report(self, report, output_path, report_type='advanced'):
        """
        Save a report to file
        
        Args:
            report: The report content
            output_path: Path where to save the report
            report_type: Type of report (determines file extension)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            output_path = Path(output_path)
            
            # Ensure directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Determine file extension
            if report_type in REPORT_TYPES:
                format_info = REPORT_TYPES[report_type]
                if format_info['format'] == 'html':
                    if not output_path.suffix.lower() == '.html':
                        output_path = output_path.with_suffix('.html')
                elif format_info['format'] == 'json':
                    if not output_path.suffix.lower() == '.json':
                        output_path = output_path.with_suffix('.json')
                elif format_info['format'] == 'pdf':
                    if not output_path.suffix.lower() == '.pdf':
                        output_path = output_path.with_suffix('.pdf')
                elif format_info['format'] == 'docx':
                    if not output_path.suffix.lower() == '.docx':
                        output_path = output_path.with_suffix('.docx')
                else:  # text
                    if not output_path.suffix.lower() == '.txt':
                        output_path = output_path.with_suffix('.txt')
            
            # Write report
            if isinstance(report, str):
                encoding = 'utf-8'
                if report_type == 'html' or report_type == 'json':
                    encoding = 'utf-8'
                
                with open(output_path, 'w', encoding=encoding) as f:
                    f.write(report)
            
            elif isinstance(report, bytes):
                with open(output_path, 'wb') as f:
                    f.write(report)
            
            else:
                # Try to convert to string
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(str(report))
            
            print(f"✓ Report saved to: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving report: {e}")
            return False
    
    def generate_and_save(self, results, filename, output_dir='reports', 
                         report_type='advanced', template='academic', 
                         algorithms=None, **kwargs):
        """
        Generate and save a report
        
        Args:
            results: Plagiarism detection results
            filename: Original filename
            output_dir: Directory to save reports
            report_type: Type of report to generate
            template: Report template to use
            algorithms: List of algorithms used
            **kwargs: Additional arguments
            
        Returns:
            Path to saved report or None
        """
        # Generate report
        report = self.generate_report(results, filename, report_type, 
                                     template, algorithms, **kwargs)
        
        # Create output filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_name = Path(filename).stem
        output_filename = f"{base_name}_{report_type}_{timestamp}"
        
        # Determine extension
        if report_type in REPORT_TYPES:
            format_info = REPORT_TYPES[report_type]
            extension = f".{format_info['format']}"
        else:
            extension = '.txt'
        
        output_path = Path(output_dir) / f"{output_filename}{extension}"
        
        # Save report
        if self.save_report(report, output_path, report_type):
            return output_path
        else:
            return None
    
    def generate_multiple_formats(self, results, filename, output_dir='reports',
                                 formats=None, template='academic', algorithms=None):
        """
        Generate reports in multiple formats
        
        Args:
            results: Plagiarism detection results
            filename: Original filename
            output_dir: Directory to save reports
            formats: List of formats to generate (None for all available)
            template: Report template to use
            algorithms: List of algorithms used
            
        Returns:
            Dictionary of generated report paths
        """
        if formats is None:
            formats = list(get_available_report_types().keys())
        
        generated = {}
        
        for report_type in formats:
            if report_type in get_available_report_types():
                try:
                    output_path = self.generate_and_save(
                        results, filename, output_dir, report_type,
                        template, algorithms
                    )
                    if output_path:
                        generated[report_type] = output_path
                except Exception as e:
                    print(f"Warning: Failed to generate {report_type} report: {e}")
        
        return generated
    
    def clear_cache(self):
        """Clear the report cache"""
        self.report_cache.clear()
    
    def get_generation_statistics(self):
        """
        Get statistics about report generation
        
        Returns:
            Dictionary with generation statistics
        """
        stats = {
            'total_generated': len(self.generated_reports),
            'cached_reports': len(self.report_cache),
            'by_type': {},
            'recent_reports': self.generated_reports[-10:] if self.generated_reports else []
        }
        
        # Count by report type
        for report in self.generated_reports:
            report_type = report['report_type']
            stats['by_type'][report_type] = stats['by_type'].get(report_type, 0) + 1
        
        return stats

# Report formatter and styler
class ReportFormatter:
    """
    Format and style reports
    """
    
    def __init__(self, style='default'):
        self.style = style
        self.styles = self._load_styles()
    
    def _load_styles(self):
        """Load report styling definitions"""
        return {
            'default': {
                'title_color': '#2c3e50',
                'header_color': '#34495e',
                'text_color': '#2c3e50',
                'highlight_color': '#3498db',
                'warning_color': '#e74c3c',
                'success_color': '#27ae60',
                'font_family': 'Arial, sans-serif',
                'line_spacing': 1.5
            },
            'academic': {
                'title_color': '#000000',
                'header_color': '#333333',
                'text_color': '#000000',
                'highlight_color': '#0066cc',
                'warning_color': '#cc0000',
                'success_color': '#008000',
                'font_family': 'Times New Roman, serif',
                'line_spacing': 2.0
            },
            'modern': {
                'title_color': '#1a237e',
                'header_color': '#283593',
                'text_color': '#37474f',
                'highlight_color': '#2962ff',
                'warning_color': '#f44336',
                'success_color': '#00c853',
                'font_family': 'Roboto, sans-serif',
                'line_spacing': 1.6
            },
            'minimal': {
                'title_color': '#000000',
                'header_color': '#666666',
                'text_color': '#333333',
                'highlight_color': '#000000',
                'warning_color': '#000000',
                'success_color': '#000000',
                'font_family': 'Helvetica, sans-serif',
                'line_spacing': 1.8
            }
        }
    
    def format_text_report(self, report_text, style=None):
        """
        Format a text report with styling
        
        Args:
            report_text: The report text
            style: Style to apply (None for current style)
            
        Returns:
            Formatted text report
        """
        if style is None:
            style = self.style
        
        style_def = self.styles.get(style, self.styles['default'])
        
        # Simple text formatting (for HTML, this would apply CSS)
        lines = report_text.split('\n')
        formatted_lines = []
        
        for line in lines:
            if line.startswith('=' * 10):  # Title separator
                formatted_lines.append(f"\n{'='*80}\n")
            elif line.startswith('-' * 10):  # Header separator
                formatted_lines.append(f"\n{'-'*80}\n")
            elif line.upper() == line and len(line) > 3 and ' ' not in line:  # Title
                formatted_lines.append(f"\n{line}\n")
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def apply_html_styling(self, html_content, style=None):
        """
        Apply CSS styling to HTML content
        
        Args:
            html_content: HTML report content
            style: Style to apply
            
        Returns:
            Styled HTML content
        """
        if style is None:
            style = self.style
        
        style_def = self.styles.get(style, self.styles['default'])
        
        # Create CSS
        css = f"""
        <style>
            body {{
                font-family: {style_def['font_family']};
                color: {style_def['text_color']};
                line-height: {style_def['line_spacing']};
                margin: 20px;
                padding: 20px;
                background-color: #f9f9f9;
            }}
            .report-title {{
                color: {style_def['title_color']};
                text-align: center;
                border-bottom: 2px solid {style_def['title_color']};
                padding-bottom: 10px;
                margin-bottom: 30px;
            }}
            .section-header {{
                color: {style_def['header_color']};
                border-left: 4px solid {style_def['highlight_color']};
                padding-left: 10px;
                margin-top: 25px;
                margin-bottom: 15px;
            }}
            .highlight {{
                color: {style_def['highlight_color']};
                font-weight: bold;
            }}
            .warning {{
                color: {style_def['warning_color']};
                font-weight: bold;
            }}
            .success {{
                color: {style_def['success_color']};
                font-weight: bold;
            }}
            .match-item {{
                background-color: #f5f5f5;
                border-left: 3px solid {style_def['highlight_color']};
                padding: 10px;
                margin: 10px 0;
                border-radius: 3px;
            }}
            .stat-box {{
                background-color: white;
                border: 1px solid #ddd;
                padding: 15px;
                margin: 10px 0;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 15px 0;
            }}
            th {{
                background-color: {style_def['header_color']};
                color: white;
                padding: 10px;
                text-align: left;
            }}
            td {{
                padding: 10px;
                border-bottom: 1px solid #ddd;
            }}
            tr:hover {{
                background-color: #f5f5f5;
            }}
        </style>
        """
        
        # Insert CSS into HTML
        if '<head>' in html_content:
            html_content = html_content.replace('<head>', f'<head>\n{css}')
        elif '<style>' in html_content:
            html_content = html_content.replace('<style>', f'<style>\n{css}')
        else:
            html_content = f"{css}\n{html_content}"
        
        return html_content
    
    def set_style(self, style):
        """
        Set the report style
        
        Args:
            style: Style name
            
        Returns:
            True if style was set, False if not found
        """
        if style in self.styles:
            self.style = style
            return True
        return False
    
    def get_available_styles(self):
        """
        Get available styles
        
        Returns:
            List of style names
        """
        return list(self.styles.keys())

# Report analyzer and statistics
class ReportAnalyzer:
    """
    Analyze and extract statistics from reports
    """
    
    def __init__(self):
        self.analyses = []
    
    def analyze_report_content(self, report_text, report_type='text'):
        """
        Analyze report content
        
        Args:
            report_text: Report content
            report_type: Type of report
            
        Returns:
            Analysis results
        """
        analysis = {
            'report_type': report_type,
            'length_chars': len(report_text),
            'length_words': len(report_text.split()),
            'sections': [],
            'keywords': {},
            'readability': {},
            'analysis_date': datetime.now().isoformat()
        }
        
        if report_type == 'text':
            analysis.update(self._analyze_text_report(report_text))
        elif report_type == 'html':
            analysis.update(self._analyze_html_report(report_text))
        elif report_type == 'json':
            analysis.update(self._analyze_json_report(report_text))
        
        self.analyses.append(analysis)
        return analysis
    
    def _analyze_text_report(self, report_text):
        """Analyze text report content"""
        analysis = {}
        
        # Count sections
        sections = []
        lines = report_text.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith(('=', '-', '•', '*', '✓', '⚠', '✗')):
                if line.upper() == line and len(line) < 50 and ' ' not in line:
                    current_section = line
                    sections.append(line)
        
        analysis['sections'] = sections
        analysis['section_count'] = len(sections)
        
        # Count keywords
        keywords = ['plagiarism', 'similarity', 'match', 'source', 'citation', 
                   'recommendation', 'risk', 'warning', 'original']
        
        keyword_counts = {}
        text_lower = report_text.lower()
        
        for keyword in keywords:
            count = text_lower.count(keyword)
            if count > 0:
                keyword_counts[keyword] = count
        
        analysis['keywords'] = keyword_counts
        
        # Simple readability
        sentences = report_text.count('.') + report_text.count('!') + report_text.count('?')
        words = len(report_text.split())
        
        if sentences > 0:
            avg_sentence_length = words / sentences
        else:
            avg_sentence_length = 0
        
        analysis['readability'] = {
            'sentence_count': sentences,
            'avg_sentence_length': avg_sentence_length,
            'word_count': words
        }
        
        return analysis
    
    def _analyze_html_report(self, report_text):
        """Analyze HTML report content"""
        analysis = {}
        
        # Extract text from HTML (simplified)
        import re
        text_content = re.sub(r'<[^>]+>', ' ', report_text)
        text_content = re.sub(r'\s+', ' ', text_content).strip()
        
        # Use text analysis
        text_analysis = self._analyze_text_report(text_content)
        analysis.update(text_analysis)
        
        # HTML-specific analysis
        analysis['html_tags'] = len(re.findall(r'<[^>]+>', report_text))
        analysis['has_css'] = '<style>' in report_text or 'style=' in report_text
        analysis['has_scripts'] = '<script>' in report_text
        
        return analysis
    
    def _analyze_json_report(self, report_text):
        """Analyze JSON report content"""
        import json
        
        analysis = {}
        
        try:
            data = json.loads(report_text)
            
            analysis['json_structure'] = self._analyze_json_structure(data)
            analysis['data_types'] = self._get_json_data_types(data)
            analysis['item_count'] = self._count_json_items(data)
            
        except json.JSONDecodeError:
            analysis['error'] = 'Invalid JSON'
        
        return analysis
    
    def _analyze_json_structure(self, data, path=''):
        """Analyze JSON structure"""
        structure = {}
        
        if isinstance(data, dict):
            for key, value in data.items():
                new_path = f"{path}.{key}" if path else key
                structure[key] = {
                    'type': type(value).__name__,
                    'structure': self._analyze_json_structure(value, new_path)
                }
        elif isinstance(data, list):
            if data:
                # Analyze first item as representative
                structure['items'] = self._analyze_json_structure(data[0], f"{path}[0]")
            structure['count'] = len(data)
        else:
            structure['type'] = type(data).__name__
            structure['value_sample'] = str(data)[:50]
        
        return structure
    
    def _get_json_data_types(self, data):
        """Get data types in JSON"""
        types = {}
        
        if isinstance(data, dict):
            for key, value in data.items():
                type_name = type(value).__name__
                types[type_name] = types.get(type_name, 0) + 1
                
                if isinstance(value, (dict, list)):
                    nested_types = self._get_json_data_types(value)
                    for nt, count in nested_types.items():
                        types[nt] = types.get(nt, 0) + count
        
        elif isinstance(data, list):
            for item in data:
                type_name = type(item).__name__
                types[type_name] = types.get(type_name, 0) + 1
                
                if isinstance(item, (dict, list)):
                    nested_types = self._get_json_data_types(item)
                    for nt, count in nested_types.items():
                        types[nt] = types.get(nt, 0) + count
        
        return types
    
    def _count_json_items(self, data):
        """Count items in JSON structure"""
        count = 0
        
        if isinstance(data, dict):
            count += len(data)
            for value in data.values():
                count += self._count_json_items(value)
        
        elif isinstance(data, list):
            count += len(data)
            for item in data:
                count += self._count_json_items(item)
        
        return count
    
    def get_analysis_statistics(self):
        """
        Get statistics about report analyses
        
        Returns:
            Dictionary with analysis statistics
        """
        if not self.analyses:
            return {}
        
        stats = {
            'total_analyses': len(self.analyses),
            'by_report_type': {},
            'avg_report_length': 0,
            'total_words_analyzed': 0
        }
        
        total_chars = 0
        total_words = 0
        
        for analysis in self.analyses:
            report_type = analysis['report_type']
            stats['by_report_type'][report_type] = stats['by_report_type'].get(report_type, 0) + 1
            
            total_chars += analysis.get('length_chars', 0)
            total_words += analysis.get('length_words', 0)
        
        if self.analyses:
            stats['avg_report_length'] = total_chars / len(self.analyses)
            stats['total_words_analyzed'] = total_words
        
        return stats

# Report factory
class ReportFactory:
    """
    Factory for creating reports and report-related objects
    """
    
    @staticmethod
    def create_generator(config=None):
        """
        Create a report generator
        
        Args:
            config: Configuration dictionary
            
        Returns:
            ReportGenerator instance
        """
        return ReportGenerator(config)
    
    @staticmethod
    def create_formatter(style='default'):
        """
        Create a report formatter
        
        Args:
            style: Default style
            
        Returns:
            ReportFormatter instance
        """
        return ReportFormatter(style)
    
    @staticmethod
    def create_analyzer():
        """
        Create a report analyzer
        
        Returns:
            ReportAnalyzer instance
        """
        return ReportAnalyzer()
    
    @staticmethod
    def create_batch_generator(config=None):
        """
        Create a batch report generator
        
        Args:
            config: Configuration dictionary
            
        Returns:
            BatchReportGenerator instance
        """
        return BatchReportGenerator(config)

# Batch report generator
class BatchReportGenerator:
    """
    Generate reports for multiple documents
    """
    
    def __init__(self, config=None):
        self.config = config or {}
        self.generator = ReportGenerator(config)
        self.results = []
        self.statistics = {
            'total_documents': 0,
            'successful_reports': 0,
            'failed_reports': 0,
            'total_formats_generated': 0,
            'total_files_created': 0
        }
    
    def generate_reports(self, documents, output_dir='reports', 
                        formats=None, template='academic'):
        """
        Generate reports for multiple documents
        
        Args:
            documents: List of dictionaries with 'filename' and 'results'
            output_dir: Directory to save reports
            formats: List of formats to generate
            template: Report template to use
            
        Returns:
            List of generated report information
        """
        self.results = []
        self.statistics['total_documents'] = len(documents)
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for doc in documents:
            filename = doc.get('filename', 'unknown')
            results = doc.get('results', {})
            algorithms = doc.get('algorithms')
            
            try:
                generated = self.generator.generate_multiple_formats(
                    results, filename, output_dir, formats, template, algorithms
                )
                
                report_info = {
                    'filename': filename,
                    'generated_reports': generated,
                    'success': True,
                    'timestamp': datetime.now().isoformat()
                }
                
                self.results.append(report_info)
                self.statistics['successful_reports'] += 1
                self.statistics['total_formats_generated'] += len(generated)
                self.statistics['total_files_created'] += len(generated)
                
            except Exception as e:
                report_info = {
                    'filename': filename,
                    'error': str(e),
                    'success': False,
                    'timestamp': datetime.now().isoformat()
                }
                
                self.results.append(report_info)
                self.statistics['failed_reports'] += 1
        
        return self.results
    
    def generate_summary_report(self, output_dir='reports', format='html'):
        """
        Generate a summary report of all generated reports
        
        Args:
            output_dir: Directory to save summary
            format: Report format
            
        Returns:
            Path to summary report or None
        """
        if not self.results:
            print("No reports to summarize")
            return None
        
        # Prepare summary data
        summary_data = {
            'metadata': {
                'generated': datetime.now().isoformat(),
                'total_documents': self.statistics['total_documents'],
                'success_rate': (self.statistics['successful_reports'] / 
                               self.statistics['total_documents'] * 100) 
                               if self.statistics['total_documents'] > 0 else 0,
                'statistics': self.statistics
            },
            'reports': self.results
        }
        
        # Generate summary report
        generator = ReportGenerator(self.config)
        
        # Create a simple results structure for the report generator
        results_stub = {
            'overall_similarity': 0,
            'total_words': 0,
            'total_sentences': 0,
            'matches': [],
            'metadata': {
                'algorithms_used': ['batch_summary']
            }
        }
        
        try:
            summary_report = generator.generate_report(
                results_stub, 
                'batch_summary', 
                format,
                'executive'
            )
            
            # Save summary
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            summary_filename = f"batch_summary_{timestamp}"
            
            if format in ['html', 'interactive_html']:
                summary_filename += '.html'
            elif format == 'json':
                summary_filename += '.json'
            elif format == 'pdf':
                summary_filename += '.pdf'
            else:
                summary_filename += '.txt'
            
            output_path = Path(output_dir) / summary_filename
            
            if generator.save_report(summary_report, output_path, format):
                return output