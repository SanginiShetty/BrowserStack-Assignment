"""
Analyze translated article headers to find repeated words.

Usage (once translator is implemented):
    from analyzer.word_analyzer import find_repeated_words

    headers = ["Fiscal clarity in rent", "Rent and the market", ...]
    repeated = find_repeated_words(headers, threshold=2)
    # repeated => {"rent": 3, ...}
"""

import re
from collections import Counter

# Common English stop-words to exclude from the analysis
STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "shall", "should", "may", "might", "can", "could", "not", "no", "nor",
    "so", "if", "then", "than", "that", "this", "it", "its", "as", "up",
    "out", "about", "into", "over", "after", "before", "between", "under",
    "again", "there", "here", "when", "where", "how", "all", "each",
    "every", "both", "few", "more", "most", "other", "some", "such",
}


def find_repeated_words(
    headers: list[str],
    threshold: int = 2,
    exclude_stop_words: bool = True,
) -> dict[str, int]:
    """
    Identify words that appear more than *threshold* times across all headers.

    Parameters
    ----------
    headers : list[str]
        Translated article headers (in English).
    threshold : int
        Minimum number of occurrences for a word to be reported (default: 2).
    exclude_stop_words : bool
        Whether to ignore common English stop-words (default: True).

    Returns
    -------
    dict[str, int]
        Mapping of repeated words to their occurrence counts, sorted
        descending by count.
    """
    words: list[str] = []
    for header in headers:
        tokens = re.findall(r"[a-záéíóúñü]+", header.lower())
        if exclude_stop_words:
            tokens = [t for t in tokens if t not in STOP_WORDS]
        words.extend(tokens)

    counter = Counter(words)
    repeated = {word: count for word, count in counter.items() if count > threshold}

    # Sort by count descending
    return dict(sorted(repeated.items(), key=lambda item: item[1], reverse=True))


def print_repeated_words(repeated: dict[str, int]) -> None:
    """Pretty-print the repeated-word analysis results."""
    if not repeated:
        print("[i] No words appear more than twice across all headers.\n")
        return

    print("=" * 50)
    print("  Repeated Words in Translated Headers")
    print("  (words appearing more than twice)")
    print("=" * 50)
    for word, count in repeated.items():
        print(f"    {word:<20s} ×{count}")
    print()


def print_all_word_counts(headers: list[str], exclude_stop_words: bool = True) -> None:
    """Print the count of every word across all headers (for debugging)."""
    words: list[str] = []
    for header in headers:
        tokens = re.findall(r"[a-záéíóúñü]+", header.lower())
        if exclude_stop_words:
            tokens = [t for t in tokens if t not in STOP_WORDS]
        words.extend(tokens)

    counter = Counter(words)
    print("=" * 50)
    print("  All Word Counts (excluding stop words)")
    print("=" * 50)
    for word, count in counter.most_common():
        marker = " <<<" if count > 2 else ""
        print(f"    {word:<20s} ×{count}{marker}")
    print()
