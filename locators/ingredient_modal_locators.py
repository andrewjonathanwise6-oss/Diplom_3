from selenium.webdriver.common.by import By


class IngredientModalLocators:
    TITLE = (By.CSS_SELECTOR, "section[class*='Modal_modal_opened'] h2[class*='Modal_modal__title']")
