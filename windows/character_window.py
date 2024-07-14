from .base_window import WindowBase
from .enum import Event
import tkinter as tk
from PIL import Image, ImageTk


class CharacterWindow(WindowBase):
    def __init__(self, root, memo_window, bubble_window, x_pos, y_pos):
        self.pic_x = 250
        self.pic_y = 1000
        super().__init__(
            root,
            "キャラウィンドウ",
            self.pic_x,
            self.pic_y,
            x_pos,
            y_pos,
            syncronized_windows=[memo_window, bubble_window],
            topmost_flag=True,
        )

        memo_window.window.lift(self.window)
        self.canvas = tk.Canvas(self.window, width=self.pic_x, height=self.pic_y, highlightthickness=0)
        self.canvas.pack()

        # ウィンドウの背景を透明に設定
        self.window.attributes("-transparentcolor", self.window["bg"])

        # 画像をロードしてリサイズ
        image = Image.open("./assets/image/body.png")

        # 背景を透明に変換
        image = self.make_background_fully_transparent(image, (255, 0, 0), tolerance=15)

        # 画像の比率を保ったままリサイズ
        original_width, original_height = image.size
        max_width, max_height = self.pic_x, self.pic_y

        ratio = min(max_width / original_width, max_height / original_height)
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)

        resized_image = image.resize((new_width, new_height))
        self.character_image = ImageTk.PhotoImage(resized_image)

        # キャンバスのサイズをリサイズ後の画像サイズに合わせる
        self.canvas.config(width=new_width, height=new_height)

        # 画像をキャンバスに表示
        self.canvas.create_image(new_width // 2, new_height // 2, image=self.character_image, anchor=tk.CENTER)

        memo_window.window.lift(self.window)

    def resize_image(self, image, max_width, max_height):
        original_width, original_height = image.size
        ratio = min(max_width / original_width, max_height / original_height)
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        return image.resize((new_width, new_height))

    def on_focus_in(self, event):
        self.syncronized_windows[0].window.lift(self.window)

    def mouse_double_click(self, event):
        # メニューモードへの切り替え
        # TODO: アニメーション処理（反応）
        self.notify_observers(Event.START_MENU_MODE)

    def update(self, event):
        super().update(event)

    def make_background_fully_transparent(self, image, color, tolerance):
        image = image.convert("RGBA")
        datas = image.getdata()

        new_data = []
        for item in datas:
            # 指定した色に近い場合に完全に透明に変換
            if all(abs(item[i] - color[i]) <= tolerance for i in range(3)):
                new_data.append((255, 255, 255, 0))  # 完全に透明に変換
            else:
                new_data.append(item)

        image.putdata(new_data)

        # 半透明部分を完全に透明に変換
        for y in range(image.height):
            for x in range(image.width):
                r, g, b, a = image.getpixel((x, y))
                if a != 255:  # 半透明ピクセル
                    image.putpixel((x, y), (r, g, b, 0))

        return image
