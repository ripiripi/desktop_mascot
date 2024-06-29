from .base_window import WindowBase
import tkinter as tk


class BubbleWindow(WindowBase):
    def __init__(self, root, x_pos, y_pos):
        super().__init__(root, "吹き出しウィンドウ", 300, 100, x_pos, y_pos, syncronized_windows=[], topmost_flag=True)
        self.update_sns_posts()

    def update_sns_posts(self):
        self.window.lift()
        label = tk.Label(self.window, text="新しいSNS投稿")
        label.pack()
        self.window.after(300000, self.update_sns_posts)

    def display_settings(self):
        self.window.lift()
        for widget in self.window.winfo_children():
            widget.destroy()
        label = tk.Label(self.window, text="設定変更オプション")
        label.pack()

    def update(self, event):
        pass
