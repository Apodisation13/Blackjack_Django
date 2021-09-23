from django import template


register = template.Library()


MENU = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Правила игры', 'url_name': 'rules'},
    {'title': 'Настройки', 'url_name': 'settings'},
]


@register.inclusion_tag('blackjack/show_money_and_bet.html')
def show_money_and_bet(money=None, bet=None):
    context = {
        'money': money,
        'bet': bet
    }
    return context


@register.inclusion_tag('blackjack/show_menu.html', takes_context=True)
def show_menu(context):
    """вот такое для проверки, аутентикейтед юзер или нет"""
    m = MENU.copy()
    context['menu'] = m
    return context
