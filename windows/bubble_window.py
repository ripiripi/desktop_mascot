from .base_window import WindowBase
import tkinter as tk
from atproto import Client
from .utils.password import generate_key, save_credentials, load_credentials
from .utils.post import extract_post_content
import os
import random
import threading


class BubbleWindow(WindowBase):
    def __init__(self, root, x_pos, y_pos):
        self.window_width_default = 300
        self.window_width = self.window_width_default + 30  # 30 is for padding
        self.window_height_default = 100
        self.window_height = 100
        self.balloon_color = "#EFFBFB"
        self.font = ("San Francisco", 12)  # ("Helvetica Neue", 12)  #
        self.current_alpha = 1.0  # 透明度
        self.hovering = False

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

        # Canvasウィジェットを作成、背景を透過させる
        self.canvas = tk.Canvas(
            self.window,
            width=self.window_width,
            height=self.window_height,
            bg=self.transparent_color,
            highlightthickness=0,
        )
        self.canvas.pack()
        self.set_balloons()

        # 初回のみキー生成
        if not os.path.exists("secret.key"):
            generate_key()
        self.bluesky_login()

        self.update_sns_posts_async()

    def set_balloons(self):

        # 既存のラベルを削除
        self.canvas.delete("balloon")
        self.window.geometry(f"{self.window_width}x{self.window_height}")
        self.canvas.config(height=self.window_height)

        hukidasi_height = self.window_height / 2
        # 吹き出しの尾部となる三角形を描画
        triangle = [
            (self.window_width_default, hukidasi_height - 5),  # バルーンの右端から出るように調整
            (self.window_width_default + 10, hukidasi_height),  # 三角形の先端をバルーンの中心線に合わせる
            (self.window_width_default, hukidasi_height + 5),
        ]
        balloon_color = self.balloon_color
        self.canvas.create_polygon(triangle, fill=balloon_color, outline=balloon_color, tags="balloon")
        # バルーンの本体部分を描画
        radius = 10  # 角の丸みの半径

        # 角が丸い長方形を描画するために、四隅に円を描く
        self.canvas.create_oval(
            0, 0, radius * 2, radius * 2, fill=balloon_color, outline=balloon_color, tags="balloon"
        )  # 左上の角
        self.canvas.create_oval(
            self.window_width_default - radius * 2,
            0,
            self.window_width_default,
            radius * 2,
            fill=balloon_color,
            outline=balloon_color,
            tags="balloon",
        )  # 右上の角
        self.canvas.create_oval(
            0,
            self.window_height - radius * 2,
            radius * 2,
            self.window_height,
            fill=balloon_color,
            outline=balloon_color,
            tags="balloon",
        )  # 左下の角
        self.canvas.create_oval(
            self.window_width_default - radius * 2,
            self.window_height - radius * 2,
            self.window_width_default,
            self.window_height,
            fill=balloon_color,
            outline=balloon_color,
            tags="balloon",
        )  # 右下の角

        # 中央の長方形と上下の長方形を描画して、角が丸い長方形を完成させる
        self.canvas.create_rectangle(
            radius,
            0,
            self.window_width_default - radius,
            self.window_height,
            fill=balloon_color,
            outline=balloon_color,
            tags="balloon",
        )  # 中央
        self.canvas.create_rectangle(
            0,
            radius,
            self.window_width_default,
            self.window_height - radius,
            fill=balloon_color,
            outline=balloon_color,
            tags="balloon",
        )  # 上下

        self.canvas.tag_lower("all")

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

    def update_sns_posts(self):
        response = self.client.get_timeline()
        rand_int = random.randint(0, len(response.feed) - 1)

        print("response_len", len(response.feed))
        post = response.feed[rand_int].post
        # print(type(response.feed[rand_int]))
        # response.feed[rand_int]の中身を確認
        # print(response.feed[rand_int])

        post_text, image_url = extract_post_content(post)  # tl["feed"].post.record.text
        print(image_url)

        # 既存のラベルを削除
        self.canvas.delete("post_text")

        # ラベルを作成して追加

        # label = tk.Label(
        #    self.canvas,
        #    text=post_text,
        #    wraplength=self.window_width - 50,
        #    anchor="nw",
        #    justify="left",
        #    bg=self.balloon_color,
        #    font=self.font,
        # )
        label = tk.Message(
            self.canvas,
            text=post_text,
            width=self.window_width - 50,
            anchor="nw",
            justify="left",
            bg=self.balloon_color,
            font=self.font,
        )
        self.canvas.update_idletasks()  # レイアウトを確定

        self.canvas.create_window(5, 10, window=label, anchor="nw", tags="post_text")

        label_height = label.winfo_reqheight()

        # サイズを確認
        print(f"height: {label_height}")

        # バルーンの高さをlabel_height + 20になるように調整し、再描画
        self.window_height = label_height + 20
        self.set_balloons()

    def update_sns_posts_async(self):
        threading.Thread(target=self.fetch_and_update_sns_posts).start()

    def fetch_and_update_sns_posts(self):
        self.update_sns_posts()
        self.window.after(6000, self.update_sns_posts_async)

    def display_settings(self):
        self.window.lift()
        for widget in self.window.winfo_children():
            widget.destroy()
        label = tk.Label(self.window, text="設定変更オプション")
        label.pack()

    def update(self, event):
        super().update(event)
