import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import threading
from datetime import datetime
from ..core.advanced_engine import AdvancedPlagiarismEngine
from ..core.database import DatabaseManager
from ..reports.advanced_report import generate_advanced_report, generate_html_report