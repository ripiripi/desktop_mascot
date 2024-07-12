from .base_window import WindowBase
import tkinter as tk
from atproto import Client
from .utils.password import generate_key, save_credentials, load_credentials
from .utils.post import extract_post_content
import os
import random
import threading
from .enum import Event


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
        self.stop_post_update = False

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

        # 初回のSNS投稿をすぐに表示
        self.update_sns_posts()
        self.update_sns_posts_async()

    def set_balloons(self):

        # 既存のラベルを削除
        self.canvas.delete("balloon")
        self.window.geometry(f"{self.window_width}x{self.window_height}")
        self.canvas.config(height=self.window_height, width=self.window_width)

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
        if self.stop_post_update:
            return

        response = self.client.get_timeline()
        rand_int = random.randint(0, len(response.feed) - 1)

        print("response_len", len(response.feed))
        post = response.feed[rand_int].post
        # print(type(response.feed[rand_int]))
        # response.feed[rand_int]の中身を確認
        # print(response.feed[rand_int])

        if self.stop_post_update:
            return

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
        if not self.stop_post_update:
            self.update_sns_timer = threading.Timer(6, self.fetch_and_update_sns_posts)
            self.update_sns_timer.start()

    def fetch_and_update_sns_posts(self):
        self.update_sns_posts()
        self.update_sns_posts_async()

    def stop_update_sns_posts(self):
        self.stop_post_update = True
        if self.update_sns_timer:
            self.update_sns_timer.cancel()

    def menu_mode(self):
        self.stop_update_sns_posts()  # 更新を停止
        self.window.lift()

        # キャンバスウィジェットを再作成
        self.canvas.destroy()
        self.canvas = tk.Canvas(
            self.window,
            width=self.window_width,
            height=self.window_height,
            bg=self.transparent_color,
            highlightthickness=0,
        )
        self.canvas.pack()
        # キャンバスのすべての要素を削除
        # self.canvas.delete("all")

        # メニューとして表示するオプション
        options = ["SNS (Bluesky)の設定をする", "さようなら", "なんでもない"]
        label_height = 0

        for option in options:
            label = tk.Label(
                self.canvas,
                text=option,
                font=self.font,
                bg=self.balloon_color,
                anchor="nw",
                justify="left",
                cursor="hand2",
            )
            label.bind("<Button-1>", lambda event, opt=option: self.option_selected(opt))
            label.bind("<Enter>", self.on_label_enter)
            label.bind("<Leave>", self.on_label_leave)
            label.original_font = label.cget("font")  # 元のフォントを保存
            self.canvas.create_window(10, label_height + 10, anchor="nw", window=label)
            label_height += label.winfo_reqheight() + 10

        self.window_height = label_height + 10
        self.window.geometry(f"{self.window_width}x{self.window_height}")
        self.set_balloons()

    def option_selected(self, option):
        print(f"選択されたオプション: {option}")
        # ここでオプションに応じた処理を実行します
        if option == "SNS (Bluesky)の設定をする":
            self.handle_option1()
        elif option == "さようなら":
            self.handle_option2()
        elif option == "なんでもない":
            self.handle_option3()

    def handle_option1(self):
        # オプション1の処理
        print("オプション1が選択されました")

    def handle_option2(self):
        # オプション2の処理
        print("オプション2が選択されました")
        self.display_goodbye_and_exit()

    def handle_option3(self):
        # オプション3の処理
        print("オプション3が選択されました")
        self.display_aaa_and_return_to_sns()

    def display_aaa_and_return_to_sns(self):
        self.canvas.delete("all")
        label = tk.Label(self.canvas, text="ん", font=self.font, bg=self.balloon_color)
        self.canvas.create_window(10, 10, anchor="nw", window=label)

        self.window_height = label.winfo_reqheight() + 20
        self.window.geometry(f"{self.window_width}x{self.window_height}")
        self.set_balloons()

        # 2秒後にバルーンを一時的に非表示にしてSNS投稿表示モードに戻る
        self.window.after(2000, self.return_to_sns_mode)

    def display_goodbye_and_exit(self):
        self.canvas.delete("all")
        label = tk.Label(self.canvas, text="じゃあね！", font=self.font, bg=self.balloon_color)
        self.canvas.create_window(10, 10, anchor="nw", window=label)

        self.window_height = label.winfo_reqheight() + 20
        self.window.geometry(f"{self.window_width}x{self.window_height}")
        self.set_balloons()

        # 3秒後にアプリケーションを終了する
        self.window.after(2000, self.exit_application)

    def exit_application(self):
        self.root.quit()  # アプリケーションを終了する

    def return_to_sns_mode(self):
        self.window.withdraw()  # バルーンを一時的に非表示にする
        self.stop_post_update = False
        self.update_sns_posts_async()
        self.window.deiconify()  # バルーンを再表示する

    def on_label_enter(self, event):
        label = event.widget
        label.config(bg="#d1e7e7")
        self.animate_label(label, 1.1)

    def on_label_leave(self, event):
        label = event.widget
        label.config(bg=self.balloon_color)
        label.config(font=label.original_font)  # 元のフォントに戻す

    def animate_label(self, label, scale_factor):
        # ラベルのフォントサイズをアニメーションさせる
        original_font = label.original_font
        font_name, font_size = original_font.rsplit(" ", 1)
        font_size = int(float(font_size) * scale_factor)
        new_font = f"{font_name} {font_size}"
        label.config(font=new_font)

    def update(self, event):
        super().update(event)
        if event == Event.START_MENU_MODE:
            self.menu_mode()
