import time
from copy import deepcopy
from typing import Iterable

import re
import scrapy
from scrapy import Request, Selector, FormRequest

from .constants.reqbot import *
from ..solve import Determinant

from random import randint

from w3lib.url import url_query_parameter

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


class ReqbotSpider(ReqParser, scrapy.Spider):
    name = "reqbot"
    cookies = {'googtrans': None}
    username = ""
    password = ""
    domain = "https://profitcentr.com/"
    tasks = []
    grind_summ = 0
    custom_settings = {
        # 'PROXY': '127.0.0.1:8080',
        # 'COOKIES_ENABLED': True,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 1,
            'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': None,
        },
        'DEFAULT_HEADERS': DEFAULT_HEADERS,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_task_page = 0
        self.username = kwargs['username']
        self.password = kwargs['password']
        self.log_task = False

    def start_requests(self):
        yield Request(**CNST_SIGN_IN(), callback=self.sign_in_step_1,
                      meta={'dont_merge_cookies': True},
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
                           dont_filter=True)

    def sign_in_step_2(self, response):
        self.cookies.update(self.get_cookies(response))
        yield Request(**CNST_MEMBERS(), callback=self.members, cookies=self.cookies,
                       dont_filter=True)

    def members(self, response):
        self.cookies.update(self.get_cookies(response))
        grind_url = f"{self.domain}{response.xpath(GRIND_URL).get()}"
        yield Request(grind_url, callback=self.grind_page, cookies=self.cookies,
                       dont_filter=True)

    def grind_page(self, response):
        self.cookies.update(self.get_cookies(response))
        youtube_url = f"{self.domain}{response.xpath(YOUTUBE_TASK_PAGE_URL).get()}"
        yield Request(youtube_url, callback=self.youtube_task_page, cookies=self.cookies,
                       dont_filter=True)

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
                self.logger.info("№".center(5, ' ') + 'TASK'.center(10, ' ') + "PRICE".center(10, ' '))
                for index, task in enumerate(self.tasks, 1):
                    self.logger.info(str(index).center(5, ' ') + str(task._id).center(10, ' ') + str(task.price).center(10, ' '))
                self.log_task = True
            self.current_task: Task = self.tasks.pop(0)

            reqdata = deepcopy(CNST_AJAX_YOUTUBE)
            reqdata.formdata['id'] = self.current_task._id
            reqdata.formdata['hash'] = self.current_task._hash
            reqdata.headers['Referer'] = self.tasks_url

            yield FormRequest(**reqdata(),
                              callback=self.activate_task,
                              cookies=self.cookies,
                              dont_filter=True,
                              )
        else:
            # yield Request(**CNST_MEMBERS(), callback=self.members, cookies=self.cookies,
            #                dont_filter=True)

            self.log_task = False
            if self.current_task_page < 8:
                self.current_task_page += 1
            else:
                self.current_task_page = 1
                self.cookies = {}
                yield from self.start_requests()
                return

            time.sleep(3)

            # yield Request(**CNST_MEMBERS(), callback=self.members, cookies=self.cookies,
            #                dont_filter=True)
            reqdata = deepcopy(CNST_LOAD_TASK_PAGE)
            reqdata.url = reqdata.url.format(self.tasks_hash)

            reqdata.formdata['pages'] = str(self.current_task_page)

            yield FormRequest(**reqdata(), callback=self.load_tasks_page, cookies=self.cookies, dont_filter=True)


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
        try:
            self.current_task.task_url = re.search(r"\['open_window_ads_in']\('(http:\/\/.+)'\);",
                                                   btn.xpath("//span/@onclick").get()).group(1)
            self.current_task._ids = url_query_parameter(self.current_task.task_url, 'id_status')
            self.current_task.id_video = url_query_parameter(self.current_task.task_url, 'id_video')
            self.current_task.success_hash = url_query_parameter(self.current_task.task_url, 'hash')
            yield Request(self.current_task.task_url, callback=self.fake_open_video, cookies=self.cookies)

            reqdata = deepcopy(CNST_CONFIRM_YOUTUBE_TASK)
            reqdata.formdata['id'] = self.current_task._id
            reqdata.formdata['ids'] = self.current_task._ids
            reqdata.formdata['hash'] = self.current_task.success_hash
            reqdata.formdata['video'] = self.current_task.id_video
            reqdata.headers['Referer'] = self.tasks_url

            time.sleep(self.current_task.duration + 2)
            yield FormRequest(**reqdata(),
                              callback=self.success_task,
                              dont_filter=True,
                              meta={'dont_merge_cookies': True})
        except:
            yield from self.grinder()

    def success_task(self, response):
        print("".join(response.xpath("//span//text()").getall()))
        yield from self.grinder()

    def fake_open_video(self, response):
        print(f"Fake open {response.url}")

