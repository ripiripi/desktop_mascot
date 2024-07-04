from .base_window import WindowBase
from .enum import Event


class CharacterWindow(WindowBase):
    def __init__(self, root, memo_window, bubble_window, x_pos, y_pos):
        super().__init__(
            root,
            "キャラウィンドウ",
            200,
            200,
            x_pos,
            y_pos,
            syncronized_windows=[memo_window, bubble_window],
            topmost_flag=True,
        )
        # self.window.lift(memo_window.window)
        memo_window.window.lift(self.window)

    def on_focus_in(self, event):
        self.syncronized_windows[0].window.lift(self.window)

    def update(self, event):
        super().update(event)
