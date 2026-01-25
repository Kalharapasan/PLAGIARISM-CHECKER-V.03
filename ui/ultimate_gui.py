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

class UltimatePlagiarismChecker:
    
    def setup_fonts(self):
        self.fonts = {
            'title': ('Segoe UI', 26, 'bold'),
            'subtitle': ('Segoe UI', 11),
            'header': ('Segoe UI', 13, 'bold'),
            'normal': ('Segoe UI', 10),
            'small': ('Segoe UI', 9),
            'monospace': ('Consolas', 9),
            'large': ('Segoe UI', 14, 'bold')
        }
    
    def run(self):
        self.root = tk.Tk()
        self._setup_window()
        self._create_menubar()
        self._create_ui()
        self._apply_theme()
        self._center_window()
        self.root.mainloop()
    
    def _setup_window(self):
        self.root.title("Plagiarism Checker Ultimate - Enterprise Edition v3.0")
        window_size = self.config.get('ui.ultimate.window_size', '1600x1000')
        self.root.geometry(window_size)
        self.root.configure(bg='#f0f0f0')
