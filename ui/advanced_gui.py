import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import threading
from datetime import datetime
from ..core.advanced_engine import AdvancedPlagiarismEngine
from ..core.database import DatabaseManager
from ..reports.advanced_report import generate_advanced_report, generate_html_report


class AdvancedPlagiarismChecker:
    
    def run(self):
        self.root = tk.Tk()
        self._setup_window()
        self._create_menubar()
        self._create_ui()
        self._center_window()
        self.root.mainloop()
    
    def _setup_window(self):
        self.root.title("Plagiarism Checker Pro - Advanced Version")
        window_size = self.config.get('ui.advanced.window_size', '1400x900')
        self.root.geometry(window_size)
        self.root.configure(bg='#f0f0f0')
    
    def _create_menubar(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)