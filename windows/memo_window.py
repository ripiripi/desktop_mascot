from .base_window import WindowBase
import tkinter as tk
from tkinter import font


class MemoWindow(WindowBase):
    def __init__(self, root):
        super().__init__(root, "メモウィンドウ", 300, 400)

    def setup_window(self):
        self.text_widget = tk.Text(self.window)
        self.text_widget.pack(expand=True, fill=tk.BOTH)

        bold_font = font.Font(self.text_widget, self.text_widget.cget("font"))
        bold_font.configure(weight="bold")
        self.text_widget.tag_configure("bold", font=bold_font)

        self.text_widget.bind("<KeyRelease>", self.decorate_text)
        self.window.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        print("メモウィンドウがクリックされました")
        # 必要に応じて他の動作を追加

    def on_configure(self, event):
        pass  # 必要に応じて実装

    def decorate_text(self, event):
        content = self.text_widget.get("1.0", tk.END)
        self.text_widget.tag_remove("bold", "1.0", tk.END)
        start = 1.0
        while True:
            start = self.text_widget.search(r"\*\*", start, stopindex=tk.END, regexp=True)
            if not start:
                break
            end = self.text_widget.search(r"\*\*", start + "+2c", stopindex=tk.END, regexp=True)
            if not end:
                break
            self.text_widget.tag_add("bold", start, end + "+2c")
            start = end + "+2c"
