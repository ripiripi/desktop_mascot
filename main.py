from tkinter import Tk
from windows.character_window import CharacterWindow
from windows.bubble_window import BubbleWindow
from windows.memo_window import MemoWindow
from windows.hand_window import HandWindow


class DesktopMascotApp:
    def __init__(self, root):
        self.root = root
        self.memo_window = MemoWindow(root, x_pos=430, y_pos=400)
        self.bubble_window = BubbleWindow(root, x_pos=130, y_pos=250)
        char_window_x = 450
        char_window_y = 175
        self.hand_window = HandWindow(root, x_pos=char_window_x, y_pos=char_window_y)
        self.char_window = CharacterWindow(
            root, self.memo_window, self.bubble_window, self.hand_window, x_pos=char_window_x, y_pos=char_window_y
        )
        self.memo_window.add_syncronized_window([self.hand_window, self.char_window])
        self.hand_window.add_syncronized_window([self.memo_window, self.char_window, self.bubble_window])

        self.char_window.add_observer([self.memo_window, self.bubble_window, self.hand_window])
        self.memo_window.add_observer([self.char_window, self.bubble_window, self.hand_window])
        self.bubble_window.add_observer([self.char_window, self.memo_window, self.hand_window])
        self.hand_window.add_observer([self.char_window, self.memo_window, self.bubble_window])


if __name__ == "__main__":
    root = Tk()
    root.withdraw()  # メインウィンドウを非表示
    app = DesktopMascotApp(root)
    root.mainloop()
