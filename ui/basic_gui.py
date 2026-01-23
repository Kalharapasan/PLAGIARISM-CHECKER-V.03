import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
from datetime import datetime
from ..core.base_engine import BasePlagiarismEngine
from ..reports.basic_report import generate_basic_report