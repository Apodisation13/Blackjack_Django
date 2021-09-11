from time import sleep

from django.http import HttpResponse
from django.shortcuts import render, redirect

# from .logic import starting_draw
from .deck import deck
from .logic_classes import Player


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
    template_name = 'blackjack/base.html'

    # dealer_score, player_score, urls = starting_draw()

    global DECK, player
    DECK = deck.copy()
    player = Player(DECK)
    player_urls = player.urls
    player_score = player.score

    global MONEY, BET, first_time
    first_time = False  # первый вход в смысле ввода бабла
    BET = request.GET.get('bet')
    if not BET.isdigit():
        return HttpResponse('ТАК НЕЛЬЗЯ')
    BET = int(BET)
    MONEY -= BET
    context = {
        # 'url1': urls[0], 'url2': urls[1],
        'player_hand_urls': player_urls,
        # 'dealer_result': dealer_score,
        'player_result': player_score,
        'money': MONEY,
        'bet': BET,
        'deck': len(DECK)
    }
    return render(request, template_name, context)


def hit(request):
    """/game/hit"""
    template_name = 'blackjack/base.html'

    global DECK, player, player_score
    player.hit(DECK)
    player_score = player.score

    player.get_urls([player.hand[-1], ])
    player_urls = player.urls

    if max(player_score) >= 21:
        sleep(1)
        return redirect('end_of_round')

    context = {
        # 'url1': urls[0], 'url2': urls[1],
        'player_hand_urls': player_urls,
        # 'dealer_result': dealer_score,
        'player_result': player_score,
        'money': MONEY,
        'bet': BET,
        'deck': len(DECK)
    }
    return render(request, template_name, context)


def end_of_round(request):
    """/game/end_of_round"""
    template_name = 'blackjack/end_of_round.html'
    global player, MONEY, BET

    player_urls = player.urls
    player_score = max(player.score)  # не забываем что там кортеж

    money_before = MONEY

    if player_score == 21:
        MONEY += BET * 3

    context = {
        # 'url1': urls[0], 'url2': urls[1],
        'player_hand_urls': player_urls,
        # 'dealer_result': dealer_score,
        'player_result': player_score,
        'money_before': money_before,
        'money': MONEY,
        'bet': BET,
        'deck': len(DECK)
    }

    return render(request, template_name, context)
