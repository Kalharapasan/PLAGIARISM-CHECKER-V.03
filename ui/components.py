class Breadcrumb(tk.Frame):
    def _create_ui(self):
        for i, (text, callback) in enumerate(self.items):
            if i > 0:
                sep_label = tk.Label(self, text=self.separator,
                                    font=('Segoe UI', 10),
                                    bg=self['bg'], fg='#a0aec0')
                sep_label.pack(side='left', padx=5)