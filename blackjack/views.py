from time import sleep

from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect

from .forms import MoneyForm, get_money, BetForm
from .logic_game_views import starting_draw_logic, hit_logic, end_of_round_logic, stand_logic
from .logic_game_views import redirect_from_start_via_blackjack
from .logic_classes import Player, Dealer
from .utils import get_context


def home(request):
    """/"""
    template_name = 'blackjack/home.html'
    return render(request, template_name, {})


def input_money_view(request):
    """/input_money"""
    template_name = 'blackjack/input_money.html'
    request.session['beginning'] = True  # флаг для первого входа, чтобы дальше не запрашивать форму MoneyForm
    return render(request, template_name, {'form': MoneyForm})


def input_bet_view(request):
    """/input_money/input-bet"""
    template_name = 'blackjack/input_bet.html'
    if request.session['beginning']:
        get_money(request)  # только при первом входе, записываем из формы в переменную
    return render(request, template_name, {'money': request.session['money'], 'form': BetForm})


def base_view(request):
    """ /game основное вью раунда """
    template_name = 'blackjack/start_game.html'

    # это для того, чтобы не анализировать форму с вводом денег далее, когда мы вернёмся на input_bet
    request.session['beginning'] = False
    request.session['double_down_pressed'] = False  # статус нажатия кнопки double-down

    starting_draw_logic(request)
    player = Player.from_json(request.session['player'])
    dealer = Dealer.from_json(request.session['dealer'])

    if redirect_from_start_via_blackjack(request, player, dealer):  # проверка на 21
        return redirect('end_of_round')

    context = get_context(request, player, dealer,
                          player_result=request.session['player_score_str'],
                          double=request.session['double_down_chance'])

    return render(request, template_name, context)


def hit(request):
    """/game/hit"""
    template_name = 'blackjack/start_game.html'

    hit_logic(request)

    player = Player.from_json(request.session['player'])
    dealer = Dealer.from_json(request.session['dealer'])

    if max(player.score) > 21:  # если больше 21, сразу перейти на конец раунда
        return redirect('end_of_round')
    elif max(player.score) == 21:  # если у игрока ровно 21, идти на логику stand, где ходы дилера
        return redirect('stand')

    context = get_context(request, player, dealer, player_result=request.session['player_score_str'])

    return render(request, template_name, context)


def end_of_round(request):
    """/game/end_of_round"""
    sleep(0.5)
    template_name = 'blackjack/end_of_round.html'

    end_of_round_logic(request)
    player = Player.from_json(request.session['player'])
    dealer = Dealer.from_json(request.session['dealer'])

    context = get_context(
        request, player, dealer, max(player.score),
        dealer_result=request.session['dealer_result'],
        money_before=request.session['money_before']
    )

    return render(request, template_name, context)


def stand(request):
    """game/stand/"""
    template_name = 'blackjack/start_game.html'

    stand_logic(request)
    player = Player.from_json(request.session['player'])
    dealer = Dealer.from_json(request.session['dealer'])

    # если дилер вылетел, или игрок вылетел, или у них ничья, то пойти на конец раунда
    if max(dealer.score) > 21 or max(player.score) >= 21 or max(dealer.score) >= max(player.score):
        return redirect('end_of_round')

    context = get_context(request, player, dealer, player_result=request.session['player_score_str'])

    return render(request, template_name, context)


def double_down(request):
    """промежуточная вью для того, чтобы отследить нажатие кнопки double-down"""
    request.session['double_down_pressed'] = True
    return redirect('end_of_round')


def zero_money(request):
    sleep(4)
    template_name = 'blackjack/zero_money.html'
    return render(request, template_name, {})


def page_not_found(request, exception):
    msg = '<h1><font color="red">СТАВКА БОЛЬШЕ ЧЕМ У ВАС ДЕНЕГ</font></h1>'
    return HttpResponseNotFound(msg)
