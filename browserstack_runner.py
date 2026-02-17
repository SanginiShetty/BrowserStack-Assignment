"""
BrowserStack parallel runner — execute the scraper across 5 browser/device
combinations simultaneously using ThreadPoolExecutor.

Usage:
    python browserstack_runner.py
"""

import json
import threading
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed

from config.browserstack_config import BROWSER_CAPS
from config.settings import OPINION_URL, MAX_ARTICLES, JSON_OUTPUT
from scraper.driver_factory import create_browserstack_driver
from scraper.cookie_handler import accept_cookies
from scraper.article_scraper import verify_spanish, collect_article_links, scrape_article
from translator.header_translator import translate_titles
from analyzer.word_analyzer import find_repeated_words, print_repeated_words, print_all_word_counts

MAX_PARALLEL_THREADS = 5
MAX_RETRIES = 1  # No retries to avoid session timeout

# Thread-safe print lock
_print_lock = threading.Lock()


def _safe_print(*args, **kwargs):
    with _print_lock:
        print(*args, **kwargs)


def _run_single_attempt(capabilities: dict, session_name: str) -> dict:
    """
    Execute one attempt of the scraping workflow on a BrowserStack session.

    Optimised for speed: extracts titles directly from the listing page
    instead of navigating to each article individually.

    Returns a dict with status, titles list.
    """
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    driver = None
    titles = []
    status = "FAILED"
    reason = ""  # Track failure reason for BrowserStack dashboard
    try:
        driver = create_browserstack_driver(capabilities)

        # Navigate to Opinion section
        driver.get(OPINION_URL)

        # Wait for article headlines to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article h2 a"))
        )

        # Accept cookies & verify language
        accept_cookies(driver)
        lang = driver.find_element(By.TAG_NAME, "html").get_attribute("lang")
        _safe_print(f"  [{session_name}] Language: {lang}")

        # Brief settle time for dynamic content
        import time
        time.sleep(0.3)

        # Extract titles directly from listing page (no extra navigations)
        link_elements = driver.find_elements(By.CSS_SELECTOR, "article h2 a")
        seen_urls = set()
        for el in link_elements:
            href = el.get_attribute("href")
            # Accept all articles on the Opinion page (we're already filtered by URL)
            if href and href not in seen_urls:
                seen_urls.add(href)
                title = el.text.strip()
                if title:
                    titles.append(title)
                    _safe_print(f"  [{session_name}] Found: {title}")
            if len(titles) >= MAX_ARTICLES:
                break

        _safe_print(f"  [{session_name}] Collected {len(titles)} title(s)")

        # iPad/tablets have large viewports, require 5 articles for all devices
        min_required = MAX_ARTICLES

        if len(titles) >= min_required:
            status = "PASSED"
            reason = f"Successfully scraped {len(titles)} articles"
        else:
            _safe_print(f"  [{session_name}] Expected {min_required}+, got {len(titles)}")
            status = "FAILED"
            reason = f"Insufficient articles: expected {min_required}, found {len(titles)}"

    except Exception as exc:
        _safe_print(f"  [{session_name}] ERROR: {exc}")
        status = "FAILED"
        reason = f"Exception: {str(exc)[:200]}"  # Truncate long error messages
    finally:
        if driver:
            try:
                # Include reason in BrowserStack session status for dashboard visibility
                import json
                reason_escaped = json.dumps(reason)  # Properly escape the reason string
                driver.execute_script(
                    f'browserstack_executor: {{"action": "setSessionStatus", '
                    f'"arguments": {{"status": "{status.lower()}", "reason": {reason_escaped}}}}}'
                )
            except Exception:
                pass
            driver.quit()

    return {
        "status": status,
        "articles": [],
        "titles": titles,
    }


def run_on_browser(capabilities: dict) -> dict:
    """
    Run the scraping workflow on a BrowserStack session with automatic retry.

    Retries up to MAX_RETRIES times on failure (handles flaky real-device sessions).
    Returns a summary dict with session name, status, article titles, and count.
    """
    session_name = capabilities.get("bstack:options", {}).get(
        "sessionName", "Unknown"
    )
    _safe_print(f"\n[⇒] Starting session: {session_name}")

    for attempt in range(1, MAX_RETRIES + 1):
        if attempt > 1:
            _safe_print(f"  [{session_name}] Retry {attempt}/{MAX_RETRIES} ...")

        outcome = _run_single_attempt(capabilities, session_name)

        if outcome["status"] == "PASSED":
            break
        elif attempt < MAX_RETRIES:
            _safe_print(f"  [{session_name}] Attempt {attempt} failed, will retry.")

    result = {
        "session": session_name,
        "status": outcome["status"],
        "articles": len(outcome["titles"]),
        "titles": outcome["titles"],
    }
    icon = "✓" if result["status"] == "PASSED" else "✗"
    _safe_print(f"[{icon}] Session '{session_name}' finished — {result['status']} ({result['articles']} titles)")
    return result


def main():
    print("=" * 70)
    print("  BrowserStack Cross-Browser Test Runner")
    print(f"  Running {len(BROWSER_CAPS)} sessions in {MAX_PARALLEL_THREADS} parallel threads")
    print("=" * 70, "\n")

    results = []

    with ThreadPoolExecutor(max_workers=MAX_PARALLEL_THREADS) as executor:
        futures = {
            executor.submit(run_on_browser, caps): caps
            for caps in BROWSER_CAPS
        }
        for future in as_completed(futures):
            results.append(future.result())

    # ---- Summary ----
    print("\n" + "=" * 70)
    print("  Cross-Browser Test Summary")
    print("=" * 70)
    for r in results:
        icon = "✓" if r["status"] == "PASSED" else "✗"
        print(f"  [{icon}] {r['session']:<30s}  {r['status']}  ({r['articles']} articles)")
    print("=" * 70)

    passed = sum(1 for r in results if r["status"] == "PASSED")
    print(f"\n  {passed}/{len(results)} sessions passed.")

    # ---- Translate & Analyse (using titles from first successful session) ----
    first_passed = next((r for r in results if r["status"] == "PASSED"), None)
    if first_passed and first_passed["titles"]:
        spanish_titles = first_passed["titles"]

        print("\n" + "=" * 70)
        print("  Translating Headers (ES → EN)")
        print("=" * 70)
        english_titles = translate_titles(spanish_titles)
        for es, en in zip(spanish_titles, english_titles):
            print(f"  {es}")
            print(f"    → {en}")
        print()

        repeated = find_repeated_words(english_titles, threshold=2)
        print_repeated_words(repeated)
        print_all_word_counts(english_titles)

    print("=" * 70)
    print("  Done.")
    print("=" * 70)


if __name__ == "__main__":
    main()
