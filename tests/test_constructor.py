
import allure

from pages.constructor_page import ConstructorPage


class TestConstructor:

    @allure.title('Счётчик ингредиента увеличивается после добавления')
    def test_ingredient_counter_increases(self, driver):
        main_page = ConstructorPage(driver)
        main_page.open()

        counter_before = main_page.bun_counter()
        bun_name = main_page.bun_name()

        main_page.add_bun()

        counter_after = main_page.bun_counter()

        assert counter_before == 0
        assert counter_after == 2
        assert main_page.constructor_bun_names() == [f'{bun_name} (верх)', f'{bun_name} (низ)']

    @allure.title('Авторизованный пользователь оформляет заказ')
    def test_authorized_user_can_place_order(self, authenticated):
        authenticated.add_bun()

        number = authenticated.submit_order()

        assert number > 0
        assert authenticated.order_confirmation_visible()
