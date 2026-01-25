import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, font
from pathlib import Path
import threading
from datetime import datetime
import json
import webbrowser
from typing import List, Dict, Optional

from ..core.ultimate_engine import UltimatePlagiarismEngine
from ..core.database import DatabaseManager
from ..core.analyzer import AdvancedTextAnalyzer
from ..reports.advanced_report import generate_advanced_report, generate_html_report, generate_json_report
from ..reports.pdf_report import generate_pdf_report
from ..utils import ProgressTracker, format_file_size, format_percentage


