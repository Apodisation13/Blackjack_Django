from .deck import deck
from .forms import get_bet
from .logic_classes import Player, Dealer


def payment_result(request, player_score, dealer_score, player_hand_len):
    """считает выигрыш в деньгах"""
    # у игрока 21 сразу, или у игрока 21 потом, но у дилера нет 21
    if player_score == 21 and (player_hand_len == 2 or dealer_score != 21):
        request.session['money'] += request.session['bet'] * 3
    elif dealer_score == player_score:  # если ничья, то все при своих, ставка вернулась
        request.session['money'] += request.session['bet']
    elif dealer_score > 21:  # у дилера > 21, игрок выиграл две ставки
        request.session['money'] += request.session['bet'] * 2


def starting_draw_logic(request):
    """
    выполняет стартовую логику: создаёт игрока и дилера, достаёт из формы ставку, вычитает ставку из денег,
    перенапправляет на конец раунда если у кого-то сразу 21, представляет счёт в стр вида 11\21
    """
    DECK = deck.copy()
    player = Player(DECK)  # стартовая рука игрока (2 карты), линки, счёт
    dealer = Dealer(DECK)  # стартовая рука дилера (2 карты), линк на 1ю карту и обложку, счёт не отображаем

    get_bet(request)  # достаём ставку из формы, записываем её в сессию

    request.session['money'] -= request.session['bet']  # после раздачи карт сразу вычесть из денег ставку

    double_down_chance = False  # возможность поставить удвоенную ставку TODO: ТУТ НЕПРАВИЛЬНО
    if request.session['money'] >= request.session['bet']:  # если денег осталось больше чем ставка, то можно удвоить
        double_down_chance = True

    player_score_str = player.set_score_to_str()  # представление - или просто число, или строка число\число

    return DECK, player, dealer, player_score_str, double_down_chance


def redirect_from_start_via_blackjack(player, dealer):
    """редирект из стартовой руки на конец раунда если у кого-то 21"""
    if max(player.score) == 21:  # если у игрока сразу блэкджек - переходим на конец раунда
        return 21  # КОСТЫЛЬ - тут можно ретёрн хоть что угодно
    if max(dealer.score) == 21:  # если у дилера сразу блэкджек, открываем его скрытую карту и на конец раунда
        dealer.get_url_for_hidden_card()
        return 21


def hit_logic(DECK, player, dealer):
    """взять карту, получить на неё линк, представление очков в виде 11/21"""
    player.hit(DECK)  # взять одну карту и пересчитать очки

    player.get_urls([player.hand[-1], ])  # сформировать линк на последнюю карту

    player_score_str = player.set_score_to_str()  # представление - или просто число, или строка 11/21

    return DECK, player, dealer, player_score_str


def end_of_round_logic(request, DECK, player, dealer, double_down_pressed):
    """вычисляем тут сколько добавить пользователю денег"""

    if double_down_pressed:
        hit_logic(DECK, player, dealer)
        if max(player.score) <= 21:
            stand_logic(DECK, player, dealer)
        request.session['money'] -= request.session['bet']  # ещё вычли деньги ставки
        request.session['bet'] *= 2

    money_before = request.session['money']  # ведь мы уже вычли ставку, это для удобства отображения
    payment_result(request, max(player.score), max(dealer.score), len(player.hand))

    dealer_score = max(dealer.score)
    # костыль: если у игрока больше 21, или сразу блэкджек, не показать счёт дилера
    if max(player.score) > 21 or (len(player.hand) == 2 and max(player.score) == 21):
        dealer_score = '???'

    return player, dealer, money_before, dealer_score


def stand_logic(DECK, player, dealer):
    """
    логика если игрок остановился:
    1) получить линк на скрытую карту дилера
    2) выполнить логику дилера - описано там
    3) получить линки на все карты дилера со 2й (вед 0 и 1 уже есть)
    4) преобразовать счёт в строку для удобства вида 11\21
    """

    dealer.get_url_for_hidden_card()  # получить линк на настоящую скрытую карту, 2ю в руке

    dealer.ai_logic(player, DECK)  # выполнить логику дилера: добор если меньше чем у игрока, или <=11
    dealer.get_urls(dealer.hand[2:])  # найти линки на все карты после 2й

    player_score_str = player.set_score_to_str()  # представление - или просто число, или строка число\число
    dealer_score_str = dealer.set_score_to_str()  # представление - или просто число, или строка число\число

    return DECK, player, dealer, player_score_str, dealer_score_str
