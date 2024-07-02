from .base_window import WindowBase
import tkinter as tk
from atproto import Client
from .utils.password import generate_key, save_credentials, load_credentials
import os

import random


class BubbleWindow(WindowBase):
    def __init__(self, root, x_pos, y_pos):
        self.window_width = 300 + 30  # 30 is for padding
        self.window_height = 100
        super().__init__(
            root,
            "吹き出しウィンドウ",
            self.window_width,
            self.window_height,
            x_pos,
            y_pos,
            syncronized_windows=[],
            topmost_flag=True,
        )
        self.client = Client()

        self.transparent_color = "#f0f0f0"
        # ウィンドウの透過色を設定
        self.window.attributes("-transparentcolor", self.transparent_color)

        self.set_balloons()

        # 初回のみキー生成
        if not os.path.exists("secret.key"):
            generate_key()
        self.bluesky_login()

        self.update_sns_posts()

    def set_balloons(self):
        # Canvasウィジェットを作成、背景を透過させる
        self.canvas = tk.Canvas(
            self.window,
            width=self.window_width,
            height=self.window_height,
            bg=self.transparent_color,
            highlightthickness=0,
        )
        self.canvas.pack()

        # 吹き出しの尾部となる三角形を描画
        triangle = [
            (300, 50),  # バルーンの右端から出るように調整
            (310, 55),  # 三角形の先端をバルーンの中心線に合わせる
            (300, 60),
        ]
        self.canvas.create_polygon(triangle, fill="ebffff", outline="ebffff")
        # バルーンの本体部分を描画
        # self.canvas.create_rectangle(0, 0, 300, 100, fill="white", outline="white")
        radius = 10  # 角の丸みの半径

        # 角が丸い長方形を描画するために、四隅に円を描く
        self.canvas.create_oval(0, 0, radius * 2, radius * 2, fill="ebffff", outline="ebffff")  # 左上の角
        self.canvas.create_oval(300 - radius * 2, 0, 300, radius * 2, fill="ebffff", outline="ebffff")  # 右上の角
        self.canvas.create_oval(0, 100 - radius * 2, radius * 2, 100, fill="ebffff", outline="ebffff")  # 左下の角
        self.canvas.create_oval(
            300 - radius * 2, 100 - radius * 2, 300, 100, fill="ebffff", outline="ebffff"
        )  # 右下の角

        # 中央の長方形と上下の長方形を描画して、角が丸い長方形を完成させる
        self.canvas.create_rectangle(radius, 0, 300 - radius, 100, fill="ebffff", outline="ebffff")  # 中央
        self.canvas.create_rectangle(0, radius, 300, 100 - radius, fill="ebffff", outline="ebffff")  # 上下

    def bluesky_login(self):

        if not os.path.exists("credentials.json"):
            print("please enter your username and password:")
            username = input()
            password = input()
            # 保存
            save_credentials(username, password)

        loaded_username, loaded_password = load_credentials()
        print("ユーザー名:", loaded_username)
        print("パスワード:", loaded_password)

        self.client.login(loaded_username, loaded_password)
        self.client.send_post(text="テスト")

    def update_sns_posts(self):
        response = self.client.get_timeline()
        rand_int = random.randint(0, 50)
        tl = {"feed": response.feed[rand_int]}
        post_text = tl["feed"].post.record.text
        # label = tk.Label(self.window, text=post_text, wraplength=self.window.winfo_width() - 20)  # 20 is for padding
        # label.pack(padx=10, pady=10)  # Set padding around the label
        # label = tk.Label(self.window, text=post_text)
        # label.pack()
        label = tk.Label(
            self.window, text=post_text, wraplength=self.window.winfo_width() - 20, anchor="w", justify="left"
        )
        label.pack(padx=10, pady=10, anchor="w")
        # self.window.after(300000, self.update_sns_posts)

    def display_settings(self):
        self.window.lift()
        for widget in self.window.winfo_children():
            widget.destroy()
        label = tk.Label(self.window, text="設定変更オプション")
        label.pack()

    def update(self, event):
        pass
