def get_context(request, player, dealer, player_result, dealer_result='???', money_before=None, double=False):
    """формирование контекста для вью base_view, stand, hit, end_of_round"""
    context = {
        'dealer_hand_urls': dealer.urls,  # линки на карты дилера
        'player_hand_urls': player.urls,  # линки на карты игрока
        'dealer_result': dealer_result,  # ??? если игрок перебрал 21, или счёт если не перебрал
        'player_result': player_result,  # счёт в виде 9/20 если в руке туз, и просто 20 если нету туза
        'money_before': money_before,  # для удобства отображения для end_of_round
        'money': request.session['money'],
        'bet': request.session['bet'],
        'double_down_chance': double,  # boolean данные о возможности удвоить ставку
        'player_hand': len(player.hand),  # для анализа на 21, в каком порядке счёт анализировать в шаблоне
        'dealer_hand': len(dealer.hand),
    }
    return context
