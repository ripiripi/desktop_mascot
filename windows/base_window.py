from abc import ABC, abstractmethod
import tkinter as tk


class WindowBase(ABC):
    def __init__(self, root, title, width, height, syncronized_windows=[]):
        self.window = tk.Toplevel(root)
        self.window.geometry(f"{width}x{height}")
        self.window.title(title)

        # 位置移動を同期させるウィンドウ
        self.pos_syncronized_windows: list[WindowBase] = syncronized_windows
        print(syncronized_windows)

        self.origin = (0, 0)
        self.isMouseDown = False
        self.originText = (0, 0)
        self.isMouseDownText = False

        self.setup_window()

    def add_syncronized_window(self, window):
        self.pos_syncronized_windows.append(window)

    def setup_window(self):
        self.window.bind("<Button-1>", self.mouseDown)
        self.window.bind("<ButtonRelease-1>", self.mouseRelease)
        self.window.bind("<B1-Motion>", self.mouseMove)
        print("unko")

    def on_click(self, event):
        print(f"{self.window.title()} がクリックされました")

    def mouseDown(self, e):
        if e.num == 1:
            self.origin = (e.x, e.y)
            self.isMouseDown = True

    def mouseRelease(self, e):
        self.isMouseDown = False

    def mouseMove(self, e):
        if self.isMouseDown:
            buf = self.window.geometry().split("+")
            self.setPos(
                e.x - self.origin[0] + int(buf[1]),
                e.y - self.origin[1] + int(buf[2]),
            )
            self.syncSubWindow(e.x - self.origin[0], e.y - self.origin[1])

    def syncSubWindow(self, dx, dy):
        # sub_window: WindowBase
        for sub_window in self.pos_syncronized_windows:
            buf = sub_window.window.geometry().split("+")
            current_x = int(buf[1])
            current_y = int(buf[2])

            new_x = current_x + dx
            new_y = current_y + dy
            sub_window.setPos(new_x, new_y)

    def mouseDownText(self, e):
        if e.num == 1:
            self.originText = (e.x, e.y)
            self.isMouseDownText = True

    def mouseReleaseText(self, e):
        self.isMouseDownText = False

    def setPos(self, x, y):
        self.window.geometry("+%s+%s" % (x, y))
