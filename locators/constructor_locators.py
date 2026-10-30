
from selenium.webdriver.common.by import By


class ConstructorLocators:
    DROP_ZONE = (
        By.CSS_SELECTOR,
        "section[class*='BurgerConstructor_basket__']"
    )
    BUN_CARD = (
        By.XPATH,
        "//h2[normalize-space()='Булки']/following-sibling::ul[1]//a[contains(@href,'/ingredient/')]",
    )
    CARD_NAME = (By.CSS_SELECTOR, "p[class*='ingredient__text']")
    CARD_COUNTER = (By.CSS_SELECTOR, "p[class*='counter_counter__num']")
    ORDER_BUTTON = (By.XPATH, "//button[normalize-space()='Оформить заказ']")
    BUN_IMAGES = (By.CSS_SELECTOR, "section[class*='BurgerConstructor_basket__'] .constructor-element__image")
    ORDER_NUMBER = (By.CSS_SELECTOR, "section[class*='Modal_modal_opened'] h2[class*='Modal_modal__title_shadow']")
    ORDER_CONFIRMATION = (
        By.XPATH,
        "//section[contains(@class,'Modal_modal_opened')]//p[normalize-space()='Ваш заказ начали готовить']",
    )
