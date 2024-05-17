import requests


class ReqConstant:
    url: str = ""
    headers: dict = {}
    cookies: dict = {}
    method: str = "GET"
    body: dict = {}
    formdata: str = {}

    def __init__(self, url="", headers={}, cookies={}, method="GET", body={}, formdata={}):
        self.url = url
        self.headers = headers
        self.cookies = cookies
        self.method = method
        self.body = body
        self.formdata = formdata

    def __call__(self, *args, **kwargs):
        return {key: self.__dict__[key] for key in self.__dict__ if self.__dict__[key]}


SIGN_IN = ReqConstant(url="https://profitcentr.com/login", headers={
    'Host': 'profitcentr.com',
    'Sec-Ch-Ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Priority': 'u=0, i',
})

GET_CAPTCHA = ReqConstant(url='https://profitcentr.com/ajax/other/ajax-capcha.php', headers={
    'Host': 'profitcentr.com',
    # 'Content-Length': '0',
    'Sec-Ch-Ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
    'Accept': 'text/html, */*; q=0.01',
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
    'Priority': 'u=1, i',
        }
    )
