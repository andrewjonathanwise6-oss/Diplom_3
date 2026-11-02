import allure

from locators.constructor_locators import ConstructorLocators
from pages.base_page import BasePage


class ConstructorPage(BasePage):
    ready_locator = ConstructorLocators.BUN_CARD

    def _bun(self):
        return self.visible(ConstructorLocators.BUN_CARD)

    def bun_name(self):
        return self.text_in_child(self._bun(), ConstructorLocators.CARD_NAME)

    def bun_counter(self):
        return int(self.text_in_child(self._bun(), ConstructorLocators.CARD_COUNTER))

    @allure.step('Открыть детали первой булки')
    def open_first_ingredient(self):
        self.click(ConstructorLocators.BUN_CARD)

    @allure.step('Добавить булку в конструктор')
    def add_bun(self):
        self.wait_no_overlay()
        source = self._bun()
        target = self.visible(ConstructorLocators.DROP_ZONE)
        if self.is_firefox():
            with allure.step('Firefox: HTML5 DragEvent (проверка обработчиков, не физического жеста)'):
                self._html5_drag(source, target)
        else:
            self.drag_and_drop(source, target)
        self.bun_counter_equals(ConstructorLocators.BUN_CARD, ConstructorLocators.CARD_COUNTER, 2)

    def _html5_drag(self, source, target):
        """Обход незавершённого native drag в Firefox/geckodriver.

        Проверяет HTML5/React DnD обработчики приложения, но не физический
        жест мышью. Redux и счётчик не изменяются напрямую.
        """
        self.execute_script('''
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
        return [e.get_attribute('alt') for e in self.find_all(ConstructorLocators.BUN_IMAGES)]

    @allure.step('Оформить заказ через интерфейс')
    def submit_order(self):
        self.click(ConstructorLocators.ORDER_BUTTON)
        # Номер по умолчанию 9999 присутствует в DOM до ответа API.
        number = self.wait_order_number(ConstructorLocators.ORDER_NUMBER)
        self.visible(ConstructorLocators.ORDER_CONFIRMATION)
        return number

    def order_confirmation_visible(self):
        return self.visible(ConstructorLocators.ORDER_CONFIRMATION).is_displayed()
