from .base_window import WindowBase
import tkinter as tk


class BubbleWindow(WindowBase):
    def __init__(self, root):
        super().__init__(root, "吹き出しウィンドウ", 300, 100)
        self.update_sns_posts()

    def setup_window(self):
        self.window.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        print("吹き出しウィンドウがクリックされました")
        # 必要に応じて他の動作を追加

    def on_configure(self, event):
        pass  # 必要に応じて実装

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
