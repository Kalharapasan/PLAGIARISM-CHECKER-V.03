import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
from datetime import datetime
from ..core.base_engine import BasePlagiarismEngine
from ..reports.basic_report import generate_basic_report

class BasicPlagiarismChecker:
    
    def _get_sample_database(self):
        return [
            {
                'source': 'Wikipedia - Academic Integrity',
                'url': 'https://en.wikipedia.org/wiki/Academic_integrity',
                'text': '''Academic integrity is the moral code or ethical policy of academia. 
                It includes values such as avoidance of cheating or plagiarism, maintenance of 
                academic standards, and honesty and rigor in research and academic publishing.'''
            },
            {
                'source': 'Educational Research Journal',
                'url': 'https://example.com/research',
                'text': '''Plagiarism is the representation of another author's language, thoughts, 
                ideas, or expressions as one's own original work. In educational contexts, proper 
                attribution is essential.'''
            }
        ]
    
    def run(self):
        self.root = tk.Tk()
        self._setup_window()
        self._create_ui()
        self._center_window()
        self.root.mainloop()
    
    def _setup_window(self):
        self.root.title("Plagiarism Checker - Basic Version")
        window_size = self.config.get('ui.basic.window_size', '1000x700')
        self.root.geometry(window_size)
        self.root.configure(bg='#f0f0f0')
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
    
    def _center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def _create_ui(self):
        header_frame = tk.Frame(self.root, bg='#667eea', height=100)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🔍 Plagiarism Checker", 
                bg='#667eea', fg='white', font=('Arial', 24, 'bold')).pack(pady=(15, 5))
        tk.Label(header_frame, text="Basic Version - For Students", 
                bg='#667eea', fg='white', font=('Arial', 10)).pack()
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        