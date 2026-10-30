import allure

from locators.auth_locators import AuthLocators
from pages.base_page import BasePage


class ForgotPasswordPage(BasePage):
    path = '/forgot-password'
    ready_locator = AuthLocators.RESTORE_BUTTON

    @allure.step('Ввести почту временного пользователя и нажать «Восстановить»')
    def restore(self, email):
        self.fill(AuthLocators.EMAIL, email)
        self.click(AuthLocators.RESTORE_BUTTON)
