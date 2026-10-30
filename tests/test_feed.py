import allure

from pages.account_page import AccountPage
from pages.feed_page import FeedPage
from pages.order_history_page import OrderHistoryPage


class TestFeed:
    @allure.title('Клик по заказу в ленте открывает его детали')
    def test_open_order_details(self, driver):
        feed = FeedPage(driver).open()

        number = feed.open_first_order()

        assert feed.details_number() == number
        assert feed.details_name()

    @allure.title('Заказ из истории пользователя отображается в общей ленте')
    def test_user_history_order_is_in_feed(self, driver, authenticated):
        authenticated.add_bun()
        number = authenticated.submit_order()
        authenticated.close_modal()
        authenticated.go_to_account()
        AccountPage(driver).wait_loaded().go_to_history()
        history = OrderHistoryPage(driver).wait_loaded()
        history_number = history.order_number(number)

        history.go_to_feed()
        feed = FeedPage(driver).wait_loaded()

        assert history_number == number
        assert feed.order_number(number) == history_number

    @allure.title('После нового заказа увеличивается «Выполнено за всё время»')
    def test_total_increases_after_order(self, driver, authenticated):
        authenticated.go_to_feed()
        feed = FeedPage(driver).wait_loaded()
        before = feed.total()
        feed.go_to_constructor()
        authenticated.wait_loaded().add_bun()

        number = authenticated.submit_order()
        authenticated.close_modal()
        authenticated.go_to_feed()
        feed.wait_loaded()
        after = feed.wait_counter_increase(before)

        assert feed.order_number(number) == number
        assert after > before

    @allure.title('После нового заказа увеличивается «Выполнено за сегодня»')
    def test_today_increases_after_order(self, driver, authenticated):
        authenticated.go_to_feed()
        feed = FeedPage(driver).wait_loaded()
        before = feed.today()
        feed.go_to_constructor()
        authenticated.wait_loaded().add_bun()

        number = authenticated.submit_order()
        authenticated.close_modal()
        authenticated.go_to_feed()
        feed.wait_loaded()
        after = feed.wait_counter_increase(before, today=True)

        assert feed.order_number(number) == number
        assert after > before

    @allure.title('Номер оформленного заказа появляется в разделе «В работе»')
    def test_order_number_appears_in_processing(self, driver, authenticated):
        authenticated.add_bun()

        number = authenticated.submit_order()
        authenticated.close_modal()
        authenticated.go_to_feed()
        feed = FeedPage(driver).wait_loaded()
        processing = feed.wait_processing_order(number)

        assert number in processing
