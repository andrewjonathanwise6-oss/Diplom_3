import allure

from pages.account_page import AccountPage
from pages.login_page import LoginPage
from pages.order_history_page import OrderHistoryPage


class TestAccount:
    @allure.title('Переход в личный кабинет авторизованного пользователя')
    def test_open_account(self, driver, authenticated, user):
        authenticated.go_to_account()
        account = AccountPage(driver)

        assert account.is_open()
        assert account.email() == user.email

    @allure.title('Переход в историю заказов')
    def test_open_order_history(self, driver, authenticated):
        authenticated.go_to_account()
        account = AccountPage(driver).wait_loaded()

        account.go_to_history()

        assert OrderHistoryPage(driver).is_open()

    @allure.title('Выход из аккаунта')
    def test_logout(self, driver, authenticated):
        authenticated.go_to_account()
        account = AccountPage(driver).wait_loaded()

        account.logout()
        login = LoginPage(driver)

        assert login.is_open()
        assert login.tokens_cleared()
