from .base_window import WindowBase
import tkinter as tk
from .interface import Subject, Observer


class BubbleWindow(WindowBase, Subject, Observer):
    def __init__(self, root):
        super().__init__(root, "吹き出しウィンドウ", 300, 100)
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

    def add_observer(self, observer):
        return super().add_observer(observer)

    def notify_observers(self, event):
        return super().notify_observers(event)

    def update(self, event):
        return super().update(event)
