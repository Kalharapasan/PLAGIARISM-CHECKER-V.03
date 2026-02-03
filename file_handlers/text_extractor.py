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