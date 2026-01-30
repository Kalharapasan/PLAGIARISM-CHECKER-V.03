import re
import io
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, BinaryIO
from datetime import datetime
import tempfile
import os
import warnings

class PDFHandler:
    
    
    def extract_text(self, filepath: str, method: str = None) -> str:
        if method is None:
            for extraction_method in self.extraction_methods:
                try:
                    text = self._extract_with_method(filepath, extraction_method)
                    if text and len(text.strip()) > 0:
                        return text
                except Exception as e:
                    continue
            return self._extract_fallback(filepath)
        else:
            return self._extract_with_method(filepath, method)
    
    def _extract_with_method(self, filepath: str, method: str) -> str:
        cache_key = f"{filepath}_{method}"
        if cache_key in self._extraction_cache:
            return self._extraction_cache[cache_key]
        
        try:
            if method == 'pdfplumber':
                text = self._extract_with_pdfplumber(filepath)
            elif method == 'pypdf':
                text = self._extract_with_pypdf(filepath)
            elif method == 'pdfminer':
                text = self._extract_with_pdfminer(filepath)
            elif method == 'fallback':
                text = self._extract_fallback(filepath)
            else:
                raise ValueError(f"Unknown extraction method: {method}")
            self._extraction_cache[cache_key] = text
            return text
            
        except ImportError:
            raise ImportError(f"Required library for {method} not installed")
        except Exception as e:
            raise Exception(f"Failed to extract text with {method}: {str(e)}")
    
    def _extract_with_pdfplumber(self, filepath: str) -> str:
        import pdfplumber
        
        text_parts = []
        with pdfplumber.open(filepath) as pdf:
            total_pages = len(pdf.pages)
            pages_to_process = range(total_pages)
            
            if self.max_pages > 0:
                pages_to_process = range(min(self.max_pages, total_pages))
        for i in pages_to_process:
                page = pdf.pages[i]
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
                if self.extract_tables:
                    tables = page.extract_tables()
                    for table in tables:
                        if table:
                            table_text = self._format_table_text(table)
                            if table_text:
                                text_parts.append(table_text)
                if self.extract_images:
                    images = page.images
                    for img in images:
                        if self.ocr_enabled:
                            ocr_text = self._extract_text_from_image(img)
                            if ocr_text:
                                text_parts.append(f"[Image Text: {ocr_text}]")
        
        return '\n'.join(text_parts)
    
    def _extract_with_pypdf(self, filepath: str) -> str:
        from pypdf import PdfReader
        
        text_parts = []
        
        with open(filepath, 'rb') as file:
            reader = PdfReader(file)
            total_pages = len(reader.pages)
            pages_to_process = range(total_pages)
            
            if self.max_pages > 0:
                pages_to_process = range(min(self.max_pages, total_pages))
            
            for i in pages_to_process:
                page = reader.pages[i]
                page_text = page.extract_text()
                if page_text:
                    page_text = self._clean_pdf_text(page_text)
                    text_parts.append(page_text)
        
        return '\n'.join(text_parts)
    
    def _extract_with_pdfminer(self, filepath: str) -> str:
        from pdfminer.high_level import extract_text
        if self.max_pages > 0:
            text = extract_text(filepath, page_numbers=list(range(self.max_pages)))
        else:
            text = extract_text(filepath)
        
        return self._clean_pdf_text(text)
    
    def _extract_fallback(self, filepath: str) -> str:
        text = ""
        try:
            import subprocess
            result = subprocess.run(
                ['pdftotext', filepath, '-'],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                text = result.stdout
        except:
            pass
        if not text.strip():
            try:
                import subprocess
                result = subprocess.run(
                    ['strings', filepath],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0:
                    text = result.stdout
                    lines = text.split('\n')
                    filtered_lines = []
                    for line in lines:
                        for line in lines:
                            if len(line) > 3 and sum(c.isprintable() for c in line) / len(line) > 0.7:
                                filtered_lines.append(line)
                    text = '\n'.join(filtered_lines)
            except:
                pass
        
        return self._clean_pdf_text(text)
    
    def _extract_text_from_image(self, image_data: Any) -> str:
        if not self.ocr_enabled:
            return ""
        try:
            import pytesseract
            from PIL import Image
            if hasattr(image_data, 'to_image'):
                pil_image = image_data.to_image()
            else:
                pil_image = Image.open(io.BytesIO(image_data['stream'].get_data()))
            text = pytesseract.image_to_string(pil_image)
            return text.strip()
        except ImportError:
            return ""
        except Exception as e:
            print(f"Warning: OCR failed: {e}")
            return ""
    
    def _format_table_text(self, table: List[List]) -> str:
        if not table:
            return ""
        formatted_rows = []
        for row in table:
            row_text = ' | '.join(str(cell) if cell is not None else '' for cell in row)
            formatted_rows.append(row_text)
        
        return '\n'.join(formatted_rows)
    
    def _clean_pdf_text(self, text: str) -> str:
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'(\w)-\s+(\w)', r'\1\2', text)  
        text = re.sub(r'\s+([.,;:!?])', r'\1', text)  
        text = re.sub(r'([.,;:!?])\s+', r'\1 ', text)  
        text = ''.join(char for char in text if char.isprintable() or char in '\n\t')
        
        return text.strip()
    
    
    def extract_metadata(self, filepath: str) -> Dict[str, Any]:
        metadata = {
            'filename': Path(filepath).name,
            'file_size': Path(filepath).stat().st_size,
            'modified': datetime.fromtimestamp(Path(filepath).stat().st_mtime).isoformat(),
            'created': datetime.fromtimestamp(Path(filepath).stat().st_ctime).isoformat(),
            'pdf_metadata': {},
            'security': {},
            'pages': 0,
            'is_scanned': False,
            'has_text_layer': True
        }
        try:
            metadata.update(self._extract_metadata_pypdf(filepath))
        except:
            try:
                metadata.update(self._extract_metadata_pdfplumber(filepath))
            except:
                try:
                    metadata.update(self._extract_metadata_pdfminer(filepath))
                except Exception as e:
                    print(f"Warning: Could not extract PDF metadata: {e}")
        metadata['is_scanned'] = self._is_scanned_pdf(filepath)
        metadata['has_text_layer'] = self._has_text_layer(filepath)
        
        return metadata

    def _extract_metadata_pypdf(self, filepath: str) -> Dict[str, Any]:
        from pypdf import PdfReader
        
        metadata = {
            'pdf_metadata': {},
            'security': {},
            'pages': 0
        }
        
        with open(filepath, 'rb') as file:
            reader = PdfReader(file)
            metadata['pages'] = len(reader.pages)
            if reader.metadata:
                for key, value in reader.metadata.items():
                    if value:
                        clean_key = key.replace('/', '').strip()
                        metadata['pdf_metadata'][clean_key] = str(value)
            if reader.is_encrypted:
                metadata['security'] = {
                    'encrypted': True,
                    'permissions': {
                        'print': not (reader._encryption.get('/Print') == 'false'),
                        'modify': not (reader._encryption.get('/Modify') == 'false'),
                        'copy': not (reader._encryption.get('/Copy') == 'false'),
                        'annotate': not (reader._encryption.get('/Annotate') == 'false')
                    }
                }
            else:
                metadata['security'] = {'encrypted': False}
        
        return metadata
    
    def _extract_metadata_pdfplumber(self, filepath: str) -> Dict[str, Any]:
        import pdfplumber
        
        metadata = {
            'pdf_metadata': {},
            'security': {},
            'pages': 0
        }
        with pdfplumber.open(filepath) as pdf:
            metadata['pages'] = len(pdf.pages)
            if hasattr(pdf, 'metadata') and pdf.metadata:
                for key, value in pdf.metadata.items():
                    if value:
                        clean_key = key.replace('/', '').strip()
                        metadata['pdf_metadata'][clean_key] = str(value)
        
        return metadata
    
    def _extract_metadata_pdfminer(self, filepath: str) -> Dict[str, Any]:
        from pdfminer.pdfparser import PDFParser
        from pdfminer.pdfdocument import PDFDocument
        from pdfminer.psparser import PSLiteral
        
        metadata = {
            'pdf_metadata': {},
            'security': {},
            'pages': 0
        }
        
        with open(filepath, 'rb') as file:
            parser = PDFParser(file)
            doc = PDFDocument(parser)
            if hasattr(doc, 'catalog'):
                pages_ref = doc.catalog.get('Pages')
                if pages_ref:
                    try:
                        metadata['pages'] = doc.catalog['Pages']['Count']
                    except:
                        pass
            if doc.info:
                for key, value in doc.info[0].items():
                    if value:
                        if isinstance(value, PSLiteral):
                            value = value.name
                        clean_key = key.replace('/', '').strip()
                        metadata['pdf_metadata'][clean_key] = str(value)
            if doc._security_handler:
                metadata['security'] = {'encrypted': True}
            else:
                metadata['security'] = {'encrypted': False}
        
        return metadata

    def _is_scanned_pdf(self, filepath: str) -> bool:
        try:
            text = self.extract_text(filepath, method='pypdf')
            if not text or len(text.strip()) < 50:
                return True
            from pypdf import PdfReader
            with open(filepath, 'rb') as file:
                reader = PdfReader(file)
                if reader.pages:
                    page_text = reader.pages[0].extract_text()
                    if page_text and len(page_text.strip()) < 100:
                        return True
            
            return False
        except:
            return True 
    
    def _has_text_layer(self, filepath: str) -> bool:
        try:
            text = self.extract_text(filepath, method='pypdf')
            if text and len(text.strip()) > 100:
                words = text.split()
                if len(words) > 20:
                    alphabetic_words = sum(1 for word in words if word.isalpha())
                    if alphabetic_words / len(words) > 0.5:
                        return True
            
            return False
            
        except:
            return False