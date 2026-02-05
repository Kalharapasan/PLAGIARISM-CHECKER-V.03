import os
import re
import json
import mimetypes
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Union
from datetime import datetime
import tempfile
import warnings

class TextExtractor:
    SUPPORTED_FORMATS = {
        '.txt': 'text/plain',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.doc': 'application/msword',
        '.pdf': 'application/pdf',
        '.rtf': 'application/rtf',
        '.odt': 'application/vnd.oasis.opendocument.text',
        '.html': 'text/html',
        '.htm': 'text/html',
        '.xml': 'application/xml',
        '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        '.ppt': 'application/vnd.ms-powerpoint',
        '.odp': 'application/vnd.oasis.opendocument.presentation',
        '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        '.xls': 'application/vnd.ms-excel',
        '.ods': 'application/vnd.oasis.opendocument.spreadsheet',
        '.csv': 'text/csv',
        '.py': 'text/x-python',
        '.java': 'text/x-java',
        '.cpp': 'text/x-c++',
        '.c': 'text/x-c',
        '.js': 'application/javascript',
        '.ts': 'application/typescript',
        '.html': 'text/html',
        '.css': 'text/css',
        '.json': 'application/json',
        '.xml': 'application/xml',
        '.md': 'text/markdown',
        '.sql': 'application/sql',
        '.tex': 'application/x-tex',
        '.epub': 'application/epub+zip',
        '.mobi': 'application/x-mobipocket-ebook',
        '.azw': 'application/vnd.amazon.ebook'
       
    }
    
    
    
    def _initialize_handlers(self):
        self.handlers = {}
        self.handlers['.txt'] = self._extract_text_file
        self.handlers['.docx'] = self._extract_docx
        self.handlers['.pdf'] = self._extract_pdf
        self.handlers['.html'] = self._extract_html
        self.handlers['.htm'] = self._extract_html
        self.handlers['.csv'] = self._extract_csv
        self.handlers['.json'] = self._extract_json
        self.handlers['.xml'] = self._extract_xml
        self.handlers['.md'] = self._extract_markdown
        self.handlers['.py'] = self._extract_code
        self.handlers['.java'] = self._extract_code
        self.handlers['.cpp'] = self._extract_code
        self.handlers['.c'] = self._extract_code
        self.handlers['.js'] = self._extract_code
        self.handlers['.ts'] = self._extract_code
        self.handlers['.css'] = self._extract_code
        self.handlers['.sql'] = self._extract_code
        self._register_external_handlers()
    
    def _register_external_handlers(self):
        try:
            from .docx_handler import DOCXHandler
            self.handlers['.docx'] = lambda f: DOCXHandler(self.config).extract_text(f)
            self.handlers['.doc'] = self._extract_doc
        except ImportError:
            pass
        
        try:
            from .pdf_handler import PDFHandler
            self.handlers['.pdf'] = lambda f: PDFHandler(self.config).extract_text(f)
        except ImportError:
            pass
        
        try:
            import striprtf
            self.handlers['.rtf'] = self._extract_rtf
        except ImportError:
            pass
        
        try:
            import zipfile
            import xml.etree.ElementTree as ET
            self.handlers['.odt'] = self._extract_odt
            self.handlers['.odp'] = self._extract_odp
            self.handlers['.ods'] = self._extract_ods
        except ImportError:
            pass
        
        try:
            import zipfile
            import xml.etree.ElementTree as ET
            self.handlers['.epub'] = self._extract_epub
        except ImportError:
            pass
        
        try:
            from pptx import Presentation
            self.handlers['.pptx'] = self._extract_pptx
            self.handlers['.ppt'] = self._extract_ppt
        except ImportError:
            pass
        
        try:
            import pandas as pd
            self.handlers['.xlsx'] = self._extract_xlsx
            self.handlers['.xls'] = self._extract_xls
        except ImportError:
            pass
    
    def _setup_mime_types(self):
        mimetypes.add_type('application/vnd.openxmlformats-officedocument.wordprocessingml.document', '.docx')
        mimetypes.add_type('application/vnd.ms-powerpoint', '.ppt')
        mimetypes.add_type('application/vnd.openxmlformats-officedocument.presentationml.presentation', '.pptx')
        mimetypes.add_type('application/vnd.ms-excel', '.xls')
        mimetypes.add_type('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', '.xlsx')
        mimetypes.add_type('application/vnd.oasis.opendocument.text', '.odt')
        mimetypes.add_type('application/vnd.oasis.opendocument.presentation', '.odp')
        mimetypes.add_type('application/vnd.oasis.opendocument.spreadsheet', '.ods')
        mimetypes.add_type('application/epub+zip', '.epub')
        mimetypes.add_type('application/x-mobipocket-ebook', '.mobi')
        mimetypes.add_type('application/vnd.amazon.ebook', '.azw')
        
    def is_supported_format(self, filepath: str) -> bool:
        ext = Path(filepath).suffix.lower()
        return ext in self.SUPPORTED_FORMATS
        
    def get_file_info(self, filepath: str) -> Dict[str, Any]:
        path = Path(filepath)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        mime_type, _ = mimetypes.guess_type(filepath)
        
        info = {
            'filename': path.name,
            'extension': path.suffix.lower(),
            'filepath': str(path.absolute()),
            'file_size': path.stat().st_size,
            'created': datetime.fromtimestamp(path.stat().st_ctime).isoformat(),
            'modified': datetime.fromtimestamp(path.stat().st_mtime).isoformat(),
            'mime_type': mime_type or 'application/octet-stream',
            'is_supported': self.is_supported_format(filepath),
            'is_readable': os.access(filepath, os.R_OK)
        }
        
        return info
    
    def extract_text(self, filepath: str, format_hint: str = None) -> str:
        file_info = self.get_file_info(filepath)
        
        if not file_info['is_supported']:
            if format_hint and format_hint.lower() in self.SUPPORTED_FORMATS:
                extension = format_hint.lower()
            else:
                raise ValueError(f"Unsupported file format: {file_info['extension']}")
        else:
            extension = file_info['extension']
        
        if extension not in self.handlers:
            return self._extract_fallback(filepath)

        try:
            text = self.handlers[extension](filepath)
            text = self._clean_extracted_text(text)
            
            return text
        except Exception as e:
            try:
                text = self._extract_fallback(filepath)
                text = self._clean_extracted_text(text)
                return text
            except Exception as fallback_error:
                raise Exception(f"Failed to extract text from {filepath}: {e}. Fallback also failed: {fallback_error}")
    def extract_with_metadata(self, filepath: str) -> Dict[str, Any]:
        file_info = self.get_file_info(filepath)
        
        try:
            text = self.extract_text(filepath)
            
            result = {
                'success': True,
                'text': text,
                'metadata': file_info,
                'text_metrics': {
                    'characters': len(text),
                    'words': len(text.split()),
                    'lines': text.count('\n') + 1,
                    'paragraphs': len([p for p in text.split('\n\n') if p.strip()])
                },
                'extraction_timestamp': datetime.now().isoformat()
            }    
            format_metadata = self._extract_format_metadata(filepath, file_info['extension'])
            if format_metadata:
                result['format_metadata'] = format_metadata
            
        except Exception as e:
            result = {
                'success': False,
                'error': str(e),
                'metadata': file_info,
                'extraction_timestamp': datetime.now().isoformat()
            }
        
        return result
    
    def extract_from_directory(self, directory: str, 
                              recursive: bool = False,
                              extensions: List[str] = None) -> List[Dict[str, Any]]:
         
        results = []
        dir_path = Path(directory)
        
        if not dir_path.exists() or not dir_path.is_dir():
            raise ValueError(f"Directory not found: {directory}")
        
        if extensions:
            patterns = [f"*{ext}" for ext in extensions]
        else:
            patterns = [f"*{ext}" for ext in self.SUPPORTED_FORMATS.keys()]
        
        files = []
        for pattern in patterns:
            if recursive:
                files.extend(dir_path.rglob(pattern))
            else:
                files.extend(dir_path.glob(pattern))
        files = sorted(set(files))
        
        for file_path in files:
            if file_path.is_file():
                try:
                    result = self.extract_with_metadata(str(file_path))
                    results.append(result)
                except Exception as e:
                    results.append({
                        'success': False,
                        'error': str(e),
                        'filepath': str(file_path),
                        'extraction_timestamp': datetime.now().isoformat()
                    })
        
        return results
    
    
    def _extract_text_file(self, filepath: str) -> str:
        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(filepath, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        with open(filepath, 'rb') as f:
            return f.read().decode('utf-8', errors='ignore')
    
    def _extract_docx(self, filepath: str) -> str:
        try:
            from docx import Document
            doc = Document(filepath)
            text_parts = []
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_parts.append(paragraph.text)
            
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        if cell.text.strip():
                            text_parts.append(cell.text)
            
            return '\n'.join(text_parts)
        except ImportError:
            return self._extract_docx_fallback(filepath)
    
    def _extract_docx_fallback(self, filepath: str) -> str:
        import zipfile
        import xml.etree.ElementTree as ET
        
        text_parts = []
        with zipfile.ZipFile(filepath) as docx:
            if 'word/document.xml' in docx.namelist():
                xml_content = docx.read('word/document.xml').decode('utf-8')
                text = re.sub(r'<[^>]+>', ' ', xml_content)
                text = re.sub(r'\s+', ' ', text)
                import html
                text = html.unescape(text)
                
                text_parts.append(text.strip())
        
        return '\n'.join(text_parts)
    
    def _extract_doc(self, filepath: str) -> str: