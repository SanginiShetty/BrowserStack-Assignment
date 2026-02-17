"""
WebDriver factory — creates a Selenium driver for local or BrowserStack runs.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from config.browserstack_config import BROWSERSTACK_URL


def create_local_driver(*, headless: bool = True):
    """Return a Chrome WebDriver configured for the Spanish locale.

    Parameters
    ----------
    headless : bool
        Run Chrome in headless mode for speed (default: True).
    """
    options = Options()
    options.add_argument("--lang=es")
    options.add_argument("--accept-lang=es")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-images")  # skip image rendering
    options.add_argument("--blink-settings=imagesEnabled=false")  # faster
    if headless:
        options.add_argument("--headless=new")
    options.page_load_strategy = "eager"  # don't wait for full load
    options.add_experimental_option("prefs", {"intl.accept_languages": "es,es-ES"})

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    return driver


def create_browserstack_driver(capabilities: dict):
    """Return a Remote WebDriver pointing at BrowserStack with *capabilities*."""
    options = _caps_to_options(capabilities)
    options.page_load_strategy = "eager"  # don't wait for full page load
    driver = webdriver.Remote(
        command_executor=BROWSERSTACK_URL,
        options=options,
    )
    driver.implicitly_wait(3)
    return driver


def _caps_to_options(capabilities: dict):
    """Convert a capabilities dict to a Chrome/Firefox/Safari Options object."""
    browser = capabilities.get("browserName", "Chrome").lower()
    if browser == "firefox":
        opts = webdriver.FirefoxOptions()
    elif browser == "safari":
        opts = webdriver.SafariOptions()
    else:
        opts = Options()

    for key, value in capabilities.items():
        if key == "browserName":
            continue
        opts.set_capability(key, value)

    return opts
