"""
Translate article headers from Spanish to English using
the Rapid Translate Multi Traduction API.

Usage:
    from translator.header_translator import translate_titles

    spanish_titles = ["Claridad fiscal en el alquiler", ...]
    english_titles = translate_titles(spanish_titles)
"""

import requests

from config.settings import RAPID_API_KEY, RAPID_TRANSLATE_URL, RAPID_TRANSLATE_HOST


def translate_titles(
    titles: list[str],
    source: str = "es",
    target: str = "en",
) -> list[str]:
    """
    Translate a list of article titles from *source* language to *target*
    in a single batch call to the Rapid Translate API.

    Parameters
    ----------
    titles : list[str]
        Article titles in the source language.
    source : str
        ISO 639-1 source language code (default: "es").
    target : str
        ISO 639-1 target language code (default: "en").

    Returns
    -------
    list[str]
        Translated titles in the target language.
    """
    if not titles:
        return []

    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": RAPID_TRANSLATE_HOST,
        "x-rapidapi-key": RAPID_API_KEY,
    }

    payload = {
        "from": source,
        "to": target,
        "q": titles,
    }

    print(f"[→] Translating {len(titles)} title(s) via Rapid Translate API ...")

    resp = requests.post(RAPID_TRANSLATE_URL, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()

    translated = resp.json()  # returns a list of translated strings

    if isinstance(translated, list) and len(translated) == len(titles):
        return translated

    # Fallback: if the response shape is unexpected, return originals
    print("[!] Unexpected API response shape — returning original titles.")
    return titles
