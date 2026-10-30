import allure
from selenium.webdriver.common.action_chains import ActionChains

from locators.constructor_locators import ConstructorLocators
from pages.base_page import BasePage


class ConstructorPage(BasePage):
    ready_locator = ConstructorLocators.BUN_CARD

    def _bun(self):
        return self.visible(ConstructorLocators.BUN_CARD)

    def bun_name(self):
        return self._bun().find_element(*ConstructorLocators.CARD_NAME).text

    def bun_counter(self):
        return int(self._bun().find_element(*ConstructorLocators.CARD_COUNTER).text)

    @allure.step('Открыть детали первой булки')
    def open_first_ingredient(self):
        self.click(ConstructorLocators.BUN_CARD)

    @allure.step('Добавить булку в конструктор')
    def add_bun(self):
        self.wait_no_overlay()
        source = self._bun()
        target = self.visible(ConstructorLocators.DROP_ZONE)
        if self.driver.capabilities['browserName'] == 'firefox':
            with allure.step('Firefox: HTML5 DragEvent (проверка обработчиков, не физического жеста)'):
                self._html5_drag(source, target)
        else:
            ActionChains(self.driver).drag_and_drop(source, target).perform()
        self.wait(
            lambda d: d.find_element(*ConstructorLocators.BUN_CARD).find_element(
                *ConstructorLocators.CARD_COUNTER
            ).text == '2',
            'Счётчик булки не стал равен 2',
        )

    def _html5_drag(self, source, target):
        """Обход незавершённого native drag в Firefox/geckodriver.

        Проверяет HTML5/React DnD обработчики приложения, но не физический
        жест мышью. Redux и счётчик не изменяются напрямую.
        """
        self.driver.execute_script('''
            const source = arguments[0], target = arguments[1];
            const transfer = new DataTransfer();
            function fire(node, type) {
                const r = node.getBoundingClientRect();
                node.dispatchEvent(new DragEvent(type, {
                    bubbles: true, cancelable: true, dataTransfer: transfer,
                    clientX: r.x + r.width / 2, clientY: r.y + r.height / 2
                }));
            }
            fire(source, 'dragstart');
            fire(target, 'dragenter');
            fire(target, 'dragover');
            fire(target, 'drop');
            fire(source, 'dragend');
        ''', source, target)

    def constructor_bun_names(self):
        return [e.get_attribute('alt') for e in self.driver.find_elements(*ConstructorLocators.BUN_IMAGES)]

    @allure.step('Оформить заказ через интерфейс')
    def submit_order(self):
        self.click(ConstructorLocators.ORDER_BUTTON)
        # Номер по умолчанию 9999 присутствует в DOM до ответа API.
        number = self.wait(
            lambda d: next((int(e.text) for e in d.find_elements(*ConstructorLocators.ORDER_NUMBER)
                            if e.is_displayed() and e.text.isdigit() and int(e.text) not in (0, 9999)), False),
            'Не получен номер оформленного заказа', timeout=60,
        )
        self.visible(ConstructorLocators.ORDER_CONFIRMATION)
        return number

    def order_confirmation_visible(self):
        return self.visible(ConstructorLocators.ORDER_CONFIRMATION).is_displayed()
