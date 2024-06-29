from .base_window import WindowBase
import tkinter as tk
from atproto import Client
from cryptography.fernet import Fernet
import os
import json


# キーの生成と保存（初回のみ実行）
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)


# キーの読み込み
def load_key():
    return open("secret.key", "rb").read()


# パスワードの暗号化
def encrypt_password(password):
    key = load_key()
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password


# パスワードの復号化
def decrypt_password(encrypted_password):
    key = load_key()
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password)
    return decrypted_password.decode()


# ユーザー名とパスワードの保存
def save_credentials(username, password):
    encrypted_password = encrypt_password(password)
    credentials = {"username": username, "password": encrypted_password.decode()}
    with open("credentials.json", "w") as file:
        json.dump(credentials, file)


# ユーザー名とパスワードの読み込み
def load_credentials():
    with open("credentials.json", "r") as file:
        credentials = json.load(file)
        username = credentials["username"]
        encrypted_password = credentials["password"].encode()
        password = decrypt_password(encrypted_password)
        return username, password


class BubbleWindow(WindowBase):
    def __init__(self, root, x_pos, y_pos):
        super().__init__(root, "吹き出しウィンドウ", 300, 100, x_pos, y_pos, syncronized_windows=[], topmost_flag=True)
        self.client = Client()
        # 初回のみキー生成
        if not os.path.exists("secret.key"):
            generate_key()
        self.bluesky_login()

        self.update_sns_posts()

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
        tl = {"feed": response.feed[20]}
        post_text = tl["feed"].post.record.text
        label = tk.Label(self.window, text=post_text)
        label.pack()
        # self.window.after(300000, self.update_sns_posts)

    def display_settings(self):
        self.window.lift()
        for widget in self.window.winfo_children():
            widget.destroy()
        label = tk.Label(self.window, text="設定変更オプション")
        label.pack()

    def update(self, event):
        pass
