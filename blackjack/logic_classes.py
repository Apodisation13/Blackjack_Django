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

        self.urls = []  # урлы для картинок

    def calc_score(self, hand):
        self.score = calc_cards(hand)

    def hit(self, deck):
        """кто-то берет 1 карту"""
        draw = choice(deck)
        deck.remove(draw)
        self.hand.append(draw)
        # self.hand.append("aceclub")  # тест на нужную карту

        self.calc_score(self.hand)

    def set_score_to_str(self):
        if not self.score[1]:
            return str(self.score[0])
        else:
            return str(f'{self.score[0]}/{self.score[1]}')

    def get_urls(self, hand: list):
        for card in hand:
            self.urls.append(links.get(card))


class Player(Participant):
    def __init__(self, deck):
        super().__init__(deck)
        # self.hand = ["5club", "9club"]  # тестирование на фиксированную руку
        # self.calc_score(self.hand)  # тестирование на фиксированную руку

        self.get_urls(self.hand)

    def hit(self, deck):
        super().hit(deck)
        # self.hand.append("5spade") # тестирование требуемой карты

        self.calc_score(self.hand)


class Dealer(Participant):
    def __init__(self, deck):
        super().__init__(deck)
        # self.hand = ["4diamond", "10hearts"] # тестирование на фиксированную руку
        # self.calc_score(self.hand) # тестирование на фиксированную руку

        self.get_starting_urls()

    def get_starting_urls(self):
        self.urls.append(links.get(self.hand[0]))  # первая карта из руки
        self.urls.append(links['cardback3'])  # вторая карта - жёстко обложка

    def get_url_for_hidden_card(self):
        self.urls[1] = links[self.hand[1]]

    def ai_logic(self, player, deck):
        if max(player.score) <= 11 and max(player.score) == max(self.score):
            self.hit(deck)
        # костыль - если у игрока 11 или меньше, то при равенстве очков дилеру не страшно рискнуть и взять карту
        # потому что при любой карте 21 он не переберёт

        while max(self.score) < max(player.score):  # если очков одинаково, дилер не рискует
            self.hit(deck)
