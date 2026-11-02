import allure

from locators.feed_locators import FeedLocators
from pages.base_page import BasePage


class FeedPage(BasePage):
    path = '/feed'
    ready_locator = FeedLocators.TOTAL

    @allure.step('Прочитать общий счётчик заказов')
    def total(self):
        return int(self.visible(FeedLocators.TOTAL).text)

    @allure.step('Прочитать счётчик заказов за сегодня')
    def today(self):
        return int(self.visible(FeedLocators.TODAY).text)

    def wait_counter_increase(self, previous, today=False):
        locator = FeedLocators.TODAY if today else FeedLocators.TOTAL

        def increased(elements):
            for element in elements:
                text = element.text
                if element.is_displayed() and text.isdigit() and int(text) > previous:
                    return int(text)
            return False

        return self.wait_for_elements(locator, increased, 'Счётчик ленты не увеличился', timeout=60)

    @allure.step('Открыть первый заказ ленты')
    def open_first_order(self):
        card = self.visible(FeedLocators.FIRST_ORDER)
        number = int(self.text_in_child(card, FeedLocators.CARD_NUMBER).lstrip('#'))
        self.click(FeedLocators.order(number))
        return number

    def details_number(self):
        return int(self.visible(FeedLocators.DETAILS_NUMBER).text.lstrip('#'))

    def details_name(self):
        return self.visible(FeedLocators.DETAILS_NAME).text

    @allure.step('Найти свой заказ в общей ленте')
    def order_number(self, number):
        card = self.visible(FeedLocators.order(number))
        return int(card.find_element(*FeedLocators.CARD_NUMBER).text.lstrip('#'))

    def wait_processing_order(self, number):
        def own_order_visible(elements):
            for element in elements:
                numbers = [int(line.strip()) for line in element.text.splitlines() if line.strip().isdigit()]
                if element.is_displayed() and number in numbers:
                    return numbers
            return False

        return self.wait_for_elements(FeedLocators.PROCESSING, own_order_visible, f'Заказ {number} не появился в разделе «В работе»', timeout=60)
