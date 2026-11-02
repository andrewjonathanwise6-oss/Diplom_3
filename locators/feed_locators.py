from selenium.webdriver.common.by import By


class FeedLocators:
    LIST = (By.CSS_SELECTOR, "ul[class*='OrderFeed_list__']")
    FIRST_ORDER = (By.CSS_SELECTOR, "a[href^='/feed/']")
    CARD_NUMBER = (By.CSS_SELECTOR, 'p.text_type_digits-default')
    TOTAL = (By.XPATH, "//p[translate(normalize-space(),'ё','е')='Выполнено за все время:']/following-sibling::p")
    TODAY = (By.XPATH, "//p[normalize-space()='Выполнено за сегодня:']/following-sibling::p")
    PROCESSING = (By.CSS_SELECTOR, "ul[class*='OrderFeed_orderListReady']")
    DETAILS_NUMBER = (
        By.CSS_SELECTOR,
        "section[class*='Modal_modal_opened'] div[class*='Modal_orderBox'] > p:first-child",
    )
    DETAILS_NAME = (By.CSS_SELECTOR, "section[class*='Modal_modal_opened'] div[class*='Modal_orderBox'] > h2")

    @staticmethod
    def order(number):
        return (By.XPATH, f"//a[starts-with(@href,'/feed/')]//p[normalize-space()='#0{int(number)}']/ancestor::a[1]")
