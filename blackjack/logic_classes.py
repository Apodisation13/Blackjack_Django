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
        self.score = ()  # счёт в руке вида (безтуза, стузом)
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
        # self.hand = ["2club", "6club"]  # тестирование на фиксированную руку
        # self.calc_score(self.hand)  # тестирование на фиксированную руку

        self.urls = []  # урлы для картинок
        self.get_urls(self.hand)

        self.show_score()

    def get_urls(self, hand):
        for card in hand:
            self.urls.append(links.get(card))

    def show_score(self):
        if self.score[1]:
            if max(self.score) == 21:
                # self.player_result.config(text="21!!!!!! BLACKJACK!!!", bg="orange")
                ...
            else:
                # self.player_result.config(text=f"Ваш результат: {self.score[0]}/{self.score[1]}", bg="green")
                ...
        else:
            if max(self.score) == 21:
                ...
                # self.player_result.config(text="21!!!!!! BLACKJACK!!!", bg="orange")

            else:
                ...
                # self.player_result.config(text=f"Ваш результат: {self.score[0]}", bg="green")

    def hit(self, deck):
        super().hit(deck)
        # self.hand.append("5spade") # тестирование требуемой карты

        self.calc_score(self.hand)
        self.show_score()
