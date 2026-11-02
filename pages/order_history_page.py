from locators.account_locators import AccountLocators
from locators.feed_locators import FeedLocators
from pages.base_page import BasePage


class OrderHistoryPage(BasePage):
    path = '/account/order-history'
    ready_locator = AccountLocators.HISTORY_ACTIVE

    def wait_loaded(self):
        super().wait_loaded()
        # Пустой список нового пользователя имеет нулевую высоту.
        self.wait(lambda d: d.find_elements(*AccountLocators.HISTORY_LIST))
        return self

    def order_number(self, number):
        card = self.visible(AccountLocators.order(number))
        return int(card.find_element(*FeedLocators.CARD_NUMBER).text.lstrip('#'))
