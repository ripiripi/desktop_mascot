from typing import Dict, Union, List, Optional
import requests
from PIL import Image, ImageTk
from io import BytesIO
import random
import tkinter as tk


def fetch_image(url: Optional[str], max_width, max_height) -> Optional[Image.Image]:
    try:
        response = requests.get(url)
        response.raise_for_status()  # URLの有効性を確認
        image = Image.open(BytesIO(response.content))

        # 画像の縮小処理
        ratio = min(max_width / image.width, max_height / image.height)
        new_size = (int(image.width * ratio), int(image.height * ratio))
        resized_image = image.resize(new_size)

        return resized_image
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch image from {url}: {e}")
        return None


def extract_post_content(post) -> tuple[str, Optional[str]]:
    post_text = post.record.text
    image_urls: Optional[str] = None

    # embedがNoneでなく、py_typeが'app.bsky.embed.images#view'を含んでいる場合
    if post.embed is not None and post.embed.py_type == "app.bsky.embed.images#view":
        image_urls = post.embed.images[0].fullsize

    return post_text, image_urls
