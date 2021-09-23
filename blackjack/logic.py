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
    elif dealer_score > 21:  # у дилера > 21, игрок выиграл две ставки, свою и выигрыш такой же
        request.session['money'] += request.session['bet'] * 2


def starting_draw_logic(request):
    """
    выполняет стартовую логику: создаёт игрока и дилера, достаёт из формы ставку, вычитает ставку из денег,
    перенапправляет на конец раунда если у кого-то сразу 21, представляет счёт в стр вида 11\21
    """
    request.session['deck'] = deck.copy()

    # стартовая рука игрока (2 карты), линки, счёт
    player = Player()
    player.start_draw(request.session['deck'])
    # стартовая рука дилера (2 карты), линк на 1ю карту и обложку, счёт не отображаем но считаем
    dealer = Dealer()
    dealer.start_draw(request.session['deck'])

    request.session['player'] = player.to_json()  # сериализация объекта в джейсон
    request.session['dealer'] = dealer.to_json()  # сериализация объекта в джейсон

    get_bet(request)  # достаём ставку из формы, записываем её в сессию

    request.session['money'] -= request.session['bet']  # после раздачи карт сразу вычесть из денег ставку

    request.session['double_down_chance'] = False  # возможность поставить удвоенную ставку, если денег >= ставка
    if request.session['money'] >= request.session['bet']:  # если денег осталось больше чем ставка, то можно удвоить
        request.session['double_down_chance'] = True

    player_score_str = player.set_score_to_str()  # представление - или просто число, или строка число\число
    request.session['player_score_str'] = player_score_str


def redirect_from_start_via_blackjack(request, player, dealer):
    """редирект из стартовой руки на конец раунда если у кого-то 21"""
    if max(player.score) == 21:  # если у игрока сразу блэкджек - переходим на конец раунда
        return 21  # КОСТЫЛЬ - тут можно ретёрн хоть что угодно)))
    if max(dealer.score) == 21:  # если у дилера сразу блэкджек, открываем его скрытую карту и на конец раунда
        dealer.get_url_for_hidden_card()
        request.session['dealer'] = dealer.to_json()  # урлы на картинки изменились, надо "обновить" объект
        return 21


def hit_logic(request):
    """взять карту, получить на неё линк, представление очков в виде 11/21"""
    player = Player.from_json(request.session['player'])

    d = player.hit(request.session['deck'])
    request.session['deck'] = d  # взять одну карту и пересчитать очки
    player.get_urls([player.hand[-1], ])  # сформировать линк на последнюю карту
    player_score_str = player.set_score_to_str()  # представление - или просто число, или строка 11/21
    request.session['player_score_str'] = player_score_str

    request.session['player'] = player.to_json()


def end_of_round_logic(request):
    """вычисляем тут сколько добавить пользователю денег"""
    player = Player.from_json(request.session['player'])
    dealer = Dealer.from_json(request.session['dealer'])

    if request.session['double_down_pressed']:
        # если кнопка удвоения нажата, берём ровно 1 карту, и если не перебрали 21, дилер ходит как обычно
        hit_logic(request)
        player = Player.from_json(request.session['player'])
        if max(player.score) <= 21:
            stand_logic(request)
            dealer = Dealer.from_json(request.session['dealer'])
        request.session['money'] -= request.session['bet']  # ещё вычли деньги ставки
        request.session['bet'] *= 2  # удвоили ставку

    money_before = request.session['money']  # ведь мы уже вычли ставку, это для удобства отображения
    request.session['money_before'] = money_before

    payment_result(request, max(player.score), max(dealer.score), len(player.hand))

    # костыль: если у игрока больше 21, или сразу блэкджек, не показать счёт дилера
    dealer_score = max(dealer.score)
    if max(player.score) > 21 or (len(player.hand) == 2 and max(player.score) == 21):
        dealer_score = '???'
    request.session['dealer_result'] = dealer_score


def stand_logic(request):
    """
    логика если игрок остановился:
    1) получить линк на скрытую карту дилера
    2) выполнить логику дилера - описано там
    3) получить линки на все карты дилера со 2й (вед 0 и 1 уже есть)
    4) преобразовать счёт в строку для удобства вида 11\21
    """
    player = Player.from_json(request.session['player'])
    dealer = Dealer.from_json(request.session['dealer'])

    dealer.get_url_for_hidden_card()  # получить линк на настоящую скрытую карту, 2ю в руке

    # выполнить логику дилера: добор если меньше чем у игрока, или <=11
    d = dealer.ai_logic(player, request.session['deck'])
    request.session['deck'] = d  # взять одну карту и пересчитать очки
    dealer.get_urls(dealer.hand[2:])  # найти линки на все карты после 2й

    player_score_str = player.set_score_to_str()  # представление - или просто число, или строка число\число
    dealer_score_str = dealer.set_score_to_str()  # представление - или просто число, или строка число\число
    request.session['player_score_str'] = player_score_str
    request.session['dealer_score_str'] = dealer_score_str
    request.session['player'] = player.to_json()  # сериализация объекта в джейсон
    request.session['dealer'] = dealer.to_json()  # сериализация объекта в джейсон
