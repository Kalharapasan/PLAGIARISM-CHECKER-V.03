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
        