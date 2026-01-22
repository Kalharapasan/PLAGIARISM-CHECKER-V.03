class Breadcrumb(tk.Frame):
    
    def __init__(self, parent, items: List[Tuple[str, Callable]] = None,
                 separator: str = "›", **kwargs):
        super().__init__(parent, **kwargs)
        
        self.items = items or []
        self.separator = separator
        
        self.config(bg=self['bg'])
        
        self._create_ui()
        
    def _create_ui(self):
        for i, (text, callback) in enumerate(self.items):
            if i > 0:
                sep_label = tk.Label(self, text=self.separator,
                                    font=('Segoe UI', 10),
                                    bg=self['bg'], fg='#a0aec0')
                sep_label.pack(side='left', padx=5)
            item_label = tk.Label(self, text=text,
                                 font=('Segoe UI', 10),
                                 bg=self['bg'], fg='#4a5568',
                                 cursor='hand2')
            item_label.pack(side='left')
            if callback:
                item_label.bind('<Button-1>', lambda e, cb=callback: cb())
                item_label.bind('<Enter>',
                               lambda e, lbl=item_label: lbl.config(fg='#4299e1', font=('Segoe UI', 10, 'underline')))
                item_label.bind('<Leave>',
                               lambda e, lbl=item_label: lbl.config(fg='#4a5568', font=('Segoe UI', 10)))
    
    def update_items(self, items: List[Tuple[str, Callable]]):
        for widget in self.winfo_children():
            widget.destroy()
        
        self.items = items
        self._create_ui()
    
    def add_item(self, text: str, callback: Callable = None):
        self.items.append((text, callback))
        self.update_items(self.items)
    
    def remove_last(self):
        if self.items:
            self.items.pop()
            self.update_items(self.items)
        
    def clear(self):
        self.items = []
        self.update_items(self.items)

class GradientFrame(tk.Frame):
    def __init__(self, parent, colors: List[str] = None,
                 direction: str = 'horizontal', **kwargs):
        super().__init__(parent, **kwargs)
        self.colors = colors or ['#667eea', '#764ba2']
        self.direction = direction
        self._create_gradient()
    
    def _create_gradient(self):
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self.bind('<Configure>', self._draw_gradient)
    
    def _draw_gradient(self, event=None):
        self.canvas.delete('all')
        
        width = self.winfo_width()
        height = self.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        if self.direction == 'horizontal':
            for i in range(width):
                ratio = i / width
                color = self._interpolate_color(self.colors, ratio)
                self.canvas.create_line(i, 0, i, height, fill=color)
        elif self.direction == 'vertical':
            for i in range(height):
                ratio = i / height
                color = self._interpolate_color(self.colors, ratio)
                self.canvas.create_line(0, i, width, i, fill=color)
        elif self.direction == 'diagonal':
            for i in range(max(width, height)):
                ratio = i / max(width, height)
                color = self._interpolate_color(self.colors, ratio)
                self.canvas.create_line(0, i, i, 0, fill=color)
                if i < width and i < height:
                    self.canvas.create_line(width - i, height, width, height - i, fill=color)
    
    def _interpolate_color(self, colors: List[str], ratio: float) -> str:
        if len(colors) == 1:
            return colors[0]
        
        segment = ratio * (len(colors) - 1)
        segment_int = int(segment)
        segment_frac = segment - segment_int
        
        if segment_int >= len(colors) - 1:
            return colors[-1]
        color1 = colors[segment_int]
        color2 = colors[segment_int + 1]
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        rgb1 = hex_to_rgb(color1)
        rgb2 = hex_to_rgb(color2)
        r = int(rgb1[0] + (rgb2[0] - rgb1[0]) * segment_frac)
        g = int(rgb1[1] + (rgb2[1] - rgb1[1]) * segment_frac)
        b = int(rgb1[2] + (rgb2[2] - rgb1[2]) * segment_frac)
        
        return f'#{r:02x}{g:02x}{b:02x}'

class NotificationBar(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.config(bg=self['bg'], height=40)
        self.pack_propagate(False)
        
        self._create_ui()
        self.hide()
    
    def _create_ui(self):
        self.message_label = tk.Label(self, text="", font=('Segoe UI', 10),
                                     bg=self['bg'], fg='white')
        self.message_label.pack(side='left', padx=15)
        self.close_btn = tk.Label(self, text="✕", font=('Segoe UI', 12),
                                 bg=self['bg'], fg='white', cursor='hand2')
        self.close_btn.pack(side='right', padx=15)
        
        self.close_btn.bind('<Button-1>', lambda e: self.hide())
        self.close_btn.bind('<Enter>', 
                           lambda e: self.close_btn.config(fg='#cbd5e0'))
        self.close_btn.bind('<Leave>', 
                           lambda e: self.close_btn.config(fg='white'))
    
    def show(self, message: str, type: str = 'info', duration: int = 5000):
        colors = {
            'info': '#4299e1',
            'success': '#48bb78',
            'warning': '#ed8936',
            'error': '#f56565'
        }
        
        color = colors.get(type, '#4299e1')
        self.config(bg=color)
        self.message_label.config(bg=color, text=message)
        self.close_btn.config(bg=color)
        self.pack(fill='x', pady=(0, 5))
        if duration > 0:
            self.after(duration, self.hide)
    
    def hide(self):
        self.pack_forget()
        
    
class DataTable(tk.Frame):
    self.tree = ttk.Treeview(self, columns=[col['id'] for col in self.columns],
                                 show='headings', height=height)
    for col in self.columns:
            self.tree.heading(col['id'], text=col['text'])
            self.tree.column(col['id'], width=col.get('width', 100),
                            anchor=col.get('anchor', 'w'))
    vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
    hsb = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
    self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    self.tree.grid(row=0, column=0, sticky='nsew')
    vsb.grid(row=0, column=1, sticky='ns')
    hsb.grid(row=1, column=0, sticky='ew')
    self.grid_rowconfigure(0, weight=1)
    self.grid_columnconfigure(0, weight=1)
    self._populate_data()
    
    def _populate_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in self.data:
            self.tree.insert('', 'end', values=row)
    
    def add_row(self, row: List):
        self.data.append(row)
        self.tree.insert('', 'end', values=row)