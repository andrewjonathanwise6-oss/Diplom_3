from selenium.webdriver.common.by import By


class AccountLocators:
    PROFILE = (By.CSS_SELECTOR, "a[href='/account/profile']")
    EMAIL = (By.XPATH, "//label[normalize-space()='Логин']/following-sibling::input")
    HISTORY_ACTIVE = (By.CSS_SELECTOR, "a[class*='Account_link_active'][href='/account/order-history']")
    HISTORY_LINK = (By.CSS_SELECTOR, "a[href='/account/order-history']")
    LOGOUT = (By.XPATH, "//button[normalize-space()='Выход']")
    HISTORY_LIST = (By.CSS_SELECTOR, "ul[class*='OrderHistory_profileList']")

    @staticmethod
    def order(number):
        return (
            By.XPATH,
            "//a[starts-with(@href,'/account/order-history/')]"
            f"//p[normalize-space()='#0{int(number)}']/ancestor::a[1]",
        )
