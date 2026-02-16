# El País Opinion Section Scraper

Selenium-based scraper that fetches articles from the **Opinion** section of [El País](https://elpais.com/opinion/), translates headers to English via the Rapid Translate API, analyzes word frequency, and runs cross-browser tests on BrowserStack across 5 parallel sessions (desktop + mobile).

---

## Project Structure

```
BrowserStack/
├── .env                         # Credentials (not committed — see below)
├── config/
│   ├── settings.py              # URLs, paths, constants, API config
│   └── browserstack_config.py   # BrowserStack credentials & 5 capability sets
├── scraper/
│   ├── driver_factory.py        # WebDriver setup (local Chrome & BrowserStack remote)
│   ├── cookie_handler.py        # Didomi cookie-consent dismissal
│   ├── article_scraper.py       # Article scraping (title, content, image)
│   └── image_downloader.py      # Image download helper
├── translator/
│   └── header_translator.py     # Translate headers (ES → EN) via Rapid Translate API
├── analyzer/
│   └── word_analyzer.py         # Find repeated words in translated headers
├── output/
│   ├── article_images/          # Downloaded cover images
│   ├── articles/                # Saved article .txt files
│   └── articles.json            # All articles in JSON format
├── main.py                      # Local single-browser entry point
├── browserstack_runner.py       # BrowserStack parallel execution (5 threads, auto-retry)
├── requirements.txt
└── README.md
```

---

## Prerequisites

- Python 3.10+
- Google Chrome (for local runs)
- A [BrowserStack](https://www.browserstack.com/) account (for cross-browser runs)
- A [RapidAPI](https://rapidapi.com/) key subscribed to **Rapid Translate Multi Traduction**

---

## Environment Variables

Create a `.env` file in the project root with the following keys:

```env
# BrowserStack Credentials
BROWSERSTACK_USERNAME=your_browserstack_username
BROWSERSTACK_ACCESS_KEY=your_browserstack_access_key

# Rapid Translate API (RapidAPI)
RAPID_API_KEY=your_rapidapi_key_here
```

> **Note:** Never commit `.env` to version control. Add it to your `.gitignore`.

---

## Quick Start

### 1. Create a virtual environment & install dependencies

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Run locally (single browser)

```bash
python main.py
```

This will:
- Open El País Opinion section in headless Chrome
- Verify the page is in Spanish (`es-ES`)
- Scrape the first 5 articles (title, content, cover image)
- Download cover images to `output/article_images/`
- Save articles to `output/articles/` and `output/articles.json`
- Translate all 5 headers from Spanish to English
- Analyze translated headers for repeated words (threshold > 2)

### 3. Run on BrowserStack (5 parallel sessions)

```bash
python browserstack_runner.py
```

This will:
- Launch **5 parallel** BrowserStack sessions across desktop and mobile browsers
- Scrape 5 articles on each session and verify results
- **Automatically retry** failed sessions up to 3 times (handles real-device flakiness)
- Translate headers and run word analysis after all sessions complete
- Print a pass/fail summary for each session

#### BrowserStack Test Matrix

| # | Browser | OS / Device       |
|---|---------|-------------------|
| 1 | Chrome  | Windows 11        |
| 2 | Firefox | Windows 11        |
| 3 | Safari  | macOS Sonoma      |
| 4 | Safari  | iPhone 15 (iOS 17)|
| 5 | Chrome  | Galaxy S24 (Android 14) |

---

## Features

| Feature                        | Status         |
|--------------------------------|----------------|
| Scrape Opinion articles        | ✅ Implemented |
| Verify Spanish language        | ✅ Implemented |
| Download cover images          | ✅ Implemented |
| Save to JSON + text files      | ✅ Implemented |
| Translate headers (ES → EN)    | ✅ Implemented |
| Analyze repeated words         | ✅ Implemented |
| BrowserStack cross-browser     | ✅ Implemented (5 sessions, auto-retry) |
| Credentials in `.env`          | ✅ Implemented |

---

## Configuration

- **`config/settings.py`** — Change `MAX_ARTICLES`, output paths, API URL/host.
- **`config/browserstack_config.py`** — Modify browser/device capabilities or add new sessions.
- **`.env`** — Store BrowserStack and RapidAPI credentials (loaded via `python-dotenv`).
