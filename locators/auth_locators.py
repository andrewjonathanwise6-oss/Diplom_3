from selenium.webdriver.common.by import By


class AuthLocators:
    EMAIL = (By.XPATH, "//label[normalize-space()='Email']/following-sibling::input")
    PASSWORD = (By.CSS_SELECTOR, "input[type='password']")
    LOGIN_BUTTON = (By.XPATH, "//button[normalize-space()='Войти']")
    FORGOT_LINK = (By.CSS_SELECTOR, "a[href='/forgot-password']")
    RESTORE_BUTTON = (By.XPATH, "//button[normalize-space()='Восстановить']")
    NEW_PASSWORD = (By.CSS_SELECTOR, "input[name='Введите новый пароль']")
    PASSWORD_ICON = (
        By.XPATH,
        "//input[@name='Введите новый пароль']/following-sibling::div[contains(@class,'input__icon')]",
    )
    PASSWORD_WRAPPER = (
        By.XPATH,
        "//input[@name='Введите новый пароль']"
        "/ancestor::div[contains(concat(' ',normalize-space(@class),' '),' input ')][1]",
    )
    SAVE_BUTTON = (By.XPATH, "//button[normalize-space()='Сохранить']")
