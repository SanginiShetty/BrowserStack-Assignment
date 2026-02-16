"""
Main entry point — run the El País Opinion scraper locally (single browser).

Steps executed:
  1. Open the Opinion section of El País
  2. Verify the page is in Spanish
  3. Scrape the first 5 articles (title, content, cover image)
  4. Save results to text files and articles.json
  5. (Future) Translate headers & analyse repeated words
"""

import json
import os
import time

from config.settings import OPINION_URL, MAX_ARTICLES, ARTICLES_DIR, JSON_OUTPUT
from scraper.driver_factory import create_local_driver
from scraper.cookie_handler import accept_cookies
from scraper.article_scraper import verify_spanish, collect_article_links, scrape_article
from translator.header_translator import translate_titles
from analyzer.word_analyzer import find_repeated_words, print_repeated_words, print_all_word_counts


def save_article_to_file(index: int, article: dict) -> str:
    """Persist an article's title, URL, and content to a .txt file."""
    os.makedirs(ARTICLES_DIR, exist_ok=True)
    filepath = os.path.join(ARTICLES_DIR, f"article_{index + 1}.txt")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"Title: {article['title']}\n")
        f.write(f"URL: {article['url']}\n")
        if article["image_path"]:
            f.write(f"Image: {article['image_path']}\n")
        f.write(f"\n{'=' * 60}\n\n")
        f.write(article["content"])
    return filepath


def run_scraper(driver) -> list[dict]:
    """Execute the full scraping workflow with the given *driver*."""
    print(f"[→] Navigating to {OPINION_URL}")
    driver.get(OPINION_URL)
    time.sleep(1)

    accept_cookies(driver)
    verify_spanish(driver)

    article_urls = collect_article_links(driver, MAX_ARTICLES)
    if not article_urls:
        print("[✗] No articles found.")
        return []

    all_articles: list[dict] = []
    for idx, url in enumerate(article_urls):
        print("-" * 70)
        print(f"  Article {idx + 1} / {len(article_urls)}")
        print("-" * 70)

        article = scrape_article(driver, url, idx)
        article_file = save_article_to_file(idx, article)
        all_articles.append(article)

        print(f"  Title   : {article['title']}")
        print(f"  URL     : {article['url']}")
        print(f"  Article : saved to {article_file}")
        if article["image_path"]:
            print(f"  Image   : saved to {article['image_path']}")
        else:
            print("  Image   : (not available)")
        print()
        print(f"  Content :\n{article['content'][:2000]}")
        if len(article["content"]) > 2000:
            print("  ... (truncated)")
        print()

    return all_articles


def main():
    print("=" * 70)
    print("  El País – Opinion Section Scraper")
    print("=" * 70, "\n")

    driver = create_local_driver()

    try:
        articles = run_scraper(driver)

        if not articles:
            return

        # Save all articles to JSON
        with open(JSON_OUTPUT, "w", encoding="utf-8") as jf:
            json.dump(articles, jf, ensure_ascii=False, indent=2)
        print(f"[✓] All articles saved to {JSON_OUTPUT}\n")

        # ------------------------------------------------------------------
        # Translate headers (ES → EN) & analyse repeated words
        # ------------------------------------------------------------------
        spanish_titles = [a["title"] for a in articles]
        english_titles = translate_titles(spanish_titles)

        print("\n" + "=" * 70)
        print("  Translated Headers (ES → EN)")
        print("=" * 70)
        for es, en in zip(spanish_titles, english_titles):
            print(f"  {es}")
            print(f"    → {en}")
        print()

        repeated = find_repeated_words(english_titles, threshold=2)
        print_repeated_words(repeated)
        print_all_word_counts(english_titles)

    finally:
        driver.quit()
        print("=" * 70)
        print("  Done. Browser closed.")
        print("=" * 70)


if __name__ == "__main__":
    main()
