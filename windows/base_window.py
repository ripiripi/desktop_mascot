from abc import ABC, abstractmethod
import tkinter as tk


class WindowBase(ABC):
    def __init__(self, root, title, width, height):
        self.window = tk.Toplevel(root)
        self.window.geometry(f"{width}x{height}")
        self.window.title(title)
        self.setup_window()

    @abstractmethod
    def setup_window(self):
        pass

    @abstractmethod
    def on_click(self, event):
        print(f"{self.window.title()} がクリックされました")

    @abstractmethod
    def on_configure(self, event):
        pass  # 必要に応じてオーバーライドして使用
