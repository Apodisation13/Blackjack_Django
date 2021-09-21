from time import sleep

from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect

from .forms import MoneyForm, get_money, BetForm
from .logic import starting_draw_logic, hit_logic, \
    redirect_from_start_via_blackjack, end_of_round_logic, stand_logic


beginning = True  # нужен флаг для того, чтобы попадать в ввод денег только 1 раз
double_down_pressed = False
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
    global beginning
    if beginning:
        get_money(request)  # только при первом входе, записываем из формы в переменную
    context = {'money': request.session['money'], 'form': BetForm}
    return render(request, template_name, context)


def base_view(request):
    """
    /game
    основное вью раунда
    """
    print(request.session['money'])
    template_name = 'blackjack/start_game.html'

    global beginning, double_down_pressed
    beginning = False  # это для того, чтобы не анализировать форму с вводом денег далее
    double_down_pressed = False

    global DECK, player, dealer
    DECK, player, dealer, player_score_str, double_down_chance = starting_draw_logic(request)

    print(request.session['money'], request.session['bet'])

    if redirect_from_start_via_blackjack(player, dealer):  # проверка на 21
        return redirect('end_of_round')

    context = {
        'dealer_hand_urls': dealer.urls,  # линки на карты дилера
        'player_hand_urls': player.urls,  # линки на карты игрока
        'dealer_result': "???",  # здесь специально ???, ибо счёт дилера игрок пока не знает
        'player_result': player_score_str,  # счёт в виде 9/20 если в руке туз, и просто 20 если нету
        'money': request.session['money'],
        'bet': request.session['bet'],
        'double_down_chance': double_down_chance  # boolean данные о возможности удвоить ставку
        # 'deck': len(DECK)
    }
    return render(request, template_name, context)


def hit(request):
    """/game/hit"""
    template_name = 'blackjack/start_game.html'

    global DECK, player, dealer
    DECK, player, dealer, player_score_str = hit_logic(DECK, player, dealer)

    if max(player.score) > 21:  # если больше 21, сразу перейти на конец раунда
        return redirect('end_of_round')
    elif max(player.score) == 21:  # если у игрока ровно 21, идти на логику stand, где ходы дилера
        return redirect('stand')

    context = {
        'dealer_hand_urls': dealer.urls,
        'player_hand_urls': player.urls,
        'dealer_result': "???",
        'player_result': player_score_str,
        'money': request.session['money'],
        'bet': request.session['bet'],
        # 'deck': len(DECK)
    }
    return render(request, template_name, context)


def end_of_round(request):
    """/game/end_of_round"""
    sleep(0.5)
    template_name = 'blackjack/end_of_round.html'

    global DECK, player, dealer, double_down_pressed
    player, dealer, money_before, dealer_score = \
        end_of_round_logic(request, DECK, player, dealer, double_down_pressed)

    context = {
        'dealer_hand_urls': dealer.urls,
        'player_hand_urls': player.urls,
        'dealer_result': dealer_score,  # если у игрока сразу 21, то дилер не покажет счёт
        'player_result': max(player.score),
        'money_before': money_before,
        'money': request.session['money'],
        'bet': request.session['bet'],
        'player_hand': len(player.hand),
        'dealer_hand': len(dealer.hand)
    }

    return render(request, template_name, context)


def stand(request):
    """game/stand/"""
    template_name = 'blackjack/start_game.html'

    global DECK, player, dealer
    DECK, player, dealer, player_score_str, dealer_score_str = stand_logic(DECK, player, dealer)

    # TODO: почему не >=
    if max(dealer.score) > 21 or max(player.score) >= 21 or max(dealer.score) >= max(player.score):
        return redirect('end_of_round')  # если дилер вылетел, или у них ничья, то пойти на конец раунда

    context = {
        'dealer_hand_urls': dealer.urls,
        'player_hand_urls': player.urls,
        'dealer_result': dealer_score_str,
        'player_result': player_score_str,
        'money': request.session['money'],
        'bet': request.session['bet'],
        # 'deck': len(DECK)
    }

    return render(request, template_name, context)


def double_down(request):
    """промежуточная вью для того, чтобы отследить нажатие кнопки double-down"""
    global double_down_pressed
    double_down_pressed = True
    return redirect('end_of_round')


def zero_money(request):
    sleep(4)
    template_name = 'blackjack/zero_money.html'
    return render(request, template_name, {})


def page_not_found(request, exception):
    msg = '<h1><font color="red">СТАВКА БОЛЬШЕ ЧЕМ У ВАС ДЕНЕГ</font></h1>'
    return HttpResponseNotFound(msg)
