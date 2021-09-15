from time import sleep

from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect

# from .deck import deck
# from .logic_classes import Player, Dealer
from .forms import MoneyForm, get_money, BetForm
from .logic import starting_draw_logic, payment_result


beginning = True  # нужен флаг для того, чтобы попадать в ввод денег только 1 раз
MONEY = 0
BET = 0
DECK, player, dealer = None, None, None


def home(request):
    """/"""
    template_name = 'blackjack/home.html'
    return render(request, template_name, {})


def input_money_view(request):
    """/input_money"""
    template_name = 'blackjack/input_money.html'
    global beginning
    beginning = True
    context = {'form': MoneyForm}
    return render(request, template_name, context)


def input_bet_view(request):
    """/input_money/input-bet"""
    template_name = 'blackjack/input_bet.html'

    global MONEY
    if beginning:
        MONEY = get_money(request)

    context = {'money': MONEY, 'form': BetForm}
    return render(request, template_name, context)


def base_view(request):
    """/game"""
    template_name = 'blackjack/start_game.html'

    global beginning
    beginning = False

    global DECK, player, dealer, MONEY, BET
    DECK, player, dealer, BET, MONEY, player_score_str = starting_draw_logic(request, MONEY)

    context = {
        'dealer_hand_urls': dealer.urls,
        'player_hand_urls': player.urls,
        'dealer_result': "???",
        'player_result': player_score_str,
        'money': MONEY,
        'bet': BET,
        # 'deck': len(DECK)
    }
    return render(request, template_name, context)


def hit(request):
    """/game/hit"""
    template_name = 'blackjack/start_game.html'

    global DECK, player, dealer
    player.hit(DECK)  # взять одну карту

    player.get_urls([player.hand[-1], ])  # сформировать линк на последнюю карту

    if max(player.score) >= 21:  # если больше 21, сразу перейти на конец раунда
        return redirect('end_of_round')

    player_score_str = player.set_score_to_str()  # представление - или просто число, или строка число\число

    context = {
        'dealer_hand_urls': dealer.urls,
        'player_hand_urls': player.urls,
        'dealer_result': "???",
        'player_result': player_score_str,
        'money': MONEY,
        'bet': BET,
        # 'deck': len(DECK)
    }
    return render(request, template_name, context)


def end_of_round(request):
    """/game/end_of_round"""
    template_name = 'blackjack/end_of_round.html'

    global player, dealer, MONEY, BET, DECK

    player_score = max(player.score)  # не забываем что там кортеж
    dealer_score = max(dealer.score)

    money_before = MONEY  # ведь мы уже вычли ставку, это для удобства отображения
    MONEY = payment_result(player_score, dealer_score, MONEY, BET)

    context = {
        'dealer_hand_urls': dealer.urls,
        'player_hand_urls': player.urls,
        'dealer_result': dealer_score,
        'player_result': player_score,
        'money_before': money_before,
        'money': MONEY,
        'bet': BET,
        # 'deck': len(DECK)
    }

    return render(request, template_name, context)


def stand(request):
    """game/stand/"""
    template_name = 'blackjack/start_game.html'
    global player, dealer, DECK, MONEY, BET

    dealer.get_url_for_hidden_card()  # получить линк на настоящую скрытую карту, 2ю в руке

    dealer.ai_logic(player, DECK)  # выполнить логику дилера: добор если меньше чем у игрока, или <=11
    dealer.get_urls(dealer.hand[2:])  # найти линки на все карты после 2й

    player_score_str = player.set_score_to_str()  # представление - или просто число, или строка число\число
    dealer_score_str = dealer.set_score_to_str()  # представление - или просто число, или строка число\число

    if max(dealer.score) > 21 or max(dealer.score) >= max(player.score):
        return redirect('end_of_round')  # если дилер вылетел, или у них ничья, то пойти на конец раунда

    context = {
        'dealer_hand_urls': dealer.urls,
        'player_hand_urls': player.urls,
        'dealer_result': dealer_score_str,
        'player_result': player_score_str,
        'money': MONEY,
        'bet': BET,
        # 'deck': len(DECK)
    }

    return render(request, template_name, context)


def zero_money(request):
    sleep(4)
    template_name = 'blackjack/zero_money.html'
    return render(request, template_name, {})


def page_not_found(request, exception):
    msg = '<h1><font color="red">СТАВКА БОЛЬШЕ ЧЕМ У ВАС ДЕНЕГ</font></h1>'
    return HttpResponseNotFound(msg)
