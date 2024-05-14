BTN_BIG_GREEN = "//span[@class='btn_big_green']"
INPUT_USERNAME_FIELD = "//form[@id='login-form']//input[@class='login_vh' and @name='username']"
INPUT_PASSWORD_FIELD = "//form[@id='login-form']//input[@class='login_vh' and @name='password']"

LOGIN = "test_accaunt_4"
PASSWORD = "jkrpjvr6"

BTN_GRIND = "//a[contains(text(), 'Заработок')]"
BTN_YOUTUBE = "//a[contains(text(), 'Youtube')]"

BTN_CHECK_SOLVE = "//span[text()='Пройти проверку']"
BTN_GO_BOTTOM = "//a[@id='Go_Bottom']"
BTN_GO_TOP = "//a[@id='Go_Top']"

RELOAD_MAIL_CAPTCHA = "//a[contains(text(), 'Не вижу код')]"

CREATE_MAIL = "//div[@id='mailbox']/div[contains(@class, 'footer')]/a"

FIELD_FNAME = "//input[@name='fname']"
FIELD_LNAME = "//input[@name='lname']"

FIELD_DAY = "//span[contains(text(), 'День')]"
FIELD_DAY_VALUE = "//div[@data-test-id='select-menu-wrapper']//span[contains(text(), '{}')]"

FIELD_MONTH = "//span[contains(text(), 'Месяц')]"
FIELD_MONTH_VALUE = "//div[@data-test-id='select-menu-wrapper']//div[contains(@class, 'textContainer')]//span[contains(text(), '{}')]"

FIELD_YEAR = "//span[contains(text(), 'Год')]"
FIELD_YEAR_VALUE = "//div[@data-test-id='select-menu-wrapper']//span[contains(text(), '{}')]"

FIELD_RESERVE_MAIL = "//a[contains(text(), 'Указать резервную')]"

CHECKBOX_WOMEN = "//input[@value='female']//ancestor::label//span[contains(text(), 'Женский')]"
CHECKBOX_MEN = "//input[@value='female']//ancestor::label//span[contains(text(), 'Мужской')]"

FIELD_NAME_MAIL = "//input[@name='partial_login']"


LIST_EMAILS = "//div[@data-email and not(contains(@data-email, '@mail') or contains(@data-email, '@internet'))]"
CHOICE_EMAIL = "//div[@data-email]//a[(contains(text(), '{}'))]"

GENERATE_PASSWORD = "//a[contains(text(), 'Сгенерировать')]"

FIELD_PASSWORD = "//input[@name='password']"

CREATE_MAIL_BTN = "//button[@type='submit' and not(@tabindex)]/span[contains(text(), 'Создать')]"

MAIL_CAPTCHA_IMG = "//img[@alt='Код']"

REFRESH_MAIL_CAPTCHA = "//a[contains(text(), 'Не вижу')]"
