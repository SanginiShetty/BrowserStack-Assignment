"""
Download and save article cover images.
"""

import requests


def download_image(img_url: str, filepath: str) -> bool:
    """Download an image from *img_url* and save it to *filepath*."""
    try:
        resp = requests.get(img_url, timeout=15)
        resp.raise_for_status()
        with open(filepath, "wb") as f:
            f.write(resp.content)
        return True
    except Exception as exc:
        print(f"    [!] Failed to download image: {exc}")
        return False
