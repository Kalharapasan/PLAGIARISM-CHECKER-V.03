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