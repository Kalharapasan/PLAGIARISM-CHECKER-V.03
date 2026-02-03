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