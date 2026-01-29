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
        except ImportError:
            return self._extract_manual(filepath)
        except Exception as e:
            try:
                return self._extract_manual(filepath)
            except Exception as e2:
                raise Exception(f"Failed to extract text from DOCX: {e2}")
    
    def _extract_with_docx(self, filepath: str) -> str:
        from docx import Document
        from docx.enum.style import WD_STYLE_TYPE
        from docx.oxml.ns import qn
        
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
        for section in doc.sections:
            header = section.header
            for paragraph in header.paragraphs:
                if paragraph.text.strip():
                    text_parts.append(paragraph.text)
        footer = section.footer
        for paragraph in footer.paragraphs:
            if paragraph.text.strip():
                text_parts.append(paragraph.text)
        text_boxes = self._extract_text_boxes_from_docx(filepath)
        text_parts.extend(text_boxes)
        
        return '\n'.join(text_parts)

    def _extract_text_boxes_from_docx(self, filepath: str) -> List[str]:
        text_boxes = []
        try:
            with zipfile.ZipFile(filepath) as docx:
                if 'word/document.xml' not in docx.namelist():
                    return text_boxes
                xml_content = docx.read('word/document.xml').decode('utf-8')
                
                root = ET.fromstring(xml_content)
                for shape in root.findall('.//w:txbxContent', self.NAMESPACES):
                    for paragraph in shape.findall('.//w:p', self.NAMESPACES):
                        text = self._extract_text_from_paragraph(paragraph)
                        if text.strip():
                            text_boxes.append(text)
                
        except Exception as e:
            print(f"Warning: Could not extract text boxes: {e}")
        
        return text_boxes
    
    def _extract_manual(self, filepath: str) -> str:
        text_parts = []
        
        with zipfile.ZipFile(filepath) as docx:
            if 'word/document.xml' in docx.namelist():
                xml_content = docx.read('word/document.xml').decode('utf-8')
                text_parts.append(self._parse_document_xml(xml_content))
            header_texts = self._extract_headers_manual(docx)
            text_parts.extend(header_texts)
            footer_texts = self._extract_footers_manual(docx)
            text_parts.extend(footer_texts)
            footnote_texts = self._extract_footnotes_manual(docx)
            text_parts.extend(footnote_texts)
            endnote_texts = self._extract_endnotes_manual(docx)
            text_parts.extend(endnote_texts)
        return '\n'.join(filter(None, text_parts))

    def _parse_document_xml(self, xml_content: str) -> str:
        try:
            root = ET.fromstring(xml_content)
            paragraphs = []
            for para in root.findall('.//w:p', self.NAMESPACES):
                para_text = self._extract_text_from_paragraph(para)
                if para_text.strip():
                    paragraphs.append(para_text)
            
            return '\n'.join(paragraphs)
        except Exception as e:
            print(f"Warning: Error parsing document XML: {e}")
            return self._extract_text_regex(xml_content)

    def _extract_text_from_paragraph(self, paragraph: ET.Element) -> str:
        text_parts = []
                



def extract_docx_as_zip(filepath: str, extract_to: str = None) -> str:
    if extract_to is None:
        extract_to = tempfile.mkdtemp(prefix='docx_extract_')
        
    try:
        with zipfile.ZipFile(filepath, 'r') as docx:
            docx.extractall(extract_to)
            
        return extract_to
    except Exception as e:
        raise Exception(f"Failed to extract DOCX: {e}")
        
    
