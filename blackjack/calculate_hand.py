def calc_cards(hand: list):
    calc_hand = []
    result = 0
    result_ace = 0

    new_hand = []

    for card in hand:
        if card[0] == 'a':
            new_hand.append("A")
        else:
            new_hand.append(card)

    for card in new_hand:
        if card[0] in ['j', 'q', 'k', '1']:
            calc_hand.append(10)
        elif card[0] != "A":
            calc_hand.append(int(card[0]))

    # print("сумма руки без туза", sum(calc_hand))
    ace_count = new_hand.count("A")
    # print("количество тузов", ace_count)

    if ace_count == 1:
        result += ace_count
        result_ace += 11
    elif ace_count == 2:
        result += ace_count
        result_ace += 12
    elif ace_count == 3:
        result += ace_count
        result_ace += 13
    elif ace_count == 4:
        result += ace_count
        result_ace += 14

    if ace_count > 0:
        result_ace += sum(calc_hand)
        # print("Результат с тузами", result_ace)
        if result_ace > 21:
            result_ace = 0

    result += sum(calc_hand)

    return result, result_ace
