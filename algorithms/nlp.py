import re
import string
import math
import json
from typing import Dict, List, Tuple, Optional, Any, Set, Union
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from enum import Enum
import hashlib
from datetime import datetime
import itertools
import numpy as np

class TextCategory(Enum):
    ACADEMIC = "academic"
    TECHNICAL = "technical"
    LITERARY = "literary"
    JOURNALISTIC = "journalistic"
    CASUAL = "casual"
    LEGAL = "legal"
    MEDICAL = "medical"
    SCIENTIFIC = "scientific"
    UNKNOWN = "unknown"

class Language(Enum):