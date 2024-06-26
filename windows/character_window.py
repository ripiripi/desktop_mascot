from .base_window import WindowBase
from .interface import Subject, Observer


class CharacterWindow(WindowBase, Subject, Observer):
    def __init__(self, root, memo_window, bubble_window):
        super().__init__(root, "キャラウィンドウ", 200, 200, syncronized_windows=[memo_window, bubble_window])

    def setup_window(self):
        super().setup_window()

    def add_observer(self, observer):
        return super().add_observer(observer)

    def notify_observers(self, event):
        return super().notify_observers(event)

    def update(self, event):
        return super().update(event)
