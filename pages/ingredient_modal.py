import allure

from locators.common_locators import CommonLocators
from locators.ingredient_modal_locators import IngredientModalLocators
from pages.base_page import BasePage


class IngredientModal(BasePage):
    def is_open(self):
        return self.visible(IngredientModalLocators.TITLE).text == 'Детали ингредиента'

    def text(self):
        return self.visible(CommonLocators.MODAL).text

    @allure.step('Закрыть детали ингредиента')
    def close(self):
        self.close_modal()

    def is_closed(self):
        return all(not e.is_displayed() for e in self.driver.find_elements(*CommonLocators.MODAL))
