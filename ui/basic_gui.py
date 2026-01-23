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