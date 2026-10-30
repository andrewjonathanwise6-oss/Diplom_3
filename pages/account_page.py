import allure

from locators.account_locators import AccountLocators
from pages.base_page import BasePage


class AccountPage(BasePage):
    path = '/account/profile'
    ready_locator = AccountLocators.EMAIL

    def email(self):
        return self.visible(AccountLocators.EMAIL).get_attribute('value')

    @allure.step('Перейти в историю заказов')
    def go_to_history(self):
        self.click(AccountLocators.HISTORY_LINK)

    @allure.step('Выйти из аккаунта')
    def logout(self):
        self.click(AccountLocators.LOGOUT)
