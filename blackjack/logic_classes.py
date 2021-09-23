import json
from random import choice

from .deck import links
from .calculate_hand import calc_cards


class Participant:
    def __init__(self):
        self.hand = []  # рука участника
        self.score = ()  # счёт в руке вида кортеж (туз считать за 1, туз считать за 11)
        self.urls = []  # урлы для картинок

    def start_draw(self, deck):
        for _ in range(2):  # тянем две случайные карты
            draw = choice(deck)
            deck.remove(draw)  # обязательно удалить карту из колоды, ведь мы её уже вытянули
            self.hand.append(draw)
        self.calc_score(self.hand)  # выполнить расчёт очков

    def calc_score(self, hand):
        """посчитать количество очков по картам в руке"""
        self.score = calc_cards(hand)

    def hit(self, deck):
        """кто-то берет 1 карту, пересчитать очки в руке"""
        draw = choice(deck)
        deck.remove(draw)
        self.hand.append(draw)
        # self.hand.append("aceclub")  # тест на нужную карту, закомментировать 3 строки выше!
        self.calc_score(self.hand)  # пересчитать очки в руке

    def set_score_to_str(self):
        """представление счёта - просто 20 если нет туза, 9/20 если есть туз в руке"""
        if not self.score[1]:
            return str(self.score[0])
        else:
            return str(f'{self.score[0]}/{self.score[1]}')

    def get_urls(self, hand: list):
        """для каждой карты из руки достаёт линки для картинок из словаря links"""
        for card in hand:
            self.urls.append(links.get(card))

    def to_json(self):
        """джанго не умеет хранить в сессии объекты класса, а только джейсоны, вот представление в виде джейсона"""
        participant = {
            'hand': self.hand,
            'score': self.score,
            'urls': self.urls
        }
        # participant = self.__dict__  # альтернативный способ, но этот дикт может не быть заполнен ещё
        return json.dumps(participant)

    @classmethod
    def from_json(cls, json_data):
        """а это соответственно наоборот - создать объект этого класса на основании джейсона"""
        data = json.loads(json_data)
        obj = cls()
        obj.hand = data['hand']
        obj.score = data['score']
        obj.urls = data['urls']
        return obj


class Player(Participant):
    def start_draw(self, deck):
        super().start_draw(deck)
        # self.hand = ["kclub", "aceclub"]  # тестирование на фиксированную руку
        # self.calc_score(self.hand)  # тестирование на фиксированную руку
        self.get_urls(self.hand)

    def hit(self, deck):
        super().hit(deck)
        # self.hand.append("6spade")  # тестирование требуемой карты, закомментить строку выше!
        # self.calc_score(self.hand)  # тестирование требуемой карты
        return deck


class Dealer(Participant):
    def start_draw(self, deck):
        super().start_draw(deck)
        # self.hand = ["acediamond", "10hearts"]  # тестирование на фиксированную руку
        # self.calc_score(self.hand)  # тестирование на фиксированную руку
        self.get_starting_urls()

    def get_starting_urls(self):
        """первую карту из руки - берем линк, а вторую - жёстко карту обложки"""
        self.urls.append(links.get(self.hand[0]))  # первая карта из руки
        self.urls.append(links['cardback1'])  # вторая карта - жёстко обложка

    def get_url_for_hidden_card(self):
        """для случая stand - получить линк на ту карту, где раньше была обложка"""
        self.urls[1] = links[self.hand[1]]

    def ai_logic(self, player, deck):
        """
        логика дилера:
        1) если у игрока меньше 11, а счёт игрока и дилера равный, то дилер возьмёт одну карту, т.к. не переберёт
        пример: 4,6==10, 3,7==10, дилеру смело можно брать 1 карту
        2) далее пока максимальный счёт дилера (с учётом туза) не больше максимального счёта игрока, брать дилеру карты
        ЭТОТ МЕТОД НЕ БУДЕТ ВЫЗЫВАТЬСЯ ЕСЛИ У ИГРОКА ПЕРЕБОР!
        """
        if max(player.score) <= 11 and max(player.score) == max(self.score):
            deck = self.hit(deck)
        while max(self.score) < max(player.score):  # если очков одинаково, дилер не рискует
            deck = self.hit(deck)
        return deck

    def hit(self, deck):
        """это здесь число для теста"""
        super().hit(deck)
        # self.hand.append("5spade")  # тестирование требуемой карты, закомментить строку выше!
        # self.calc_score(self.hand)  # тестирование требуемой карты
        return deck
