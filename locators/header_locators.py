
from selenium.webdriver.common.by import By


class HeaderLocators:
    ORDER_FEED_LINK = (By.CSS_SELECTOR, "a[href$='/feed']")
    CONSTRUCTOR_LINK = (
        By.CSS_SELECTOR,
        "a[class*='AppHeader_header__link'][href='/']"
    )
    ACCOUNT_LINK = (By.CSS_SELECTOR, "header a[href='/account']")
