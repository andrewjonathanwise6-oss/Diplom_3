from selenium.webdriver.common.by import By


class CommonLocators:
    MODAL = (By.CSS_SELECTOR, "section[class*='Modal_modal_opened'] div[class*='Modal_modal__container']")
    CLOSE_MODAL = (By.CSS_SELECTOR, "section[class*='Modal_modal_opened'] button[class*='Modal_modal__close']")
    OVERLAYS = (By.CSS_SELECTOR, "div[class*='Modal_modal_overlay']")
    HEADING = (By.CSS_SELECTOR, 'h2')
