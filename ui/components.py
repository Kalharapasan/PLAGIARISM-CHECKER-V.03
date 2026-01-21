class Breadcrumb(tk.Frame):
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