import random
from datetime import datetime
from enum import Enum
import random
import time
import locale
locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"  # Note: do not use "de_DE" as it doesn't work
)

def random_date():
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime("1/1/1972", '%m/%d/%Y'))
    etime = time.mktime(time.strptime("1/1/2000", '%m/%d/%Y'))

    ptime = stime + random.random() * (etime - stime)

    return datetime.strptime(time.strftime('%m/%d/%Y', time.localtime(ptime)), '%m/%d/%Y')


MEN_NAMES = []
MEN_SECOND_NAMES = []

WOMEN_NAMES = ['Аврора', 'Агафья', 'Аглая', 'Агриппина', 'Аделаида', 'Аза', 'Акулина', 'Алевтина', 'Александра',
               'Алина', 'Алиса', 'Алла', 'Анастасия', 'Ангелина', 'Анжела', 'Анжелика', 'Анна', 'Антонина', 'Анфиса',
               'Валентина', 'Валерия', 'Варвара', 'Василиса', 'Васса', 'Вера', 'Вероника', 'Виктория', 'Галина',
               'Глафира', 'Гликерия', 'Дана', 'Дарья', 'Евгения', 'Евдокия', 'Евлалия', 'Евлампия',
               'Евпраксия', 'Евфросиния', 'Екатерина', 'Елена', 'Елизавета', 'Епистима', 'Ермиония', 'Жанна', 'Зинаида',
               'Злата', 'Зоя', 'Инга', 'Инесса', 'Инна', 'Иоанна', 'Ираида', 'Ирина', 'Ия', 'Капитолина', 'Карина',
               'Каролина', 'Кира', 'Клавдия', 'Клара', 'Ксения', 'Лада', 'Лариса', 'Лидия', 'Любовь', 'Людмила',
               'Маргарита', 'Марина', 'Мария', 'Марфа', 'Матрёна', 'Милица', 'Мирослава', 'Надежда', 'Наталья',
               'Неонилла', 'Нина', 'Нинель', 'Нонна', 'Оксана', 'Октябрина', 'Олимпиада', 'Ольга', 'Павлина', 'Пелагея',
               'Пинна', 'Полина', 'Прасковья', 'Рада', 'Раиса', 'Регина', 'Римма', 'Рогнеда', 'Светлана', 'Серафима',
               'Снежана', 'София', 'Сусанна', 'Таисия', 'Тамара', 'Татьяна', 'Улита', 'Ульяна', 'Урсула', 'Фаина',
               'Феврония', 'Фёкла', 'Феодора', 'Целестина', 'Элеонора', 'Элла', 'Эмма', 'Юлия', 'Яна', 'Ярослава']

WOMEN_SECOND_NAMES = ['Авдеева', 'Агапова', 'Агафонова', 'Агеева', 'Акимова', 'Аксёнова', 'Александрова', 'Алексеева',
                      'Алёхина', 'Алешина', 'Алёшина', 'Ананьева', 'Андреева', 'Андрианова', 'Аникина', 'Анисимова',
                      'Анохина', 'Антипова', 'Антонова', 'Артамонова', 'Артёмова', 'Архипова', 'Астафьева', 'Астахова',
                      'Афанасьева', 'Бабушкина', 'Баженова', 'Балашова', 'Баранова', 'Барсукова', 'Басова', 'Безрукова',
                      'Беликова', 'Белкина', 'Белова', 'Белоусова', 'Беляева', 'Белякова', 'Березина', 'Берия',
                      'Беспалова', 'Бессонова', 'Бирюкова', 'Блинова', 'Блохина', 'Боброва', 'Богданова', 'Богомолова',
                      'Болдырева', 'Большакова', 'Бондарева', 'Борисова', 'Бородина', 'Бочарова', 'Булатова',
                      'Булгакова', 'Бурова', 'Быкова', 'Бычкова', 'Вавилова', 'Вагина',
                      'Васильева', 'Вдовина', 'Верещагина', 'Вешнякова', 'Виноградова', 'Винокурова', 'Вишневская',
                      'Владимирова', 'Власова', 'Волкова', 'Волошина', 'Воробьёва', 'Воронина', 'Воронкова', 'Воронова',
                      'Воронцова', 'Второва', 'Высоцкая', 'Гаврилова', 'Гайдукова', 'Гакабова', 'Галкина', 'Герасимова',
                      'Гладкова', 'Глебова', 'Глухова', 'Глушкова', 'Гноева', 'Голикова', 'Голованова', 'Головина',
                      'Голубева', 'Гончарова', 'Горбань', 'Горбачёва', 'Горбунова', 'Гордеева', 'Горелова', 'Горлова',
                      'Горохова', 'Горшкова', 'Горюнова', 'Горячева', 'Грачёва', 'Грекова', 'Грибкова', 'Грибова',
                      'Григорьева', 'Гришина', 'Громова', 'Губанова', 'Гуляева', 'Гурова', 'Гусева', 'Гущина',
                      'Давыдова', 'Дадаева', 'Дадина', 'Данилова', 'Дарвина', 'Дашкова', 'Дегтярева', 'Дегтярёва',
                      'Дедова', 'Дементьева', 'Демидова', 'Дёмина', 'Демьянова', 'Денисова', 'Дмитриева', 'Добрынина',
                      'Долгова', 'Дорофеева', 'Дорохова', 'Дроздова', 'Дружинина', 'Дубинина', 'Дубова', 'Дубровина',
                      'Дьякова', 'Дьяконова', 'Евдокимова', 'Евсеева', 'Егорова', 'Ежова', 'Елизарова', 'Елисеева',
                      'Ельцина', 'Емельянова', 'Еремеева', 'Ерёмина', 'Ермакова', 'Ермилова', 'Ермолаева', 'Ермолова',
                      'Еромлаева', 'Ерофеева', 'Ершова', 'Ефимова', 'Ефремова', 'Жарова', 'Жданова', 'Жилина',
                      'Жириновская', 'Жукова', 'Журавлёва', 'Завьялова', 'Заец', 'Зайцева', 'Захарова', 'Зверева',
                      'Звягинцева', 'Зеленина', 'Зимина', 'Зиновьева', 'Злобина', 'Золотарева', 'Золотарёва',
                      'Золотова', 'Зорина', 'Зотова', 'Зубкова', 'Зубова', 'Зуева', 'Зыкова', 'Зюганова', 'Иванова',
                      'Ивашова', 'Игнатова', 'Игнатьева', 'Измайлова', 'Ильина', 'Ильинская', 'Ильюхина', 'Исаева',
                      'Исакова', 'Казакова', 'Казанцева', 'Калачева', 'Калачёва', 'Калашникова', 'Калинина',
                      'Калмыкова', 'Калугина', 'Капустина', 'Карасева', 'Карасёва', 'Карпова', 'Карташова', 'Касаткина',
                      'Касьянова', 'Киреева', 'Кириллова', 'Киселёва', 'Кислова', 'Климова', 'Клюева', 'Князева',
                      'Ковалёва', 'Коваленко', 'Коваль', 'Кожевникова', 'Козина', 'Козлова', 'Козловская', 'Козырева',
                      'Колесникова', 'Колесова', 'Колосова', 'Колпакова', 'Кольцова', 'Комарова', 'Комиссарова',
                      'Кондратова', 'Кондратьева', 'Кондрашова', 'Коновалова', 'Кононова', 'Константинова', 'Копылова',
                      'Корнева', 'Корнеева', 'Корнилова', 'Коровина', 'Королёва', 'Королькова', 'Короткова',
                      'Корчагина', 'Коршунова', 'Косарева', 'Костина', 'Котова', 'Кочергина', 'Кочеткова', 'Кочетова',
                      'Кошелева', 'Кравцова', 'Краснова', 'Красоткина', 'Круглова', 'Крылова', 'Крюкова', 'Крючкова',
                      'Кудрявцева', 'Кудряшова', 'Кузина', 'Кузнецова', 'Кузьмина', 'Кукушкина', 'Кулагина', 'Кулакова',
                      'Кулешова', 'Куликова', 'Куприянова', 'Курочкина', 'Лаврентьева', 'Лаврова', 'Лазарева', 'Лапина',
                      'Лаптева', 'Лапшина', 'Ларина', 'Ларионова', 'Латышева', 'Лебедева',
                      'Левина', 'Леонова', 'Леонтьева', 'Литвинова', 'Лобанова', 'Логинова',
                      'Лопатина', 'Лосева', 'Лужкова', 'Лукина', 'Лукьянова', 'Лыкова',
                      'Львова', 'Любимова', 'Майорова', 'Макарова', 'Макеева', 'Максимова',
                      'Малахова', 'Малинина', 'Малофеева', 'Малышева', 'Мальцева', 'Маркелова', 'Маркина', 'Маркова',
                      'Мартынова', 'Масленникова', 'Маслова', 'Матвеева', 'Матвиенко', 'Медведева', 'Медейко',
                      'Мельникова', 'Меньшова', 'Меркулова', 'Мешкова', 'Мещерякова', 'Минаева', 'Минина', 'Миронова',
                      'Митрофанова', 'Михайлова', 'Михеева', 'Мишустина', 'Моисеева', 'Молчанова', 'Моргунова',
                      'Морозова', 'Москвина', 'Муравьёва', 'Муратова', 'Муромцева', 'Мухина',
                      'Мясникова', 'Навальная', 'Назарова', 'Наумова', 'Некрасова', 'Нестерова', 'Нефёдова', 'Нечаева',
                      'Никитина', 'Никифорова', 'Николаева', 'Никольская', 'Никонова', 'Никулина', 'Новикова',
                      'Новодворская', 'Носкова', 'Носова', 'Овсянникова', 'Овчинникова', 'Одинцова', 'Озерова',
                      'Окулова', 'Олейникова', 'Орехова', 'Орлова', 'Осипова', 'Островская', 'Павлова', 'Павловская',
                      'Панина', 'Панкова', 'Панкратова', 'Панова', 'Пантелеева', 'Панфилова', 'Парамонова', 'Парфёнова',
                      'Пастухова', 'Пахомова', 'Пекарева', 'Петрова', 'Петровская', 'Петухова', 'Пименова', 'Пирогова',
                      'Платонова', 'Плотникова', 'Позднякова', 'Покровская', 'Поликарпова', 'Полякова',
                      'Пономарёва', 'Попова', 'Порошина', 'Порывай', 'Постникова',
                      'Потапова', 'Похлёбкина', 'Прокофьева', 'Прохорова', 'Прошина', 'Пугачёва', 'Путина', 'Ракова',
                      'Рогова', 'Родина', 'Родионова', 'Рожкова', 'Розанова', 'Романова', 'Рублёва', 'Рубцова',
                      'Рудакова', 'Руднева', 'Румянцева', 'Русакова', 'Русанова', 'Рыбакова', 'Рыжикова', 'Рыжкова',
                      'Рыжова', 'Рябинина', 'Рябова', 'Савельева', 'Савина', 'Савицкая', 'Сазонова', 'Сальникова',
                      'Самойлова', 'Самсонова', 'Сафонова', 'Сахарова', 'Светличная', 'Светлова', 'Свешникова',
                      'Свиридова', 'Севастьянова', 'Седова', 'Селезнёва', 'Селиванова', 'Семёнова', 'Сёмина',
                      'Сергеева', 'Серебрякова', 'Серова', 'Сидорова', 'Сизова', 'Симонова', 'Синицына', 'Ситникова',
                      'Скворцова', 'Скрябина', 'Смирнова', 'Снегирёва', 'Соболева', 'Собянина', 'Соколова', 'Соловьёва',
                      'Сомова', 'Сорокина', 'Сотникова', 'Софронова', 'Спиридонова', 'Старикова', 'Старостина',
                      'Степанова', 'Столярова', 'Стрелкова', 'Стрельникова', 'Строева',
                      'Субботина', 'Суворова', 'Судакова', 'Суркова', 'Суслова', 'Суханова',
                      'Сухарева', 'Сухова', 'Сычёва', 'Тарасова', 'Терентьева', 'Терехова', 'Тимофеева', 'Титова',
                      'Тихомирова', 'Тихонова', 'Ткачёва', 'Токарева', 'Толкачёва', 'Торшина', 'Третьякова',
                      'Трифонова', 'Троицкая', 'Трофимова', 'Троцкая', 'Трошина', 'Туманова', 'Уварова', 'Ульянова',
                      'Усова', 'Успенская', 'Устинова', 'Уткина', 'Ушакова', 'Фадеева', 'Фёдорова', 'Федосеева',
                      'Федосова', 'Федотова', 'Фетисова', 'Филатова', 'Филимонова', 'Филиппова', 'Фирсова', 'Фокина',
                      'Фомина', 'Фомичева', 'Фомичёва', 'Фролова', 'Харитонова', 'Хомякова', 'Хромова', 'Хрущёва',
                      'Худякова', 'Царёва', 'Цветкова', 'Чеботарёва', 'Черепанова', 'Черкасова', 'Черная', 'Чёрная',
                      'Чернова', 'Черных', 'Чернышева', 'Чернышёва', 'Черняева', 'Чеснокова', 'Чижова', 'Чистякова',
                      'Чумакова', 'Шаповалова', 'Шапошникова', 'Шарова', 'Швецова', 'Шевелёва', 'Шевцова', 'Шестакова',
                      'Шилова', 'Широкова', 'Ширяева', 'Шишкина', 'Шмелёва', 'Шубина', 'Шувалова', 'Шульгина',
                      'Щеглова', 'Щербакова', 'Щукина', 'Юдина', 'Яковлева', 'Яшина']


class Sex(Enum):
    female = 0
    male = 1

class Person:
    def __init__(self, sex=Sex.female):
        self.sex = sex
        self.name = random.choice(WOMEN_NAMES if sex == Sex.female else MEN_NAMES)
        self.second_name = random.choice(WOMEN_SECOND_NAMES if sex == Sex.female else MEN_SECOND_NAMES)
        self.birthday = random_date()
        self.email = str()
        self.password = str()

    def __str__(self):
        return f"Имя: {self.second_name}\nФамилия: {self.name}\nДень рождения: {self.birthday}\nEmail: {self.email}\nPassword: {self.password}"
