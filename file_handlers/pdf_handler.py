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