from urllib.parse import urlsplit

import allure
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.common_locators import CommonLocators
from locators.header_locators import HeaderLocators
from urls import BASE_URL


class BasePage:
    path = '/'
    ready_locator = None

    def __init__(self, driver, timeout=25):
        self.driver = driver
        self.timeout = timeout

    def wait(self, condition, message='', timeout=None):
        return WebDriverWait(
            self.driver, self.timeout if timeout is None else timeout,
            ignored_exceptions=(StaleElementReferenceException,),
        ).until(condition, message)

    def visible(self, locator):
        return self.wait(
            lambda d: next((e for e in d.find_elements(*locator) if e.is_displayed()), False),
            f'Не виден элемент {locator}',
        )

    def wait_no_overlay(self):
        self.wait(
            lambda d: all(not e.is_displayed() for e in d.find_elements(*CommonLocators.OVERLAYS)),
            'Не исчезло перекрытие страницы',
        )

    def click(self, locator):
        def click_ready(driver):
            if any(e.is_displayed() for e in driver.find_elements(*CommonLocators.OVERLAYS)):
                return False
            try:
                element = EC.element_to_be_clickable(locator)(driver)
                if not element:
                    return False
                element.click()
                return True
            except ElementClickInterceptedException:
                return False
        self.wait(click_ready, f'Не удалось нажать {locator}')

    def fill(self, locator, value):
        element = self.visible(locator)
        element.clear()
        element.send_keys(value)

    @allure.step('Открыть страницу')
    def open(self):
        self.driver.get(BASE_URL + self.path)
        self.wait_loaded()
        return self

    def wait_loaded(self):
        self.wait(lambda d: urlsplit(d.current_url).path == self.path, f'Ожидался путь {self.path}')
        if self.ready_locator:
            self.visible(self.ready_locator)
        self.wait_no_overlay()
        return self

    def is_open(self):
        self.wait_loaded()
        return urlsplit(self.driver.current_url).path == self.path

    @allure.step('Перейти в конструктор через шапку')
    def go_to_constructor(self):
        self.click(HeaderLocators.CONSTRUCTOR_LINK)

    @allure.step('Перейти в ленту заказов через шапку')
    def go_to_feed(self):
        self.click(HeaderLocators.ORDER_FEED_LINK)

    @allure.step('Перейти в личный кабинет через шапку')
    def go_to_account(self):
        self.click(HeaderLocators.ACCOUNT_LINK)

    @allure.step('Закрыть модальное окно по крестику')
    def close_modal(self):
        # Overlay модалки виден намеренно; общее ожидание overlay здесь неприменимо.
        self.visible(CommonLocators.CLOSE_MODAL).click()
        self.wait(lambda d: all(not e.is_displayed() for e in d.find_elements(*CommonLocators.MODAL)))
