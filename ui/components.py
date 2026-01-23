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
    
    def clear(self):
        self.data = []
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def get_selected(self):
        selection = self.tree.selection()
        if selection:
            return self.tree.item(selection[0])['values']
        return None

class Badge(tk.Frame):
    def __init__(self, parent, text: str = "", color: str = '#4299e1',
                 size: str = 'medium', **kwargs):
        
        super().__init__(parent, **kwargs)
        
        self.text = text
        self.color = color
        sizes = {
            'small': {'font': ('Segoe UI', 8), 'padding': (4, 2), 'radius': 8},
            'medium': {'font': ('Segoe UI', 9), 'padding': (6, 3), 'radius': 10},
            'large': {'font': ('Segoe UI', 10), 'padding': (8, 4), 'radius': 12}
        }
        
        self.size_config = sizes.get(size, sizes['medium'])
        
        self.config(bg=self['bg'])
        self._create_ui()
    
    def _create_ui(self):
        self.badge_frame = tk.Frame(self, bg=self.color, bd=0)
        self.badge_frame.pack()
        self.label = tk.Label(self.badge_frame, text=self.text,
                             font=self.size_config['font'],
                             bg=self.color, fg='white',
                             padx=self.size_config['padding'][0],
                             pady=self.size_config['padding'][1])
        self.label.pack()
        self.badge_frame.update_idletasks()
        width = self.badge_frame.winfo_reqwidth()
        height = self.badge_frame.winfo_reqheight()
        self.badge_frame.config(width=width, height=height)
    
    def update_text(self, text: str):
        self.text = text
        self.label.config(text=text)
        self._update_size()
    
    def update_color(self, color: str):
        self.color = color
        self.badge_frame.config(bg=color)
        self.label.config(bg=color)
    
    def _update_size(self):
        self.badge_frame.update_idletasks()
        width = self.badge_frame.winfo_reqwidth()
        height = self.badge_frame.winfo_reqheight()
        self.badge_frame.config(width=width, height=height)

class RatingStars(tk.Frame):
    def __init__(self, parent, max_stars: int = 5, rating: float = 0,
                 editable: bool = False, on_rating_change: Callable = None,
                 **kwargs):
        super().__init__(parent, **kwargs)
        
        self.max_stars = max_stars
        self.rating = rating
        self.editable = editable
        self.on_rating_change = on_rating_change
        
        self.config(bg=self['bg'])
        self._create_ui()
    
    def _create_ui(self):
        self.stars = []
        
        for i in range(self.max_stars):
            star_label = tk.Label(self, text="★", font=('Segoe UI', 16),
                                 bg=self['bg'], fg='#cbd5e0',
                                 cursor='hand2' if self.editable else 'arrow')
            star_label.pack(side='left', padx=1)
            
            if self.editable:
                star_label.bind('<Enter>', lambda e, idx=i: self._on_star_hover(idx))
                star_label.bind('<Leave>', lambda e: self._update_stars())
                star_label.bind('<Button-1>', lambda e, idx=i: self._set_rating(idx + 1))
            
            self.stars.append(star_label)
        
        self._update_stars()
    
    def _update_stars(self):
        full_stars = int(self.rating)
        has_half = self.rating - full_stars >= 0.5
        
        for i, star in enumerate(self.stars):
            if i < full_stars:
                star.config(fg='#f6ad55') 
            elif i == full_stars and has_half:
                star.config(fg='#f6ad55')
            else:
                star.config(fg='#cbd5e0') 
    
    def _on_star_hover(self, index: int):
        if self.editable:
            for i, star in enumerate(self.stars):
                if i <= index:
                    star.config(fg='#f6ad55')
                else:
                    star.config(fg='#cbd5e0')
    
    def _set_rating(self, rating: int):
        if self.editable and 0 <= rating <= self.max_stars:
            self.rating = rating
            self._update_stars()
            if self.on_rating_change:
                self.on_rating_change(rating)
    
    def get_rating(self) -> float:
        return self.rating
    
    def set_rating(self, rating: float):
        if 0 <= rating <= self.max_stars:
            self.rating = rating
            self._update_stars()
            
class LoadingSpinner(tk.Frame):
    def __init__(self, parent, size: int = 40, color: str = '#4299e1',
                 speed: int = 50, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.size = size
        self.color = color
        self.speed = speed
        self.angle = 0
        self.running = False
        
        self.config(bg=self['bg'])
        self._create_ui()
    
    def _create_ui(self):
        self.canvas = tk.Canvas(self, width=self.size, height=self.size,
                               bg=self['bg'], highlightthickness=0)
        self.canvas.pack()
    
    def start(self):
        if not self.running:
            self.running = True
            self._animate()
    
    def stop(self):
        self.running = False
    
    def _animate(self):
        if not self.running:
            return
        
        self.canvas.delete('all')
        center = self.size // 2
        radius = self.size // 2 - 2
        for i in range(8):
            start_angle = self.angle + (i * 45)
            extent = 30  
            opacity = (i + 1) / 8
            rgb_color = self._hex_to_rgb(self.color)
            faded_color = self._fade_color(rgb_color, opacity)
            self.canvas.create_arc(
                center - radius, center - radius,
                center + radius, center + radius,
                start=start_angle, extent=extent,
                style='arc', width=3,
                outline=faded_color
            )
        self.angle = (self.angle + 10) % 360
        self.after(self.speed, self._animate)
    
    def _hex_to_rgb(self, hex_color: str):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def _fade_color(self, rgb: tuple, opacity: float) -> str:
        r, g, b = rgb
        bg_r, bg_g, bg_b = 255, 255, 255
        
        r = int(r * opacity + bg_r * (1 - opacity))
        g = int(g * opacity + bg_g * (1 - opacity))
        b = int(b * opacity + bg_b * (1 - opacity))
        
        return f'#{r:02x}{g:02x}{b:02x}'

class SplitPane(tk.Frame):
    
    def _create_ui(self):
        self.left_pane = tk.Frame(self, bg=self['bg'])
        self.right_pane = tk.Frame(self, bg=self['bg'])
        self.left_widget.pack(in_=self.left_pane, fill='both', expand=True)
        self.right_widget.pack(in_=self.right_pane, fill='both', expand=True)
        self.splitter = tk.Frame(self, bg='#cbd5e0', cursor='sb_h_double_arrow' 
                                 if self.orientation == 'horizontal' else 'sb_v_double_arrow')
        self.splitter.bind('<Button-1>', self._start_drag)
        self.splitter.bind('<B1-Motion>', self._on_drag)
        self.splitter.bind('<ButtonRelease-1>', self._stop_drag)
        self._update_layout()
        self.dragging = False
        self.start_pos = 0
    
    def _update_layout(self):
        for widget in self.winfo_children():
            widget.pack_forget()
        
        if self.orientation == 'horizontal':
            left_width = int(self.winfo_width() * self.split_ratio)
            self.left_pane.pack(side='left', fill='both', expand=True)
            self.splitter.pack(side='left', fill='y', padx=1)
            self.right_pane.pack(side='left', fill='both', expand=True)
            self.left_pane.config(width=left_width)
            self.splitter.config(width=4)
        else:
            left_height = int(self.winfo_height() * self.split_ratio)            
            self.left_pane.pack(side='top', fill='both', expand=True)
            self.splitter.pack(side='top', fill='x', pady=1)
            self.right_pane.pack(side='top', fill='both', expand=True)
            self.left_pane.config(height=left_height)
            self.splitter.config(height=4)
    
    def _start_drag(self, event):
        self.dragging = True
        self.start_pos = event.x if self.orientation == 'horizontal' else event.y
    
    def _on_drag(self, event):
        if not self.dragging:
            return
        if self.orientation == 'horizontal':
            total_width = self.winfo_width()
            delta = event.x - self.start_pos
            new_left_width = int(total_width * self.split_ratio) + delta
            if new_left_width < self.min_size:
                new_left_width = self.min_size
            if total_width - new_left_width < self.min_size:
                new_left_width = total_width - self.min_size
            self.split_ratio = new_left_width / total_width
        else:
            total_height = self.winfo_height()
            delta = event.y - self.start_pos
            new_left_height = int(total_height * self.split_ratio) + delta
            if new_left_height < self.min_size:
                new_left_height = self.min_size
            if total_height - new_left_height < self.min_size:
                new_left_height = total_height - self.min_size
                self.split_ratio = new_left_height / total_height
        self._update_layout()
    