import json
import sqlite3
import random



class Connector:
    def __init__(self):
        self.connection = sqlite3.connect('database/profitcenter')
        self.cursor = self.connection.cursor()

    def get_bots(self, active=False):
        self.cursor.execute('SELECT * FROM bots WHERE status = ?', (0, ))
        self.bots = self.cursor.fetchall()
        return self.bots

    def get_bot(self, username):
        bot = self.cursor.execute('SELECT * FROM bots WHERE username = ?', (username,))
        return bot

    def create_bot(self, email, host, port, username, password):
        self.cursor.execute('INSERT INTO bots (email, proxy, username, password) VALUES (?, ?, ?, ?)',
                       (email, f"http://GfEGR2:IjbL8SVayj@{host}:{port}", username, password))

        # Сохраняем изменения и закрываем соединение
        self.connection.commit()


class BotData:
    login: str = ""
    password: str = ""
    email: str = ""
    email_password: str = ""
    proxy: str = ""
    cookies: str = ""
    amount: float = .0
    status: int = 0

    def __init__(self):
        import os
        print(os.listdir())
        self.connection = sqlite3.connect('database/profitcenter')
        self.cursor = self.connection.cursor()

        self.cursor.execute('SELECT * FROM bots WHERE status = ?', (0,))
        data = random.choice(self.cursor.fetchall())

        for attr_name, value in zip(self.__annotations__.keys(), data):
            setattr(self, attr_name, value)

        self.cursor.execute('UPDATE bots SET status = ? WHERE login = ?', (1, self.login))
        self.connection.commit()

    def update_cookies(self, cookies):
        self.cursor.execute('UPDATE bots SET cookies = ? WHERE login = ?', (json.dumps(cookies), self.login))
        self.connection.commit()

    def add_amount(self, value):
        self.amount += value
        self.cursor.execute('UPDATE bots SET amount = ? WHERE login = ?', (self.amount, self.login))
        self.connection.commit()

    def close_connection(self):
        self.cursor.execute('UPDATE bots SET status = ? WHERE login = ?', (0, self.login))
        self.connection.commit()
        self.connection.close()