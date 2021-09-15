from django.shortcuts import redirect

from .deck import deck
from .forms import get_bet
from .logic_classes import Player, Dealer


def payment_result(player_score, dealer_score, money, bet):
    if player_score == 21:  # у игрока 21 - утраиваем выигрыш
        money += bet * 3
    if dealer_score > 21:  # у дилера > 21, игрок выиграл две ставки
        money += bet * 2
    if dealer_score == player_score:  # если ничья, то все при своих, ставка вернулась
        money += bet
    return money


def starting_draw_logic(request, MONEY):
    DECK = deck.copy()
    player = Player(DECK)  # стартовая рука игрока (2 карты), линки, счёт
    dealer = Dealer(DECK)  # стартовая рука дилера (2 карты), линк на 1ю карту и обложку, счёт не отображаем

    BET = get_bet(request, MONEY)

    MONEY -= BET  # после раздачи карт сразу вычесть из денег ставку

    if max(player.score) == 21:  # если у игрока сразу блэкджек - переходим на конец раунда
        return redirect('end_of_round')
    if max(dealer.score) == 21:  # если у дилера сразу блэкджек, открываем его скрытую карту и на конец раунда
        dealer.get_url_for_hidden_card()
        return redirect('end_of_round')

    player_score_str = player.set_score_to_str()  # представление - или просто число, или строка число\число

    return DECK, player, dealer, BET, MONEY, player_score_str
