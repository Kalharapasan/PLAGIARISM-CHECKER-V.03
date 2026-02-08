import json
import hashlib
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
import threading
import queue
import sys

class ProgressTracker: