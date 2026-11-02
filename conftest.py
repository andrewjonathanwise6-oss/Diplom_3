import json

import allure
import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from helpers.api_client import ApiClient, TestUser
from locators.constructor_locators import ConstructorLocators
from pages.constructor_page import ConstructorPage
from pages.forgot_password_page import ForgotPasswordPage
from pages.login_page import LoginPage
from pages.reset_password_page import ResetPasswordPage


def pytest_addoption(parser):
    parser.addoption('--browser', choices=('chrome', 'firefox', 'all'), default='all')
    parser.addoption('--headless', action='store_true', help='Запустить браузеры без окна')


def pytest_generate_tests(metafunc):
    if 'driver' in metafunc.fixturenames:
        choice = metafunc.config.getoption('--browser')
        browsers = ['chrome', 'firefox'] if choice == 'all' else [choice]
        metafunc.parametrize('driver', browsers, indirect=True, ids=browsers)


@pytest.fixture
def driver(request):
    browser_name = request.param
    options = webdriver.ChromeOptions() if browser_name == 'chrome' else webdriver.FirefoxOptions()
    if request.config.getoption('--headless'):
        options.add_argument('--headless=new' if browser_name == 'chrome' else '-headless')
    factory = webdriver.Chrome if browser_name == 'chrome' else webdriver.Firefox
    browser = factory(options=options)
    try:
        browser.set_window_size(1440, 900)
        browser.set_page_load_timeout(45)
        allure.dynamic.parameter('browser', browser_name)
        allure.attach(
            json.dumps(
                {k: browser.capabilities.get(k) for k in ('browserName', 'browserVersion', 'platformName')},
                indent=2,
            ),
            'Browser', allure.attachment_type.JSON,
        )
        yield browser
    finally:
        browser.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    report = (yield).get_result()
    if report.failed:
        browser = item.funcargs.get('driver')
        if browser:
            attach_failure(browser, report.when)


def attach_failure(browser, phase):
    try:
        allure.attach(browser.get_screenshot_as_png(), f'Failure ({phase})', allure.attachment_type.PNG)
        allure.attach(browser.current_url, 'Current URL', allure.attachment_type.TEXT)
    except WebDriverException as error:
        allure.attach(type(error).__name__, 'Screenshot unavailable', allure.attachment_type.TEXT)


@pytest.fixture
def user(request):
    client = ApiClient()
    account = TestUser.unique()

    def cleanup():
        try:
            with allure.step('Удалить временного пользователя через API'):
                result = client.delete_user(account)
                allure.attach(result, 'User cleanup', allure.attachment_type.TEXT)
        except Exception:
            browser = request.node.funcargs.get('driver')
            if browser:
                attach_failure(browser, 'user cleanup')
            raise
        finally:
            client.close()

    request.addfinalizer(cleanup)
    with allure.step('Создать уникального временного пользователя через API'):
        client.register(account)
    return account


@pytest.fixture
def authenticated(driver, user):
    login = LoginPage(driver).open()
    login.login(user)
    constructor = ConstructorPage(driver).wait_loaded()
    constructor.visible(ConstructorLocators.ORDER_BUTTON)
    return constructor


@pytest.fixture
def reset_page(driver, user):
    ForgotPasswordPage(driver).open().restore(user.email)
    return ResetPasswordPage(driver).wait_loaded()
