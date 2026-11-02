from urllib.parse import urlsplit

import allure
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
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

    def find_all(self, locator):
        return self.driver.find_elements(*locator)

    def wait_for_elements(self, locator, evaluate, message='', timeout=None):
        return self.wait(lambda driver: evaluate(driver.find_elements(*locator)), message, timeout)

    def text_in_child(self, element, locator):
        return element.find_element(*locator).text

    def execute_script(self, script, *args):
        return self.driver.execute_script(script, *args)

    def is_firefox(self):
        return self.driver.capabilities['browserName'] == 'firefox'

    def drag_and_drop(self, source, target):
        ActionChains(self.driver).drag_and_drop(source, target).perform()

    def active_element(self):
        return self.driver.switch_to.active_element

    def bun_counter_equals(self, card_locator, counter_locator, expected):
        def matches(elements):
            return any(
                card.find_element(*counter_locator).text == str(expected)
                for card in elements if card.is_displayed()
            )
        return self.wait_for_elements(card_locator, matches, 'Счётчик булки не изменился')

    def wait_order_number(self, locator):
        def order_number(elements):
            return next(
                (int(e.text) for e in elements
                 if e.is_displayed() and e.text.isdigit() and int(e.text) not in (0, 9999)),
                False
            )
        return self.wait_for_elements(locator, order_number, 'Не получен номер заказа', 60)

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
        # Затемнение является частью открытой модалки: обычный click() ждёт его
        # исчезновения и здесь неприменим. Firefox может кратковременно
        # перехватывать клик во время анимации, поэтому повторяем нативный клик.
        def close_when_clickable(driver):
            button = EC.element_to_be_clickable(CommonLocators.CLOSE_MODAL)(driver)
            if not button:
                return False
            try:
                button.click()
                return True
            except ElementClickInterceptedException:
                return False

        self.wait(close_when_clickable, 'Крестик модального окна остаётся перекрытым')
        self.wait(
            lambda d: all(not e.is_displayed() for e in d.find_elements(*CommonLocators.MODAL)),
            'Модальное окно не закрылось',
        )
