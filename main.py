from tkinter import Tk
from windows.character_window import CharacterWindow
from windows.bubble_window import BubbleWindow
from windows.memo_window import MemoWindow


class DesktopMascotApp:
    def __init__(self, root):
        self.root = root
        self.memo_window = MemoWindow(root)
        self.bubble_window = BubbleWindow(root)
        self.char_window = CharacterWindow(root, self.memo_window)
        self.link_windows()

    def link_windows(self):
        # キャラウィンドウとメモウィンドウの位置連動はCharacterWindowクラスで行います
        pass


if __name__ == "__main__":
    root = Tk()
    root.withdraw()  # メインウィンドウを非表示
    app = DesktopMascotApp(root)
    root.mainloop()
