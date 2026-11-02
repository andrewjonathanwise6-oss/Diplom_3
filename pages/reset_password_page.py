import allure

from locators.auth_locators import AuthLocators
from locators.common_locators import CommonLocators
from pages.base_page import BasePage


class ResetPasswordPage(BasePage):
    path = '/reset-password'
    ready_locator = AuthLocators.SAVE_BUTTON

    def enter_password(self, password):
        self.fill(AuthLocators.NEW_PASSWORD, password)
        # Снимаем фокус, чтобы следующий шаг проверял именно нажатие значка.
        self.visible(CommonLocators.HEADING).click()

    @allure.step('Нажать значок показа или скрытия пароля')
    def click_password_visibility_icon(self):
        self.click(AuthLocators.PASSWORD_ICON)

    def password_state(self):
        field = self.visible(AuthLocators.NEW_PASSWORD)
        wrapper = self.visible(AuthLocators.PASSWORD_WRAPPER)
        return {
            'type': field.get_attribute('type'),
            'focused': field == self.active_element(),
            'highlighted': 'input_status_active' in wrapper.get_attribute('class').split(),
        }
