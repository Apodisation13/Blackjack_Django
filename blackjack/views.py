from time import sleep

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from .deck import deck
from .logic_classes import Player, Dealer


def home(request):
    """/"""
    template_name = 'blackjack/home.html'
    return render(request, template_name, {})


def input_money_view(request):
    """/input_money"""
    template_name = 'blackjack/input_money.html'
    global first_time  # первый вход для ввода бабла
    first_time = True
    return render(request, template_name, {})


def input_bet_view(request):
    """/input_money/input-bet"""
    template_name = 'blackjack/input_bet.html'
    global MONEY, first_time
    if first_time:  # особенности джанго - только при первом входе смотреть чё там
        MONEY = request.GET.get('money')
        if not MONEY.isdigit():
            return HttpResponse('ТАК НЕЛЬЗЯ')
        MONEY = int(MONEY)
    return render(request, template_name, {'money': MONEY})


def base_view(request):
    """/game"""
    template_name = 'blackjack/start_game.html'

    # dealer_score, player_score, urls = starting_draw()

    global DECK, player, dealer
    DECK = deck.copy()
    player = Player(DECK)
    dealer = Dealer(DECK)

    global MONEY, BET, first_time
    first_time = False  # первый вход в смысле ввода бабла
    BET = request.GET.get('bet')
    if not BET.isdigit():
        return HttpResponse('ТАК НЕЛЬЗЯ')
    BET = int(BET)
    MONEY -= BET

    if max(player.score) == 21:
        return redirect('end_of_round')
    if max(dealer.score) == 21:
        dealer.get_url_for_hidden_card()
        return redirect('end_of_round')

    player_score_str = player.set_score_to_str()  # представление - или просто число, или строка число\число

    context = {
        'dealer_hand_urls': dealer.urls,
        'player_hand_urls': player.urls,
        'dealer_result': "???",
        'player_result': player_score_str,
        'money': MONEY,
        'bet': BET,
        'deck': len(DECK)
    }
    return render(request, template_name, context)


def hit(request):
    """/game/hit"""
    template_name = 'blackjack/start_game.html'

    global DECK, player, dealer
    player.hit(DECK)

    player.get_urls([player.hand[-1], ])

    if max(player.score) >= 21:
        return redirect('end_of_round')

    player_score_str = player.set_score_to_str()  # представление - или просто число, или строка число\число

    context = {
        'dealer_hand_urls': dealer.urls,
        'player_hand_urls': player.urls,
        'dealer_result': "???",
        'player_result': player_score_str,
        'money': MONEY,
        'bet': BET,
        'deck': len(DECK)
    }
    return render(request, template_name, context)


def end_of_round(request):
    """/game/end_of_round"""
    template_name = 'blackjack/end_of_round.html'
    global player, dealer, MONEY, BET

    player_score = max(player.score)  # не забываем что там кортеж
    dealer_score = max(dealer.score)

    money_before = MONEY

    if player_score == 21:
        MONEY += BET * 3
    if dealer_score > 21:
        MONEY += BET * 2
    if dealer_score == player_score:
        MONEY += BET

    context = {
        'dealer_hand_urls': dealer.urls,
        'player_hand_urls': player.urls,
        'dealer_result': dealer_score,
        'player_result': player_score,
        'money_before': money_before,
        'money': MONEY,
        'bet': BET,
        'deck': len(DECK)
    }

    return render(request, template_name, context)


def stand(request):
    """game/stand/"""
    template_name = 'blackjack/start_game.html'
    global player, dealer, DECK, MONEY, BET

    dealer.get_url_for_hidden_card()

    dealer.ai_logic(player, DECK)
    dealer.get_urls(dealer.hand[2:])

    player_score_str = player.set_score_to_str()  # представление - или просто число, или строка число\число
    dealer_score_str = dealer.set_score_to_str()  # представление - или просто число, или строка число\число

    if max(dealer.score) > 21 or max(dealer.score) >= max(player.score):
        return redirect('end_of_round')

    context = {
        'dealer_hand_urls': dealer.urls,
        'player_hand_urls': player.urls,
        'dealer_result': dealer_score_str,
        'player_result': player_score_str,
        'money': MONEY,
        'bet': BET,
        'deck': len(DECK)
    }

    return render(request, template_name, context)


def zero_money(request):
    sleep(4)
    template_name = 'blackjack/zero_money.html'
    return render(request, template_name, {})
