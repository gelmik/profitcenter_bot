import json
import random
import time
from copy import deepcopy
from typing import Iterable, Union

import re
import scrapy
from scrapy import Request, Selector, FormRequest, Spider
from twisted.internet.defer import Deferred

from .constants.reqbot import *
from ..solve import Determinant

from random import randint

from w3lib.url import url_query_parameter
from ..utils import BotData

from datetime import datetime

from enum import Enum


class TaskStatus(Enum):
    undefinded = 0
    in_progress = 1
    ready = 2
    badly = 3


class Task:
    def __init__(self, selector: Selector = None):
        self.status = TaskStatus.undefinded
        self._ids = ""

        if selector:
            self.video_url = selector.xpath(YOUTUBE_TASK_VIDEO_URL).get()
            try:
                self.price = float(selector.xpath(YOUTUBE_TASK_PRICE).get())
            except:
                self.price = selector.xpath(YOUTUBE_TASK_PRICE).get()
            self.review_count = int(selector.xpath(YOUTUBE_TASK_COUNT_REVIEW).get()[1:-1])

            onclick_data = selector.xpath(YOUTUBE_TASK_ONCLICK_DATA).get()
            onclick_data = onclick_data[onclick_data.find('(') + 1:onclick_data.rfind(')')].replace('\'', '')
            onclick_data = onclick_data.split(', ')
            self._id = onclick_data[0]
            self._hash = onclick_data[1]

            desk = "".join(selector.xpath(YOUTUBE_TASK_DESK).getall())
            self.duration = int(re.search(r"Таймер:\s(\d+)\sсекунд", desk).group(1))


        else:
            self.video_url = ''
            self.price = 0
            self.review_count = 0
            self._id = ''
            self._hash = ''
            self.duration = 10

    def __repr__(self):
        return f"id: {self._id}, status: {self.status}, price: {self.price}, video: {self.video_url}"


class ReqParser:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.solver = Determinant()
        self.data = BotData()

    def get_cookies(self, response):
        cookies = {}
        for cookie in response.headers.getlist(b'Set-Cookie'):
            cookie = cookie.decode()
            key, value = cookie[:cookie.find(';')].split('=')
            cookies[key] = value

        return cookies

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

    def solve_captcha(self, response):
        images_selectors = [Selector(text=image) for image in response.xpath(CAPTCHA_IMAGES).getall()]
        data_images = []
        for images_selector in images_selectors:
            base64_image = re.search(r"background-image:url\(data:image/jpg;base64,(.+)\)",
                                     images_selector.xpath("//label/@style").get()).group(1)
            value = images_selector.xpath("//label/input/@value").get()
            data_images.append((self.solver.solve(base64_image), value))
        task = self.captcha_task(response.xpath(CAPTCHA_TASK).get())
        answers = [answer[1] for answer in data_images if answer[0] == task]
        return answers

    def get_tasks(self, response):
        tasks_selectors = [Selector(text=task) for task in response.xpath(YOUTUBE_TASKS).getall()]
        tasks = [Task(selector) for selector in tasks_selectors]
        return tasks


class RegbotSpider(ReqParser, scrapy.Spider):
    name = "register"
    cookies = {'googtrans': None}
    username = ""
    password = ""
    domain = "https://profitcentr.com/"
    tasks = []
    grind_summ = 0
    custom_settings = {
        # 'COOKIES_ENABLED': True,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 1,
            'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': None,
        },
        'DEFAULT_HEADERS': DEFAULT_HEADERS,
    }

    def __init__(self, *args, **kwargs):
        self.host = kwargs['host']
        self.port = kwargs['port']
        self.email = kwargs['email']
        self.username = self.email.split("@")[0][:9].replace('.', '')
        self.proxy = f"http://GfEGR2:IjbL8SVayj@{kwargs['host']}:{kwargs['port']}"
        super().__init__(*args, **kwargs)

    def start_requests(self):
        yield Request(
            "https://profitcentr.com/register",
            callback=self.step_register,
            meta={'dont_merge_cookies': True, "proxy": self.proxy},
            dont_filter=True)

    def step_register(self, response):
        yield from self.step_active(response)
        return
        reqdata = deepcopy(CNST_REG_CAPTCHA_REGISTER)
        reqdata.formdata['username'] = self.username
        reqdata.formdata['email'] = self.email
        reqdata.formdata['capcha[]'] = self.solve_captcha(response)

        yield FormRequest(**reqdata(), callback=self.step_active,
                          cookies=self.cookies,
                          meta={"proxy": self.proxy},
                          dont_filter=True)

    def step_active(self, response):
        from scrapy.shell import open_in_browser
        open_in_browser(response)
        reg_input_href = input("Введите ссылку для активации: ")
        self.password = input("Введите пароль: ")

        reqdata = deepcopy(CNST_REG_CAPTCHA_ACTIVATE)
        reqdata.formdata['id'] = url_query_parameter(reg_input_href, 'id')
        reqdata.formdata['code'] = url_query_parameter(reg_input_href, 'code')
        reqdata.formdata['capcha[]'] = self.solve_captcha(response)

        yield FormRequest(**reqdata(), callback=self.sign_in,
                          cookies=self.cookies,
                          meta={"proxy": self.proxy},
                          dont_filter=True)

    def sign_in(self, response):
        from scrapy.shell import open_in_browser
        open_in_browser(response)
        reqdata = deepcopy(CNST_GET_CAPTCHA)
        reqdata.formdata['username'] = self.username
        reqdata.formdata['password'] = self.password
        reqdata.formdata['capcha[]'] = self.solve_captcha(response)

        yield FormRequest(**reqdata(), callback=self.update_cookies,
                          cookies=self.cookies,
                          meta={"proxy": self.proxy},
                          dont_filter=True)

    def update_cookies(self, response):
        self.connector.create_bot(self.email, self.host, self.port, self.username, self.password)
        self.connector.update_cookies(self.username, json.dumps(self.get_cookies(response)))
        print("SUCCESS")


class ReqbotSpider(ReqParser, scrapy.Spider):
    name = "farm"
    cookies = {'googtrans': None}
    username = ""
    password = ""
    domain = "https://profitcentr.com/"
    tasks = []
    grind_summ = 0
    custom_settings = {
        # 'PROXY': 'http://GfEGR2:IjbL8SVayj@91.188.244.215:3000',
        # 'COOKIES_ENABLED': True,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 1,
            'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': None,
            'profitcenter.middlewares.DelayedRequestsMiddleware': 2,
        },
        'DEFAULT_HEADERS': DEFAULT_HEADERS,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_task_page = 0
        self.username = self.data.login
        self.password = self.data.password
        self.cookies = json.loads(self.data.cookies)
        self.proxy = self.data.proxy
        self.log_task = False
        self.tasks_stack = []

    def start_requests(self):
        if not self.cookies:
            yield Request(**CNST_SIGN_IN(), callback=self.sign_in_step_1,
                          meta={'dont_merge_cookies': True, 'proxy': self.proxy},
                          dont_filter=True)
        else:
            yield Request(**CNST_MEMBERS(), callback=self.members, cookies=self.cookies,
                          meta={'proxy': self.proxy},
                          dont_filter=True)

    def sign_in_step_1(self, response):
        self.cookies.update(self.get_cookies(response))
        for cookie_name in ['newprov_png', 'newprov_etag', 'newprov_cache']:
            self.cookies[cookie_name] = self.cookies['menu_ref']

        reqdata = deepcopy(CNST_GET_CAPTCHA)
        reqdata.formdata['username'] = self.username
        reqdata.formdata['password'] = self.password
        reqdata.formdata['capcha[]'] = self.solve_captcha(response)

        yield FormRequest(**reqdata(), callback=self.sign_in_step_2,
                          cookies=self.cookies,
                          meta={'proxy': self.proxy},
                          dont_filter=True)

    def sign_in_step_2(self, response):
        self.cookies.update(self.get_cookies(response))
        yield Request(**CNST_MEMBERS(), callback=self.members, cookies=self.cookies,
                      dont_filter=True,
                      meta={'proxy': self.proxy})

    def members(self, response):
        self.cookies.update(self.get_cookies(response))
        self.data.update_cookies(self.cookies)
        grind_url = f"{self.domain}{response.xpath(GRIND_URL).get()}"
        yield Request(grind_url, callback=self.grind_page, cookies=self.cookies,
                      dont_filter=True,
                      meta={'proxy': self.proxy})

    def grind_page(self, response):
        self.cookies.update(self.get_cookies(response))
        youtube_url = f"{self.domain}{response.xpath(YOUTUBE_TASK_PAGE_URL).get()}"
        yield Request(youtube_url, callback=self.youtube_task_page, cookies=self.cookies,
                      dont_filter=True,
                      meta={'proxy': self.proxy})

    def youtube_task_page(self, response):
        self.cookies.update(self.get_cookies(response))
        if response.xpath(CAPTCHA_TASK).get():
            need_solve = True
        else:
            need_solve = False

        if need_solve:
            reqdata = deepcopy(CNST_GET_CAPTCHA)
            reqdata.url = response.url
            reqdata.formdata['username'] = self.username
            reqdata.formdata['password'] = self.password
            reqdata.formdata['capcha[]'] = self.solve_captcha(response)

            yield FormRequest(**reqdata(),
                              callback=self.youtube_task_page,
                              cookies=self.cookies,
                              dont_filter=True,
                              meta={'proxy': self.proxy}
                              )
            return

        self.tasks_url = response.url
        self.tasks_hash = url_query_parameter(self.tasks_url, 'hash')
        self.tasks = self.get_tasks(response)
        self.grind_summ = sum([task.price for task in self.tasks])
        print(self.grind_summ)
        # self.current_task_page += 1

        yield from self.grinder()

    def grinder(self):
        if self.tasks:
            if not self.log_task:
                self.logger.info(
                    "№".center(5, ' ') + 'TASK'.center(10, ' ') + "PRICE".center(10, ' ') + "DURATION".center(10, " "))

                for index, task in enumerate(self.tasks, 1):
                    self.logger.info(
                        str(index).center(5, ' ') + str(task._id).center(10, ' ') + str(task.price).center(10,
                                                                                                           ' ') + str(
                            task.duration).center(10, " "))
                self.log_task = True

            if len(self.tasks_stack) < 5:
                for i in range(min(5, len(self.tasks)) - len(self.tasks_stack)):
                    self.tasks_stack.append(self.tasks.pop(0))

                for task in [t for t in self.tasks_stack if t.status == TaskStatus.undefinded]:
                    task.status = TaskStatus.in_progress
                    reqdata = deepcopy(CNST_AJAX_YOUTUBE)
                    reqdata.formdata['id'] = task._id
                    reqdata.formdata['hash'] = task._hash
                    reqdata.headers['Referer'] = self.tasks_url
                    yield FormRequest(**reqdata(),
                                      callback=self.activate_task,
                                      cookies=self.cookies,
                                      dont_filter=True,
                                      meta={'task': task,
                                            'delay_request_by': random.random() * 2 + 1, 'proxy': self.proxy}
                                      )

        else:
            self.log_task = False
            if self.current_task_page <= 6:
                self.current_task_page += 1
            else:
                self.current_task_page = 0
                time_now = datetime.now()
                wait_to = datetime(year=time_now.year, month=time_now.month, day=time_now.day, hour=time_now.hour + 1)
                sleep_seconds = (wait_to - time_now).seconds + random.randint(200, 300)
                self.logger.info(f"SLEEP MINUTS: {sleep_seconds // 60} SECONDS: {sleep_seconds % 60} TO NEXT HOUR")
                time.sleep(sleep_seconds)

                # self.cookies = {}
                # yield from self.start_requests()
                # return

            time.sleep(3)

            # yield Request(**CNST_MEMBERS(), callback=self.members, cookies=self.cookies,
            #                dont_filter=True)
            reqdata = deepcopy(CNST_LOAD_TASK_PAGE)
            reqdata.url = reqdata.url.format(self.tasks_hash)

            reqdata.formdata['pages'] = str(self.current_task_page)

            yield FormRequest(**reqdata(), callback=self.load_tasks_page, cookies=self.cookies, dont_filter=True,
                              meta={'proxy': self.proxy})

    def load_tasks_page(self, response):
        data = response.json()

        if data.get("html_code"):
            page = Selector(text=data.get("html_code"))
            self.tasks = self.get_tasks(page)
            self.tasks = sorted(self.tasks, key=lambda task: task.price, reverse=True)
            self.grind_summ += sum([task.price for task in self.tasks])
            print(self.grind_summ)
        else:
            self.logger.warning(f"Not tasks from {self.current_task_page}")
            # self.current_task_page = randint(1, 5)

        yield from self.grinder()

    def activate_task(self, response):
        data = response.json()
        btn = Selector(text=data['html'])
        task = response.meta['task']
        self.logger.info(f"ACTIVATE Task {task.__repr__()}")
        try:
            task.task_url = re.search(r"\['open_window_ads_in']\('(http:\/\/.+)'\);",
                                      btn.xpath("//span/@onclick").get()).group(1)
            task._ids = url_query_parameter(task.task_url, 'id_status')
            task.id_video = url_query_parameter(task.task_url, 'id_video')
            task.success_hash = url_query_parameter(task.task_url, 'hash')
            yield Request(task.task_url, callback=self.fake_open_video, cookies=self.cookies,
                          meta={'proxy': self.proxy})

            reqdata = deepcopy(CNST_CONFIRM_YOUTUBE_TASK)
            reqdata.formdata['id'] = task._id
            reqdata.formdata['ids'] = task._ids
            reqdata.formdata['hash'] = task.success_hash
            reqdata.formdata['video'] = task.id_video
            reqdata.headers['Referer'] = self.tasks_url
            self.logger.info(f"CONFIRM SEND Task {task.__repr__()}")
            yield FormRequest(**reqdata(),
                              callback=self.success_task,
                              dont_filter=True,
                              meta={'dont_merge_cookies': True, 'task': task, 'delay_request_by': task.duration + 2,
                                    'proxy': self.proxy})
        except:
            yield from self.grinder()

    def success_task(self, response):
        task = response.meta['task']
        self.logger.info(f"CONFIRM Task {task.__repr__()}")
        self.logger.info("".join(response.xpath("//span//text()").getall()))
        task.status = TaskStatus.ready

        value = float(re.search(r'\d\.\d+', "".join(response.xpath("//span//text()").getall())).group(0))
        self.data.add_amount(value)
        if task in self.tasks_stack:
            self.tasks_stack.remove(task)
        else:
            a = 1

        yield from self.grinder()

    def fake_open_video(self, response):
        self.logger.info(f"Fake open {response.url}")

    def close(self, reason: str):
        self.data.close_connection()
        super().close(self, reason)
