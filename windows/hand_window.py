from .base_window import WindowBase
import tkinter as tk
from PIL import Image, ImageTk


class HandWindow(WindowBase):
    def __init__(self, root, x_pos, y_pos):
        self.pic_x = 250
        self.pic_y = 1000
        super().__init__(
            root,
            "ハンドウィンドウ",
            self.pic_x,
            self.pic_y,
            x_pos,
            y_pos,
            syncronized_windows=[],
            topmost_flag=True,
        )

        self.canvas = tk.Canvas(self.window, width=self.pic_x, height=self.pic_y, highlightthickness=0)
        self.canvas.pack()

        # ウィンドウの背景を透明に設定
        self.window.attributes("-transparentcolor", self.window["bg"])

        # 画像をロードしてリサイズ
        image = Image.open("./assets/image/hand_250.png")

        # 背景を透明に変換
        image = self.make_background_fully_transparent(image, (255, 0, 0), tolerance=15)

        # 画像の比率を保ったままリサイズ
        original_width, original_height = image.size
        max_width, max_height = self.pic_x, self.pic_y

        ratio = min(max_width / original_width, max_height / original_height)
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)

        resized_image = image.resize((new_width, new_height))
        self.hand_image = ImageTk.PhotoImage(resized_image)

        # キャンバスのサイズをリサイズ後の画像サイズに合わせる
        self.canvas.config(width=new_width, height=new_height)

        # 画像をキャンバスに表示
        self.canvas.create_image(new_width // 2, new_height // 2, image=self.hand_image, anchor=tk.CENTER)

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
