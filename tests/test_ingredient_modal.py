
import allure

from pages.constructor_page import ConstructorPage
from pages.ingredient_modal import IngredientModal


class TestIngredientModal:

    @allure.title('Открытие деталей ингредиента')
    def test_open_ingredient_details(self, driver):
        main_page = ConstructorPage(driver)
        ingredient_modal = IngredientModal(driver)

        main_page.open()
        ingredient_name = main_page.bun_name()
        main_page.open_first_ingredient()

        assert ingredient_modal.is_open()
        assert ingredient_name in ingredient_modal.text()

    @allure.title('Закрытие деталей ингредиента по крестику')
    def test_close_ingredient_details(self, driver):
        main_page = ConstructorPage(driver)
        ingredient_modal = IngredientModal(driver)

        main_page.open()
        main_page.open_first_ingredient()
        ingredient_modal.close()

        assert ingredient_modal.is_closed()
