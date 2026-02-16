"""
Scrape articles from the El País Opinion section.

Responsibilities:
  - Verify the page is in Spanish
  - Collect article links from the listing page
  - Extract title, content, and cover-image URL from each article page
"""

import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.settings import IMAGE_DIR, MAX_ARTICLES
from scraper.image_downloader import download_image


# ---------------------------------------------------------------------------
# Language verification
# ---------------------------------------------------------------------------

def verify_spanish(driver) -> str:
    """Return the page lang attribute and print confirmation."""
    lang = driver.find_element(By.TAG_NAME, "html").get_attribute("lang")
    if lang and lang.startswith("es"):
        print(f"[✓] Page language confirmed: {lang}\n")
    else:
        print(f"[!] Page language is '{lang}' – expected 'es'. Continuing anyway.\n")
    return lang


# ---------------------------------------------------------------------------
# Link collection
# ---------------------------------------------------------------------------

def collect_article_links(driver, max_count: int = MAX_ARTICLES) -> list[str]:
    """Return up to *max_count* article URLs from the Opinion listing page."""
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "article h2 a"))
    )
    link_elements = driver.find_elements(By.CSS_SELECTOR, "article h2 a")

    urls: list[str] = []
    for el in link_elements:
        href = el.get_attribute("href")
        if href and href not in urls:
            urls.append(href)
        if len(urls) >= max_count:
            break

    print(f"[i] Found {len(urls)} article link(s) to scrape.\n")
    return urls


# ---------------------------------------------------------------------------
# Single-article scraping
# ---------------------------------------------------------------------------

def scrape_article(driver, url: str, index: int) -> dict:
    """
    Navigate to *url*, extract the article's title, content, and cover image.

    Returns a dict with keys: title, content, image_path, url
    """
    driver.get(url)

    # --- Title ---
    try:
        title_el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "article h1, h1.a_t")
            )
        )
        title = title_el.text.strip()
    except Exception:
        title = "(título no disponible)"

    # --- Content ---
    try:
        paragraphs = driver.find_elements(
            By.CSS_SELECTOR,
            "article .a_c p, article .article_body p, "
            "article [data-dtm-region='articulo_cuerpo'] p",
        )
        if not paragraphs:
            paragraphs = driver.find_elements(By.CSS_SELECTOR, "article p")
        content = "\n".join(p.text.strip() for p in paragraphs if p.text.strip())
    except Exception:
        content = "(contenido no disponible)"

    # --- Cover image ---
    image_path = None
    try:
        img_el = driver.find_element(
            By.CSS_SELECTOR, "article figure img, article .a_m_w img"
        )
        img_url = img_el.get_attribute("src")
        if img_url:
            os.makedirs(IMAGE_DIR, exist_ok=True)
            filename = f"article_{index + 1}.jpg"
            filepath = os.path.join(IMAGE_DIR, filename)
            if download_image(img_url, filepath):
                image_path = filepath
    except Exception:
        pass

    return {
        "title": title,
        "content": content,
        "image_path": image_path,
        "url": url,
    }
