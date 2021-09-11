from random import choice

from .deck import links
from .calculate_hand import calc_cards


class Participant:
    def __init__(self, deck):
        self.hand = []
        for _ in range(2):  # тянем две случайные карты
            draw = choice(deck)
            deck.remove(draw)  # обязательно удалить карту из колоды, ведь мы её уже вытянули
            self.hand.append(draw)
        self.score = ()  # счёт в руке вида кортеж (без_туза, с_тузом)
        self.calc_score(self.hand)  # выполнить расчёт очков

    def calc_score(self, hand):
        self.score = calc_cards(hand)

    def hit(self, deck):
        """кто-то берет 1 карту"""
        draw = choice(deck)
        deck.remove(draw)
        self.hand.append(draw)

        # self.hand.append("aceclub")  # тест на нужную карту


class Player(Participant):
    def __init__(self, deck):
        super().__init__(deck)
        # self.hand = ["10club", "aceclub"]  # тестирование на фиксированную руку
        # self.calc_score(self.hand)  # тестирование на фиксированную руку

        self.urls = []  # урлы для картинок
        self.get_urls(self.hand)

    def get_urls(self, hand):
        for card in hand:
            self.urls.append(links.get(card))

    def hit(self, deck):
        super().hit(deck)
        # self.hand.append("5spade") # тестирование требуемой карты

        self.calc_score(self.hand)


class Dealer(Participant):
    def __init__(self, deck):
        super().__init__(deck)
        # self.hand = ["qdiamond", "7hearts"] # тестирование на фиксированную руку
        # self.calc_score(self.hand) # тестирование на фиксированную руку

        # self.number = 0  # номер карты в руке дилера
        # self.open_card(self.number)  # выполняем метод открыть карту
        # self.hidden_card()  # выполняем метод скрытой карты

        self.urls = []  # урлы для картинок
        self.get_urls(self.hand)

    def get_urls(self, hand):
        self.urls.append(links.get(hand[0]))
        self.urls.append(links['cardback'])
