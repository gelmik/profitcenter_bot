import random
import time
import urllib

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

from person import Person, Sex
from constants import *

DOMAIN_MAIL = "https://mail.ru"


class RegisterBot:
    def __init__(self):

        options = Options()
        # options.page_load_strategy = 'normal'
        options.page_load_strategy = 'eager'
        driver = webdriver.Chrome(options=options)
        driver.fullscreen_window()
        self.wait = WebDriverWait(driver, 3)
        driver.implicitly_wait(3)
        # driver.set_page_load_timeout(3)
        self.delay_action = 0.5
        self.driver = driver
        # self.solver = Determinant(3, 3)

        self.tasks_url = ""
        self.bad_task = 0

    def register_mail(self):
        self.driver.get(DOMAIN_MAIL)

        self.driver.find_element(By.XPATH, CREATE_MAIL).click()

        time.sleep(2)

        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[-1])

        person = Person()

        self.input_person_data(person)

        print(person)
        self.driver.find_element(By.XPATH, CREATE_MAIL_BTN).click()

        a = 1

        # time.sleep(self.delay_action*4)
        # for i in range(2000):
        #
        #     with open(f"mail_images/{random.randint(10*10, 10**20)}.png", 'wb') as file:
        #         file.write(self.driver.find_element(By.XPATH, MAIL_CAPTCHA_IMG).screenshot_as_png)
        #     time.sleep(1)
        #     self.driver.find_element(By.XPATH, RELOAD_MAIL_CAPTCHA).click()
        #     time.sleep(1)



    def input_person_data(self, person):
        self.fill_name(person)
        time.sleep(self.delay_action)
        self.fill_birthday(person)
        time.sleep(self.delay_action)
        self.fill_sex(person)
        time.sleep(self.delay_action)
        self.click_reserve_mail()
        self.fill_email(person)
        time.sleep(self.delay_action)
        self.fill_password(person)
        time.sleep(self.delay_action)


    def click_reserve_mail(self):
        while True:
            try:
                self.driver.find_element(By.XPATH, FIELD_RESERVE_MAIL).click()
                break
            except Exception as e:
                print(e)
                self.driver.refresh()

    def fill_name(self, person):
        fname_field = self.driver.find_element(By.XPATH, FIELD_FNAME)
        fname_field.send_keys(person.name)

        lname_field = self.driver.find_element(By.XPATH, FIELD_LNAME)
        lname_field.send_keys(person.second_name)

    def fill_birthday(self, person):
        self.driver.find_element(By.XPATH, FIELD_DAY).click()

        self.driver.find_element(By.XPATH, FIELD_DAY_VALUE.format(person.birthday.day)).click()

        self.driver.find_element(By.XPATH, FIELD_MONTH).click()

        self.driver.find_element(By.XPATH, FIELD_MONTH_VALUE.format(person.birthday.strftime("%B"))).click()

        self.driver.find_element(By.XPATH, FIELD_YEAR).click()

        self.driver.find_element(By.XPATH, FIELD_YEAR_VALUE.format(person.birthday.year)).click()


    def fill_sex(self, person):
        if person.sex == Sex.male:
            self.driver.find_element(By.XPATH, CHECKBOX_MEN).click()
        elif person.sex == Sex.female:
            self.driver.find_element(By.XPATH, CHECKBOX_WOMEN).click()

    def fill_email(self, person):
        self.driver.find_element(By.XPATH, FIELD_NAME_MAIL).click()

        time.sleep(1)

        emails = [email.get_attribute("data-email") for email in self.driver.find_elements(By.XPATH, LIST_EMAILS)]

        person.email = random.choice(emails)

        self.driver.find_element(By.XPATH, CHOICE_EMAIL.format(person.email)).click()

    def fill_password(self, person):
        self.driver.find_element(By.XPATH, GENERATE_PASSWORD).click()

        person.password = self.driver.find_element(By.XPATH, FIELD_PASSWORD).get_attribute("value")

regbot = RegisterBot()

regbot.register_mail()


a=1
