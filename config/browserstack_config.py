"""
BrowserStack credentials and desired-capabilities for cross-browser testing.

Set your credentials via environment variables:
    BROWSERSTACK_USERNAME
    BROWSERSTACK_ACCESS_KEY
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Credentials
# ---------------------------------------------------------------------------
BROWSERSTACK_USERNAME = os.getenv("BROWSERSTACK_USERNAME", "")
BROWSERSTACK_ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY", "")
BROWSERSTACK_URL = (
    f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}"
    f"@hub-cloud.browserstack.com/wd/hub"
)

# ---------------------------------------------------------------------------
# Common capabilities shared across all browsers
# ---------------------------------------------------------------------------
COMMON_CAPS = {
    "bstack:options": {
        "projectName": "El Pais Scraper",
        "buildName": "Opinion Section Test",
        "sessionName": "Cross-Browser Test",
        "debug": True,
        "networkLogs": True,
    }
}

# ---------------------------------------------------------------------------
# Per-browser capability sets (5 total — mix of desktop & mobile)
# ---------------------------------------------------------------------------
BROWSER_CAPS = [
    # Desktop — Chrome (Windows 11)
    {
        "browserName": "Chrome",
        "browserVersion": "latest",
        "bstack:options": {
            **COMMON_CAPS["bstack:options"],
            "os": "Windows",
            "osVersion": "11",
            "sessionName": "Chrome - Windows 11",
        },
    },
    # Desktop — Firefox (Windows 11)
    {
        "browserName": "Firefox",
        "browserVersion": "latest",
        "bstack:options": {
            **COMMON_CAPS["bstack:options"],
            "os": "Windows",
            "osVersion": "11",
            "sessionName": "Firefox - Windows 11",
        },
    },
    # Desktop — Safari (macOS Sonoma)
    {
        "browserName": "Safari",
        "browserVersion": "latest",
        "bstack:options": {
            **COMMON_CAPS["bstack:options"],
            "os": "OS X",
            "osVersion": "Sonoma",
            "sessionName": "Safari - macOS Sonoma",
        },
    },
    # Mobile — iPhone (Safari)
    {
        "browserName": "Safari",
        "bstack:options": {
            **COMMON_CAPS["bstack:options"],
            "deviceName": "iPhone 15",
            "osVersion": "17",
            "realMobile": True,
            "sessionName": "iPhone 15 - Safari",
        },
    },
    # Mobile — Samsung Galaxy (Chrome)
    {
        "browserName": "Chrome",
        "bstack:options": {
            **COMMON_CAPS["bstack:options"],
            "deviceName": "Samsung Galaxy S24",
            "osVersion": "14.0",
            "realMobile": True,
            "sessionName": "Galaxy S24 - Chrome",
        },
    },
]
