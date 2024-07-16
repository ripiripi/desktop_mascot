from cryptography.fernet import Fernet
import json


# キーの生成と保存（初回のみ実行）
def generate_key():
    key = Fernet.generate_key()
    with open("data/secret.key", "wb") as key_file:
        key_file.write(key)


# キーの読み込み
def load_key():
    return open("data/secret.key", "rb").read()


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
    with open("data/credentials.json", "w") as file:
        json.dump(credentials, file)


# ユーザー名とパスワードの読み込み
def load_credentials():
    with open("data/credentials.json", "r") as file:
        credentials = json.load(file)
        username = credentials["username"]
        encrypted_password = credentials["password"].encode()
        password = decrypt_password(encrypted_password)
        return username, password
