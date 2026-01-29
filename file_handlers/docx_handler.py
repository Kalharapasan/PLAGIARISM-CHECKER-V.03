import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
import tempfile
import os

class DOCXHandler:
    NAMESPACES = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
        'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
        'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
        'v': 'urn:schemas-microsoft-com:vml'
    }
    
    def __init__(self, config=None):
        self.config = config or {}
        self._register_namespaces()
    
    def _register_namespaces(self):
        for prefix, uri in self.NAMESPACES.items():
            ET.register_namespace(prefix, uri)
    
    def extract_text(self, filepath: str) -> str:
        try:
            return self._extract_with_docx(filepath)



def extract_docx_as_zip(filepath: str, extract_to: str = None) -> str:
    if extract_to is None:
        extract_to = tempfile.mkdtemp(prefix='docx_extract_')
        
    try:
        with zipfile.ZipFile(filepath, 'r') as docx:
            docx.extractall(extract_to)
            
        return extract_to
    except Exception as e:
        raise Exception(f"Failed to extract DOCX: {e}")
        
    
    