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
        self.score_frame = tk.Frame(right_frame, bg='white', height=150)
        self.score_frame.pack(fill='x', pady=20)
        self.score_frame.pack_propagate(False)
        
        self.score_label = tk.Label(self.score_frame, text="--", 
                                    font=('Arial', 48, 'bold'), bg='white', fg='#718096')
        self.score_label.pack(pady=10)
        
        self.score_desc = tk.Label(self.score_frame, text="Upload a document to begin", 
                                   bg='white', fg='#718096', font=('Arial', 10))
        self.score_desc.pack()
        self.stats_frame = tk.Frame(right_frame, bg='#f7fafc')
        self.stats_frame.pack(fill='x', padx=15, pady=10)
        tk.Label(right_frame, text="Detailed Matches:", 
                bg='white', fg='#4a5568', font=('Arial', 10)).pack(padx=15, pady=(10, 5), anchor='w')
        
        self.results_text = scrolledtext.ScrolledText(right_frame, height=15, 
                                                     font=('Arial', 9), wrap='word',
                                                     state='disabled')
        self.results_text.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        self.export_button = tk.Button(right_frame, text="💾 Export Report", 
                                      bg='#667eea', fg='white', font=('Arial', 10, 'bold'),
                                      command=self.export_report, cursor='hand2', relief='flat',
                                      state='disabled', activebackground='#5a67d8',
                                      activeforeground='white')
        self.export_button.pack(fill='x', padx=15, pady=(0, 15))
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief='sunken', 
                                  anchor='w', bg='#e2e8f0', font=('Arial', 9))
        self.status_bar.pack(side='bottom', fill='x')
    
    def select_file(self):
        filetypes = [
            ('All Supported', '*.txt *.docx *.pdf'),
            ('Text Files', '*.txt'),
            ('Word Documents', '*.docx'),
            ('PDF Files', '*.pdf')
        ]
        
        filename = filedialog.askopenfilename(title="Select Document", filetypes=filetypes)
        
        if filename:
            self.current_file = filename
            self.file_label.config(text=f"📎 {Path(filename).name}")
            self.text_input.delete(1.0, tk.END)
            self.status_bar.config(text=f"File selected: {Path(filename).name}")
    
    def clear_file(self):
        self.current_file = None
        self.file_label.config(text="No file selected")
        self.status_bar.config(text="Ready")
    
    def run_check(self):
        import threading
        if self.current_file:
            self.status_bar.config(text="Extracting text from file...")
            try:
                text = self.engine.extract_text(self.current_file)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {str(e)}")
                self.status_bar.config(text="Error reading file")
                return
        else:
            text = self.text_input.get(1.0, tk.END).strip()
        
        if not text or len(text) < 50:
            messagebox.showwarning("Warning", "Please provide a document or text (minimum 50 characters)")
            return
        
        self.current_text = text
        self.check_button.config(state='disabled', text="⏳ Analyzing...")
        self.status_bar.config(text="Analyzing document for plagiarism...")
        thread = threading.Thread(target=self.perform_check)
        thread.daemon = True
        thread.start()
    
    def perform_check(self):
        try:
            results = self.engine.analyze_basic(self.current_text, self.database)
            self.results = results
            self.root.after(0, self.display_results)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Analysis failed: {str(e)}"))
            self.root.after(0, lambda: self.check_button.config(state='normal', text="🔍 Check for Plagiarism"))
        
    def display_results(self):
        if not self.results:
            return
        score = self.results['overall_similarity']
        self.score_label.config(text=f"{score}%")
        if score < 15:
            color = '#48bb78'  
            desc = "Low Similarity - Acceptable"
        elif score < 30:
            color = '#ed8936'  
            desc = "Moderate Similarity - Review Needed"
        else:
            color = '#f56565'  
            desc = "High Similarity - Significant Concern"
        
        self.score_label.config(fg=color)
        self.score_desc.config(text=desc, foreground=color)
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        stats = [
            ("Total Words", self.results['total_words']),
            ("Sources Found", len(self.results['matches'])),
            ("Citations", self.results['citations_found'])
        ]
        
        for label, value in stats:
            stat_box = tk.Frame(self.stats_frame, bg='white', relief='solid', bd=1)
            stat_box.pack(side='left', expand=True, fill='both', padx=5, pady=5)
            
            tk.Label(stat_box, text=str(value), font=('Arial', 16, 'bold'),
                    bg='white', fg='#667eea').pack(pady=(10, 0))
            tk.Label(stat_box, text=label, font=('Arial', 8),
                    bg='white', fg='#718096').pack(pady=(0, 10))
        
        self.results_text.config(state='normal')
        self.results_text.delete(1.0, tk.END)
        
        if self.results['matches']:
            for idx, match in enumerate(self.results['matches'], 1):
                self.results_text.insert(tk.END, f"\n━━ Match #{idx} ━━\n")
                self.results_text.insert(tk.END, f"Source: {match['source']}\n")
                if match['url']:
                    self.results_text.insert(tk.END, f"URL: {match['url']}\n")
                self.results_text.insert(tk.END, f"Similarity: {match['similarity']}%\n\n")
                
                if match['matched_sequences']:
                    self.results_text.insert(tk.END, "Matched Sequences:\n")
                    for seq in match['matched_sequences'][:3]:
                        text = seq['text'][:100] + '...' if len(seq['text']) > 100 else seq['text']
                        self.results_text.insert(tk.END, f"• \"{text}\" ({seq['length']} words)\n")
                
                self.results_text.insert(tk.END, "\n")
        else:
            self.results_text.insert(tk.END, "\n✓ No significant matches found.\n\n")
            self.results_text.insert(tk.END, "The document appears to be largely original content.\n")
        
        self.results_text.config(state='disabled')
        self.check_button.config(state='normal', text="🔍 Check for Plagiarism")
        self.export_button.config(state='normal')
        self.status_bar.config(text=f"Analysis complete - {score}% similarity detected")
    
    def export_report(self):
        if not self.results:
            return
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            initialfile=f"plagiarism_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        if not filename:
            return
        document_name = Path(self.current_file).name if self.current_file else "Pasted Text"
        report = generate_basic_report(self.results, document_name)