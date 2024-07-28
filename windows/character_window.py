from .base_window import WindowBase
from .enum import Event
import tkinter as tk
from PIL import Image, ImageTk
import random
import threading
import time


class CharacterWindow(WindowBase):
    def __init__(self, root, syncronized_windows, x_pos, y_pos):
        self.pic_x = 250
        self.pic_y = 1000
        super().__init__(
            root,
            "キャラウィンドウ",
            width=self.pic_x,
            height=self.pic_y,
            x_pos=x_pos,
            y_pos=y_pos,
            syncronized_windows=syncronized_windows,
            topmost_flag=True,
        )

        syncronized_windows[0].window.lift(self.window)  # memo_window
        self.canvas = tk.Canvas(self.window, width=self.pic_x, height=self.pic_y, highlightthickness=0)
        self.canvas.pack()

        # ウィンドウの背景を透明に設定
        self.window.attributes("-transparentcolor", self.window["bg"])

        # 画像をロードしてリサイズ
        self.default_image_path = "./assets/image/tekku_0.png"
        self.blink_image_paths = ["./assets/image/tekku_1.png", "./assets/image/tekku_2.png"]
        self.load_images()

        # 画像キャンバスの初期化
        self.image_ids = []
        for image in self.character_images:
            image_id = self.canvas.create_image(0, 0, image=image, anchor=tk.NW)
            self.image_ids.append(image_id)

        self.current_image_index = 0
        self.update_image_visibility()

        # まばたき処理を開始
        self.blink_timer = None
        self.schedule_blink()

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
        image = self.make_background_fully_transparent(image, (255, 0, 0), tolerance=35)
        # 画像の比率を保ったままリサイズ
        resized_image = self.resize_image(image, self.pic_x, self.pic_y)
        return ImageTk.PhotoImage(resized_image)

    def update_image_visibility(self):
        for index, image_id in enumerate(self.image_ids):
            if index == self.current_image_index:
                self.canvas.itemconfig(image_id, state="normal")
            else:
                self.canvas.itemconfig(image_id, state="hidden")

    def mouse_down(self, e):
        self.lift_windows()
        return super().mouse_down(e)

    def on_focus_in(self, event):
        self.lift_windows()

    def lift_windows(self):
        for window in self.syncronized_windows:
            if window.title == "メモウィンドウ":
                memo_window = window
            if window.title == "ハンドウィンドウ":
                hand_window = window
        hand_window.window.lift(self.window)  # hand
        memo_window.window.lift(self.window)  # memo

    def resize_image(self, image, max_width, max_height):
        original_width, original_height = image.size
        ratio = min(max_width / original_width, max_height / original_height)
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        return image.resize((new_width, new_height))

    def mouse_double_click(self, event):
        # メニューモードへの切り替え
        # TODO: アニメーション処理（反応）
        self.notify_observers(Event.START_MENU_MODE)

    def update(self, event):
        super().update(event)
        if event == Event.SET_WINDOWPOS:
            self.check_relative_positions()

    def make_background_fully_transparent(self, image, color, tolerance):
        image = image.convert("RGBA")
        datas = image.getdata()

        new_data = []
        for item in datas:
            if all(abs(item[i] - color[i]) <= tolerance for i in range(3)):
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)

        image.putdata(new_data)

        for y in range(image.height):
            for x in range(image.width):
                r, g, b, a = image.getpixel((x, y))
                if a != 255:
                    image.putpixel((x, y), (r, g, b, 0))

        return image

    def schedule_blink(self):
        values = [1, 2, 3, 4, 5]
        probabilities = [0.45, 0.25, 0.2, 0.08, 0.02]

        delay = random.choices(values, probabilities)[0]

        self.blink_timer = threading.Timer(delay, self.start_blinking)
        self.blink_timer.start()

    def check_relative_positions(self):
        # メインウィンドウの位置を取得
        main_geom = self.window.geometry().split("+")
        main_x, main_y = int(main_geom[1]), int(main_geom[2])
        for index, window in enumerate(self.syncronized_windows):
            rel_x, rel_y = self.relative_pos[index]
            expected_x, expected_y = main_x + rel_x, main_y + rel_y
            # サブウィンドウの現在の位置を取得
            sub_geom = window.window.geometry().split("+")
            current_x, current_y = int(sub_geom[1]), int(sub_geom[2])
            # 吹き出しウィンドウの場合、ある程度の誤差であればそのまま
            if window.title == "吹き出しウィンドウ":
                if abs(current_x - expected_x) > 150 or abs(current_y - expected_y) > 150:
                    window.setPos(expected_x, expected_y)
                    self.lift_windows()
            elif (current_x, current_y) != (expected_x, expected_y):
                window.setPos(expected_x, expected_y)
                self.lift_windows()

    def check_transparency(self):
        for window in self.syncronized_windows:
            if window.translucent != self.translucent:
                window.turn_translucent()

    def start_blinking(self):
        self.check_relative_positions()
        self.check_transparency()

        self.blink_index = 0
        self.blink_sequence = [0, 1, 2, 1, 0]
        self.blink_time = [0.08, 0.06, 0.05, 0.06, 0.08]
        self.blink_images()

    def blink_images(self):
        if self.blink_index < len(self.blink_sequence):
            self.current_image_index = self.blink_sequence[self.blink_index]
            self.update_image_visibility()

            trans_time = self.blink_time[self.blink_index]

            self.blink_index += 1
            self.blink_timer = threading.Timer(trans_time, self.blink_images)
            self.blink_timer.start()
        else:
            self.schedule_blink()
