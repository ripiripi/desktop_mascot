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
        self.window.lift(memo_window.window)

    def update(self, event):
        if event == Event.set_charwindow_topmost:
            self.window.lift(self.syncronized_windows[0].window)  # memo window
