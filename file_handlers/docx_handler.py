import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
import tempfile
import os

class DOCXHandler:
    



def extract_docx_as_zip(filepath: str, extract_to: str = None) -> str:
    if extract_to is None:
        extract_to = tempfile.mkdtemp(prefix='docx_extract_')
        
    try:
        with zipfile.ZipFile(filepath, 'r') as docx:
            docx.extractall(extract_to)
            
        return extract_to
    except Exception as e:
        raise Exception(f"Failed to extract DOCX: {e}")
        
    
    