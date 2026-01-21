class Breadcrumb(tk.Frame):
    def _create_ui(self):
        for i, (text, callback) in enumerate(self.items):