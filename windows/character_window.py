from .base_window import WindowBase


class CharacterWindow(WindowBase):
    def __init__(self, root, memo_window):
        super().__init__(root, "キャラウィンドウ", 200, 200)
        self.memo_window = memo_window

    def setup_window(self):
        self.window.bind("<Button-1>", self.on_click)
        self.window.bind("<Configure>", self.on_configure)

    def on_click(self, event):
        print("キャラウィンドウがクリックされました")
        # 必要に応じて他の動作を追加

    def on_configure(self, event):
        x = self.window.winfo_x() + 220  # キャラウィンドウの右にメモウィンドウを配置
        y = self.window.winfo_y()
        self.memo_window.window.geometry(f"+{x}+{y}")
