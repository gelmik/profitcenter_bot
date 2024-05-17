import io
import random
import re

import httpx
# import pyautogui
import w3lib.url
from PIL import Image
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import base64
import time
import os

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from solve import Determinant
# from hyper.contrib import HTTP20Adapter

from constants import *
from selenium.webdriver.chrome.options import Options
import requests

# from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume



def base64_to_image(base_64, name):
    image = base64.b64decode(base_64)
    with open(fr"images/{name}", 'wb') as f:
        f.write(image)


class Bot:
    def __init__(self, login, password):
        self.login = login
        self.password = password

        options = Options()
        options.page_load_strategy = 'normal'
        options.page_load_strategy = 'eager'
        # options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        driver.fullscreen_window()
        self.wait = WebDriverWait(driver, 3)
        driver.implicitly_wait(3)
        # driver.set_page_load_timeout(3)

        self.driver = driver
        self.solver = Determinant(3, 3)

        self.tasks_url = ""
        self.bad_task = 0
        self.is_new_task = True
        
    def sign_in(self):

        time.sleep(1)
        self.driver.get('https://profitcentr.com')

        time.sleep(2)

        sign_in = self.driver.find_element(By.XPATH, "//a[@class='btn btn_second btn_log']")
        sign_in.click()

        time.sleep(1)

        time.sleep(1)

        self.solve_captcha()

        username_field = self.driver.find_element(By.XPATH, INPUT_USERNAME_FIELD)
        password_field = self.driver.find_element(By.XPATH, INPUT_PASSWORD_FIELD)
        username_field.send_keys(self.login)
        password_field.send_keys(self.password)

        self.driver.find_element(By.XPATH, BTN_BIG_GREEN).click()

        time.sleep(5)

    def get_balance(self):
        balance = self.driver.find_element(By.XPATH, BALANCE)
        print(balance.text)

    def solve_captcha(self):
        images_count = len(self.driver.find_elements(By.XPATH, "(//div[.//form]//div[@class='out-capcha'])[1]/label"))
        answers = []
        task = self.captcha_task(self.driver.find_element(By.XPATH, "//div[@class='out-capcha-title']").text)

        for i in range(images_count):
            image = self.driver.find_element(By.XPATH,
                                        f"((//div[.//form]//div[@class='out-capcha'])[1]/label)[{1 + i}]").get_attribute(
                "style")[45:-2]
            answers.append(self.solver.solve(Image.open(io.BytesIO(base64.b64decode(image)))))

        print(answers)
        answers = [answer == task for answer in answers]
        print(answers)

        for i in range(images_count):
            if answers[i]:
                self.driver.find_element(By.XPATH, f"((//div[.//form]//div[@class='out-capcha'])[1]/label)[{1 + i}]").click()

    def captcha_task(self, text):
        if re.search(r"животным", text):
            return "animal"

        if re.search(r"машин", text):
            return "car"

        if re.search(r"цвет", text):
            return "flower"

        if re.search(r"дорожным", text):
            return "road_sign"

        if re.search(r"мотоцикл", text):
            return "motorcycle"

        if re.search(r"девушк", text):
            return "women"


    def go_to_youtube_task(self):
        time.sleep(2)
        self.driver.get_screenshot_as_file('LambdaTestVisibleScreen.png')
        self.driver.find_element(By.XPATH, BTN_GRIND).click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, BTN_YOUTUBE).click()
        time.sleep(2)
        self.solve_captcha()
        time.sleep(2)
        self.driver.find_element(By.XPATH, BTN_CHECK_SOLVE).click()
        time.sleep(2)

        # try:
        #     while btn := driver.find_element(By.XPATH, BTN_GO_BOTTOM):
        #         btn.click()
        #         time.sleep(1)
        # except:
        #     driver.find_element(By.XPATH, BTN_GO_TOP).click()

        self.tasks_url = self.driver.current_url

    def choice_task(self):
        time.sleep(1)
        self.get_balance()
        btn = self.driver.find_element(By.XPATH, f"(//div[@id='work-youtube']/div//span[@onclick])[{1 + self.bad_task}]")
        self.is_new_task = True
        btn.click()
        time.sleep(1)
        try:
            self.driver.find_element(By.XPATH, f"(//div[@id='work-youtube']/div//span[@onclick])[{1 + self.bad_task}]").click()
            time.sleep(1)
            while len(self.driver.window_handles) > 2:
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.driver.close()

            self.driver.switch_to.window(self.driver.window_handles[1])
        except:
            self.driver.execute_script("window.stop();")

    def solve_task(self):

        time.sleep(2)
        timer = int(w3lib.url.url_query_parameter(self.driver.current_url, 'timer'))
        # timer = max(timer//10, 3)
        # target_url = w3lib.url.add_or_replace_parameter(self.driver.current_url, "timer", str(timer))
        target_url = self.driver.current_url

        try:
            # self.driver.get(target_url)
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//table[@id='start-video']/tbody/tr[2]")))
        except:
            self.driver.execute_script("window.stop();")

        self.driver.switch_to.frame("video-start")
        try:
            time.sleep(1)

            self.driver.find_element(By.XPATH, "//button[@aria-label='Смотреть']").click()

            time.sleep(timer)

            self.driver.switch_to.default_content()

            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, "//button[text()='Подтвердить просмотр']")
            ))
            # self.driver.find_element(By.XPATH, "//button[text()='Подтвердить просмотр']").click()

            header = self.driver.find_element(By.XPATH, "//table[@class='frame_table']")
            self.driver.execute_script("arguments[0].focus();", header)

            # pyautogui.moveTo(x=600, y=600, duration=0.2)
            # pyautogui.moveTo(x=400, y=110, duration=0.2)
            #
            # pyautogui.mouseDown(button='left', x=400, y=110)
            # pyautogui.moveTo(x=450, y=115, duration=0.1)
            # pyautogui.mouseUp(button='left')

            link = self.driver.find_element(By.XPATH, "//button[text()='Подтвердить просмотр']")
            # self.driver.execute_script('arguments[0].click();', link)
            actions = ActionChains(self.driver)
            actions.move_to_element(link).move_by_offset(200, 10).click().perform()
            time.sleep(1)
            actions.click(link).perform()
            time.sleep(2)

        except:
            print("Не удалось выполнить задание")
            if self.is_new_task:
                self.is_new_task = False
                self.bad_task += 1


    def grinded(self):
        while True:
            time.sleep(random.randint(2, 6))
            self.choice_task()
            # self.driver.refresh()
            # time.sleep(random.randint(1, 3))
            self.solve_task()
            retry_count = 0
            try:
                is_solve = bool(self.driver.find_element(By.XPATH, "//span[contains(text(), 'Готово')]"))
                if is_solve:
                    print("Success Task")
            except:
                print("Start retry task")
                is_solve = False
                while not is_solve:
                    self.driver.refresh()
                    self.solve_task()
                    retry_count += 1
                    try:
                        is_solve = bool(self.driver.find_element(By.XPATH, "//span[contains(text(), 'Готово')]"))
                        print(f"Success retry {retry_count}")
                    except:
                        print(f"Retry {retry_count}")
                    if retry_count > 5:
                        print(f"STOP Retry {retry_count}")
                        break

            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])


# def get_tasks():
#     tasks = []
#
#
#     buttons_count = len(driver.find_elements(By.XPATH, "//div[@id='work-youtube']/div//span[@onclick]"))
#
#     for i in range(1, buttons_count + 1):
#         btn = driver.find_element(By.XPATH, f"(//div[@id='work-youtube']/div//span[@onclick])[{i}]")
#         btn_data = btn.get_attribute("onclick")
#         _id = re.search(r"\((\d+),", btn_data).group(1)
#         _hash = re.search(r"\(\d+,\s+\'(\w+)\'", btn_data).group(1)
#
#         data = {
#             'id': _id,
#             'hash': _hash,
#             'func': 'ads-start',
#             'token': '',
#         }
#
#         response = requests.post('https://profitcentr.com/ajax/earnings/ajax-youtube.php',
#                                  cookies=cookies1,
#                                  headers=headers1,
#                                  data=data)
#
#         headers2 = {
#             'accept': '*/*',
#             'Accept-Encoding': 'gzip, deflate, br, zstd',
#             'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
#             'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
#             'origin': 'https://newprofitplus.blogspot.com',
#             'referer': 'https://newprofitplus.blogspot.com/',
#             'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
#             'sec-ch-ua-mobile': '?0',
#             'sec-ch-ua-platform': '"Windows"',
#             'sec-fetch-dest': 'empty',
#             'sec-fetch-mode': 'cors',
#             'sec-fetch-site': 'cross-site',
#             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
#         }
#
#         rdata = response.json()['html']
#
#         _id_video = re.search(r"id_video=(\w+)", rdata).group(1)
#         _ids = re.search(r"id_status=(\d+)", rdata).group(1)
#         _hash = re.search(r"hash=(\w+)", rdata).group(1)
#         data = {
#             'func': 'ads-status',
#             'code': '1',
#             'hash': _hash,
#             'ids': _ids,
#             'id': _id,
#             'video': _id_video,
#         }
#         try:
#             with httpx.Client(http2=True, timeout=5) as client:
#                 r = client.post('https://profitcentr.com/ajax/earnings/ajax-youtube-in.php',
#                                 headers=headers2,
#                                 data=data)
#         except:
#             pass
#         time.sleep(5)
#         print("TEXT", r.text)
#         while not r.text:
#             try:
#                 with httpx.Client(http2=True, timeout=5) as client:
#                     r = client.post('https://profitcentr.com/ajax/earnings/ajax-youtube-in.php',
#                                     headers=headers2,
#                                     data=data)
#                     print("TEXT", r.text)
#                     time.sleep(5)
#             except:
#                 pass
#         a = 1
#
#     return tasks

bot = Bot(LOGIN, PASSWORD)

bot.sign_in()
bot.go_to_youtube_task()
bot.grinded()