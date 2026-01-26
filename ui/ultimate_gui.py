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
        
        
