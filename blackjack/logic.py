from random import choice

from blackjack.calculate_hand import calc_cards
from blackjack.deck import links, deck


def starting_draw():
    global DECK
    DECK = deck.copy()

    dealer_hand = []
    for _ in range(2):
        draw = choice(DECK)
        DECK.remove(draw)
        dealer_hand.append(draw)

    urls = []

    urls.append(links.get(dealer_hand[0]))
    urls.append(links.get('cardback'))

    dealer_score = calc_cards(dealer_hand)  # кортеж вида (счет с тузом, счёт без туза)

    player_hand = []
    for _ in range(2):
        draw = choice(DECK)
        DECK.remove(draw)
        player_hand.append(draw)

    for card in player_hand:
        urls.append(links.get(card))

    player_score = calc_cards(player_hand)

    return dealer_score, player_score, urls


def hit():
    ...


def show_score(score: tuple):
    if not score[1]:
        return str(score[0])
    else:
        return str(f'{score[0]}/{score[1]}')
