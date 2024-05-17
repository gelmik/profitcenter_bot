import requests
from constants import *
from req_constants import *


class ReqFarmBot:
    cookies = {'googtrans': None}
    count_ontime_task = 5

    def __init__(self):
        pass

    def sign_in(self):
        login_response = requests.get(**SIGN_IN(), verify=False)
        self.cookies.update(login_response.cookies.get_dict())
        for cookie_name in ['newprov_png', 'newprov_etag', 'newprov_cache']:
            self.cookies[cookie_name] = self.cookies['menu_ref']

        captcha_response = requests.post('https://profitcentr.com/ajax/other/ajax-capcha.php', cookies=cookies, headers=headers, verify=False)

        a = 1


reqfarmbot = ReqFarmBot()
reqfarmbot.sign_in()
