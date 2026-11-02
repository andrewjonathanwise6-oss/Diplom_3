
import allure

from pages.constructor_page import ConstructorPage
from pages.feed_page import FeedPage


class TestNavigation:

    @allure.title('Переход в ленту заказов')
    def test_open_order_feed(self, driver):
        main_page = ConstructorPage(driver)

        main_page.open()
        main_page.go_to_feed()

        assert FeedPage(driver).is_open()

    @allure.title('Переход из ленты заказов в конструктор')
    def test_open_constructor(self, driver):
        main_page = ConstructorPage(driver)
        feed_page = FeedPage(driver)

        main_page.open()
        main_page.go_to_feed()
        feed_page.go_to_constructor()

        assert main_page.is_open()
