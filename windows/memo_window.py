from .base_window import WindowBase
import tkinter as tk
from tkinter import font
from .enum import Event
import os


class MemoWindow(WindowBase):
    def __init__(self, root, x_pos, y_pos):
        super().__init__(root, "メモウィンドウ", 250, 250, x_pos, y_pos, syncronized_windows=[], topmost_flag=True)

    def setup_window(self):
        self.text_widget = tk.Text(self.window)
        self.text_widget.pack(expand=True, fill=tk.BOTH)
        self.file_path = "assets/text.txt"
        self.auto_save_interval = 5000  # 自動保存の間隔（ミリ秒）

        bold_font = font.Font(self.text_widget, self.text_widget.cget("font"))
        bold_font.configure(weight="bold")
        self.text_widget.tag_configure("bold", font=bold_font)

        self.text_widget.bind("<KeyRelease>", self.decorate_text)
        self.load_text()

        super().setup_window()
        self.auto_save()  # 自動保存を開始
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

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

    def mouse_move(self, event):
        pass

    def update(self, event):
        super().update(event)

    def save_text(self):
        content = self.text_widget.get("1.0", tk.END)
        with open(self.file_path, "w", encoding="utf-8") as file:
            file.write(content)

    def load_text(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as file:
                content = file.read()
                self.text_widget.insert("1.0", content)

    def auto_save(self):
        self.save_text()
        self.window.after(self.auto_save_interval, self.auto_save)

    def on_close(self):
        self.save_text()
        self.window.destroy()
