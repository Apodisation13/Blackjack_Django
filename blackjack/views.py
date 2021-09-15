from time import sleep

from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect

from .deck import deck
from .logic_classes import Player, Dealer
from .forms import MoneyForm, BetForm


# first_time = True
MONEY = 0
BET = 0


def home(request):
    """/"""
    template_name = 'blackjack/home.html'
    # global first_time
    # first_time = True
    return render(request, template_name, {})


def input_money_view(request):
    """/input_money"""
    template_name = 'blackjack/input_money.html'
    form = MoneyForm
    context = {'form': form}
    return render(request, template_name, context)


def input_bet_view(request):
    """/input_money/input-bet"""
    template_name = 'blackjack/input_bet.html'
    global MONEY
    # global first_time
    if request.method == 'POST':
        form = MoneyForm(request.POST)
        if form.is_valid():
            MONEY = form.cleaned_data.get('money')
            print('денег', MONEY)

    form = BetForm
    # if first_time:  # особенности джанго - только при первом входе смотреть чё там
    #     MONEY = request.GET.get('money')
    context = {'money': MONEY, 'form': form}
    return render(request, template_name, context)


def base_view(request):
    """/game"""
    template_name = 'blackjack/start_game.html'

    # dealer_score, player_score, urls = starting_draw()

    global DECK, player, dealer
    DECK = deck.copy()
    player = Player(DECK)
    dealer = Dealer(DECK)

    global MONEY, BET
    # global first_time
    # first_time = False  # первый вход в смысле ввода бабла
    # BET = request.GET.get('bet')
    # if not BET.isdigit():
    #     return HttpResponse('ТАК НЕЛЬЗЯ')
    # BET = int(BET)

    if request.method == 'POST':
        form = BetForm(request.POST)
        if form.clean_bet(MONEY):
            BET = int(form.data.get('bet'))
            print('ставка', BET)
            print('денег', MONEY)

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


def page_not_found(request, exception):
    msg = '<h1><font color="red">СТАВКА БОЛЬШЕ ЧЕМ У ВАС ДЕНЕГ</font></h1>'
    return HttpResponseNotFound(msg)
