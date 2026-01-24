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
        paned = ttk.PanedWindow(tab, orient='horizontal')
        paned.pack(fill='both', expand=True)
        left_frame = tk.Frame(paned, bg='white', relief='raised', bd=1)
        paned.add(left_frame, weight=1)
        input_header = tk.Frame(left_frame, bg='#f7fafc', height=50)
        input_header.pack(fill='x')
        input_header.pack_propagate(False)
        
        tk.Label(input_header, text="📄 Document Input", 
                bg='#f7fafc', fg='#2d3748', font=('Arial', 13, 'bold')).pack(pady=15, padx=15, anchor='w')
        upload_frame = tk.Frame(left_frame, bg='white')
        upload_frame.pack(fill='x', padx=15, pady=15)
        
        self.file_label = tk.Label(upload_frame, text="No file selected", 
                                  bg='white', fg='#4a5568', font=('Arial', 10))
        self.file_label.pack(pady=(0, 10))
        
        button_frame = tk.Frame(upload_frame, bg='white')
        button_frame.pack()
        
        tk.Button(button_frame, text="📁 Choose File", command=self.select_file,
                 bg='#4299e1', fg='white', font=('Arial', 10, 'bold'),
                 relief='flat', cursor='hand2').pack(side='left', padx=5)
        
        tk.Button(button_frame, text="🗑️ Clear", command=self.clear_file,
                 bg='#e53e3e', fg='white', font=('Arial', 10, 'bold'),
                 relief='flat', cursor='hand2').pack(side='left', padx=5)
        algo_frame = tk.LabelFrame(left_frame, text="Detection Algorithms", 
                                  bg='white', font=('Arial', 10, 'bold'))
        algo_frame.pack(fill='x', padx=15, pady=10)
        
        self.algo_vars = {}
        algorithms = [
            ('cosine', 'Cosine Similarity (TF-IDF)'),
            ('jaccard', 'Jaccard Index'),
            ('ngram', 'N-Gram Analysis'),
            ('sequence', 'Sequence Matching')
        ]
        
        for algo_id, algo_name in algorithms:
            var = tk.BooleanVar(value=algo_id in self.selected_algorithms)
            self.algo_vars[algo_id] = var
            cb = tk.Checkbutton(algo_frame, text=algo_name, variable=var, 
                              bg='white', font=('Arial', 9), anchor='w')
            cb.pack(fill='x', padx=10, pady=2)
        tk.Label(left_frame, text="Or paste text directly:", 
                bg='white', fg='#4a5568', font=('Arial', 10)).pack(padx=15, pady=(10, 5), anchor='w')
        
        self.text_input = scrolledtext.ScrolledText(left_frame, height=12, 
                                                   font=('Arial', 10), wrap='word')
        self.text_input.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        self.check_button = tk.Button(left_frame, text="🔍 Analyze Document", 
                                     bg='#48bb78', fg='white', font=('Arial', 12, 'bold'),
                                     command=self.run_advanced_check, cursor='hand2', relief='flat')
        self.check_button.pack(fill='x', padx=15, pady=(0, 15))
        right_frame = tk.Frame(paned, bg='white', relief='raised', bd=1)
        paned.add(right_frame, weight=2)
        results_header = tk.Frame(right_frame, bg='#f7fafc', height=50)
        results_header.pack(fill='x')
        results_header.pack_propagate(False)
        
        tk.Label(results_header, text="📊 Analysis Results", 
                bg='#f7fafc', fg='#2d3748', font=('Arial', 13, 'bold')).pack(pady=15, padx=15, anchor='w')
        self.score_frame = tk.Frame(right_frame, bg='white', height=120)
        self.score_frame.pack(fill='x', pady=15)
        self.score_frame.pack_propagate(False)
        
        score_container = tk.Frame(self.score_frame, bg='white')
        score_container.pack(expand=True)
        
        self.score_label = tk.Label(score_container, text="--", 
                                   font=('Arial', 56, 'bold'), bg='white', fg='#718096')
        self.score_label.grid(row=0, column=0, padx=20)
        
        self.score_desc = tk.Label(score_container, text="Ready to analyze", 
                                  bg='white', fg='#718096', font=('Arial', 10))
        self.score_desc.grid(row=1, column=0)
        self.stats_frame = tk.Frame(right_frame, bg='#f7fafc')
        self.stats_frame.pack(fill='x', padx=15, pady=10)
        results_notebook = ttk.Notebook(right_frame)
        results_notebook.pack(fill='both', expand=True, padx=15, pady=10)
        matches_tab = ttk.Frame(results_notebook)
        results_notebook.add(matches_tab, text="Matches")
        
        self.results_text = scrolledtext.ScrolledText(matches_tab, font=('Arial', 9), 
                                                     wrap='word', state='disabled')
        self.results_text.pack(fill='both', expand=True)
        stats_tab = ttk.Frame(results_notebook)
        results_notebook.add(stats_tab, text="Statistics")
        
        self.stats_text = scrolledtext.ScrolledText(stats_tab, font=('Courier', 9), 
                                                   wrap='word', state='disabled')
        self.stats_text.pack(fill='both', expand=True)
        export_frame = tk.Frame(right_frame, bg='white')
        export_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Button(export_frame, text="💾 Export TXT", bg='#667eea', fg='white', 
                 font=('Arial', 10, 'bold'), command=lambda: self.export_report('txt'),
                 relief='flat', cursor='hand2').pack(side='left', padx=5)
        
        tk.Button(export_frame, text="📄 Export HTML", bg='#667eea', fg='white',
                 font=('Arial', 10, 'bold'), command=lambda: self.export_report('html'),
                 relief='flat', cursor='hand2').pack(side='left', padx=5)
    
    def create_batch_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📦 Batch Processing")
        
        tk.Label(tab, text="Batch Document Processing", 
                font=('Arial', 16, 'bold')).pack(pady=20)
        list_frame = tk.Frame(tab)
        list_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.batch_listbox = tk.Listbox(list_frame, font=('Arial', 10), height=15)
        self.batch_listbox.pack(side='left', fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(list_frame, command=self.batch_listbox.yview)
        scrollbar.pack(side='right', fill='y')
        self.batch_listbox.config(yscrollcommand=scrollbar.set)
        btn_frame = tk.Frame(tab)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Add Files", command=self.add_batch_files,
                 bg='#48bb78', fg='white', font=('Arial', 11, 'bold'), 
                 relief='flat', cursor='hand2', padx=20, pady=10).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Process All", command=self.process_batch,
                 bg='#667eea', fg='white', font=('Arial', 11, 'bold'),
                 relief='flat', cursor='hand2', padx=20, pady=10).pack(side='left', padx=5)
        
        self.batch_progress = ttk.Progressbar(tab, mode='determinate')
        self.batch_progress.pack(fill='x', padx=20, pady=10)
        
        self.batch_status = tk.Label(tab, text="Ready", font=('Arial', 10))
        self.batch_status.pack()
    
    def create_database_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="💾 Reference Database")
        
        tk.Label(tab, text="Reference Document Database", 
                font=('Arial', 16, 'bold')).pack(pady=20)
        list_frame = tk.Frame(tab)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        columns = ('Source', 'Category', 'Words')
        self.db_tree = ttk.Treeview(list_frame, columns=columns, show='tree headings', height=15)
        
        self.db_tree.heading('#0', text='ID')
        self.db_tree.heading('Source', text='Source')
        self.db_tree.heading('Category', text='Category')
        self.db_tree.heading('Words', text='Word Count')
        
        self.db_tree.column('#0', width=50)
        self.db_tree.column('Source', width=300)
        self.db_tree.column('Category', width=150)
        self.db_tree.column('Words', width=100)
        
        self.db_tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(list_frame, command=self.db_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.db_tree.config(yscrollcommand=scrollbar.set)
        self.refresh_database_view()
        btn_frame = tk.Frame(tab)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Add Document", command=self.add_to_database,
                 bg='#48bb78', fg='white', font=('Arial', 11, 'bold'),
                 relief='flat', cursor='hand2', padx=20, pady=10).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Delete Selected", command=self.delete_from_database,
                 bg='#f56565', fg='white', font=('Arial', 11, 'bold'),
                 relief='flat', cursor='hand2', padx=20, pady=10).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Refresh", command=self.refresh_database_view,
                 bg='#667eea', fg='white', font=('Arial', 11, 'bold'),
                 relief='flat', cursor='hand2', padx=20, pady=10).pack(side='left', padx=5)
        
    def create_analytics_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📈 Analytics & History")
        
        tk.Label(tab, text="Check History & Analytics", 
                font=('Arial', 16, 'bold')).pack(pady=20)
        list_frame = tk.Frame(tab)
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('Date', 'File', 'Score', 'Words', 'Sources')
        self.history_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.history_tree.heading(col, text=col)
        
        self.history_tree.column('Date', width=150)
        self.history_tree.column('File', width=250)
        self.history_tree.column('Score', width=100)
        self.history_tree.column('Words', width=100)
        self.history_tree.column('Sources', width=100)
        
        self.history_tree.pack(side='left', fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(list_frame, command=self.history_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.history_tree.config(yscrollcommand=scrollbar.set)
        btn_frame = tk.Frame(tab)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Refresh History", command=self.refresh_history,
                 bg='#667eea', fg='white', font=('Arial', 11, 'bold'),
                 relief='flat', cursor='hand2', padx=20, pady=10).pack(side='left', padx=5)
        
        self.refresh_history()
    
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
    
    def run_advanced_check(self):
        self.selected_algorithms = [algo for algo, var in self.algo_vars.items() if var.get()]
        
        if not self.selected_algorithms:
            messagebox.showwarning("Warning", "Please select at least one detection algorithm")
            return
        if self.current_file:
            self.status_bar.config(text="Extracting text...")
            try:
                text = self.engine.extract_text(self.current_file)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {str(e)}")
                return
        else:
            text = self.text_input.get(1.0, tk.END).strip()
        
        if len(text) < 50:
            messagebox.showwarning("Warning", "Text too short (minimum 50 characters)")
            return
        
        self.current_text = text
        self.check_button.config(state='disabled', text="⏳ Analyzing...")
        self.status_bar.config(text="Running advanced analysis...")
        thread = threading.Thread(target=self.perform_advanced_check)
        thread.daemon = True
        thread.start()
    
    def perform_advanced_check(self):
        try:
            results = self.engine.analyze_text(
                self.current_text, 
                self.database,
                self.selected_algorithms
            )
            self.results = results
            self.root.after(0, self.display_advanced_results)
            filename = Path(self.current_file).name if self.current_file else "Pasted Text"
            self.db_manager.save_check_history(filename, results)
        
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Analysis failed: {str(e)}"))
            self.root.after(0, lambda: self.check_button.config(state='normal', text="🔍 Analyze Document"))
    
    def display_advanced_results(self):
        if not self.results:
            return
        
        score = self.results['overall_similarity']
        self.score_label.config(text=f"{score}%")
        
        if score < 15:
            color, desc = '#48bb78', "Low Risk - Acceptable"
        elif score < 30:
            color, desc = '#ed8936', "Moderate Risk - Review Needed"
        else:
            color, desc = '#f56565', "High Risk - Significant Concern"
        
        self.score_label.config(fg=color)
        self.score_desc.config(text=desc, foreground=color)
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        stats = self.results.get('statistics', {})
        stats_data = [
            ("Total Words", self.results['total_words']),
            ("Matched", stats.get('matched_words', 0)),
            ("Unique", f"{stats.get('unique_percentage', 0)}%"),
            ("Sources", len(self.results['matches'])),
            ("Citations", self.results.get('citations_found', 0))
        ]
        
        for label, value in stats_data:
            box = tk.Frame(self.stats_frame, bg='white', relief='solid', bd=1)
            box.pack(side='left', expand=True, fill='both', padx=3, pady=3)
            
            tk.Label(box, text=str(value), font=('Arial', 14, 'bold'),
                    bg='white', fg='#667eea').pack(pady=(8, 0))
            tk.Label(box, text=label, font=('Arial', 8),
                    bg='white', fg='#718096').pack(pady=(0, 8))
        
        self.results_text.config(state='normal')
        self.results_text.delete(1.0, tk.END)
        
        if self.results['matches']:
            for idx, match in enumerate(self.results['matches'], 1):
                self.results_text.insert(tk.END, f"\n━━━ Match #{idx} ━━━\n")
                self.results_text.insert(tk.END, f"{match['source']}\n")
                if match['url']:
                    self.results_text.insert(tk.END, f"🔗 {match['url']}\n")
                self.results_text.insert(tk.END, f"Similarity: {match['similarity']}% | Confidence: {match.get('confidence', 'N/A')}\n\n")
                self.results_text.insert(tk.END, "Algorithm Scores:\n")
                
                for algo, score in match.get('algorithm_scores', {}).items():
                    self.results_text.insert(tk.END, f"  • {algo.capitalize()}: {score}%\n")
                
                if match['matched_sequences']:
                    self.results_text.insert(tk.END, f"\nMatched Sequences ({len(match['matched_sequences'])}):\n")
                    for seq in match['matched_sequences'][:3]:
                        text = seq['text'][:120] + '...' if len(seq['text']) > 120 else seq['text']
                        self.results_text.insert(tk.END, f"• \"{text}\" ({seq['length']} words)\n")
                
                self.results_text.insert(tk.END, "\n")
        else:
            self.results_text.insert(tk.END, "\n✓ No significant matches found\n")
        
        self.results_text.config(state='disabled')
        self.stats_text.config(state='normal')
        self.stats_text.delete(1.0, tk.END)
        
        stats_report = f"""
STATISTICAL ANALYSIS
{'='*60}

Document Metrics:
  Total Words: {self.results['total_words']}
  Total Sentences: {self.results['total_sentences']}
  Citations Detected: {self.results.get('citations_found', 0)}

Similarity Metrics:
  Overall Score: {score}%
  Matched Words: {stats.get('matched_words', 0)}
  Unique Words: {stats.get('unique_words', 0)}
  Unique Percentage: {stats.get('unique_percentage', 0)}%

Match Analysis:
  Sources Found: {len(self.results['matches'])}
  Average Match Length: {stats.get('average_sequence_length', 0)} words
  Longest Match: {stats.get('longest_sequence', 0)} words

Algorithm Performance:
"""
        if self.results.get('algorithm_scores'):
                for algo, perf in self.results['algorithm_scores'].items():
                    stats_report += f"  {algo.capitalize()}: {perf.get('average', 0):.2f}% (avg)\n"
            
        self.stats_text.insert(tk.END, stats_report)
        self.stats_text.config(state='disabled')
            
        self.check_button.config(state='normal', text="🔍 Analyze Document")
        self.status_bar.config(text=f"Analysis complete - {score}% similarity | {len(self.results['matches'])} sources matched")
        
    
    def export_report(self, format_type='txt'):
        if not self.results:
            messagebox.showwarning("Warning", "No results to export")
            return
        
        filename = Path(self.current_file).stem if self.current_file else "analysis"
        
        if format_type == 'txt':
            filepath = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt")],
                initialfile=f"plagiarism_report_{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            )
            
            if filepath:
                document_name = Path(self.current_file).name if self.current_file else "Pasted Text"
                report = generate_advanced_report(self.results, document_name, self.selected_algorithms)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(report)
                messagebox.showinfo("Success", f"Report exported to:\n{filepath}")
        
        elif format_type == 'html':
            filepath = filedialog.asksaveasfilename(
                defaultextension=".html",
                filetypes=[("HTML Files", "*.html")],
                initialfile=f"plagiarism_report_{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            )
            
            if filepath:
                document_name = Path(self.current_file).name if self.current_file else "Pasted Text"
                report = generate_html_report(self.results, document_name, self.selected_algorithms)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(report)
                messagebox.showinfo("Success", f"HTML report exported to:\n{filepath}")   
    
    def refresh_database_view(self):
        self.db_tree.delete(*self.db_tree.get_children())
        self.database = self.db_manager.get_all_documents()
        
        for idx, doc in enumerate(self.database, 1):
            word_count = len(self.engine.tokenize(doc['text']))
            self.db_tree.insert('', 'end', text=str(idx),
                               values=(doc['source'], doc.get('category', 'General'), word_count))
        
        self.status_bar.config(text=f"Database: {len(self.database)} documents loaded")
    
    def add_to_database(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Document to Database")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Add Reference Document", 
                font=('Arial', 14, 'bold')).pack(pady=10)
        tk.Label(dialog, text="Source Name:").pack(anchor='w', padx=20)
        source_entry = tk.Entry(dialog, font=('Arial', 10), width=50)
        source_entry.pack(padx=20, pady=5)
        tk.Label(dialog, text="URL (optional):").pack(anchor='w', padx=20)
        url_entry = tk.Entry(dialog, font=('Arial', 10), width=50)
        url_entry.pack(padx=20, pady=5)
        tk.Label(dialog, text="Category:").pack(anchor='w', padx=20)
        category_var = tk.StringVar(value="General")
        category_combo = ttk.Combobox(dialog, textvariable=category_var, 
                                     values=["General", "Academic", "Technical", "Literature", "News"],
                                     width=47)
        category_combo.pack(padx=20, pady=5)
        tk.Label(dialog, text="Document Text:").pack(anchor='w', padx=20)
        text_widget = scrolledtext.ScrolledText(dialog, height=10, width=60)
        text_widget.pack(padx=20, pady=5)
        
        def save_document():
            source = source_entry.get().strip()
            url = url_entry.get().strip()
            text = text_widget.get(1.0, tk.END).strip()
            category = category_var.get()
            
            if not source or not text:
                messagebox.showwarning("Warning", "Source name and text are required")
                return
            
            if self.db_manager.add_document(source, text, url, category):
                messagebox.showinfo("Success", "Document added to database")
                self.refresh_database_view()
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Failed to add document (might be duplicate)")
        
        tk.Button(dialog, text="Save", command=save_document, bg='#48bb78', fg='white',
                 font=('Arial', 11, 'bold'), relief='flat', cursor='hand2',
                 padx=30, pady=10).pack(pady=10)
    
    def delete_from_database(self):
        selected = self.db_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a document to delete")
            return
        
        item = self.db_tree.item(selected[0])
        source = item['values'][0]
        
        if messagebox.askyesno("Confirm", f"Delete '{source}' from database?"):
            if self.db_manager.delete_document(source):
                messagebox.showinfo("Success", "Document deleted")
                self.refresh_database_view()
            else:
                messagebox.showerror("Error", "Failed to delete document")