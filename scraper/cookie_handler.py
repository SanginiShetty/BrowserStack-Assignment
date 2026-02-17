"""
Handle the cookie-consent banner that El País displays on first visit.
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def accept_cookies(driver, timeout: int = 5):
    """Click the 'Accept' button on the Didomi cookie banner, if present."""
    try:
        accept_btn = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button"))
        )
        accept_btn.click()
    except Exception:
        pass  # Banner may not appear or was already dismissed
