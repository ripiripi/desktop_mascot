from .base_window import WindowBase
import tkinter as tk
from tkinter import font
from .enum import Event


class MemoWindow(WindowBase):
    def __init__(self, root, x_pos, y_pos):
        super().__init__(root, "メモウィンドウ", 300, 400, x_pos, y_pos, syncronized_windows=[], topmost_flag=True)

    def setup_window(self):

        self.text_widget = tk.Text(self.window)
        self.text_widget.pack(expand=True, fill=tk.BOTH)

        bold_font = font.Font(self.text_widget, self.text_widget.cget("font"))
        bold_font.configure(weight="bold")
        self.text_widget.tag_configure("bold", font=bold_font)

        self.text_widget.bind("<KeyRelease>", self.decorate_text)
        super().setup_window()

    def on_configure(self, event):
        pass  # 必要に応じて実装

    def on_focus_in(self, event):
        self.notify_observers(event=Event.set_charwindow_topmost)

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

    def update(self, event):
        pass
