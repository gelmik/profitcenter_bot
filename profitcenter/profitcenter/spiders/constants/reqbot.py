import requests
from datetime import datetime


class ReqConstant:
    url: str = ""
    headers: dict = {}
    cookies: dict = {}
    method: str = 'GET'
    body: dict = {}
    formdata: dict = {}

    def __init__(self, url="", headers={}, cookies={}, method="GET", body={}, formdata={}):
        self.url = url
        self.headers = headers
        self.cookies = cookies
        self.method = method
        self.body = body
        self.formdata = formdata

    def __call__(self, *args, **kwargs):
        return {key: self.__dict__[key] for key in self.__dict__ if self.__dict__[key]}


CNST_SIGN_IN = ReqConstant(url="https://profitcentr.com/login", headers={
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'referer': 'https://profitcentr.com/login',
    'sec-ch-ua': '"Opera GX";v="109", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0 (Edition Yx GX)',
})

CNST_GET_CAPTCHA = ReqConstant(url='https://profitcentr.com/ajax/log_reg.php',
                               method='POST',
                               headers={
                                   'Host': 'profitcentr.com',
                                   # 'Content-Length': '707',
                                   'Sec-Ch-Ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
                                   'Accept': 'application/json, text/javascript, */*; q=0.01',
                                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                                   'X-Requested-With': 'XMLHttpRequest',
                                   'Sec-Ch-Ua-Mobile': '?0',
                                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36',
                                   'Sec-Ch-Ua-Platform': '"Windows"',
                                   'Origin': 'https://profitcentr.com',
                                   'Sec-Fetch-Site': 'same-origin',
                                   'Sec-Fetch-Mode': 'cors',
                                   'Sec-Fetch-Dest': 'empty',
                                   'Referer': 'https://profitcentr.com/login',
                                   # 'Accept-Encoding': 'gzip, deflate, br',
                                   'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                                   'Priority': 'u=4, i',
                                   # 'Cookie': 'SESSIONID=abkqkp4uvulq965o1bbpl7o35t; googtrans=null; googtrans=null; newprov_png=8c4e2b131511ed4a9b249826bab85c9a; newprov_etag=8c4e2b131511ed4a9b249826bab85c9a; newprov_cache=8c4e2b131511ed4a9b249826bab85c9a; menu_ref=8c4e2b131511ed4a9b249826bab85c9a',
                               }, formdata={
        'username': '',
        'password': '',
        'capcha[]': [],
        'func': 'login',
        'dopinfa': 'ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Ti (0x000024C9) Direct3D11 vs_5_0 ps_5_0, D3D11)',
        'dopinfaw': '1879x495',
        'dopinfan': {"size": "1879x495", "lang": "Русский (ru-RU)",
                     "date": datetime.now().strftime(
                         '%a+%b+%d+%Y+%H:%M:%S+GMT+0300+(Москва,+стандартное+время)'),
                     "plagen": ["PDF Viewer (internal-pdf-viewer)",
                                "Chrome PDF Viewer (internal-pdf-viewer)",
                                "Chromium PDF Viewer (internal-pdf-viewer)",
                                "Microsoft Edge PDF Viewer (internal-pdf-viewer)",
                                "WebKit built-in PDF (internal-pdf-viewer)"]
                     }
    }
                               )

CNST_MEMBERS = ReqConstant(url='https://profitcentr.com/members', headers={
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'referer': 'https://profitcentr.com/login',
    'sec-ch-ua': '"Opera GX";v="109", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0 (Edition Yx GX)',
})

CAPTCHA_TASK = "//div[@class='out-capcha-title']"
CAPTCHA_IMAGES = "//div[@id='page_1']//div[@class='out-capcha']/label"
