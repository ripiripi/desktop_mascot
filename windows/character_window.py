from .base_window import WindowBase
from .enum import Event
import tkinter as tk
from PIL import Image, ImageTk
import random


class CharacterWindow(WindowBase):
    def __init__(self, root, memo_window, bubble_window, hand_window, x_pos, y_pos):
        self.pic_x = 250
        self.pic_y = 1000
        super().__init__(
            root,
            "キャラウィンドウ",
            self.pic_x,
            self.pic_y,
            x_pos,
            y_pos,
            syncronized_windows=[
                memo_window,
                hand_window,
                bubble_window,
            ],
            topmost_flag=True,
        )

        memo_window.window.lift(self.window)
        self.canvas = tk.Canvas(self.window, width=self.pic_x, height=self.pic_y, highlightthickness=0)
        self.canvas.pack()

        # ウィンドウの背景を透明に設定
        self.window.attributes("-transparentcolor", self.window["bg"])

        # 画像をロードしてリサイズ
        self.default_image_path = "./assets/image/tekku_0.png"
        self.blink_image_paths = ["./assets/image/tekku_1.png", "./assets/image/tekku_2.png"]
        self.load_images()

        # デフォルトの画像を表示
        self.display_image(self.character_images[0])

        memo_window.window.lift(self.window)

        # 一秒ごとにmabatakiメソッドを呼び出す
        self.window.after(1000, self.mabataki)

    def load_images(self):
        # 画像をロードしてリサイズ
        self.character_images = []
        default_image = Image.open(self.default_image_path)
        self.character_images.append(self.prepare_image(default_image))

        for path in self.blink_image_paths:
            image = Image.open(path)
            self.character_images.append(self.prepare_image(image))

    def prepare_image(self, image):
        # 背景を透明に変換
        image = self.make_background_fully_transparent(image, (255, 0, 0), tolerance=15)
        # 画像の比率を保ったままリサイズ
        resized_image = self.resize_image(image, self.pic_x, self.pic_y)
        return ImageTk.PhotoImage(resized_image)

    def display_image(self, image):
        self.canvas.config(width=image.width(), height=image.height())
        self.canvas.create_image(image.width() // 2, image.height() // 2, image=image, anchor=tk.CENTER)

    def resize_image(self, image, max_width, max_height):
        original_width, original_height = image.size
        ratio = min(max_width / original_width, max_height / original_height)
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        return image.resize((new_width, new_height))

    def on_focus_in(self, event):
        self.syncronized_windows[1].window.lift(self.window)  # hand
        self.syncronized_windows[0].window.lift(self.window)  # memo

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

    def mabataki(self):
        # 一定確率でまばたきを行う
        if random.random() < 0.45:
            self.start_blinking()

        # 次の呼び出しを1秒後に設定
        self.window.after(1000, self.mabataki)

    def start_blinking(self):
        self.blink_index = 0
        self.blink_sequence = [0, 1, 2, 1, 0]
        self.blink_images()

    def blink_images(self):
        if self.blink_index < len(self.blink_sequence):
            image_index = self.blink_sequence[self.blink_index]
            self.display_image(self.character_images[image_index])

            trans_time = 0
            if self.blink_index % 2 == 0:
                trans_time = 40
                self.window.after(trans_time, self.blink_images)
            else:
                if self.blink_index == 3:
                    trans_time = 30
                    self.window.after(25, self.blink_images)
                else:
                    trans_time = 85
                    self.window.after(80, self.blink_images)
            self.blink_index += 1
