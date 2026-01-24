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
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Document", command=self.select_file)
        file_menu.add_command(label="Batch Check", command=self.open_batch_mode)
        file_menu.add_separator()
        file_menu.add_command(label="Export Report (TXT)", command=lambda: self.export_report('txt'))
        file_menu.add_command(label="Export Report (HTML)", command=lambda: self.export_report('html'))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        db_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Database", menu=db_menu)
        db_menu.add_command(label="Manage References", command=self.manage_database)
        db_menu.add_command(label="Add Document", command=self.add_to_database)
        db_menu.add_command(label="View Statistics", command=self.show_db_stats)
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="User Guide", command=self.show_help)
        help_menu.add_command(label="About", command=self.show_about)
    
    def _create_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        self.create_checker_tab()
        self.create_batch_tab()
        self.create_database_tab()
        self.create_analytics_tab()
        self.status_bar = tk.Label(self.root, 
                                  text=f"Ready | Database: {len(self.database)} documents loaded", 
                                  bd=1, relief='sunken', anchor='w', 
                                  bg='#e2e8f0', font=('Arial', 9))
        self.status_bar.pack(side='bottom', fill='x')
    
    def create_checker_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📝 Document Checker")