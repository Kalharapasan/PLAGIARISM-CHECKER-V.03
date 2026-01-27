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
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        self.root.minsize(1400, 800)
    
    def _create_menubar(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="📁 Open Document", command=self.select_file, accelerator="Ctrl+O")
        file_menu.add_command(label="📂 Open Folder", command=self.select_folder)
        file_menu.add_command(label="📋 Paste Text", command=self.paste_text)
        file_menu.add_separator()
        file_menu.add_command(label="🔄 Batch Processing", command=lambda: self.notebook.select(1))
        file_menu.add_command(label="📊 Dashboard", command=lambda: self.notebook.select(4))
        file_menu.add_separator()
        export_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="📤 Export Report", menu=export_menu)
        export_menu.add_command(label="Text Report (.txt)", command=lambda: self.export_report('txt'))
        export_menu.add_command(label="HTML Report (.html)", command=lambda: self.export_report('html'))
        export_menu.add_command(label="PDF Report (.pdf)", command=lambda: self.export_report('pdf'))
        export_menu.add_command(label="JSON Data (.json)", command=lambda: self.export_report('json'))
        export_menu.add_command(label="Excel Summary (.xlsx)", command=lambda: self.export_report('excel'))
        
        file_menu.add_separator()
        file_menu.add_command(label="⚙️ Settings", command=self.open_settings)
        file_menu.add_command(label="📖 User Guide", command=self.show_user_guide)
        file_menu.add_separator()
        file_menu.add_command(label="🚪 Exit", command=self.root.quit)
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="✂️ Cut", accelerator="Ctrl+X")
        edit_menu.add_command(label="📋 Copy", accelerator="Ctrl+C")
        edit_menu.add_command(label="📄 Paste", accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="🔍 Find", accelerator="Ctrl+F")
        edit_menu.add_command(label="🔄 Replace", accelerator="Ctrl+H")
        edit_menu.add_separator()
        edit_menu.add_command(label="📝 Text Tools", command=self.open_text_tools)
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="👁️ Show Sidebar", command=self.toggle_sidebar)
        view_menu.add_command(label="📈 Show Analytics", command=self.toggle_analytics)
        view_menu.add_separator()
        theme_menu = tk.Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label="🎨 Theme", menu=theme_menu)
        theme_menu.add_command(label="🌞 Light Mode", command=lambda: self.switch_theme('light'))
        theme_menu.add_command(label="🌙 Dark Mode", command=lambda: self.switch_theme('dark'))
        theme_menu.add_command(label="🖥️ System Default", command=lambda: self.switch_theme('system'))
        
        view_menu.add_separator()
        view_menu.add_command(label="🔍 Zoom In", accelerator="Ctrl++")
        view_menu.add_command(label="🔍 Zoom Out", accelerator="Ctrl+-")
        view_menu.add_command(label="🔍 Reset Zoom", accelerator="Ctrl+0")
        db_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Database", menu=db_menu)
        db_menu.add_command(label="💾 Manage References", command=lambda: self.notebook.select(2))
        db_menu.add_command(label="➕ Add Document", command=self.add_to_database)
        db_menu.add_command(label="📥 Import", command=self.import_documents)
        db_menu.add_command(label="📤 Export", command=self.export_database)
        db_menu.add_separator()
        db_menu.add_command(label="🔍 Search", command=self.search_database)
        db_menu.add_command(label="📊 Statistics", command=self.show_db_stats)
        db_menu.add_command(label="🧹 Optimize", command=self.optimize_database)
        db_menu.add_command(label="💾 Backup", command=self.backup_database)
        analysis_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Analysis", menu=analysis_menu)
        analysis_menu.add_command(label="🔍 Quick Check", command=self.quick_check)
        analysis_menu.add_command(label="🔬 Deep Analysis", command=self.deep_analysis)
        analysis_menu.add_command(label="📈 Compare Documents", command=self.compare_documents)
        analysis_menu.add_separator()
        algo_menu = tk.Menu(analysis_menu, tearoff=0)
        analysis_menu.add_cascade(label="⚙️ Algorithms", menu=algo_menu)
        algo_menu.add_command(label="🧮 Configure", command=self.configure_algorithms)
        algo_menu.add_command(label="📊 Performance", command=self.show_algorithm_performance)
        
        analysis_menu.add_separator()
        analysis_menu.add_command(label="📊 Generate Report", command=self.generate_comprehensive_report)
        analysis_menu.add_command(label="📈 Create Visualizations", command=self.generate_visualizations)
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="📝 Text Analysis", command=self.text_analysis_tool)
        tools_menu.add_command(label="📚 Citation Checker", command=self.citation_checker)
        tools_menu.add_command(label="📖 Readability Analyzer", command=self.readability_analyzer)
        tools_menu.add_command(label="🎯 Paraphrase Detector", command=self.paraphrase_detector)
        tools_menu.add_separator()
        tools_menu.add_command(label="⚡ Performance Monitor", command=self.performance_monitor)
        tools_menu.add_command(label="🔒 Security Settings", command=self.security_settings)
        history_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="History", menu=history_menu)
        history_menu.add_command(label="📜 View History", command=lambda: self.notebook.select(3))
        history_menu.add_command(label="📊 Analytics", command=self.show_history_analytics)
        history_menu.add_command(label="📈 Trends", command=self.show_trends)
        history_menu.add_separator()
        history_menu.add_command(label="🧹 Clear History", command=self.clear_history)
        history_menu.add_command(label="💾 Export History", command=self.export_history)
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="📖 User Guide", command=self.show_user_guide)
        help_menu.add_command(label="🎓 Tutorial", command=self.show_tutorial)
        help_menu.add_command(label="🔧 API Documentation", command=self.show_api_docs)
        help_menu.add_separator()
        help_menu.add_command(label="📊 About Algorithms", command=self.show_algorithm_info)
        help_menu.add_command(label="⚙️ System Info", command=self.show_system_info)
        help_menu.add_separator()
        help_menu.add_command(label="🌟 Check for Updates", command=self.check_for_updates)
        help_menu.add_command(label="💬 Support", command=self.show_support)
        help_menu.add_command(label="📄 About", command=self.show_about)
        self.root.bind('<Control-o>', lambda e: self.select_file())
        self.root.bind('<Control-s>', lambda e: self.save_results())
        self.root.bind('<Control-e>', lambda e: self.export_report('txt'))
        self.root.bind('<F1>', lambda e: self.show_user_guide())
        self.root.bind('<F5>', lambda e: self.refresh_all())
    
    def _create_ui(self):
        self.main_container = tk.PanedWindow(self.root, orient='horizontal', sashwidth=5)
        self.main_container.pack(fill='both', expand=True)
        self.create_sidebar()
        self.content_frame = tk.Frame(self.main_container, bg='#f8f9fa')
        self.main_container.add(self.content_frame, width=1200)
        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        self.create_dashboard_tab()
        self.create_checker_tab()
        self.create_batch_tab()
        self.create_database_tab()
        self.create_history_tab()
        self.create_analytics_tab()
        self.create_settings_tab()
        self.create_status_bar()
    
    def create_sidebar(self):
        self.sidebar = tk.Frame(self.main_container, bg='#2d3748', width=200)
        self.main_container.add(self.sidebar, width=200)
        logo_frame = tk.Frame(self.sidebar, bg='#1a202c', height=80)
        logo_frame.pack(fill='x', pady=(0, 10))
        logo_frame.pack_propagate(False)
        
        tk.Label(logo_frame, text="🔍", font=('Segoe UI', 24), 
                bg='#1a202c', fg='#63b3ed').pack(pady=(20, 5))
        tk.Label(logo_frame, text="Plagiarism\nUltimate", 
                font=('Segoe UI', 10, 'bold'), bg='#1a202c', fg='white',
                justify='center').pack()
        actions_frame = tk.Frame(self.sidebar, bg='#2d3748')
        actions_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(actions_frame, text="QUICK ACTIONS", font=('Segoe UI', 9, 'bold'),
                bg='#2d3748', fg='#a0aec0', anchor='w').pack(fill='x', pady=(0, 10))
        
        self.create_sidebar_button(actions_frame, "📁 Open File", self.select_file)
        self.create_sidebar_button(actions_frame, "📋 Paste Text", self.paste_text)
        self.create_sidebar_button(actions_frame, "🔍 Quick Check", self.quick_check)
        self.create_sidebar_button(actions_frame, "📊 Dashboard", lambda: self.notebook.select(0))
        self.create_sidebar_button(actions_frame, "💾 Database", lambda: self.notebook.select(3))
        recent_frame = tk.Frame(self.sidebar, bg='#2d3748')
        recent_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(recent_frame, text="RECENT FILES", font=('Segoe UI', 9, 'bold'),
                bg='#2d3748', fg='#a0aec0', anchor='w').pack(fill='x', pady=(0, 10))
        
        self.recent_files_list = tk.Frame(recent_frame, bg='#2d3748')
        self.recent_files_list.pack(fill='x')
        self.load_recent_files()
        stats_frame = tk.Frame(self.sidebar, bg='#2d3748')
        stats_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(stats_frame, text="STATISTICS", font=('Segoe UI', 9, 'bold'),
                bg='#2d3748', fg='#a0aec0', anchor='w').pack(fill='x', pady=(0, 10))
        
        self.stats_labels = {}
        stats = [
            ("Documents", f"{len(self.database):,}"),
            ("Checks Today", "0"),
            ("Avg Similarity", "0%"),
            ("High Risk", "0")
        ]
        
        for label, value in stats:
            stat_frame = tk.Frame(stats_frame, bg='#2d3748')
            stat_frame.pack(fill='x', pady=2)
            
            tk.Label(stat_frame, text=label, font=('Segoe UI', 8),
                    bg='#2d3748', fg='#cbd5e0', anchor='w').pack(side='left')
            
            value_label = tk.Label(stat_frame, text=value, font=('Segoe UI', 9, 'bold'),
                                  bg='#2d3748', fg='#63b3ed', anchor='e')
            value_label.pack(side='right')
            self.stats_labels[label] = value_label
    
    def create_sidebar_button(self, parent, text, command):
        btn = tk.Button(parent, text=text, font=('Segoe UI', 10),
                       bg='#4a5568', fg='white', bd=0, padx=10, pady=8,
                       command=command, anchor='w', cursor='hand2',
                       activebackground='#2d3748', activeforeground='white')
        btn.pack(fill='x', pady=2)
        return btn

    
    def create_dashboard_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📊 Dashboard")
        header_frame = tk.Frame(tab, bg='#667eea', height=100)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="📊 Analytics Dashboard", 
                font=self.fonts['title'], bg='#667eea', fg='white').pack(pady=(25, 5))
        tk.Label(header_frame, text="Comprehensive overview and analytics", 
                font=self.fonts['subtitle'], bg='#667eea', fg='#e2e8f0').pack()
        stats_frame = tk.Frame(tab, bg='#f8f9fa')
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        self.dashboard_stats = {}
        stats_cards = [
            ("Total Checks", "0", "#4c51bf"),
            ("Avg Similarity", "0%", "#38a169"),
            ("High Risk", "0", "#e53e3e"),
            ("Database Size", f"{len(self.database)}", "#d69e2e"),
            ("Files Today", "0", "#3182ce"),
            ("Citations", "0", "#805ad5")
        ]
        
        for i, (title, value, color) in enumerate(stats_cards):
            card = tk.Frame(stats_frame, bg='white', relief='raised', bd=1)
            card.grid(row=0, column=i, padx=5, pady=5, sticky='nsew')
            stats_frame.columnconfigure(i, weight=1)
            
            tk.Label(card, text=title, font=('Segoe UI', 9),
                    bg='white', fg='#718096').pack(pady=(10, 5))
            
            value_label = tk.Label(card, text=value, font=('Segoe UI', 24, 'bold'),
                                  bg='white', fg=color)
            value_label.pack(pady=(0, 10))
            
            self.dashboard_stats[title] = value_label
        
        charts_frame = tk.Frame(tab, bg='#f8f9fa')
        charts_frame.pack(fill='both', expand=True, padx=20, pady=10)
        left_charts = tk.Frame(charts_frame, bg='#f8f9fa')
        left_charts.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        right_charts = tk.Frame(charts_frame, bg='#f8f9fa')
        right_charts.pack(side='right', fill='both', expand=True, padx=(10, 0))
        similarity_card = self.create_chart_card(left_charts, "Similarity Distribution")
        self.similarity_chart = tk.Frame(similarity_card, bg='white', height=200)
        self.similarity_chart.pack(fill='both', expand=True, padx=10, pady=10)
        risk_card = self.create_chart_card(left_charts, "Risk Level Distribution")
        self.risk_chart = tk.Frame(risk_card, bg='white', height=200)
        self.risk_chart.pack(fill='both', expand=True, padx=10, pady=10)
        algo_card = self.create_chart_card(right_charts, "Algorithm Performance")
        self.algo_chart = tk.Frame(algo_card, bg='white', height=200)
        self.algo_chart.pack(fill='both', expand=True, padx=10, pady=10)
        activity_card = self.create_chart_card(right_charts, "Recent Activity")
        self.activity_list = tk.Frame(activity_card, bg='white')
        self.activity_list.pack(fill='both', expand=True, padx=10, pady=10)
        actions_frame = tk.Frame(tab, bg='#f8f9fa')
        actions_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(actions_frame, text="Quick Actions", font=self.fonts['header'],
                bg='#f8f9fa', fg='#2d3748').pack(anchor='w', pady=(0, 10))
        
        action_buttons = [
            ("🔍 New Check", self.select_file),
            ("📊 Generate Report", self.generate_comprehensive_report),
            ("📈 View Analytics", self.show_history_analytics),
            ("⚙️ Settings", self.open_settings)
        ]
        
        for text, command in action_buttons:
            tk.Button(actions_frame, text=text, font=('Segoe UI', 10),
                     bg='#4299e1', fg='white', padx=20, pady=10,
                     command=command, cursor='hand2').pack(side='left', padx=5)
        self.load_dashboard_data()
    
    def create_chart_card(self, parent, title):
        card = tk.Frame(parent, bg='white', relief='raised', bd=1)
        card.pack(fill='both', expand=True, pady=(0, 10))
        
        tk.Label(card, text=title, font=('Segoe UI', 11, 'bold'),
                bg='white', fg='#2d3748').pack(anchor='w', padx=10, pady=10)
        
        return card

    def create_checker_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔍 Document Checker")
        main_paned = tk.PanedWindow(tab, orient='horizontal', sashwidth=5)
        main_paned.pack(fill='both', expand=True)
        left_panel = tk.Frame(main_paned, bg='white')
        main_paned.add(left_panel, width=400)
        self.create_input_section(left_panel)
        self.create_configuration_section(left_panel)
        right_panel = tk.Frame(main_paned, bg='#f8f9fa')
        main_paned.add(right_panel, width=800)
        results_header = tk.Frame(right_panel, bg='#667eea', height=60)
        results_header.pack(fill='x')
        results_header.pack_propagate(False)
        
        tk.Label(results_header, text="📊 Analysis Results", 
                font=self.fonts['header'], bg='#667eea', fg='white').pack(pady=15, padx=15, anchor='w')
        self.create_results_metrics(right_panel)
        results_notebook = ttk.Notebook(right_panel)
        results_notebook.pack(fill='both', expand=True, padx=10, pady=10)
        matches_tab = ttk.Frame(results_notebook)
        results_notebook.add(matches_tab, text="🔍 Matches")
        self.create_matches_section(matches_tab)
        stats_tab = ttk.Frame(results_notebook)
        results_notebook.add(stats_tab, text="📈 Statistics")
        self.create_statistics_section(stats_tab)
        details_tab = ttk.Frame(results_notebook)
        results_notebook.add(details_tab, text="📋 Details")
        self.create_details_section(details_tab)
        viz_tab = ttk.Frame(results_notebook)
        results_notebook.add(viz_tab, text="📊 Visualizations")
        self.create_visualization_section(viz_tab)
    
    def create_input_section(self, parent):
        input_frame = tk.LabelFrame(parent, text="📄 Document Input", 
                                   font=self.fonts['header'], bg='white', 
                                   fg='#2d3748', padx=15, pady=15)
        input_frame.pack(fill='x', padx=10, pady=10)
        upload_frame = tk.Frame(input_frame, bg='white')
        upload_frame.pack(fill='x', pady=(0, 15))
        
        self.file_label = tk.Label(upload_frame, text="No file selected", 
                                  font=self.fonts['normal'], bg='white', fg='#4a5568')
        self.file_label.pack(pady=(0, 10))
        btn_frame = tk.Frame(upload_frame, bg='white')
        btn_frame.pack()
        
        tk.Button(btn_frame, text="📁 Choose File", command=self.select_file,
                 bg='#4299e1', fg='white', font=('Segoe UI', 10, 'bold'),
                 relief='flat', cursor='hand2', padx=15, pady=8).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="📋 Paste", command=self.paste_text,
                 bg='#38a169', fg='white', font=('Segoe UI', 10, 'bold'),
                 relief='flat', cursor='hand2', padx=15, pady=8).pack(side='left', padx=5)
        tk.Label(upload_frame, text="Supported formats: DOCX, PDF, TXT, RTF, HTML, EPUB", 
                font=self.fonts['small'], bg='white', fg='#a0aec0').pack(pady=(10, 0))
        tk.Label(input_frame, text="Or enter text directly:", 
                font=self.fonts['normal'], bg='white', fg='#4a5568').pack(anchor='w', pady=(0, 5))
        
        self.text_input = scrolledtext.ScrolledText(input_frame, height=15, 
                                                   font=self.fonts['monospace'], 
                                                   wrap='word', bg='#f7fafc', 
                                                   fg='#2d3748', bd=1, relief='solid')
        self.text_input.pack(fill='both', expand=True)
        quick_frame = tk.Frame(input_frame, bg='white')
        quick_frame.pack(fill='x', pady=(10, 0))
        
        tk.Button(quick_frame, text="🔍 Quick Check", command=self.quick_check,
                 bg='#ed8936', fg='white', font=('Segoe UI', 10, 'bold'),
                 relief='flat', cursor='hand2').pack(side='left', padx=2)
        
        tk.Button(quick_frame, text="🔬 Deep Analysis", command=self.deep_analysis,
                 bg='#9f7aea', fg='white', font=('Segoe UI', 10, 'bold'),
                 relief='flat', cursor='hand2').pack(side='left', padx=2)
        self.analyze_button = tk.Button(input_frame, text="🚀 Run Ultimate Analysis", 
                                       bg='#48bb78', fg='white', font=('Segoe UI', 12, 'bold'),
                                       command=self.run_ultimate_check, cursor='hand2',
                                       relief='flat', padx=20, pady=12)
        self.analyze_button.pack(fill='x', pady=(15, 0))
    
    def create_configuration_section(self, parent):
        config_frame = tk.LabelFrame(parent, text="⚙️ Analysis Configuration", 
                                    font=self.fonts['header'], bg='white', 
                                    fg='#2d3748', padx=15, pady=15)
        config_frame.pack(fill='both', expand=True, padx=10, pady=10)
        algo_frame = tk.Frame(config_frame, bg='white')
        algo_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(algo_frame, text="Detection Algorithms:", 
                font=self.fonts['normal'], bg='white', fg='#4a5568').pack(anchor='w')
        algo_canvas = tk.Canvas(algo_frame, bg='white', height=150, highlightthickness=0)
        algo_scrollbar = tk.Scrollbar(algo_frame, orient='vertical', command=algo_canvas.yview)
        algo_scrollable_frame = tk.Frame(algo_canvas, bg='white')
        
        algo_scrollable_frame.bind(
            "<Configure>",
            lambda e: algo_canvas.configure(scrollregion=algo_canvas.bbox("all"))
        )
        
        algo_canvas.create_window((0, 0), window=algo_scrollable_frame, anchor="nw")
        algo_canvas.configure(yscrollcommand=algo_scrollbar.set)
        
        algo_canvas.pack(side="left", fill="both", expand=True)
        algo_scrollbar.pack(side="right", fill="y")
        self.algo_vars = {}
        algorithms = [
            ('cosine_tfidf', 'Cosine Similarity (TF-IDF)', 'Best for general comparison'),
            ('cosine_count', 'Cosine Similarity (Count)', 'Simple word frequency'),
            ('jaccard', 'Jaccard Index', 'Set-based similarity'),
            ('overlap', 'Overlap Coefficient', 'Subset detection'),
            ('dice', 'Dice Coefficient', 'Balanced comparison'),
            ('ngram_3', '3-gram Analysis', 'Pattern matching'),
            ('ngram_5', '5-gram Analysis', 'Detailed patterns'),
            ('sequence', 'Sequence Matching', 'Exact phrase detection'),
            ('semantic', 'Semantic Similarity', 'Meaning-based (ML)'),
            ('lsi', 'LSI Analysis', 'Latent semantic indexing')
        ]
        
        for algo_id, algo_name, algo_desc in algorithms:
            var = tk.BooleanVar(value=algo_id in self.selected_algorithms)
            self.algo_vars[algo_id] = var
            
            cb_frame = tk.Frame(algo_scrollable_frame, bg='white')
            cb_frame.pack(fill='x', pady=2)
            
            cb = tk.Checkbutton(cb_frame, text=algo_name, variable=var, 
                               bg='white', font=('Segoe UI', 9), anchor='w')
            cb.pack(side='left', padx=(0, 5))
            
            tk.Label(cb_frame, text=algo_desc, font=('Segoe UI', 8),
                    bg='white', fg='#a0aec0').pack(side='left')
        
        options_frame = tk.Frame(config_frame, bg='white')
        options_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(options_frame, text="Additional Analysis:", 
                font=self.fonts['normal'], bg='white', fg='#4a5568').pack(anchor='w', pady=(0, 5))
        
        self.analysis_vars = {
            'readability': tk.BooleanVar(value=self.config.get('detection.ultimate.enable_readability', True)),
            'citations': tk.BooleanVar(value=self.config.get('detection.ultimate.enable_citations', True)),
            'keyphrases': tk.BooleanVar(value=True),
            'structure': tk.BooleanVar(value=True),
            'paraphrasing': tk.BooleanVar(value=True)
        }
        
        for option, var in self.analysis_vars.items():
            cb = tk.Checkbutton(options_frame, text=option.replace('_', ' ').title(),
                               variable=var, bg='white', font=('Segoe UI', 9), anchor='w')
            cb.pack(anchor='w', pady=1)
        
        sensitivity_frame = tk.Frame(config_frame, bg='white')
        sensitivity_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(sensitivity_frame, text="Detection Sensitivity:", 
                font=self.fonts['normal'], bg='white', fg='#4a5568').pack(anchor='w')
        
        self.sensitivity_var = tk.DoubleVar(value=5.0)
        sensitivity_slider = tk.Scale(sensitivity_frame, from_=1, to=20, 
                                     orient='horizontal', variable=self.sensitivity_var,
                                     bg='white', fg='#2d3748', length=300)
        sensitivity_slider.pack(fill='x', pady=5)
        preset_frame = tk.Frame(config_frame, bg='white')
        preset_frame.pack(fill='x')
        
        tk.Button(preset_frame, text="🎓 Academic", command=self.set_academic_preset,
                 bg='#4299e1', fg='white', font=('Segoe UI', 9),
                 relief='flat', cursor='hand2').pack(side='left', padx=2)
        
        tk.Button(preset_frame, text="⚡ Fast", command=self.set_fast_preset,
                 bg='#38a169', fg='white', font=('Segoe UI', 9),
                 relief='flat', cursor='hand2').pack(side='left', padx=2)
        
        tk.Button(preset_frame, text="🔍 Thorough", command=self.set_thorough_preset,
                 bg='#ed8936', fg='white', font=('Segoe UI', 9),
                 relief='flat', cursor='hand2').pack(side='left', padx=2)
    
    
    def create_results_metrics(self, parent):
        metrics_frame = tk.Frame(parent, bg='#f8f9fa')
        metrics_frame.pack(fill='x', padx=10, pady=10)
        score_card = tk.Frame(metrics_frame, bg='white', relief='raised', bd=1)
        score_card.pack(side='left', fill='both', expand=True, padx=5)
        
        self.score_label = tk.Label(score_card, text="--", 
                                   font=('Segoe UI', 48, 'bold'), bg='white', fg='#718096')
        self.score_label.pack(pady=10)
        
        self.score_desc = tk.Label(score_card, text="Ready to analyze", 
                                  font=self.fonts['normal'], bg='white', fg='#718096')
        self.score_desc.pack(pady=(0, 10))
        self.metric_labels = {}
        stats = [
            ("Words", "0"),
            ("Matches", "0"),
            ("Sources", "0"),
            ("Risk", "--")
        ]
        
        for label, value in stats:
            stat_card = tk.Frame(metrics_frame, bg='white', relief='raised', bd=1)
            stat_card.pack(side='left', fill='both', expand=True, padx=5)
            
            value_label = tk.Label(stat_card, text=value, font=('Segoe UI', 24, 'bold'),
                                  bg='white', fg='#667eea')
            value_label.pack(pady=(15, 5))
            
            tk.Label(stat_card, text=label, font=self.fonts['small'],
                    bg='white', fg='#718096').pack(pady=(0, 15))
            
            self.metric_labels[label] = value_label
    
    def create_matches_section(self, parent):
        toolbar = tk.Frame(parent, bg='#f7fafc')
        toolbar.pack(fill='x', padx=10, pady=(10, 5))
        
        tk.Label(toolbar, text="Matched Sources", font=self.fonts['header'],
                bg='#f7fafc', fg='#2d3748').pack(side='left')
        
        tk.Button(toolbar, text="📋 Copy All", command=self.copy_all_matches,
                 bg='#4299e1', fg='white', font=('Segoe UI', 9),
                 relief='flat', cursor='hand2').pack(side='right', padx=5)
        
        tk.Button(toolbar, text="🔍 Filter", command=self.filter_matches,
                 bg='#38a169', fg='white', font=('Segoe UI', 9),
                 relief='flat', cursor='hand2').pack(side='right', padx=5)
        tree_frame = tk.Frame(parent, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        tree_scroll_y = tk.Scrollbar(tree_frame)
        tree_scroll_y.pack(side='right', fill='y')
        
        tree_scroll_x = tk.Scrollbar(tree_frame, orient='horizontal')
        tree_scroll_x.pack(side='bottom', fill='x')
        
        columns = ('#', 'Source', 'Similarity', 'Confidence', 'Risk', 'Sequences')
        self.matches_tree = ttk.Treeview(tree_frame, columns=columns, 
                                        show='headings', height=15,
                                        yscrollcommand=tree_scroll_y.set,
                                        xscrollcommand=tree_scroll_x.set)
        self.matches_tree.heading('#', text='#')
        self.matches_tree.heading('Source', text='Source')
        self.matches_tree.heading('Similarity', text='Similarity')
        self.matches_tree.heading('Confidence', text='Confidence')
        self.matches_tree.heading('Risk', text='Risk Level')
        self.matches_tree.heading('Sequences', text='Sequences')
        
        self.matches_tree.column('#', width=40, anchor='center')
        self.matches_tree.column('Source', width=250)
        self.matches_tree.column('Similarity', width=80, anchor='center')
        self.matches_tree.column('Confidence', width=100, anchor='center')
        self.matches_tree.column('Risk', width=100, anchor='center')
        self.matches_tree.column('Sequences', width=80, anchor='center')
        
        self.matches_tree.pack(side='left', fill='both', expand=True)
        
        tree_scroll_y.config(command=self.matches_tree.yview)
        tree_scroll_x.config(command=self.matches_tree.xview)
        self.matches_tree.bind('<Double-Button-1>', self.show_match_details)
    
    def create_statistics_section(self, parent):
        stats_notebook = ttk.Notebook(parent)
        stats_notebook.pack(fill='both', expand=True, padx=10, pady=10)
        basic_tab = ttk.Frame(stats_notebook)
        stats_notebook.add(basic_tab, text="Basic")
        
        self.basic_stats_text = scrolledtext.ScrolledText(basic_tab, 
                                                         font=self.fonts['monospace'],
                                                         wrap='word', state='disabled')
        self.basic_stats_text.pack(fill='both', expand=True)
        readability_tab = ttk.Frame(stats_notebook)
        stats_notebook.add(readability_tab, text="Readability")
        
        self.readability_text = scrolledtext.ScrolledText(readability_tab,
                                                         font=self.fonts['monospace'],
                                                         wrap='word', state='disabled')
        self.readability_text.pack(fill='both', expand=True)
        algo_tab = ttk.Frame(stats_notebook)
        stats_notebook.add(algo_tab, text="Algorithms")
        
        self.algorithm_text = scrolledtext.ScrolledText(algo_tab,
                                                       font=self.fonts['monospace'],
                                                       wrap='word', state='disabled')
        self.algorithm_text.pack(fill='both', expand=True)
    
    def create_details_section(self, parent):
        details_notebook = ttk.Notebook(parent)
        details_notebook.pack(fill='both', expand=True, padx=10, pady=10)
        text_tab = ttk.Frame(details_notebook)
        details_notebook.add(text_tab, text="Text Analysis")
        
        self.text_analysis_text = scrolledtext.ScrolledText(text_tab,
                                                           font=self.fonts['monospace'],
                                                           wrap='word', state='disabled')
        self.text_analysis_text.pack(fill='both', expand=True)
        citations_tab = ttk.Frame(details_notebook)
        details_notebook.add(citations_tab, text="Citations")
        
        self.citations_text = scrolledtext.ScrolledText(citations_tab,
                                                       font=self.fonts['monospace'],
                                                       wrap='word', state='disabled')
        self.citations_text.pack(fill='both', expand=True)
        phrases_tab = ttk.Frame(details_notebook)
        details_notebook.add(phrases_tab, text="Key Phrases")
        
        self.phrases_text = scrolledtext.ScrolledText(phrases_tab,
                                                     font=self.fonts['monospace'],
                                                     wrap='word', state='disabled')
        self.phrases_text.pack(fill='both', expand=True)
    
    def create_visualization_section(self, parent):
        viz_frame = tk.Frame(parent, bg='white')
        viz_frame.pack(fill='both', expand=True, padx=10, pady=10)
        viz_toolbar = tk.Frame(viz_frame, bg='#f7fafc')
        viz_toolbar.pack(fill='x', pady=(0, 10))
        
        tk.Label(viz_toolbar, text="Visualizations", font=self.fonts['header'],
                bg='#f7fafc', fg='#2d3748').pack(side='left')
        
        tk.Button(viz_toolbar, text="📈 Generate", command=self.generate_visualizations,
                 bg='#4299e1', fg='white', font=('Segoe UI', 9),
                 relief='flat', cursor='hand2').pack(side='right', padx=5)
        
        tk.Button(viz_toolbar, text="💾 Save", command=self.save_visualizations,
                 bg='#38a169', fg='white', font=('Segoe UI', 9),
                 relief='flat', cursor='hand2').pack(side='right', padx=5)
        self.viz_canvas = tk.Canvas(viz_frame, bg='white', highlightthickness=0)
        self.viz_canvas.pack(fill='both', expand=True)
        placeholder = tk.Label(self.viz_canvas, text="Visualizations will appear here\nClick 'Generate' to create charts",
                              font=self.fonts['normal'], bg='white', fg='#a0aec0')
        placeholder.place(relx=0.5, rely=0.5, anchor='center')
    
    def create_batch_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📦 Batch Processing")
        
        tk.Label(tab, text="🔄 Batch Document Processing", 
                font=self.fonts['title'], bg='#f8f9fa', fg='#2d3748').pack(pady=(20, 10))
        batch_container = tk.PanedWindow(tab, orient='horizontal')
        batch_container.pack(fill='both', expand=True, padx=20, pady=10)
        left_panel = tk.Frame(batch_container, bg='white', relief='raised', bd=1)
        batch_container.add(left_panel, width=400)
        tk.Label(left_panel, text="Selected Files", font=self.fonts['header'],
                bg='white', fg='#2d3748').pack(pady=15, padx=15, anchor='w')
        
        list_frame = tk.Frame(left_panel, bg='white')
        list_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        self.batch_listbox = tk.Listbox(list_frame, font=self.fonts['monospace'],
                                       selectmode='extended', bg='#f7fafc')
        self.batch_listbox.pack(side='left', fill='both', expand=True)
        
        list_scrollbar = tk.Scrollbar(list_frame, command=self.batch_listbox.yview)
        list_scrollbar.pack(side='right', fill='y')
        self.batch_listbox.config(yscrollcommand=list_scrollbar.set)
        file_buttons = tk.Frame(left_panel, bg='white')
        file_buttons.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Button(file_buttons, text="📁 Add Files", command=self.add_batch_files,
                 bg='#4299e1', fg='white', font=('Segoe UI', 10),
                 relief='flat', cursor='hand2').pack(side='left', padx=2)
        
        tk.Button(file_buttons, text="📂 Add Folder", command=self.add_batch_folder,
                 bg='#38a169', fg='white', font=('Segoe UI', 10),
                 relief='flat', cursor='hand2').pack(side='left', padx=2)
        
        tk.Button(file_buttons, text="🗑️ Remove", command=self.remove_batch_file,
                 bg='#e53e3e', fg='white', font=('Segoe UI', 10),
                 relief='flat', cursor='hand2').pack(side='left', padx=2)
        
        tk.Button(file_buttons, text="🧹 Clear All", command=self.clear_batch_files,
                 bg='#a0aec0', fg='white', font=('Segoe UI', 10),
                 relief='flat', cursor='hand2').pack(side='left', padx=2)
        right_panel = tk.Frame(batch_container, bg='white', relief='raised', bd=1)
        batch_container.add(right_panel, width=400)
        tk.Label(right_panel, text="Configuration", font=self.fonts['header'],
                bg='white', fg='#2d3748').pack(pady=15, padx=15, anchor='w')
        
        config_frame = tk.Frame(right_panel, bg='white')
        config_frame.pack(fill='x', padx=15, pady=(0, 15))
        tk.Label(config_frame, text="Output Directory:", 
                font=self.fonts['normal'], bg='white', fg='#4a5568').pack(anchor='w', pady=(0, 5))
        
        output_frame = tk.Frame(config_frame, bg='white')
        output_frame.pack(fill='x', pady=(0, 10))
        
        self.output_dir_var = tk.StringVar(value="batch_reports")
        output_entry = tk.Entry(output_frame, textvariable=self.output_dir_var,
                               font=self.fonts['normal'], bg='#f7fafc')
        output_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        tk.Button(output_frame, text="📁", command=self.choose_output_dir,
                 bg='#a0aec0', fg='white', font=('Segoe UI', 10),
                 relief='flat', cursor='hand2').pack(side='right')
        tk.Label(config_frame, text="Report Format:", 
                font=self.fonts['normal'], bg='white', fg='#4a5568').pack(anchor='w', pady=(0, 5))
        
        self.report_format_var = tk.StringVar(value="html")
        format_frame = tk.Frame(config_frame, bg='white')
        format_frame.pack(fill='x', pady=(0, 10))
        
        formats = [("Text", "txt"), ("HTML", "html"), ("PDF", "pdf"), ("All", "all")]
        for text, value in formats:
            rb = tk.Radiobutton(format_frame, text=text, value=value,
                               variable=self.report_format_var, bg='white',
                               font=self.fonts['small'])
            rb.pack(side='left', padx=5)
        
        options_frame = tk.Frame(right_panel, bg='white')
        options_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        self.batch_options = {
            'skip_errors': tk.BooleanVar(value=True),
            'generate_summary': tk.BooleanVar(value=True),
            'save_to_history': tk.BooleanVar(value=True),
            'use_multithreading': tk.BooleanVar(value=True)
        }
        
        for option, var in self.batch_options.items():
            cb = tk.Checkbutton(options_frame, text=option.replace('_', ' ').title(),
                               variable=var, bg='white', font=self.fonts['small'], anchor='w')
            cb.pack(anchor='w', pady=2)
        
        progress_frame = tk.Frame(right_panel, bg='white')
        progress_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Label(progress_frame, text="Progress", font=self.fonts['header'],
                bg='white', fg='#2d3748').pack(anchor='w', pady=(0, 10))
        
        self.batch_progress = ttk.Progressbar(progress_frame, mode='determinate')
        self.batch_progress.pack(fill='x', pady=(0, 5))
        
        self.progress_label = tk.Label(progress_frame, text="Ready", 
                                      font=self.fonts['small'], bg='white', fg='#4a5568')
        self.progress_label.pack()
        
        self.time_label = tk.Label(progress_frame, text="Estimated time: --", 
                                  font=self.fonts['small'], bg='white', fg='#a0aec0')
        self.time_label.pack()
        control_frame = tk.Frame(right_panel, bg='white')
        control_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Button(control_frame, text="🚀 Start Processing", command=self.process_batch,
                 bg='#48bb78', fg='white', font=('Segoe UI', 12, 'bold'),
                 relief='flat', cursor='hand2', padx=20, pady=10).pack(fill='x')
        
        tk.Button(control_frame, text="⏸️ Pause", command=self.pause_batch,
                 bg='#ed8936', fg='white', font=('Segoe UI', 10),
                 relief='flat', cursor='hand2').pack(side='left', padx=2, pady=5)
        
        tk.Button(control_frame, text="⏹️ Stop", command=self.stop_batch,
                 bg='#e53e3e', fg='white', font=('Segoe UI', 10),
                 relief='flat', cursor='hand2').pack(side='right', padx=2, pady=5)
    
    def create_database_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="💾 Database")
        
        tk.Label(tab, text="📚 Reference Database Management", 
                font=self.fonts['title'], bg='#f8f9fa', fg='#2d3748').pack(pady=(20, 10))
        db_container = tk.PanedWindow(tab, orient='horizontal')
        db_container.pack(fill='both', expand=True, padx=20, pady=10)
        left_panel = tk.Frame(db_container, bg='white', relief='raised', bd=1)
        db_container.add(left_panel, width=600)
        toolbar = tk.Frame(left_panel, bg='#f7fafc', height=50)
        toolbar.pack(fill='x')
        toolbar.pack_propagate(False)
        
        tk.Label(toolbar, text="Documents", font=self.fonts['header'],
                bg='#f7fafc', fg='#2d3748').pack(side='left', padx=15, pady=15)
        
        search_frame = tk.Frame(toolbar, bg='#f7fafc')
        search_frame.pack(side='right', padx=15, pady=10)
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                               font=self.fonts['normal'], width=30, bg='white')
        search_entry.pack(side='left', padx=(0, 5))
        search_entry.bind('<Return>', lambda e: self.search_database())
        
        tk.Button(search_frame, text="🔍", command=self.search_database,
                 bg='#4299e1', fg='white', font=('Segoe UI', 10),
                 relief='flat', cursor='hand2').pack(side='right')
        tree_frame = tk.Frame(left_panel, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        columns = ('ID', 'Source', 'Category', 'Words', 'Added', 'URL')
        self.db_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.db_tree.heading(col, text=col)
            self.db_tree.column(col, width=100)
        
        self.db_tree.column('ID', width=50)
        self.db_tree.column('Source', width=200)
        self.db_tree.column('Category', width=100)
        self.db_tree.column('Words', width=80)
        self.db_tree.column('Added', width=120)
        self.db_tree.column('URL', width=150)
        
        self.db_tree.pack(side='left', fill='both', expand=True)
        
        tree_scrollbar = tk.Scrollbar(tree_frame, command=self.db_tree.yview)
        tree_scrollbar.pack(side='right', fill='y')
        self.db_tree.config(yscrollcommand=tree_scrollbar.set)
        right_panel = tk.Frame(db_container, bg='white', relief='raised', bd=1)
        db_container.add(right_panel, width=400)
        tk.Label(right_panel, text="Document Details", font=self.fonts['header'],
                bg='white', fg='#2d3748').pack(pady=15, padx=15, anchor='w')
        
        self.doc_details = {}
        details_frame = tk.Frame(right_panel, bg='white')
        details_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        fields = ['Source', 'Category', 'URL', 'Words', 'Added', 'Content']
        for field in fields:
            frame = tk.Frame(details_frame, bg='white')
            frame.pack(fill='x', pady=2)
            
            tk.Label(frame, text=f"{field}:", font=self.fonts['normal'],
                    bg='white', fg='#4a5568', width=10, anchor='w').pack(side='left')
            
            if field == 'Content':
                text_widget = scrolledtext.ScrolledText(frame, height=10,
                                                       font=self.fonts['small'],
                                                       wrap='word', state='disabled')
                text_widget.pack(side='left', fill='both', expand=True)
                self.doc_details[field] = text_widget
            else:
                label = tk.Label(frame, text="", font=self.fonts['normal'],
                                bg='white', fg='#2d3748', anchor='w')
                label.pack(side='left', fill='x', expand=True)
                self.doc_details[field] = label
        control_frame = tk.Frame(right_panel, bg='white')
        control_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Button(control_frame, text="➕ Add Document", command=self.add_to_database,
                 bg='#48bb78', fg='white', font=('Segoe UI', 10, 'bold'),
                 relief='flat', cursor='hand2').pack(fill='x', pady=2)
        
        tk.Button(control_frame, text="✏️ Edit Selected", command=self.edit_document,
                 bg='#4299e1', fg='white', font=('Segoe UI', 10),
                 relief='flat', cursor='hand2').pack(fill='x', pady=2)
        
        tk.Button(control_frame, text="🗑️ Delete Selected", command=self.delete_from_database,
                 bg='#e53e3e', fg='white', font=('Segoe UI', 10),
                 relief='flat', cursor='hand2').pack(fill='x', pady=2)
        
        tk.Button(control_frame, text="📥 Import", command=self.import_documents,
                 bg='#9f7aea', fg='white', font=('Segoe UI', 10),
                 relief='flat', cursor='hand2').pack(fill='x', pady=2)
        
        tk.Button(control_frame, text="📤 Export", command=self.export_database,
                 bg='#ed8936', fg='white', font=('Segoe UI', 10),
                 relief='flat', cursor='hand2').pack(fill='x', pady=2)
        self.refresh_database_view()
        self.db_tree.bind('<<TreeviewSelect>>', self.on_document_select)
    
    def create_history_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📜 History")
        
        tk.Label(tab, text="📊 Check History & Analytics", 
                font=self.fonts['title'], bg='#f8f9fa', fg='#2d3748').pack(pady=(20, 10))
        history_container = tk.PanedWindow(tab, orient='horizontal')
        history_container.pack(fill='both', expand=True, padx=20, pady=10)
        left_panel = tk.Frame(history_container, bg='white', relief='raised', bd=1)
        history_container.add(left_panel, width=600)
        toolbar = tk.Frame(left_panel, bg='#f7fafc', height=50)
        toolbar.pack(fill='x')
        toolbar.pack_propagate(False)
        
        tk.Label(toolbar, text="Check History", font=self.fonts['header'],
                bg='#f7fafc', fg='#2d3748').pack(side='left', padx=15, pady=15)
        filter_frame = tk.Frame(toolbar, bg='#f7fafc')
        filter_frame.pack(side='right', padx=15, pady=10)
        
        self.filter_var = tk.StringVar(value="all")
        filter_menu = ttk.Combobox(filter_frame, textvariable=self.filter_var,
                                  values=["All", "Today", "This Week", "This Month", "High Risk"],
                                  width=15, state='readonly')
        filter_menu.pack(side='left', padx=(0, 5))
        filter_menu.bind('<<ComboboxSelected>>', lambda e: self.filter_history())
        
        tk.Button(filter_frame, text="🔄 Refresh", command=self.refresh_history,
                 bg='#4299e1', fg='white', font=('Segoe UI', 10),
                 relief='flat', cursor='hand2').pack(side='right', padx=2)
        tree_frame = tk.Frame(left_panel, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        columns = ('Date', 'File', 'Score', 'Words', 'Sources', 'Risk', 'Report')
        self.history_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.history_tree.heading(col, text=col)
        
        self.history_tree.column('Date', width=150)
        self.history_tree.column('File', width=200)
        self.history_tree.column('Score', width=80)
        self.history_tree.column('Words', width=80)
        self.history_tree.column('Sources', width=80)
        self.history_tree.column('Risk', width=80)
        self.history_tree.column('Report', width=100)
        
        self.history_tree.pack(side='left', fill='both', expand=True)
        
        tree_scrollbar = tk.Scrollbar(tree_frame, command=self.history_tree.yview)
        tree_scrollbar.pack(side='right', fill='y')
        self.history_tree.config(yscrollcommand=tree_scrollbar.set)
        self.history_tree.bind('<Double-Button-1>', self.open_history_report)
        right_panel = tk.Frame(history_container, bg='white', relief='raised', bd=1)
        history_container.add(right_panel, width=400)
        tk.Label(right_panel, text="History Details", font=self.fonts['header'],
                bg='white', fg='#2d3748').pack(pady=15, padx=15, anchor='w')
        
        self.history_details = {}
        details_frame = tk.Frame(right_panel, bg='white')
        details_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        detail_fields = ['Date', 'File', 'Score', 'Words', 'Sources', 'Risk', 'Algorithms']
        for field in detail_fields:
            frame = tk.Frame(details_frame, bg='white')
            frame.pack(fill='x', pady=2)
            
            tk.Label(frame, text=f"{field}:", font=self.fonts['normal'],
                    bg='white', fg='#4a5568', width=10, anchor='w').pack(side='left')
            
            label = tk.Label(frame, text="", font=self.fonts['normal'],
                            bg='white', fg='#2d3748', anchor='w')
            label.pack(side='left', fill='x', expand=True)
            self.history_details[field] = label
        
        analytics_frame = tk.Frame(right_panel, bg='white')
        analytics_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Label(analytics_frame, text="Analytics Summary", font=self.fonts['header'],
                bg='white', fg='#2d3748').pack(anchor='w', pady=(0, 10))
        
        self.analytics_labels = {}
        analytics_data = [
            ("Total Checks", "0"),
            ("Average Score", "0%"),
            ("High Risk", "0"),
            ("Most Checked", "--")
        ]
        
        for label, value in analytics_data:
            frame = tk.Frame(analytics_frame, bg='white')
            frame.pack(fill='x', pady=2)
            
            tk.Label(frame, text=label, font=self.fonts['normal'],
                    bg='white', fg='#4a5568').pack(side='left')
            
            value_label = tk.Label(frame, text=value, font=self.fonts['normal'],
                                  bg='white', fg='#667eea')
            value_label.pack(side='right')
            self.analytics_labels[label] = value_label
        
        control_frame = tk.Frame(right_panel, bg='white')
        control_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Button(control_frame, text="📊 View Analytics", command=self.show_history_analytics,
                 bg='#9f7aea', fg='white', font=('Segoe UI', 10),
                 relief='flat', cursor='hand2').pack(fill='x', pady=2)
        
        tk.Button(control_frame, text="📈 View Trends", command=self.show_trends,
                 bg='#ed8936', fg='white', font=('Segoe UI', 10),
                 relief='flat', cursor='hand2').pack(fill='x', pady=2)
        
        tk.Button(control_frame, text="📋 Export History", command=self.export_history,
                 bg='#4299e1', fg='white', font=('Segoe UI', 10),
                 relief='flat', cursor='hand2').pack(fill='x', pady=2)
        
        tk.Button(control_frame, text="🧹 Clear History", command=self.clear_history,
                 bg='#e53e3e', fg='white', font=('Segoe UI', 10),
                 relief='flat', cursor='hand2').pack(fill='x', pady=2)
        self.refresh_history()
        self.history_tree.bind('<<TreeviewSelect>>', self.on_history_select)
    
    def create_analytics_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📈 Analytics")
        
        tk.Label(tab, text="📊 Advanced Analytics", 
                font=self.fonts['title'], bg='#f8f9fa', fg='#2d3748').pack(pady=(20, 10))
        analytics_notebook = ttk.Notebook(tab)
        analytics_notebook.pack(fill='both', expand=True, padx=20, pady=10)
        overview_tab = ttk.Frame(analytics_notebook)
        analytics_notebook.add(overview_tab, text="Overview")
        trends_tab = ttk.Frame(analytics_notebook)
        analytics_notebook.add(trends_tab, text="Trends")
        performance_tab = ttk.Frame(analytics_notebook)
        analytics_notebook.add(performance_tab, text="Performance")
        stats_tab = ttk.Frame(analytics_notebook)
        analytics_notebook.add(stats_tab, text="Statistics")
    
    def create_settings_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="⚙️ Settings")
        
        tk.Label(tab, text="⚙️ Application Settings", 
                font=self.fonts['title'], bg='#f8f9fa', fg='#2d3748').pack(pady=(20, 10))
        settings_notebook = ttk.Notebook(tab)
        settings_notebook.pack(fill='both', expand=True, padx=20, pady=10)
        general_tab = ttk.Frame(settings_notebook)
        settings_notebook.add(general_tab, text="General")
        analysis_tab = ttk.Frame(settings_notebook)
        settings_notebook.add(analysis_tab, text="Analysis")
        database_tab = ttk.Frame(settings_notebook)
        settings_notebook.add(database_tab, text="Database")
        ui_tab = ttk.Frame(settings_notebook)
        settings_notebook.add(ui_tab, text="Interface") 
        performance_tab = ttk.Frame(settings_notebook)
        settings_notebook.add(performance_tab, text="Performance")
        advanced_tab = ttk.Frame(settings_notebook)
        settings_notebook.add(advanced_tab, text="Advanced")
    
    def create_status_bar(self):
        self.status_bar = tk.Frame(self.root, bg='#2d3748', height=25)
        self.status_bar.pack(side='bottom', fill='x')
        self.status_bar.pack_propagate(False)
        self.status_label = tk.Label(self.status_bar, text="Ready", 
                                    font=self.fonts['small'], bg='#2d3748', fg='#e2e8f0')
        self.status_label.pack(side='left', padx=10)
        sysinfo_frame = tk.Frame(self.status_bar, bg='#2d3748')
        sysinfo_frame.pack(side='right', padx=10)
        self.db_label = tk.Label(sysinfo_frame, text=f"DB: {len(self.database)} docs", 
                                font=self.fonts['small'], bg='#2d3748', fg='#a0aec0')
        self.db_label.pack(side='right', padx=5)
        self.memory_label = tk.Label(sysinfo_frame, text="Memory: --", 
                                    font=self.fonts['small'], bg='#2d3748', fg='#a0aec0')
        self.memory_label.pack(side='right', padx=5)
        self.update_memory_usage()
    
    def _apply_theme(self):
        if self.current_theme == 'dark':
            self.apply_dark_theme()
        else:
            self.apply_light_theme()
            
    def apply_light_theme(self):
        self.dark_mode = False
        self.current_theme = 'light'
        colors = {
            'bg': '#f8f9fa',
            'fg': '#2d3748',
            'card_bg': 'white',
            'sidebar_bg': '#2d3748',
            'sidebar_fg': 'white',
            'status_bg': '#2d3748',
            'status_fg': '#e2e8f0'
        }
        self.root.configure(bg=colors['bg'])
    
    def apply_dark_theme(self):
        self.dark_mode = True
        self.current_theme = 'dark'
        colors = {
            'bg': '#1a202c',
            'fg': '#e2e8f0',
            'card_bg': '#2d3748',
            'sidebar_bg': '#1a202c',
            'sidebar_fg': '#e2e8f0',
            'status_bg': '#1a202c',
            'status_fg': '#a0aec0'
        }
        self.root.configure(bg=colors['bg'])
    
    def _center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def select_file(self):
        filetypes = [
            ('All Supported', '*.txt *.docx *.pdf *.rtf *.html *.htm *.md *.tex *.odt *.epub'),
            ('Text Files', '*.txt'),
            ('Word Documents', '*.docx'),
            ('PDF Files', '*.pdf'),
            ('Rich Text', '*.rtf'),
            ('HTML Files', '*.html *.htm'),
            ('Markdown', '*.md'),
            ('LaTeX', '*.tex'),
            ('OpenDocument', '*.odt'),
            ('EPUB', '*.epub')
        ]
        
        filename = filedialog.askopenfilename(title="Select Document", filetypes=filetypes)
        
        if filename:
            self.current_file = filename
            self.file_label.config(text=f"📎 {Path(filename).name}")
            self.text_input.delete(1.0, tk.END)
            self.status_label.config(text=f"File selected: {Path(filename).name}")
            self.add_to_recent_files(filename)
    
    def select_folder(self):
        folder = filedialog.askdirectory(title="Select Folder")
        if folder:
            self.add_batch_folder(folder)
    
    def paste_text(self):
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append("")  
            text = self.root.clipboard_get()
            
            if text and len(text) > 10: 
                self.text_input.delete(1.0, tk.END)
                self.text_input.insert(1.0, text)
                self.current_file = None
                self.file_label.config(text="📋 Pasted Text")
                self.status_label.config(text="Text pasted from clipboard")
            else:
                messagebox.showinfo("Info", "Clipboard is empty or text is too short")
        except:
            messagebox.showerror("Error", "Could not access clipboard")
    
    def run_ultimate_check(self):
        self.selected_algorithms = [algo for algo, var in self.algo_vars.items() if var.get()]
        
        if not self.selected_algorithms:
            messagebox.showwarning("Warning", "Please select at least one detection algorithm")
            return

        if self.current_file:
            self.status_label.config(text="Extracting text...")
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
        self.analyze_button.config(state='disabled', text="⏳ Running Ultimate Analysis...")
        self.status_label.config(text="Running comprehensive analysis with all selected algorithms...")
        thread = threading.Thread(target=self.perform_ultimate_check)
        thread.daemon = True
        thread.start()
    
    def perform_ultimate_check(self):
        try:
            self.engine.enable_readability = self.analysis_vars['readability'].get()
            self.engine.enable_nlp = any([self.analysis_vars['keyphrases'].get(),
                                         self.analysis_vars['structure'].get(),
                                         self.analysis_vars['paraphrasing'].get()])
            results = self.engine.analyze_comprehensive(
                self.current_text, 
                self.database,
                self.selected_algorithms
            )
            self.results = results
            self.root.after(0, self.display_ultimate_results)
            filename = Path(self.current_file).name if self.current_file else "Pasted Text"
            self.db_manager.save_check_history(filename, results)
            self.root.after(0, self.update_dashboard_stats)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Analysis failed: {str(e)}"))
            self.root.after(0, lambda: self.analyze_button.config(state='normal', text="🚀 Run Ultimate Analysis"))
    
    def display_ultimate_results(self):
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
        stats = self.results.get('statistics', {})
        self.metric_labels['Words'].config(text=str(self.results['total_words']))
        self.metric_labels['Matches'].config(text=str(stats.get('matched_words', 0)))
        self.metric_labels['Sources'].config(text=str(len(self.results['matches'])))
        self.metric_labels['Risk'].config(text=self._get_overall_risk_level(score))
        self.update_matches_tree()
        self.update_statistics_tabs()
        self.update_details_tabs()
        self.analyze_button.config(state='normal', text="🚀 Run Ultimate Analysis")
        self.status_label.config(text=f"Analysis complete - {score}% similarity | {len(self.results['matches'])} sources matched")
        self.notebook.select(1)
    
    def update_matches_tree(self):
        for item in self.matches_tree.get_children():
            self.matches_tree.delete(item)
        for idx, match in enumerate(self.results['matches'], 1):
            values = (
                idx,
                match['source'][:50] + '...' if len(match['source']) > 50 else match['source'],
                f"{match['similarity']}%",
                match.get('confidence', 'N/A'),
                match.get('risk_level', 'N/A'),
                match.get('total_sequences', 0)
            )
            self.matches_tree.insert('', 'end', values=values, iid=str(idx))
    
    def update_statistics_tabs(self):
        self.basic_stats_text.config(state='normal')
        self.basic_stats_text.delete(1.0, tk.END)
        
        stats = self.results.get('statistics', {})
        basic_stats = f"""BASIC STATISTICS
{'='*60}

Document Analysis:
  Total Words: {self.results['total_words']}
  Total Sentences: {self.results['total_sentences']}
  Total Characters: {self.results.get('total_characters', 0)}
  
Similarity Analysis:
  Overall Similarity: {self.results['overall_similarity']}%
  Matched Words: {stats.get('matched_words', 0)}
  Unique Words: {stats.get('unique_words', 0)}
  Unique Percentage: {stats.get('unique_percentage', 0)}%
  
Match Analysis:
  Sources Found: {len(self.results['matches'])}
  High Risk Sources: {stats.get('high_risk_sources', 0)}
  Total Sequences: {stats.get('total_sequences', 0)}
  Average Sequence Length: {stats.get('average_sequence_length', 0)} words
  Longest Sequence: {stats.get('longest_sequence', 0)} words
  
Citation Analysis:
  Citations Detected: {self.results.get('citations_found', 0)}
  Citation Density: {stats.get('citation_density', 0)} citations/sentence
"""
        self.basic_stats_text.insert(1.0, basic_stats)
        self.basic_stats_text.config(state='disabled')
        
        if 'readability' in self.results:
            self.readability_text.config(state='normal')
            self.readability_text.delete(1.0, tk.END)
            
            readability = self.results['readability']
            readability_stats = f"""READABILITY ANALYSIS
{'='*60}

Scores:
  Flesch Reading Ease: {readability.get('flesch_reading_ease', 0)} (0-100, higher is easier)
  Flesch-Kincaid Grade Level: {readability.get('flesch_kincaid_grade', 0)} (U.S. grade level)
  Gunning Fog Index: {readability.get('gunning_fog_index', 0)} (years of education)
  SMOG Index: {readability.get('smog_index', 0)} (years of education)
  Coleman-Liau Index: {readability.get('coleman_liau_index', 0)} (U.S. grade level)
  Automated Readability Index: {readability.get('automated_readability_index', 0)} (U.S. grade level)
  Dale-Chall Score: {readability.get('dale_chall_score', 0)} (U.S. grade level)

Interpretation:
  • Reading Ease {readability.get('flesch_reading_ease', 0)}: {'Very easy' if readability.get('flesch_reading_ease', 0) > 80 else 'Easy' if readability.get('flesch_reading_ease', 0) > 60 else 'Standard' if readability.get('flesch_reading_ease', 0) > 40 else 'Difficult' if readability.get('flesch_reading_ease', 0) > 20 else 'Very difficult'}
  • Average Grade Level: {readability.get('flesch_kincaid_grade', 0)}
  • Complex Words: {readability.get('complex_word_percentage', 0)}%

Document Metrics:
  Average Sentence Length: {readability.get('avg_sentence_length', 0)} words
  Average Syllables per Word: {readability.get('avg_syllables_per_word', 0)}
  Total Syllables: {readability.get('total_syllables', 0)}
"""
            self.readability_text.insert(1.0, readability_stats)
            self.readability_text.config(state='disabled')
            
            if 'algorithm_scores' in self.results:
                self.algorithm_text.config(state='normal')
                self.algorithm_text.delete(1.0, tk.END)
                
                algo_stats = f"""ALGORITHM PERFORMANCE
{'='*60}

Algorithms Used: {', '.join(self.results.get('metadata', {}).get('algorithms_used', []))}

Performance Summary:
"""
            for algo, perf in self.results['algorithm_scores'].items():
                algo_stats += f"  {algo.upper()}: {perf.get('average', 0):.2f}% (avg), {perf.get('max', 0):.2f}% (max), {perf.get('min', 0):.2f}% (min)\n"
            
            self.algorithm_text.insert(1.0, algo_stats)
            self.algorithm_text.config(state='disabled')

    def update_details_tabs(self):
        self.text_analysis_text.config(state='normal')
        self.text_analysis_text.delete(1.0, tk.END)
        if self.current_text:
            text_stats = self.analyzer.generate_text_statistics(self.current_text)
            
            analysis_text = f"""TEXT ANALYSIS DETAILS
{'='*60}

Document Structure:
  Paragraphs: {text_stats['basic_statistics']['total_paragraphs']}
  Sentences: {text_stats['basic_statistics']['total_sentences']}
  Words: {text_stats['basic_statistics']['total_words']}
  Characters: {text_stats['basic_statistics']['total_characters']}
  Unique Words: {text_stats['basic_statistics']['unique_words']}

Character Distribution:
  Alphabetic: {text_stats['basic_statistics']['character_distribution']['alphabetic']}
  Numeric: {text_stats['basic_statistics']['character_distribution']['numeric']}
  Spaces: {text_stats['basic_statistics']['character_distribution']['spaces']}
  Punctuation: {text_stats['basic_statistics']['character_distribution']['punctuation']}
  Other: {text_stats['basic_statistics']['character_distribution']['other']}

Averages:
  Word Length: {text_stats['averages']['avg_word_length']} characters
  Sentence Length: {text_stats['averages']['avg_sentence_length']} words
  Paragraph Length: {text_stats['averages']['avg_paragraph_length']} words
  Words per Sentence: {text_stats['averages']['words_per_sentence']}
  Sentences per Paragraph: {text_stats['averages']['sentences_per_paragraph']}

Vocabulary:
  Type-Token Ratio: {text_stats['writing_style'].get('type_token_ratio', 0):.4f}
  Vocabulary Richness: {text_stats['writing_style'].get('vocabulary_richness', 0):.4f}
"""
            self.text_analysis_text.insert(1.0, analysis_text)
        
        self.text_analysis_text.config(state='disabled')
        
        self.citations_text.config(state='normal')
        self.citations_text.delete(1.0, tk.END)
        
        citations_text = f"""CITATION ANALYSIS
{'='*60}

Total Citations Found: {self.results.get('citations_found', 0)}

Citation Types:
"""
        if 'advanced_citations' in self.results:
            citations = self.results['advanced_citations']
            for i, citation in enumerate(citations[:10], 1):
                citations_text += f"\n{i}. {citation['text']}"
                citations_text += f"\n   Type: {citation['type']}, Author: {citation.get('author', 'N/A')}"
        
        self.citations_text.insert(1.0, citations_text)
        self.citations_text.config(state='disabled')
        self.phrases_text.config(state='normal')
        self.phrases_text.delete(1.0, tk.END)
        
        phrases_text = f"""KEY PHRASE EXTRACTION
{'='*60}

Top Key Phrases:
"""
        if 'key_phrases' in self.results:
            for phrase, freq, score in self.results['key_phrases']:
                phrases_text += f"\n• {phrase} (Frequency: {freq}, Score: {score})"
        
        self.phrases_text.insert(1.0, phrases_text)
        self.phrases_text.config(state='disabled')
        
    def generate_visualizations(self):
        if not self.results:
            messagebox.showinfo("Info", "Please run an analysis first")
            return

        try:
            for widget in self.viz_canvas.winfo_children():
                widget.destroy()
            import matplotlib.pyplot as plt
            from matplotlib.figure import Figure
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            fig = Figure(figsize=(10, 6), dpi=100)
            ax1 = fig.add_subplot(221)
            similarities = [m['similarity'] for m in self.results['matches']]
            if similarities:
                ax1.hist(similarities, bins=10, color='skyblue', edgecolor='black')
                ax1.set_title('Similarity Distribution')
                ax1.set_xlabel('Similarity (%)')
                ax1.set_ylabel('Frequency')
            ax2 = fig.add_subplot(222)
            risk_levels = [m.get('risk_level', 'Unknown') for m in self.results['matches']]
            if risk_levels:
                risk_counts = {}
                for risk in risk_levels:
                    risk_counts[risk] = risk_counts.get(risk, 0) + 1
                
                ax2.bar(risk_counts.keys(), risk_counts.values(), color=['#48bb78', '#ed8936', '#f56565', '#a0aec0'])
                ax2.set_title('Risk Level Distribution')
                ax2.set_ylabel('Count')
            ax3 = fig.add_subplot(223)
            if 'algorithm_scores' in self.results:
                algorithms = list(self.results['algorithm_scores'].keys())
                avg_scores = [self.results['algorithm_scores'][algo].get('average', 0) for algo in algorithms]
                
                ax3.barh(algorithms, avg_scores, color='#9f7aea')
                ax3.set_title('Algorithm Performance')
                ax3.set_xlabel('Average Similarity (%)')
            ax4 = fig.add_subplot(224)
            all_sequences = [seq for match in self.results['matches'] for seq in match.get('matched_sequences', [])]
            sequence_lengths = [seq['length'] for seq in all_sequences]
            if sequence_lengths:
                ax4.hist(sequence_lengths, bins=10, color='#f6ad55', edgecolor='black')
                ax4.set_title('Match Length Distribution')
                ax4.set_xlabel('Sequence Length (words)')
                ax4.set_ylabel('Frequency')
            
            fig.tight_layout()
            canvas = FigureCanvasTkAgg(fig, self.viz_canvas)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
            self.visualization_figures.append(fig)
            self.status_label.config(text="Visualizations generated successfully")
        
        except ImportError:
            self.viz_canvas.config(bg='white')
            label = tk.Label(self.viz_canvas, text="Matplotlib not installed\nInstall with: pip install matplotlib",
                            font=self.fonts['normal'], bg='white', fg='#a0aec0')
            label.place(relx=0.5, rely=0.5, anchor='center')
            messagebox.showwarning("Warning", "Matplotlib is required for visualizations")
    
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
                messagebox.showinfo("Success", f"Text report exported to:\n{filepath}")
        
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
        
        elif format_type == 'pdf':
            filepath = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf")],
                initialfile=f"plagiarism_report_{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )
            
            if filepath:
                document_name = Path(self.current_file).name if self.current_file else "Pasted Text"
                try:
                    generate_pdf_report(self.results, document_name, self.selected_algorithms, filepath)
                    messagebox.showinfo("Success", f"PDF report exported to:\n{filepath}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to generate PDF: {str(e)}")
        
        elif format_type == 'json':
            filepath = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON Files", "*.json")],
                initialfile=f"plagiarism_report_{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            
            if filepath:
                document_name = Path(self.current_file).name if self.current_file else "Pasted Text"
                report = generate_json_report(self.results, document_name, self.selected_algorithms)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(report)
                messagebox.showinfo("Success", f"JSON data exported to:\n{filepath}")
        
        elif format_type == 'excel':
            filepath = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel Files", "*.xlsx")],
                initialfile=f"plagiarism_report_{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )
            
            if filepath:
                messagebox.showinfo("Info", "Excel export coming soon!")
    
    def quick_check(self):
        self.set_fast_preset()
        self.run_ultimate_check()
    
    def deep_analysis(self):
        for var in self.algo_vars.values():
            var.set(True)
        for var in self.analysis_vars.values():
            var.set(True)
        
        self.run_ultimate_check()
    
    def set_academic_preset(self):
        algorithms = ['cosine_tfidf', 'ngram_3', 'ngram_5', 'sequence', 'semantic']
        for algo_id, var in self.algo_vars.items():
            var.set(algo_id in algorithms)
        self.analysis_vars['readability'].set(True)
        self.analysis_vars['citations'].set(True)
        self.analysis_vars['keyphrases'].set(True)
        self.sensitivity_var.set(8.0)
        self.status_label.config(text="Academic preset applied")
    
    def set_fast_preset(self):
        algorithms = ['cosine_tfidf', 'jaccard', 'ngram_3']
        for algo_id, var in self.algo_vars.items():
            var.set(algo_id in algorithms)
        for var in self.analysis_vars.values():
            var.set(False)
        self.sensitivity_var.set(3.0)
        self.status_label.config(text="Fast preset applied")
    
    def set_thorough_preset(self):
        for var in self.algo_vars.values():
            var.set(True)
        for var in self.analysis_vars.values():
            var.set(True)
        self.sensitivity_var.set(15.0)
        self.status_label.config(text="Thorough preset applied")
        
    def refresh_database_view(self):
        self.db_tree.delete(*self.db_tree.get_children())
        self.database = self.db_manager.get_all_documents()
        
        for idx, doc in enumerate(self.database, 1):
            word_count = len(self.engine.tokenize(doc['text']))
            added_date = datetime.fromisoformat(doc['added_date']).strftime('%Y-%m-%d') if doc['added_date'] else 'Unknown'
            
            values = (
                idx,
                doc['source'][:50] + '...' if len(doc['source']) > 50 else doc['source'],
                doc.get('category', 'General'),
                word_count,
                added_date,
                doc.get('url', '')[:30] + '...' if doc.get('url') and len(doc['url']) > 30 else doc.get('url', '')
            )
            self.db_tree.insert('', 'end', values=values, iid=str(idx))
        
        self.db_label.config(text=f"DB: {len(self.database)} docs")
        self.status_label.config(text=f"Database loaded: {len(self.database)} documents")
    
    def on_document_select(self, event):
        selected = self.db_tree.selection()
        if not selected:
            return
        
        idx = int(selected[0]) - 1
        if 0 <= idx < len(self.database):
            doc = self.database[idx]
            
            self.doc_details['Source'].config(text=doc['source'])
            self.doc_details['Category'].config(text=doc.get('category', 'General'))
            self.doc_details['URL'].config(text=doc.get('url', 'None'))
            self.doc_details['Words'].config(text=str(len(self.engine.tokenize(doc['text']))))
            self.doc_details['Added'].config(text=doc.get('added_date', 'Unknown'))
            self.doc_details['Content'].config(state='normal')
            self.doc_details['Content'].delete(1.0, tk.END)
            self.doc_details['Content'].insert(1.0, doc['text'][:1000] + '...' if len(doc['text']) > 1000 else doc['text'])
            self.doc_details['Content'].config(state='disabled')
    
    def add_to_database(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Document to Database")
        dialog.geometry("600x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Add Reference Document", 
                font=self.fonts['large'], bg='white', fg='#2d3748').pack(pady=10)
        fields_frame = tk.Frame(dialog, bg='white')
        fields_frame.pack(fill='both', expand=True, padx=20, pady=10)
        tk.Label(fields_frame, text="Source Name*:", font=self.fonts['normal'],
                bg='white', fg='#4a5568', anchor='w').grid(row=0, column=0, sticky='w', pady=5)
        source_entry = tk.Entry(fields_frame, font=self.fonts['normal'], width=40)
        source_entry.grid(row=0, column=1, sticky='ew', pady=5, padx=(10, 0))
        tk.Label(fields_frame, text="URL:", font=self.fonts['normal'],
                bg='white', fg='#4a5568', anchor='w').grid(row=1, column=0, sticky='w', pady=5)
        url_entry = tk.Entry(fields_frame, font=self.fonts['normal'], width=40)
        url_entry.grid(row=1, column=1, sticky='ew', pady=5, padx=(10, 0))
        tk.Label(fields_frame, text="Category:", font=self.fonts['normal'],
                bg='white', fg='#4a5568', anchor='w').grid(row=2, column=0, sticky='w', pady=5)
        category_var = tk.StringVar(value="General")
        category_combo = ttk.Combobox(fields_frame, textvariable=category_var,
                                     values=["General", "Academic", "Technical", "Literature", 
                                             "News", "Research", "Legal", "Business"],
                                     width=38)
        category_combo.grid(row=2, column=1, sticky='ew', pady=5, padx=(10, 0))
        tk.Label(fields_frame, text="Document Text*:", font=self.fonts['normal'],
                bg='white', fg='#4a5568', anchor='w').grid(row=3, column=0, sticky='nw', pady=5)
        text_widget = scrolledtext.ScrolledText(fields_frame, height=15, width=40,
                                               font=self.fonts['small'], wrap='word')
        text_widget.grid(row=3, column=1, sticky='nsew', pady=5, padx=(10, 0))
        fields_frame.columnconfigure(1, weight=1)
        fields_frame.rowconfigure(3, weight=1)
        
        def save_document():
            source = source_entry.get().strip()
            url = url_entry.get().strip()
            text = text_widget.get(1.0, tk.END).strip()
            category = category_var.get()
            
            if not source or not text:
                messagebox.showwarning("Warning", "Source name and text are required")
                return
            metadata = {
                'added_by': 'GUI',
                'word_count': len(text.split()),
                'character_count': len(text)
            }
            
            if self.db_manager.add_document(source, text, url, category, metadata):
                messagebox.showinfo("Success", "Document added to database")
                self.refresh_database_view()
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Failed to add document (might be duplicate)")
        btn_frame = tk.Frame(dialog, bg='white')
        btn_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        tk.Button(btn_frame, text="Cancel", command=dialog.destroy,
                 bg='#a0aec0', fg='white', font=('Segoe UI', 10),
                 relief='flat', cursor='hand2').pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Save", command=save_document,
                 bg='#48bb78', fg='white', font=('Segoe UI', 10, 'bold'),
                 relief='flat', cursor='hand2').pack(side='right', padx=5)
    
    def edit_document(self):
        selected = self.db_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a document to edit")
            return
        messagebox.showinfo("Info", "Edit feature coming soon!")
    
    def delete_from_database(self):
        selected = self.db_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a document to delete")
            return
        
        item = self.db_tree.item(selected[0])
        source = item['values'][1] 
        
        if messagebox.askyesno("Confirm", f"Delete '{source}' from database?"):
            if self.db_manager.delete_document(source):
                messagebox.showinfo("Success", "Document deleted")
                self.refresh_database_view()
            else:
                messagebox.showerror("Error", "Failed to delete document")
    
    def search_database(self):
        query = self.search_var.get().strip()
        if not query:
            self.refresh_database_view()
            return
        
        results = self.db_manager.search_documents(query)
        self.db_tree.delete(*self.db_tree.get_children())
        
        for idx, doc in enumerate(results, 1):
            word_count = len(self.engine.tokenize(doc['text']))
            values = (
                idx,
                doc['source'][:50] + '...' if len(doc['source']) > 50 else doc['source'],
                doc.get('category', 'General'),
                word_count,
                doc.get('added_date', 'Unknown'),
                doc.get('url', '')[:30] + '...' if doc.get('url') and len(doc.get('url')) > 30 else doc.get('url', '')
            )
            self.db_tree.insert('', 'end', values=values)
        
        self.status_label.config(text=f"Found {len(results)} documents matching '{query}'")
    
    def import_documents(self):
        filepath = filedialog.askopenfilename(
            title="Import Documents",
            filetypes=[("JSON Files", "*.json"), ("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    if filepath.endswith('.json'):
                        data = json.load(f)
                        if isinstance(data, list):
                            count = 0
                            for doc in data:
                                if self.db_manager.add_document(
                                    doc.get('source', 'Imported'),
                                    doc.get('text', ''),
                                    doc.get('url', ''),
                                    doc.get('category', 'General')
                                ):
                                    count += 1
                            messagebox.showinfo("Success", f"Imported {count} documents from JSON")
                        else:
                            messagebox.showerror("Error", "Invalid JSON format")
                    else:
                        text = f.read()
                        source = Path(filepath).name
                        if self.db_manager.add_document(source, text, '', 'General'):
                            messagebox.showinfo("Success", "Document imported successfully")
                
                self.refresh_database_view()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import: {str(e)}")
    
    def export_database(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("Text Files", "*.txt"), ("CSV Files", "*.csv")],
            initialfile=f"database_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        if filepath:
            try:
                if filepath.endswith('.json'):
                    data = []
                    for doc in self.database:
                        data.append({
                            'source': doc['source'],
                            'url': doc.get('url', ''),
                            'text': doc['text'][:10000],  
                            'category': doc.get('category', 'General'),
                            'added_date': doc.get('added_date', '')
                        })
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                
                elif filepath.endswith('.txt'):
                    with open(filepath, 'w', encoding='utf-8') as f:
                        for doc in self.database:
                            f.write(f"Source: {doc['source']}\n")
                            f.write(f"Category: {doc.get('category', 'General')}\n")
                            f.write(f"URL: {doc.get('url', '')}\n")
                            f.write(f"Text: {doc['text'][:500]}...\n\n")
                            f.write("-" * 80 + "\n\n")
                
                messagebox.showinfo("Success", f"Database exported to:\n{filepath}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def show_db_stats(self):
        stats = self.db_manager.get_statistics()
        
        stats_text = f"""DATABASE STATISTICS
{'='*60}

Overall:
  Total Documents: {stats['total_documents']:,}
  Total Checks: {stats['total_checks']:,}
  Average Similarity: {stats['avg_similarity']}%

Categories:
"""
        for cat_stat in stats['category_stats']:
            stats_text += f"  {cat_stat['category']}: {cat_stat['count']:,} documents\n"
        
        stats_text += f"\nRecent Activity ({stats['analysis_period_days']} days):\n"
        for day_stat in stats['daily_stats'][:7]: 
            stats_text += f"  {day_stat['date']}: {day_stat['checks_today']} checks, avg {day_stat['avg_similarity']:.1f}%\n"
        
        messagebox.showinfo("Database Statistics", stats_text)