from .base_window import WindowBase
import tkinter as tk
from tkinter import font
import customtkinter as ctk
from tkinter import ttk
from .enum import Event
import os
import re
import webbrowser


class MemoWindow(WindowBase):
    def __init__(self, root, x_pos, y_pos):
        self.width = 250
        self.height = 230
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.topmost_flag = True
        self.file_path = "data/memo.txt"
        self.auto_save_interval = 5000  # 自動保存の間隔（ミリ秒）
        super().__init__(root, "メモウィンドウ", 250, 250, x_pos, y_pos, syncronized_windows=[], topmost_flag=True)

    def on_focus_in(self, event):
        self.syncronized_windows[0].window.lift(self.window)

    def setup_window(self):
        # 外側に黒色のフレームを追加（角を丸くしない）
        self.outer_frame = ctk.CTkFrame(self.window, fg_color="#000000", corner_radius=0)
        self.outer_frame.pack(expand=True, fill=ctk.BOTH)

        # 内側に白色のフレームを追加しパディングを適用（角を丸くしない）
        self.inner_frame = ctk.CTkFrame(self.outer_frame, fg_color="#FFFFFF", corner_radius=0)
        self.inner_frame.pack(expand=True, fill=ctk.BOTH, padx=1, pady=1)

        # テキストウィジェットを配置
        self.text_widget = tk.Text(self.inner_frame, wrap=tk.WORD, bd=0, bg="#FFFFFF", fg="#000000")
        self.text_widget.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.text_widget.tag_configure("link", foreground="blue", underline=True)
        self.text_widget.tag_configure("checked", foreground="gray", overstrike=True)

        self.text_widget.bind("<KeyRelease>", self.decorate_text)
        self.text_widget.bind("<Button-1>", self.on_click)
        self.text_widget.tag_bind("link", "<Double-1>", self.open_link)

        self.load_text()
        self.decorate_text(None)

        super().setup_window()
        self.auto_save()  # 自動保存を開始
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    def decorate_text(self, event):
        content = self.text_widget.get("1.0", tk.END)
        self.text_widget.tag_remove("link", "1.0", tk.END)

        self.apply_checkbox(content)  # 先にチェックボックスを適用
        self.apply_links(content)  # 次にリンクを適用

    def apply_checkbox(self, content):
        checkbox_pattern = re.compile(r"^\[ \] (.*)", re.MULTILINE)
        for match in checkbox_pattern.finditer(content):
            start, end = match.span(0)
            self.text_widget.delete(f"1.0+{start}c", f"1.0+{start + 3}c")
            self.text_widget.insert(f"1.0+{start}c", "☐")

        checkbox_checked_pattern = re.compile(r"^\[x\] (.*)", re.MULTILINE)
        for match in checkbox_checked_pattern.finditer(content):
            start, end = match.span(0)
            self.text_widget.delete(f"1.0+{start}c", f"1.0+{start + 3}c")
            self.text_widget.insert(f"1.0+{start}c", "☑")

        # 各行について、☑が冒頭にある時、チェックボックス以降のその行に"checked"のtag_addを行う
        line_start = "1.0"
        while True:
            line_start = self.text_widget.search("☑", line_start, stopindex=tk.END)
            if not line_start:
                break
            line_end = self.text_widget.index(f"{line_start} lineend")
            self.text_widget.tag_add("checked", f"{line_start} + 2c", line_end)
            line_start = line_end

    def apply_links(self, content):
        url_pattern = re.compile(r"(https?://[^\s]+)")
        for match in url_pattern.finditer(content):
            start, end = match.span(0)
            self.text_widget.tag_add("link", f"1.0+{start}c", f"1.0+{end}c")

    def open_link(self, event):
        index = self.text_widget.index(f"@{event.x},{event.y}")
        start = self.text_widget.search("https://", index, backwards=True, stopindex="1.0", regexp=True)
        end = self.text_widget.search(r"\s", start, stopindex=tk.END, regexp=True)
        if not end:
            end = tk.END
        url = self.text_widget.get(start, end)
        webbrowser.open(url)

    def on_click(self, event):
        index = self.text_widget.index(f"@{event.x},{event.y}")
        line_start = f"{index.split('.')[0]}.0"
        line_end = f"{index.split('.')[0]}.end"
        line_text = self.text_widget.get(line_start, line_end)

        if line_text.startswith("☐ "):
            self.toggle_checkbox(line_start, "☐ ", "☑ ")
        elif line_text.startswith("☑ "):
            self.toggle_checkbox(line_start, "☑ ", "☐ ")

        self.decorate_text(None)

    def toggle_checkbox(self, line_start, old_symbol, new_symbol):
        self.text_widget.delete(line_start, f"{line_start}+2c")
        self.text_widget.insert(line_start, new_symbol)
        if new_symbol == "☑":
            self.text_widget.tag_add("checked", f"{line_start} + 2c", f"{line_start} lineend")
        else:
            self.text_widget.tag_remove("checked", f"{line_start} + 2c", f"{line_start} lineend")

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
