from copy import deepcopy
from typing import Iterable

import re
import scrapy
from scrapy import Request, Selector, FormRequest

from .constants.reqbot import *
from solve import Determinant

from datetime import datetime


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


class ReqbotSpider(ReqParser, scrapy.Spider):
    name = "reqbot"
    cookies = {'googtrans': None}
    username = ""
    password = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = kwargs['username']
        self.password = kwargs['password']

    def start_requests(self):
        yield Request(**CNST_SIGN_IN(), callback=self.sign_in_step_1)

    def sign_in_step_1(self, response):
        self.cookies.update(self.get_cookies(response))
        for cookie_name in ['newprov_png', 'newprov_etag', 'newprov_cache']:
            self.cookies[cookie_name] = self.cookies['menu_ref']

        reqdata = deepcopy(CNST_GET_CAPTCHA)
        reqdata.formdata['username'] = self.username
        reqdata.formdata['password'] = self.password
        reqdata.formdata['capcha[]'] = self.solve_captcha(response)

        yield FormRequest(**reqdata(), callback=self.sign_in_step_2)

    def sign_in_step_2(self, response):
        self.cookies.update(self.get_cookies(response))
        yield Request(**CNST_MEMBERS(), callback=self.members, cookies=self.cookies)

    def members(self, response):
        from scrapy.shell import open_in_browser
        open_in_browser(response)
        a = 1

    def parse(self, response):
        pass
