import hashlib
import json

hash = "2a7e24653988fab7dd10e7f479bf692d"

data = {
'email': 'yelizaveta.ulyanova.80@list.ru',
'redirect_uri': 'https://e.mail.ru/inbox?newreg=1&app_id_mytracker=58519',
'adblock': False,
'client': 'touch',
'from': 'main',
'reg_anketa': {"id":"dLrCzsdWEy42MnQ6","capcha":"yktyck"},
'promo_referrer': 'https://mail.ru',
'htmlencoded': False,
'utm': {},
'referrer': 'https://mail.ru/',
}

hash_object = hashlib.md5("yktyck".encode('utf-8'))
print(hash_object.hexdigest())