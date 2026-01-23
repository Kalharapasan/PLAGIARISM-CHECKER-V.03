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
        left_frame = tk.Frame(main_container, bg='white', relief='raised', bd=1)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        input_header = tk.Frame(left_frame, bg='#f7fafc', height=50)
        input_header.pack(fill='x')
        input_header.pack_propagate(False)
        
        tk.Label(input_header, text="📄 Document Input", 
                bg='#f7fafc', fg='#2d3748', font=('Arial', 12, 'bold')).pack(pady=15, padx=15, anchor='w')
        upload_frame = tk.Frame(left_frame, bg='white')
        upload_frame.pack(fill='x', padx=15, pady=15)
        
        self.file_label = tk.Label(upload_frame, text="No file selected", 
                                  bg='white', fg='#4a5568', font=('Arial', 10))
        self.file_label.pack(pady=(0, 10))
        
        button_frame = tk.Frame(upload_frame, bg='white')
        button_frame.pack()
        
        tk.Button(button_frame, text="📁 Choose File", 
                 command=self.select_file, bg='#4299e1', fg='white',
                 font=('Arial', 10, 'bold'), relief='flat', cursor='hand2',
                 activebackground='#3182ce').pack(side='left', padx=5)
        
        tk.Button(button_frame, text="🗑️ Clear", 
                 command=self.clear_file, bg='#e53e3e', fg='white',
                 font=('Arial', 10, 'bold'), relief='flat', cursor='hand2',
                 activebackground='#c53030').pack(side='left', padx=5)
        tk.Label(upload_frame, text="Supported: DOCX, PDF, TXT", 
                bg='white', fg='#a0aec0', font=('Arial', 9)).pack(pady=(10, 0))
        tk.Label(left_frame, text="Or paste text directly:", 
                bg='white', fg='#4a5568', font=('Arial', 10)).pack(padx=15, pady=(10, 5), anchor='w')
        
        self.text_input = scrolledtext.ScrolledText(left_frame, height=15, 
                                                    font=('Arial', 10), wrap='word')
        self.text_input.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        self.check_button = tk.Button(left_frame, text="🔍 Check for Plagiarism", 
                                     bg='#48bb78', fg='white', font=('Arial', 12, 'bold'),
                                     command=self.run_check, cursor='hand2', relief='flat',
                                     activebackground='#38a169', activeforeground='white')
        self.check_button.pack(fill='x', padx=15, pady=(0, 15))
        right_frame = tk.Frame(main_container, bg='white', relief='raised', bd=1)
        right_frame.pack(side='right', fill='both', expand=True)
        results_header = tk.Frame(right_frame, bg='#f7fafc', height=50)
        results_header.pack(fill='x')
        results_header.pack_propagate(False)
        
        tk.Label(results_header, text="📊 Analysis Results", 
                bg='#f7fafc', fg='#2d3748', font=('Arial', 12, 'bold')).pack(pady=15, padx=15, anchor='w')
        