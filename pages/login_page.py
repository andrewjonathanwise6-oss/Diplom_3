import allure

from locators.auth_locators import AuthLocators
from pages.base_page import BasePage


class LoginPage(BasePage):
    path = '/login'
    ready_locator = AuthLocators.LOGIN_BUTTON

    @allure.step('Авторизоваться временным пользователем через UI')
    def login(self, user):
        self.fill(AuthLocators.EMAIL, user.email)
        self.fill(AuthLocators.PASSWORD, user.password)
        self.click(AuthLocators.LOGIN_BUTTON)

    @allure.step('Нажать «Восстановить пароль»')
    def go_to_password_recovery(self):
        self.click(AuthLocators.FORGOT_LINK)

    def tokens_cleared(self):
        return self.execute_script(
            "return !localStorage.getItem('accessToken') && !localStorage.getItem('refreshToken')"
        )
