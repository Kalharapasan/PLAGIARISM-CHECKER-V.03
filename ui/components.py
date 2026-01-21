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
    def hide(self):
        self.pack_forget()
        
        