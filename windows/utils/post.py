from typing import Dict, Union, List, Optional


def extract_post_content(post) -> tuple[str, Optional[str]]:
    post_text = post.record.text
    image_urls: Optional[str] = None

    # embedがNoneでなく、py_typeが'app.bsky.embed.images#view'を含んでいる場合
    if post.embed is not None and post.embed.py_type == "app.bsky.embed.images#view":
        image_urls = post.embed.images[0].fullsize

    return post_text, image_urls
