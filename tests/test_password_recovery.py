import allure

from pages.forgot_password_page import ForgotPasswordPage
from pages.login_page import LoginPage
from pages.reset_password_page import ResetPasswordPage


class TestPasswordRecovery:
    @allure.title('Переход по ссылке «Восстановить пароль»')
    def test_open_password_recovery(self, driver):
        login = LoginPage(driver).open()

        login.go_to_password_recovery()

        assert ForgotPasswordPage(driver).is_open()

    @allure.title('Ввод почты и нажатие «Восстановить» открывают сброс пароля')
    def test_submit_recovery_email(self, driver, user):
        forgot = ForgotPasswordPage(driver).open()

        forgot.restore(user.email)

        assert ResetPasswordPage(driver).is_open()

    @allure.title('Клик по значку пароля активирует и подсвечивает поле')
    def test_password_icon_focuses_and_highlights_field(self, reset_page):
        reset_page.enter_password('NewDiplomPassword123')
        before = reset_page.password_state()

        reset_page.click_password_visibility_icon()
        activated = reset_page.password_state()

        assert not before['focused']
        assert not before['highlighted']
        assert activated['focused']
        assert activated['highlighted']
